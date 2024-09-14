import os

ENV = os.getenv('ENV') or ""
DATABASE_HOST = os.getenv('DATABASE_HOST') or "127.0.0.1"
DATABASE_NAME = os.getenv('DATABASE_NAME') or "dapdap"
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME') or "postgres"
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD') or ""
REDIS_HOST = os.getenv('REDIS_HOST') or "localhost"
REDIS_PORT = os.getenv('REDIS_PORT') or 6379
REDIS_DB = os.getenv('REDIS_DB') or 1
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD') or ""
REDIS_USE_TLS = os.getenv('REDIS_USE_TLS') or 1


class Settings:
    VERSION = '0.1.0'
    APP_TITLE = 'cab-api'
    PROJECT_NAME = 'cab'
    APP_DESCRIPTION = 'cab-api'

    SERVER_HOST = 'localhost'

    DEBUG = True

    ENV = ENV

    APPLICATIONS = [
        'user',
    ]

    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    BASE_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))
    LOGS_ROOT = os.path.join(PROJECT_ROOT, "logs")

    DB_URL = f"postgres://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:5432/{DATABASE_NAME}"
    DB_CONNECTIONS = {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'db_url': DB_URL,
            'credentials': {
                'host': DATABASE_HOST,
                'port': 5432,
                'user': DATABASE_USERNAME,
                'password': DATABASE_PASSWORD,
                'database': DATABASE_NAME,
            }
        },
    }

    SECRET_KEY = '665c3ffa948a78fbaccd71c44c7cca7b988013fe337e758c06b9faa5f2d6b71e'  # openssl rand -hex 32
    REFRESH_SECRET_KEY = '5e89bdc45ab0c611ca52668717e23509bff38021ae731847e1e162f605ef2119'  # openssl rand -hex 32
    JWT_ALGORITHM = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30  # 30 day
    JWT_REFRESH_ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30  # 30 day

    LOGIN_URL = SERVER_HOST + '/api/auth/login/access-token'

    REDIS_HOST = REDIS_HOST
    REDIS_PORT = REDIS_PORT
    REDIS_DB = int(REDIS_DB)
    REDIS_PASSWORD = REDIS_PASSWORD
    REDIS_USE_TLS = True if int(REDIS_USE_TLS) else False

    APPLICATIONS_MODULE = 'apps'

    CORS_ORIGINS = [
        "*"
    ]
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_METHODS = ["*"]
    CORS_ALLOW_HEADERS = ["*"]


settings = Settings()