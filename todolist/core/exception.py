"""Custom exceptions for the ToDoList application."""

class ToDoListError(Exception):
    """Base exception for all ToDoList errors."""
    pass

class ValidationError(ToDoListError):
    """Raised when input validation fails."""
    pass

class LimitExceededError(ToDoListError):
    """Raised when maximum limits are exceeded."""
    pass

class NotFoundError(ToDoListError):
    """Raised when a project or task is not found."""
    pass

class DuplicateError(ToDoListError):
    """Raised when duplicate items are detected."""
    pass