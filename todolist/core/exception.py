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

