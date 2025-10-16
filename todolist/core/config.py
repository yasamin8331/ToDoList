"""Project configuration loader using dotenv."""

import os
from dotenv import load_dotenv

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
