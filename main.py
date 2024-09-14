from fastapi import FastAPI

from core.exceptions import SettingNotFound
from core.init_app import configure_logging, init_middlewares, register_db, register_exceptions, register_routers, \
    register_slowapi, init_http_middleware
import uvicorn

try:
    from settings.config import settings
except ImportError:
    raise SettingNotFound('Can not import settings. Create settings file from template.config.py')


app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.VERSION,
    docs_url=None if settings.ENV == "prod" else "/docs",
    redoc_url=None if settings.ENV == "prod" else "/redoc"
)
configure_logging()
init_middlewares(app)
register_db(app)
register_exceptions(app)
register_slowapi(app)
init_http_middleware(app)
register_routers(app)

if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=8080, reload=True, workers=5)
