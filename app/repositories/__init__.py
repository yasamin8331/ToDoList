"""Repository layer for the app."""

from todolist.storage.repository import ProjectRepository
from todolist.storage.sqlalchemy_storage import SqlAlchemyStorage

# In this simple app we have a single repository implementation that
# handles both projects and tasks.

DefaultProjectRepository = SqlAlchemyStorage

__all__ = ["ProjectRepository", "DefaultProjectRepository"]


