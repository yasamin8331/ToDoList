from datetime import date

from typing import Literal, Optional

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

        if not title:
            raise ValueError("Title cannot be empty.")
        if len(title) > 30:
            raise ValueError("Title must not exceed 30 characters.")
        if len(description) > 150:
            raise ValueError("Description must not exceed 150 characters.")
        if status not in ("todo", "doing", "done"):
            raise ValueError(f"Invalid status: {status}")

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

    def __repr__(self) -> str:
        return f"<Task {self.id}: {self.title} [{self.status}]>"
