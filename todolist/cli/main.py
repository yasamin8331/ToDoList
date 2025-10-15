"""CLI entrypoint for the ToDoList (In-Memory) application.

This module provides a simple command line interface to create and
display projects using the InMemoryStorage implementation.
"""

from typing import Any, Iterable
from todolist.storage.in_memory import InMemoryStorage


def print_menu() -> None:
    """Print the main menu to the user."""
    print("\n=== ToDoList CLI ===")
    print("1. Create project")
    print("2. List projects")
    print("3. Exit")


def prompt_project_creation(storage: InMemoryStorage) -> None:
    """Prompt the user for project data and create a project.

    Validation and exceptions raised by the storage layer are printed
    as user-friendly messages.
    """
    try:
        name = input("Project name: ").strip()
        description = input("Project description: ").strip()
        project = storage.add_project(name, description)
    except Exception as exc:  # storage raises e.g. ValueError or custom errors
        print(f"❌ Error: {exc}")
    else:
        # try to present the created project's id/name/description robustly
        pid = getattr(project, "id", getattr(project, "project_id", None))
        pname = getattr(project, "name", "<unknown>")
        print(f"✅ Project created: [{pid}] {pname}")


def get_projects_iter(storage: InMemoryStorage) -> Iterable[Any]:
    """Return an iterable of project objects from storage.

    This helper tries a few common APIs to be resilient to small
    differences in storage implementation.
    """
    # Preferred: storage.list_projects() if implemented
    if hasattr(storage, "list_projects"):
        return storage.list_projects()  # type: ignore
    # Fallback: a dict attribute `projects`
    projects_attr = getattr(storage, "projects", None)
    if isinstance(projects_attr, dict):
        return projects_attr.values()
    # Last fallback: try an attribute named `projects_list`
    projects_list = getattr(storage, "projects_list", None)
    if isinstance(projects_list, list):
        return projects_list
    # If nothing found, return empty list
    return []


def display_projects(storage: InMemoryStorage) -> None:
    """Print all projects stored in storage in a readable format."""
    projects = list(get_projects_iter(storage))
    if not projects:
        print("ℹ️ No projects found.")
        return

    # Try to sort by creation id or by attribute if available
    try:
        projects.sort(key=lambda p: getattr(p, "id", getattr(p, "project_id", 0)))
    except Exception:
        pass

    print("\n--- Projects ---")
    for p in projects:
        pid = getattr(p, "id", getattr(p, "project_id", "?"))
        name = getattr(p, "name", "<no name>")
        desc = getattr(p, "description", "")
        print(f"{pid}. {name} — {desc}")


def main() -> None:
    """Main loop of the CLI."""
    storage = InMemoryStorage()

    try:
        while True:
            print_menu()
            choice = input("> ").strip()

            if choice == "1":
                prompt_project_creation(storage)
            elif choice == "2":
                display_projects(storage)
            elif choice == "3":
                print("Goodbye 👋")
                break
            else:
                print("Invalid option — please choose 1, 2 or 3.")
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye 👋")


if __name__ == "__main__":
    main()
