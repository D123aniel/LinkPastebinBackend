import sqlalchemy
from sqlalchemy.orm import Session
from .env import getenv


def _engine_str(database: str = getenv("POSTGRES_DB")) -> str:
    user = getenv("POSTGRES_USER")
    password = getenv("POSTGRES_PASSWORD")
    host = getenv("POSTGRES_HOST")
    port = getenv("POSTGRES_PORT")
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"


engine = sqlalchemy.create_engine(_engine_str())


def db_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
