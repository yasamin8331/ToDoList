"""Exception hierarchy for the app."""

from todolist.core.exception import (
    ToDoListError,
    ValidationError,
    LimitExceededError,
    NotFoundError,
    DuplicateError,
)

__all__ = [
    "ToDoListError",
    "ValidationError",
    "LimitExceededError",
    "NotFoundError",
    "DuplicateError",
]


