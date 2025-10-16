"""Project configuration loader using dotenv."""

import os
from dotenv import load_dotenv
from .exception import ValidationError
# Load environment variables from .env
load_dotenv()


class Config:
    """Application configuration with validation."""

    # Read configuration values with defaults and validation
    MAX_PROJECTS: int = int(os.getenv("MAX_NUMBER_OF_PROJECT", "5"))
    MAX_TASKS_PER_PROJECT: int = int(os.getenv("MAX_NUMBER_OF_TASK", "20"))

    # Validation
    if MAX_PROJECTS <= 0:
        raise ValueError("MAX_NUMBER_OF_PROJECT must be positive")
    if MAX_TASKS_PER_PROJECT <= 0:
        raise ValueError("MAX_NUMBER_OF_TASK must be positive")

    @classmethod
    def validate_project_name(cls, name: str) -> None:
        """Validate project name according to requirements."""
        if not name or len(name.strip()) == 0:
            raise ValidationError("Project name cannot be empty")
        if len(name) > 30:
            raise ValidationError("Project name must not exceed 30 characters")

    @classmethod
    def validate_project_description(cls, description: str) -> None:
        """Validate project description according to requirements."""
        if len(description) > 150:
            raise ValidationError("Description must not exceed 150 characters")

    @classmethod
    def validate_task_title(cls, title: str) -> None:
        """Validate task title according to requirements."""
        if not title or len(title.strip()) == 0:
            raise ValidationError("Task title cannot be empty")
        if len(title) > 30:
            raise ValidationError("Task title must not exceed 30 characters")

    @classmethod
    def validate_task_description(cls, description: str) -> None:
        """Validate task description according to requirements."""
        if len(description) > 150:
            raise ValidationError("Task description must not exceed 150 characters")