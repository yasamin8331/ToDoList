"""CLI entrypoint for the ToDoList (In-Memory) application."""

from datetime import datetime, date
from typing import Optional
from todolist.storage.in_memory import InMemoryStorage
from todolist.core.exception import ToDoListError, ValidationError, NotFoundError

def print_main_menu() -> None:
    """Print the main menu to the user."""
    print("\n" + "=" * 50)
    print("🎯 ToDoList CLI - Main Menu")
    print("=" * 50)
    print("1. 📁 Project Management")
    print("2. 📝 Task Management")
    print("3. 📊 View Reports")
    print("4. 🚪 Exit")
    print("-" * 50)


def print_project_menu() -> None:
    """Print the project management menu."""
    print("\n" + "=" * 40)
    print("📁 Project Management")
    print("=" * 40)
    print("1. ➕ Create new project")
    print("2. 📋 List all projects")
    print("3. ✏️ Update project")
    print("4. 🗑️ Delete project")
    print("5. 🔙 Back to main menu")
    print("-" * 40)


def print_task_menu() -> None:
    """Print the task management menu."""
    print("\n" + "=" * 40)
    print("📝 Task Management")
    print("=" * 40)
    print("1. ➕ Add new task")
    print("2. 📋 List tasks in project")
    print("3. ✏️ Update task")
    print("4. 🔄 Change task status")
    print("5. 🗑️ Delete task")
    print("6. 🔙 Back to main menu")
    print("-" * 40)


def print_reports_menu() -> None:
    """Print the report menu."""
    print("\n" + "=" * 40)
    print("📊 Reports & Statistics")
    print("=" * 40)
    print("1. 📈 Project statistics")
    print("2. 📋 All projects with tasks")
    print("3. 🔍 Filter tasks by status")
    print("4. 🔙 Back to main menu")
    print("-" * 40)


def get_validated_input(prompt: str, validation_func=None, error_message: str = "Invalid input") -> str:
    """Get validated input from user with error handling."""
    while True:
        try:
            value = input(prompt).strip()
            if validation_func:
                validation_func(value)
            return value
        except (ValueError, ValidationError) as e:
            print(f"❌ {error_message}: {e}")
            print("Please try again.")


def get_validated_date(prompt: str) -> Optional[date]:
    """Get validated date input from user."""
    while True:
        date_str = input(prompt).strip()
        if not date_str:  # Empty input means no deadline
            return None

        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD format (e.g., 2024-01-15) or leave empty.")
            print("Please try again.")


def get_validated_status() -> str:
    """Get validated status input from user."""
    while True:
        status = input("Status (default: todo): ").strip().lower() or "todo"
        if status in ("todo", "doing", "done"):
            return status
        else:
            print("❌ Invalid status. Please choose from: todo, doing, done")
            print("Please try again.")


def get_validated_project_id(storage: InMemoryStorage) -> int:
    """Get validated project ID from user."""
    while True:
        try:
            project_id = int(input("Select project ID: ").strip())
            storage.get_project(project_id)  # This will raise NotFoundError if project doesn't exist
            return project_id
        except ValueError:
            print("❌ Invalid project ID. Please enter a number.")
        except NotFoundError as e:
            print(f"❌ {e}")
        print("Please try again.")


def handle_project_creation(storage: InMemoryStorage) -> None:
    """Handle project creation with user input."""
    try:
        print("\n--- Create New Project ---")
        name = get_validated_input(
            "Project name: ",
            lambda x: None if x.strip() else exec('raise ValueError("Project name cannot be empty")'),
            "Project name validation failed"
        )
        description = input("Project description: ").strip()

        project = storage.add_project(name, description)
        print(f"✅ Project created successfully!")
        print(f"   ID: {project.id}, Name: {project.name}")

    except ToDoListError as e:
        print(f"❌ Error: {e}")


def handle_project_listing(storage: InMemoryStorage) -> None:
    """Display all projects in a formatted way."""
    projects = storage.list_projects()

    if not projects:
        print("ℹ️ No projects found.")
        return

    print(f"\n--- All Projects ({len(projects)}) ---")
    for project in projects:
        status_counts = project.get_tasks_by_status()
        print(f"\n📁 {project.name} (ID: {project.id})")
        print(f"   📝 {project.description}")
        print(f"   📊 Tasks: {project.get_task_count()} total | "
              f"⏳ Todo: {len(status_counts['todo'])} | "
              f"🔄 Doing: {len(status_counts['doing'])} | "
              f"✅ Done: {len(status_counts['done'])}")


