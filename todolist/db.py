"""Database setup using SQLAlchemy."""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    """Base class for all ORM models."""


def _get_database_url() -> str:
    """Build database URL from environment variables.

    Defaults are suitable for the docker-compose PostgreSQL service.
    """
    load_dotenv()

    db_user = os.getenv("DB_USER", "todolist")
    db_password = os.getenv("DB_PASSWORD", "todolist")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "todolist")

    return f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


DATABASE_URL = _get_database_url()

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
)


def init_db() -> None:
    """Create all tables in the database."""
    from todolist.storage.sqlalchemy_storage import (  # noqa: F401
        ProjectModel,
        TaskModel,
    )

    Base.metadata.create_all(bind=engine)


