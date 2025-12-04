"""CLI command: auto-close overdue tasks.

This wraps the existing scheduler-based implementation so that the
project structure matches the desired `app/commands` layout.
"""

from todolist.cron_autoclose import main, run_once  # re-export

__all__ = ["main", "run_once"]


