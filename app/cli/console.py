"""Console-based CLI for the app.

This simply re-uses the existing CLI implementation while exposing it
under the new `app.cli` namespace.
"""

from todolist.cli.main import main

__all__ = ["main"]


