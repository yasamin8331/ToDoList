"""Project model under the app.models namespace.

Currently this simply re-exports the domain Project from the legacy
package structure to match the desired layout.
"""

from todolist.core.project import Project

__all__ = ["Project"]


