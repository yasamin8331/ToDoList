"""Project repository definitions and default SQLAlchemy implementation."""

from todolist.storage.repository import ProjectRepository  # Protocol
from todolist.storage.sqlalchemy_storage import SqlAlchemyStorage

# For now our concrete project repository is the existing SqlAlchemyStorage.

SqlAlchemyProjectRepository = SqlAlchemyStorage

__all__ = ["ProjectRepository", "SqlAlchemyProjectRepository"]


