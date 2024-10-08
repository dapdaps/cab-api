import logging
import secrets
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from starlette.requests import Request
from tortoise.contrib.fastapi import register_tortoise

from core.exceptions import APIException, on_api_exception
from core.utils.base_util import get_limiter
from settings.config import settings
from settings.log import DEFAULT_LOGGING
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from core.auth.routes import router as auth_router


def configure_logging(log_settings: dict = None):
    log_settings = log_settings or DEFAULT_LOGGING
    logging.config.dictConfig(log_settings)


def init_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )
    add_pagination(app)


def init_http_middleware(app: FastAPI):
    logger = logging.getLogger(__name__)

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        idem = secrets.token_hex(8)
        logger.info(f"rid={idem} start request path={request.url.path}")
        start_time = time.time()

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        formatted_process_time = '{0:.2f}'.format(process_time)
        logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

        return response


def get_app_list():
    app_list = [f'{settings.APPLICATIONS_MODULE}.{app}.models' for app in settings.APPLICATIONS]
    return app_list


def get_tortoise_config() -> dict:
    app_list = get_app_list()
    config = {
        'connections': settings.DB_CONNECTIONS,
        'apps': {
            'models': {
                'models': app_list,
                'default_connection': 'default',
            },
        }
    }
    return config


TORTOISE_ORM = get_tortoise_config()


def register_db(app: FastAPI):
    register_tortoise(
        app,
        config=TORTOISE_ORM,
    )


def register_exceptions(app: FastAPI):
    app.add_exception_handler(APIException, on_api_exception)


def register_slowapi(app: FastAPI):
    limiter = get_limiter()
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


def register_routers(app: FastAPI):
    app.include_router(auth_router)
