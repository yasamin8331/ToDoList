import os
from datetime import date
from typing import List, Optional

from dotenv import load_dotenv

from .config import Config
from .exception import (
    ValidationError,
    LimitExceededError,
    DuplicateError,
    NotFoundError,
)
from .task import Task

load_dotenv()

MAX_NUMBER_OF_TASK = int(os.getenv("MAX_NUMBER_OF_TASK", 100))


class Project:
    """Represents a project containing multiple tasks."""

    def __init__(self, id_: int, name: str, description: str = ""):
        """Initialize a project with validation."""
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
                f"Cannot add more tasks. Maximum limit "
                f"({Config.MAX_TASKS_PER_PROJECT}) reached."
            )

        # Check for duplicate task titles
        if any(t.title.lower() == task.title.lower() for t in self.tasks):
            raise DuplicateError(
                "A task with this title already exists in this project."
            )

        self.tasks.append(task)
        print(f"✅ Task '{task.title}' added to project '{self.name}'")

    def remove_task(self, task_id: int) -> None:
        """Remove a task by ID with proper error handling."""
        task_to_remove = None
        for task in self.tasks:
            if task.id == task_id:
                task_to_remove = task
                break

        if task_to_remove:
            self.tasks.remove(task_to_remove)
            print(f"🗑️ Task '{task_to_remove.title}' removed from project '{self.name}'")
        else:
            raise NotFoundError(f"Task with id {task_id} not found in project '{self.name}'")

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def list_all_tasks(self) -> List[Task]:
        """Return all tasks."""
        return list(self.tasks)

    def list_tasks(self, status_filter: Optional[str] = None) -> List[Task]:
        """Return all tasks, optionally filtered by status."""
        if status_filter:
            if status_filter not in ("todo", "doing", "done"):
                raise ValidationError("Invalid status filter. Use 'todo', 'doing', or 'done'.")
            return [task for task in self.tasks if task.status == status_filter]
        return list(self.tasks)

    def get_tasks_by_status(self) -> dict:
        """Get tasks grouped by status."""
        grouped = {"todo": [], "doing": [], "done": []}
        for task in self.tasks:
            grouped[task.status].append(task)
        return grouped

    def get_task_count(self) -> int:
        """Return the number of tasks in this project."""
        return len(self.tasks)

    def to_dict(self) -> dict:
        """Convert project to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "task_count": len(self.tasks),
            "created_at": self.created_at.isoformat(),
            "tasks": [task.to_dict() for task in self.tasks]
        }

    def __repr__(self) -> str:
        """Official string representation."""
        return f"<Project {self.id}: {self.name} ({len(self.tasks)} tasks)>"

    def __str__(self) -> str:
        """User-friendly string representation."""
        status_counts = self.get_tasks_by_status()
        return (f"📁 {self.name} - {self.description} | "
                f"📊 Todo: {len(status_counts['todo'])}, "
                f"Doing: {len(status_counts['doing'])}, "
                f"Done: {len(status_counts['done'])}")