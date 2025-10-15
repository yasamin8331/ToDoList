from typing import Dict
from todolist.core.project import Project
from todolist.core.task import Task
from todolist.core.config import MAX_PROJECTS, MAX_TASKS

class InMemoryStorage:
    """A simple in-memory storage backend."""

    def __init__(self) -> None:
        self.projects: Dict[int, Project] = {}
        self.project_counter = 1
        self.task_counter = 1

    # ----------------------------
    # Project-related operations
    # ----------------------------

    def add_project(self, name: str, description: str = "") -> Project:
        """Add a new project to storage."""
        if len(self.projects) >= MAX_PROJECTS:
            raise ValueError(f"Cannot create more than {MAX_PROJECTS} projects.")

        for p in self.projects.values():
            if p.name == name:
                raise ValueError(f"A project named '{name}' already exists.")

        project = Project(self.project_counter, name, description)
        self.projects[self.project_counter] = project
        self.project_counter += 1
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
        """Retrieve a single project by ID."""
        try:
            return self.projects[project_id]
        except KeyError:
            raise ValueError("Project not found.")

    # ----------------------------
    # Task-related operations
    # ----------------------------

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