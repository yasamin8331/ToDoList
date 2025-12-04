"""Service layer for project business logic."""

from typing import List

from todolist.core.config import Config
from todolist.core.exception import (
    LimitExceededError,
    DuplicateError,
    NotFoundError,
    ValidationError,
)
from todolist.core.project import Project
from todolist.storage.in_memory import InMemoryStorage


class ProjectService:
    """Service for managing project business logic."""

    def __init__(self, storage: InMemoryStorage):
        """Initialize project service with storage."""
        self._storage = storage

    def create_project(self, name: str, description: str = "") -> Project:
        """
        Create a new project with business logic validation.
        
        Business rules:
        - Validate project name and description
        - Check maximum projects limit
        - Check for duplicate project names
        """
        # Validate inputs
        Config.validate_project_name(name)
        Config.validate_project_description(description)

        # Check maximum projects limit
        existing_projects = self._storage.list_projects()
        if len(existing_projects) >= Config.MAX_PROJECTS:
            raise LimitExceededError(
                f"Cannot create more projects. Maximum limit "
                f"({Config.MAX_PROJECTS}) reached."
            )

        # Check for duplicate project names
        if any(p.name.lower() == name.lower() for p in existing_projects):
            raise DuplicateError("A project with this name already exists.")

        # Create project through storage
        project_id = self._storage.get_next_project_id()
        project = Project(project_id, name, description)
        self._storage.save_project(project)

        return project

    def update_project(
        self, project_id: int, name: str, description: str
    ) -> Project:
        """
        Update project with business logic validation.
        
        Business rules:
        - Validate project name and description
        - Check for duplicate project names (excluding current project)
        - Ensure project exists
        """
        # Get existing project
        project = self._storage.get_project(project_id)

        # Validate inputs
        Config.validate_project_name(name)
        Config.validate_project_description(description)

        # Check for duplicate names (excluding current project)
        existing_projects = self._storage.list_projects()
        if any(
            p.id != project_id and p.name.lower() == name.lower()
            for p in existing_projects
        ):
            raise DuplicateError("Another project with this name already exists.")

        # Update project
        project.name = name
        project.description = description
        self._storage.save_project(project)

        return project

    def delete_project(self, project_id: int) -> None:
        """
        Delete a project with cascade delete of all tasks.
        
        Business rules:
        - Ensure project exists
        - Delete all tasks in the project (cascade delete)
        """
        project = self._storage.get_project(project_id)
        self._storage.delete_project(project_id)

    def get_project(self, project_id: int) -> Project:
        """Get a project by ID."""
        return self._storage.get_project(project_id)

    def list_projects(self) -> List[Project]:
        """List all projects."""
        return self._storage.list_projects()

    def get_project_statistics(self) -> dict:
        """Get statistics about all projects."""
        projects = self._storage.list_projects()
        total_projects = len(projects)
        total_tasks = sum(project.get_task_count() for project in projects)

        status_counts = {"todo": 0, "doing": 0, "done": 0}
        for project in projects:
            project_statuses = project.get_tasks_by_status()
            for status, tasks in project_statuses.items():
                status_counts[status] += len(tasks)

        return {
            "total_projects": total_projects,
            "total_tasks": total_tasks,
            "tasks_by_status": status_counts,
            "max_projects": Config.MAX_PROJECTS,
            "max_tasks_per_project": Config.MAX_TASKS_PER_PROJECT,
        }

