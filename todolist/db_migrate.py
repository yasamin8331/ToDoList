"""Helper CLI to run Alembic migrations from within the project.

Usage (via Poetry script):

    poetry run todolist-db-upgrade
"""

from alembic import command
from alembic.config import Config


def main() -> None:
    """Upgrade database schema to the latest Alembic revision."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


if __name__ == "__main__":
    main()


