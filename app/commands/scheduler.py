"""Optional scheduler command (if using schedule library instead of Cron).

Currently this just re-exports the same main function as the
`autoclose_overdue` command, since that module already contains the
schedule loop.
"""

from todolist.cron_autoclose import main  # type: ignore[F401]

__all__ = ["main"]


