from typing import Dict, List, Optional
from todolist.core.project import Project
from todolist.core.task import Task
from todolist.core.config import Config
from todolist.core.exception import LimitExceededError, DuplicateError, NotFoundError

class InMemoryStorage:
    """In-memory storage implementation for projects and tasks."""

    def __init__(self) :
        self._projects: Dict[int, Project] = {}
        self._next_project_id = 1
        self._next_task_id = 1

    def add_project(self, name: str, description: str = "") -> Project:
        """Create a new project with validation."""
        # Check maximum projects limit
        if len(self._projects) >= Config.MAX_PROJECTS:
            raise LimitExceededError(
                f"Cannot create more projects. Maximum limit ({Config.MAX_PROJECTS}) reached."
            )

        # Check for duplicate project names
        if any(p.name.lower() == name.lower() for p in self._projects.values()):
            raise DuplicateError("A project with this name already exists.")

        # Validate inputs
        Config.validate_project_name(name)
        Config.validate_project_description(description)

        project_id = self._next_project_id
        project = Project(project_id, name, description)
        self._projects[project_id] = project
        self._next_project_id += 1

        return project

    def delete_project(self, project_id: int) -> None:
        """Delete a project and all its tasks (cascade delete)."""
        project = self.get_project(project_id)
        project_name = project.name
        del self._projects[project_id]
        print(f"🗑️ Project '{project_name}' and all its tasks have been deleted.")

    def list_projects(self) -> List[Project]:
        """Return all projects sorted by ID."""
        return sorted(self._projects.values(), key=lambda p: p.id)

    def get_project(self, project_id: int) -> Project:
        """Get a project by ID."""
        project = self._projects.get(project_id)
        if not project:
            raise NotFoundError(f"Project with id {project_id} not found.")
        return project

    def update_project(self, project_id: int, name: str, description: str) -> Project:
        """Update project details."""
        project = self.get_project(project_id)

        # Check for duplicate names (excluding current project)
        if any(p.id != project_id and p.name.lower() == name.lower()
               for p in self._projects.values()):
            raise DuplicateError("Another project with this name already exists.")

        Config.validate_project_name(name)
        Config.validate_project_description(description)

        project.name = name
        project.description = description

        return project

    def add_task(
        self, project_id: int, title: str, description: str = ""
    ) -> Task:
        """Add a new task to a project."""
        project = self.get_project(project_id)
        if len(project.tasks) >= MAX_TASKS:
            raise ValueError(f"Cannot add more than {MAX_TASKS} tasks per project.")

        task = Task(self.task_counter, title, description)
        project.add_task(task)
        self.task_counter += 1
        return task

    def delete_task(self, project_id: int, task_id: int) -> None:
        """Delete a task from a project."""
        project = self.get_project(project_id)
        project.remove_task(task_id)