"""Task model - data structure only.

This module contains only the data model for Task.
All business logic and validation should be in the service layer.
"""

from datetime import date
from typing import Literal, Optional

Status = Literal["todo", "doing", "done"]


class Task:
    """Represents a single task belonging to a project.
    
    This is a pure data model with no business logic.
    All validation and business rules are in the service layer.
    """

    def __init__(
        self,
        id_: int,
        title: str,
        description: str = "",
        status: Status = "todo",
        deadline: Optional[date] = None,
    ):
        """Initialize a Task instance - no validation, just data assignment."""
        self.id = id_
        self.title = title
        self.description = description
        self.status = status
        self.deadline = deadline
        self.created_at = date.today()

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
        """Official string representation for debugging."""
        deadline_str = f", deadline: {self.deadline}" if self.deadline else ""
        return f"<Task {self.id}: {self.title} [{self.status}]{deadline_str}>"

    def __str__(self) -> str:
        """User-friendly string representation."""
        status_icons = {"todo": "⏳", "doing": "🔄", "done": "✅"}
        icon = status_icons.get(self.status, "📝")
        deadline_info = f" | 📅 {self.deadline}" if self.deadline else ""
        return f"{icon} {self.title} - {self.status}{deadline_info}"
