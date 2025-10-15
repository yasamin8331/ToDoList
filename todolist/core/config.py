"""Project configuration loader using dotenv."""

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read configuration values with defaults
MAX_PROJECTS: int = int(os.getenv("MAX_NUMBER_OF_PROJECT", 5))
MAX_TASKS: int = int(os.getenv("MAX_NUMBER_OF_TASK", 20))