def handle_task_creation(storage: InMemoryStorage) -> None:
    """Handle task creation with user input."""
    try:
        print("\n--- Add New Task ---")

        # Show available projects
        projects = storage.list_projects()
        if not projects:
            print("❌ No projects available. Please create a project first.")
            return

        print("Available projects:")
        for project in projects:
            print(f"  {project.id}. {project.name}")

        project_id = get_validated_project_id(storage)
        title = get_validated_input(
            "Task title: ",
            lambda x: None if x.strip() else exec('raise ValueError("Task title cannot be empty")'),
            "Task title validation failed"
        )
        description = input("Task description: ").strip()

        print("Status options: todo, doing, done")
        status = get_validated_status()

        deadline = get_validated_date("Deadline (YYYY-MM-DD, optional): ")

        task = storage.add_task_to_project(project_id, title, description, status, deadline)
        print(f"✅ Task '{task.title}' added successfully to project!")

    except ToDoListError as e:
        print(f"❌ Error: {e}")


def display_tasks_in_project(storage: InMemoryStorage) -> None:
    """Display all tasks in a specific project."""
    try:
        print("\n--- View Tasks in Project ---")

        projects = storage.list_projects()
        if not projects:
            print("ℹ️ No projects available.")
            return

        print("Available projects:")
        for project in projects:
            print(f"  {project.id}. {project.name}")

        project_id = get_validated_project_id(storage)
        project = storage.get_project(project_id)

        tasks = storage.list_tasks(project_id)
        if not tasks:
            print(f"ℹ️ No tasks found in project '{project.name}'.")
            return

        print(f"\n--- Tasks in '{project.name}' ({len(tasks)} tasks) ---")
        for i, task in enumerate(tasks, 1):
            deadline_str = f" | 📅 {task.deadline}" if task.deadline else ""
            status_icons = {"todo": "⏳", "doing": "🔄", "done": "✅"}
            icon = status_icons.get(task.status, "📝")
            print(f"{i}. {icon} {task.title} - {task.status}{deadline_str}")
            if task.description:
                print(f"   📝 {task.description}")

    except ToDoListError as e:
        print(f"❌ Error: {e}")


def show_project_statistics(storage: InMemoryStorage) -> None:
    """Display comprehensive project statistics."""
    try:
        stats = storage.get_project_stats()

        print("\n" + "=" * 50)
        print("📈 PROJECT STATISTICS")
        print("=" * 50)
        print(f"📁 Total Projects: {stats['total_projects']}/{stats['max_projects']}")
        print(f"📝 Total Tasks: {stats['total_tasks']}")
        print(f"📊 Task Status Distribution:")
        print(f"   ⏳ Todo: {stats['tasks_by_status']['todo']}")
        print(f"   🔄 Doing: {stats['tasks_by_status']['doing']}")
        print(f"   ✅ Done: {stats['tasks_by_status']['done']}")
        print("=" * 50)

    except Exception as e:
        print(f"❌ Error generating statistics: {e}")


def main() -> None:
    """Main application loop."""
    storage = InMemoryStorage()

    print("🚀 Welcome to ToDoList CLI!")
    print("Managing your projects and tasks made easy.")

    try:
        while True:
            print_main_menu()
            choice = input("Select an option (1-4): ").strip()

            if choice == "1":
                # Project Management
                while True:
                    print_project_menu()
                    sub_choice = input("Select an option (1-5): ").strip()

                    if sub_choice == "1":
                        handle_project_creation(storage)
                    elif sub_choice == "2":
                        handle_project_listing(storage)
                    elif sub_choice == "3":
                        # Implement project update
                        print("🛠️ Project update feature coming soon...")
                    elif sub_choice == "4":
                        # Implement project deletion
                        print("🛠️ Project deletion feature coming soon...")
                    elif sub_choice == "5":
                        break
                    else:
                        print("❌ Invalid option. Please choose 1-5.")

            elif choice == "2":
                # Task Management
                while True:
                    print_task_menu()
                    sub_choice = input("Select an option (1-6): ").strip()

                    if sub_choice == "1":
                        handle_task_creation(storage)
                    elif sub_choice == "2":
                        display_tasks_in_project(storage)
                    elif sub_choice == "3":
                        # Implement task update
                        print("🛠️ Task update feature coming soon...")
                    elif sub_choice == "4":
                        # Implement status change
                        print("🛠️ Status change feature coming soon...")
                    elif sub_choice == "5":
                        # Implement task deletion
                        print("🛠️ Task deletion feature coming soon...")
                    elif sub_choice == "6":
                        break
                    else:
                        print("❌ Invalid option. Please choose 1-6.")

            elif choice == "3":
                # Reports
                while True:
                    print_reports_menu()
                    sub_choice = input("Select an option (1-4): ").strip()

                    if sub_choice == "1":
                        show_project_statistics(storage)
                    elif sub_choice == "2":
                        handle_project_listing(storage)
                    elif sub_choice == "3":
                        # Implement status filtering
                        print("🛠️ Status filtering feature coming soon...")
                    elif sub_choice == "4":
                        break
                    else:
                        print("❌ Invalid option. Please choose 1-4.")

            elif choice == "4":
                print("\n👋 Thank you for using ToDoList CLI! Goodbye!")
                break
            else:
                print("❌ Invalid option. Please choose 1-4.")

    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user. Goodbye! 👋")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")


if __name__ == "__main__":
    main()