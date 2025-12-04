"""Task repository definitions.

In this simplified architecture, tasks are always loaded and persisted
through their parent Project. Therefore, we reuse the same underlying
SqlAlchemyStorage as for projects.
"""

from todolist.storage.repository import ProjectRepository  # Protocol
from todolist.storage.sqlalchemy_storage import SqlAlchemyStorage

SqlAlchemyTaskRepository = SqlAlchemyStorage

__all__ = ["ProjectRepository", "SqlAlchemyTaskRepository"]


