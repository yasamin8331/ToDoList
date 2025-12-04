"""SQLAlchemy-based storage implementation for projects and tasks."""

from __future__ import annotations

from datetime import date
from typing import List, Optional

from sqlalchemy import Date, ForeignKey, Integer, String, Text, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from todolist.core.exception import NotFoundError
from todolist.core.project import Project
from todolist.core.task import Task
from todolist.db import Base, SessionLocal


class ProjectModel(Base):
    """ORM model for projects."""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[date] = mapped_column(Date, default=date.today)

    tasks: Mapped[List["TaskModel"]] = relationship(
        "TaskModel",
        back_populates="project",
        cascade="all, delete-orphan",
    )


class TaskModel(Base):
    """ORM model for tasks."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(20), default="todo")
    deadline: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    created_at: Mapped[date] = mapped_column(Date, default=date.today)

    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    project: Mapped[ProjectModel] = relationship("ProjectModel", back_populates="tasks")


class SqlAlchemyStorage:
    """Storage implementation using SQLAlchemy and PostgreSQL."""

    def __init__(self) -> None:
        self._session_factory = SessionLocal

    # ==================== Project CRUD Operations ====================

    def save_project(self, project: Project) -> None:
        """Save or update a project."""
        with self._session_factory() as session:
            db_project = session.get(ProjectModel, project.id)
            if not db_project:
                db_project = ProjectModel(id=project.id)
                session.add(db_project)

            db_project.name = project.name
            db_project.description = project.description
            db_project.created_at = project.created_at

            # sync tasks
            db_project.tasks.clear()
            for task in project.tasks:
                db_task = TaskModel(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    status=task.status,
                    deadline=task.deadline,
                    created_at=task.created_at,
                )
                db_project.tasks.append(db_task)

            session.commit()

    def get_project(self, project_id: int) -> Project:
        """Get a project by ID."""
        with self._session_factory() as session:
            db_project = session.get(ProjectModel, project_id)
            if not db_project:
                raise NotFoundError(f"Project with id {project_id} not found.")

            project = Project(
                id_=db_project.id,
                name=db_project.name,
                description=db_project.description,
            )
            project.created_at = db_project.created_at

            for db_task in db_project.tasks:
                task = Task(
                    id_=db_task.id,
                    title=db_task.title,
                    description=db_task.description,
                    status=db_task.status,
                    deadline=db_task.deadline,
                )
                task.created_at = db_task.created_at
                project.tasks.append(task)

            return project

    def delete_project(self, project_id: int) -> None:
        """Delete a project and its tasks."""
        with self._session_factory() as session:
            db_project = session.get(ProjectModel, project_id)
            if not db_project:
                raise NotFoundError(f"Project with id {project_id} not found.")
            session.delete(db_project)
            session.commit()

    def list_projects(self) -> List[Project]:
        """Return all projects sorted by ID."""
        with self._session_factory() as session:
            result = session.scalars(select(ProjectModel).order_by(ProjectModel.id)).all()

            projects: List[Project] = []
            for db_project in result:
                project = Project(
                    id_=db_project.id,
                    name=db_project.name,
                    description=db_project.description,
                )
                project.created_at = db_project.created_at

                for db_task in db_project.tasks:
                    task = Task(
                        id_=db_task.id,
                        title=db_task.title,
                        description=db_task.description,
                        status=db_task.status,
                        deadline=db_task.deadline,
                    )
                    task.created_at = db_task.created_at
                    project.tasks.append(task)

                projects.append(project)

            return projects

    # ==================== ID Management ====================

    def get_next_project_id(self) -> int:
        """Get the next project ID using max(id)+1 strategy."""
        with self._session_factory() as session:
            max_id = session.scalar(select(ProjectModel.id).order_by(ProjectModel.id.desc()))
            return (max_id or 0) + 1

    def get_next_task_id(self) -> int:
        """Get the next task ID using max(id)+1 strategy."""
        with self._session_factory() as session:
            max_id = session.scalar(select(TaskModel.id).order_by(TaskModel.id.desc()))
            return (max_id or 0) + 1


