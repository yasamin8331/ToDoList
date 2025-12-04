"""Service layer for task business logic."""

from datetime import date
from typing import List, Optional

from todolist.core.config import Config
from todolist.core.exception import (
    LimitExceededError,
    DuplicateError,
    NotFoundError,
    ValidationError,
)
from todolist.core.project import Project
from todolist.core.task import Task, Status
from todolist.storage.in_memory import InMemoryStorage


class TaskService:
    """Service for managing task business logic."""

    def __init__(self, storage: InMemoryStorage):
        """Initialize task service with storage."""
        self._storage = storage

    def create_task(
        self,
        project_id: int,
        title: str,
        description: str = "",
        status: Status = "todo",
        deadline: Optional[date] = None,
    ) -> Task:
        """
        Create a new task with business logic validation.
        
        Business rules:
        - Validate task title and description
        - Check maximum tasks per project limit
        - Check for duplicate task titles in the project
        - Ensure project exists
        """
        # Get project
        project = self._storage.get_project(project_id)

        # Validate inputs
        Config.validate_task_title(title)
        Config.validate_task_description(description)

        if status not in ("todo", "doing", "done"):
            raise ValidationError(f"Invalid status: {status}")

        if deadline is not None and not isinstance(deadline, date):
            raise ValidationError("Deadline must be a valid date object.")

        # Check maximum tasks per project limit
        if project.get_task_count() >= Config.MAX_TASKS_PER_PROJECT:
            raise LimitExceededError(
                f"Cannot add more tasks. Maximum limit "
                f"({Config.MAX_TASKS_PER_PROJECT}) reached."
            )

        # Check for duplicate task titles in the project
        existing_tasks = project.list_all_tasks()
        if any(t.title.lower() == title.lower() for t in existing_tasks):
            raise DuplicateError(
                "A task with this title already exists in this project."
            )

        # Create task
        task_id = self._storage.get_next_task_id()
        task = Task(task_id, title, description, status, deadline)

        # Add task to project
        project.tasks.append(task)
        self._storage.save_project(project)

        return task

    def update_task(
        self,
        project_id: int,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[Status] = None,
        deadline: Optional[date] = None,
    ) -> Task:
        """
        Update a task with business logic validation.
        
        Business rules:
        - Validate all provided fields
        - Check for duplicate task titles (if title is being updated)
        - Ensure project and task exist
        """
        # Get project and task
        project = self._storage.get_project(project_id)
        task = project.get_task(task_id)
        if not task:
            raise NotFoundError(
                f"Task with id {task_id} not found in project {project_id}."
            )

        # Validate and update title
        if title is not None:
            Config.validate_task_title(title)
            # Check for duplicate titles (excluding current task)
            existing_tasks = project.list_all_tasks()
            if any(
                t.id != task_id and t.title.lower() == title.lower()
                for t in existing_tasks
            ):
                raise DuplicateError(
                    "Another task with this title already exists in this project."
                )
            task.title = title

        # Validate and update description
        if description is not None:
            Config.validate_task_description(description)
            task.description = description

        # Validate and update status
        if status is not None:
            if status not in ("todo", "doing", "done"):
                raise ValidationError(f"Invalid status: {status}")
            task.status = status

        # Validate and update deadline
        if deadline is not None:
            if not isinstance(deadline, date):
                raise ValidationError("Deadline must be a valid date object.")
            task.deadline = deadline

        # Save project
        self._storage.save_project(project)

        return task

    def change_task_status(
        self, project_id: int, task_id: int, new_status: Status
    ) -> Task:
        """
        Change task status with business logic validation.
        
        Business rules:
        - Validate status
        - Ensure project and task exist
        """
        if new_status not in ("todo", "doing", "done"):
            raise ValidationError(f"Invalid status: {new_status}")

        return self.update_task(project_id, task_id, status=new_status)

    def delete_task(self, project_id: int, task_id: int) -> None:
        """
        Delete a task with business logic validation.
        
        Business rules:
        - Ensure project and task exist
        """
        project = self._storage.get_project(project_id)
        task = project.get_task(task_id)
        if not task:
            raise NotFoundError(
                f"Task with id {task_id} not found in project {project_id}."
            )

        project.tasks.remove(task)
        self._storage.save_project(project)

    def get_task(self, project_id: int, task_id: int) -> Task:
        """Get a task by ID."""
        project = self._storage.get_project(project_id)
        task = project.get_task(task_id)
        if not task:
            raise NotFoundError(
                f"Task with id {task_id} not found in project {project_id}."
            )
        return task

    def list_tasks(
        self, project_id: int, status_filter: Optional[str] = None
    ) -> List[Task]:
        """
        List tasks in a project with optional status filter.
        
        Business rules:
        - Validate status filter if provided
        - Ensure project exists
        """
        project = self._storage.get_project(project_id)

        if status_filter:
            if status_filter not in ("todo", "doing", "done"):
                raise ValidationError(
                    "Invalid status filter. Use 'todo', 'doing', or 'done'."
                )
            return project.list_tasks(status_filter)

        return project.list_all_tasks()

    # ==================== Cron/Job Helpers ====================

    def autoclose_overdue_tasks(self, today: Optional[date] = None) -> int:
        """Auto-close overdue tasks (deadline < today & status != done).

        Returns the number of tasks that were updated.
        """
        if today is None:
            today = date.today()

        updated_count = 0

        # Iterate over all projects and their tasks
        projects: List[Project] = self._storage.list_projects()
        for project in projects:
            changed = False
            for task in project.list_all_tasks():
                if (
                    task.deadline is not None
                    and task.deadline < today
                    and task.status != "done"
                ):
                    task.status = "done"
                    # نوع فیلد مطابق مدل: فقط تاریخ بسته‌شدن
                    task.closed_at = today
                    updated_count += 1
                    changed = True

            if changed:
                self._storage.save_project(project)

        return updated_count

