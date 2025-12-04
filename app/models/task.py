"""Task model under the app.models namespace.

Currently this simply re-exports the domain Task from the legacy
package structure to match the desired layout.
"""

from todolist.core.task import Task

__all__ = ["Task"]


