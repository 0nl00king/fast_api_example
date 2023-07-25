from envparse import env

DB_HOST = env.str("DB_HOST", default='db')
DB_PORT = env.int("DB_PORT", default=5432)
DB_NAME = env.str("DB_NAME", default='postgres')
DB_USER = env.str("DB_USER", default='postgres')
DB_PASS = env.str("DB_PASS", default='postgres')

DB_URL = env.str(
    "DB_URL",
    default="postgresql+asyncpg://postgres:postgres@db:5432/postgres?async_fallback=True",
)
APP_PORT = env.int("APP_PORT", default=8000)
APP_HOST = env.str("APP_HOST", default='rest')

SECRET_KEY: str = env.str("SECRET_KEY", default="secret_key")
ALGORITHM: str = env.str("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int(
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    default=30,
)
