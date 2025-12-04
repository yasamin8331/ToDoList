"""In-memory storage implementation for projects and tasks.

This layer is responsible ONLY for data persistence (CRUD operations).
All business logic should be in the service layer.
"""

from typing import Dict, List

from todolist.core.exception import NotFoundError
from todolist.core.project import Project


class InMemoryStorage:
    """In-memory storage implementation for projects and tasks.
    
    This class provides only data access operations (CRUD).
    No business logic, validation, or duplicate checking is done here.
    """

    def __init__(self) -> None:
        """Initialize project and task storage."""
        self._projects: Dict[int, Project] = {}
        self._next_project_id = 1
        self._next_task_id = 1

    # ==================== Project CRUD Operations ====================

    def save_project(self, project: Project) -> None:
        """Save or update a project in storage."""
        self._projects[project.id] = project

    def get_project(self, project_id: int) -> Project:
        """Get a project by ID."""
        project = self._projects.get(project_id)
        if not project:
            raise NotFoundError(f"Project with id {project_id} not found.")
        return project

    def delete_project(self, project_id: int) -> None:
        """Delete a project from storage."""
        if project_id not in self._projects:
            raise NotFoundError(f"Project with id {project_id} not found.")
        del self._projects[project_id]

    def list_projects(self) -> List[Project]:
        """Return all projects sorted by ID."""
        return sorted(self._projects.values(), key=lambda p: p.id)

    # ==================== ID Management ====================

    def get_next_project_id(self) -> int:
        """Get the next available project ID and increment counter."""
        project_id = self._next_project_id
        self._next_project_id += 1
        return project_id

    def get_next_task_id(self) -> int:
        """Get the next available task ID and increment counter."""
        task_id = self._next_task_id
        self._next_task_id += 1
        return task_id
