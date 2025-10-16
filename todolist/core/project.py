from .task import Task
from typing import List, Optional
from .exception import ValidationError, LimitExceededError, DuplicateError, NotFoundError
from .config import Config
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()

MAX_NUMBER_OF_TASK = int(os.getenv("MAX_NUMBER_OF_TASK", 20))
class Project:
    """Represents a project containing multiple tasks."""

    def __init__(self, id_: int, name: str, description: str = ""):

        # Validate inputs using Config validation methods
        Config.validate_project_name(name)
        Config.validate_project_description(description)

        self.id = id_
        self.name = name
        self.description = description
        self.tasks: List[Task] = []
        self.created_at = date.today()

    def add_task(self, task: Task) -> None:
        """Add a new task to the project with validation."""
        if len(self.tasks) >= Config.MAX_TASKS_PER_PROJECT:
            raise LimitExceededError(
                f"Cannot add more tasks. Maximum limit ({Config.MAX_TASKS_PER_PROJECT}) reached."
            )

            # Check for duplicate task titles
        if any(t.title.lower() == task.title.lower() for t in self.tasks):
            raise DuplicateError("A task with this title already exists in this project.")

        self.tasks.append(task)
        print(f"✅ Task '{task.title}' added to project '{self.name}'")

    def remove_task(self, task_id: int) -> None:
        """Remove a task by ID."""
        before_count = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        if len(self.tasks) == before_count:
            raise ValueError(f"Task with id {task_id} not found.")

    def list_tasks(self) -> List[Task]:
        """Return all tasks."""
        return list(self.tasks)

    def __repr__(self) -> str:
        return f"<Project {self.id}: {self.name} ({len(self.tasks)} tasks)>"