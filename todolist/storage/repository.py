"""Repository abstractions for projects and tasks.

This module defines the Repository Pattern interfaces that the service
layer depends on. Concrete implementations can be in-memory, SQLAlchemy,
or any other storage backend, as long as they implement this protocol.
"""

from __future__ import annotations

from typing import Protocol, List

from todolist.core.project import Project


class ProjectRepository(Protocol):
    """Abstract repository for accessing and persisting projects and tasks.

    Both in-memory and SQLAlchemy-based storages implement this protocol.
    The service layer only depends on this abstraction, not on concrete
    storage details.
    """

    # Project CRUD
    def save_project(self, project: Project) -> None:
        pass

    def get_project(self, project_id: int) -> Project:
        ...

    def delete_project(self, project_id: int) -> None:
        ...

    def list_projects(self) -> List[Project]:
        ...

    # ID generation helpers
    def get_next_project_id(self) -> int:
        ...

    def get_next_task_id(self) -> int:
        ...


