"""Main application entrypoint.

This delegates to the console-based CLI.
"""

from app.cli.console import main as console_main


def main() -> None:
    console_main()


if __name__ == "__main__":
    main()


