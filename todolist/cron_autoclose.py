"""Cron-style job to auto-close overdue tasks using schedule.

Command name (conceptually):
    todolist tasks:autoclose-overdue

Poetry entrypoint:
    poetry run todolist-tasks-autoclose-overdue
"""

from datetime import date
import time

import schedule

from todolist.service.task_service import TaskService
from todolist.storage.sqlalchemy_storage import SqlAlchemyStorage
from todolist.db import init_db


def run_once() -> None:
    """Run a single auto-close pass and print a short summary."""
    storage = SqlAlchemyStorage()
    service = TaskService(storage)  # type: ignore[arg-type]

    today = date.today()
    updated = service.autoclose_overdue_tasks(today=today)

    if updated:
        print(
            f"✅ Auto-closed {updated} overdue task(s) for {today.isoformat()}."
        )
    else:
        print(f"ℹ️ No overdue tasks found for {today.isoformat()}.")


def main() -> None:
    """Entry point: initialize DB and start schedule loop."""
    init_db()

    # Schedule the job to run every minute (adjust as needed)
    schedule.every(1).minutes.do(run_once)

    print(
        "🚀 Started 'todolist tasks:autoclose-overdue' scheduler "
        "(runs every 1 minute)..."
    )

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()


