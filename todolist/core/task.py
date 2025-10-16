from datetime import date
from typing import Literal, Optional
from .exception import ValidationError
from .config import Config

Status = Literal["todo", "doing", "done"]

class Task:
    """Represents a single task belonging to a project."""


    def __init__(
        self,
        id_: int,
        title: str,
        description: str = "",
        status: Status = "todo",
        deadline: Optional[date] = None,
    ):
        # Validate inputs using Config validation methods
        Config.validate_task_title(title)
        Config.validate_task_description(description)

        if not title:
            raise ValueError("Title cannot be empty.")
        if len(title) > 30:
            raise ValueError("Title must not exceed 30 characters.")
        if len(description) > 150:
            raise ValueError("Description must not exceed 150 characters.")
        if status not in ("todo", "doing", "done"):
            raise ValueError(f"Invalid status: {status}")
        if deadline is not None and not isinstance(deadline, date):
            raise ValueError("Deadline must be a valid date object.")

        self.id = id_
        self.title = title
        self.description = description
        self.status = status
        self.deadline = deadline

    def change_status(self, new_status: Status) -> None:
        """Update the task status."""
        if new_status not in ("todo", "doing", "done"):
            raise ValueError(f"Invalid new status: {new_status}")
        self.status = new_status

    def update_task(
            self,
            title: Optional[str] = None,
            description: Optional[str] = None,
            status: Optional[Status] = None,
            deadline: Optional[date] = None,
    ) -> None:
        """Edit task attributes (title, description, status, deadline)."""
        if title is not None:
            if len(title) > 30:
                raise ValueError("Title must not exceed 30 characters.")
            self.title = title

        if description is not None:
            if len(description) > 150:
                raise ValueError("Description must not exceed 150 characters.")
            self.description = description

        if status is not None:
            if status not in ("todo", "doing", "done"):
                raise ValueError(f"Invalid status: {status}")
            self.status = status

        if deadline is not None:
            if not isinstance(deadline, date):
                raise ValueError("Deadline must be a valid date object.")
            self.deadline = deadline


    def __repr__(self) -> str:
        return f"<Task {self.id}: {self.title} [{self.status}]>"
