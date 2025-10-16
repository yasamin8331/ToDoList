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
            raise ValidationError("Title cannot be empty.")
        if len(title) > 30:
            raise ValidationError("Title must not exceed 30 characters.")
        if len(description) > 150:
            raise ValidationError("Description must not exceed 150 characters.")
        if status not in ("todo", "doing", "done"):
            raise ValidationError(f"Invalid status: {status}")

        if deadline is not None and not isinstance(deadline, date):
            raise ValidationError("Deadline must be a valid date object.")
        self.id = id_
        self.title = title
        self.description = description
        self.status = status
        self.deadline = deadline
        self.created_at = date.today()

    def change_status(self, new_status: Status) -> None:
        """Update the task status with validation."""
        if new_status not in ("todo", "doing", "done"):
            raise ValidationError(f"Invalid new status: {new_status}")
        self.status = new_status

        old_status = self.status
        self.status = new_status
        print(f"Task status changed from '{old_status}' to '{new_status}'")

    def update_task(
            self,
            title: Optional[str] = None,
            description: Optional[str] = None,
            status: Optional[Status] = None,
            deadline: Optional[date] = None,
    ) -> None:
        """Edit task attributes with comprehensive validation."""

        updates_applied = []

        if title is not None:
            Config.validate_task_title(title)
            self.title = title
            updates_applied.append("title")

        if description is not None:
            Config.validate_task_description(description)
            self.description = description
            updates_applied.append("description")

        if status is not None:
            if status not in ("todo", "doing", "done"):
                raise ValidationError(f"Invalid status: {status}")
            old_status = self.status
            self.status = status
            updates_applied.append(f"status (from '{old_status}' to '{status}')")

        if deadline is not None:
            if not isinstance(deadline, date):
                raise ValidationError("Deadline must be a valid date object.")
            self.deadline = deadline
            updates_applied.append("deadline")

        if updates_applied:
            print(f"Task updated: {', '.join(updates_applied)}")

    def to_dict(self) -> dict:
        """Convert task to dictionary for serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "created_at": self.created_at.isoformat()
        }

    def __repr__(self) -> str:
        deadline_str = f", deadline: {self.deadline}" if self.deadline else ""
        return f"<Task {self.id}: {self.title} [{self.status}]{deadline_str}>"

    def __str__(self) -> str:
        """User-friendly string representation."""
        status_icons = {"todo": "⏳", "doing": "🔄", "done": "✅"}
        icon = status_icons.get(self.status, "📝")
        deadline_info = f" | 📅 {self.deadline}" if self.deadline else ""
        return f"{icon} {self.title} - {self.status}{deadline_info}"
