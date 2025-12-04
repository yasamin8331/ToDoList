"""Project model - data structure only.

This module contains only the data model for Project.
All business logic and validation should be in the service layer.
"""

from datetime import date
from typing import List, Optional

from .task import Task


class Project:
    """Represents a project containing multiple tasks.
    
    This is a pure data model with no business logic.
    All validation and business rules are in the service layer.
    """

    def __init__(self, id_: int, name: str, description: str = ""):
        """Initialize a project - no validation, just data assignment."""
        self.id = id_
        self.name = name
        self.description = description
        self.tasks: List[Task] = []
        self.created_at = date.today()

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