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
        """Delete a project by ID."""
        if project_id not in self.projects:
            raise ValueError("Project not found.")
        del self.projects[project_id]

    def list_projects(self) -> List[Project]:
        """Return a list of all projects."""
        return list(self.projects.values())

    def get_project(self, project_id: int) -> Project:
        """Get a project by ID."""
        project = self._projects.get(project_id)
        if not project:
            raise NotFoundError(f"Project with id {project_id} not found.")
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