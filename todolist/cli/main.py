"""CLI entrypoint for the ToDoList (In-Memory) application."""

from datetime import datetime, date
from typing import Optional

from todolist.storage.in_memory import InMemoryStorage
from todolist.service.project_service import ProjectService
from todolist.service.task_service import TaskService
from todolist.core.exception import ToDoListError, ValidationError, NotFoundError


# ========================== MENU PRINT FUNCTIONS ========================== #

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
    """Print the reports and statistics menu."""
    print("\n" + "=" * 40)
    print("📊 Reports & Statistics")
    print("=" * 40)
    print("1. 📈 Project statistics")
    print("2. 📋 All projects with tasks")
    print("3. 🔍 Filter tasks by status")
    print("4. 🔙 Back to main menu")
    print("-" * 40)


# ========================== INPUT VALIDATION HELPERS ========================== #

def get_validated_input(
    prompt: str,
    validation_func=None,
    error_message: str = "Invalid input",
) -> str:
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
        if not date_str:
            return None

        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print(
                "❌ Invalid date format. Use YYYY-MM-DD (e.g., 2024-01-15) "
                "or leave empty."
            )


def get_validated_status() -> str:
    """Get validated status input from user."""
    while True:
        status = input("Status (default: todo): ").strip().lower() or "todo"
        if status in ("todo", "doing", "done"):
            return status

        print("❌ Invalid status. Choose from: todo, doing, done")


def get_validated_project_id(project_service: ProjectService) -> int:
    """Get validated project ID from user."""
    while True:
        try:
            project_id = int(input("Select project ID: ").strip())
            project_service.get_project(project_id)
            return project_id
        except ValueError:
            print("❌ Invalid project ID. Please enter a number.")
        except NotFoundError as e:
            print(f"❌ {e}")


def get_validated_task_id(task_service: TaskService, project_id: int) -> int:
    """Get validated task ID from user."""
    while True:
        try:
            task_id = int(input("Select task ID: ").strip())
            task_service.get_task(project_id, task_id)
            return task_id
        except ValueError:
            print("❌ Invalid task ID. Please enter a number.")
        except NotFoundError as e:
            print(f"❌ {e}")


# ========================== PROJECT HANDLERS ========================== #

def handle_project_creation(project_service: ProjectService) -> None:
    """Handle project creation with user input."""
    try:
        print("\n--- Create New Project ---")
        name = get_validated_input(
            "Project name: ",
            lambda x: None if x.strip() else exec(
                'raise ValueError("Project name cannot be empty")'
            ),
            "Project name validation failed",
        )
        description = input("Project description: ").strip()

        project = project_service.create_project(name, description)
        print(f"✅ Project created successfully!")
        print(f"   ID: {project.id}, Name: {project.name}")

    except ToDoListError as e:
        print(f"❌ Error: {e}")


def handle_project_listing(project_service: ProjectService) -> None:
    """Display all projects in a formatted way."""
    projects = project_service.list_projects()

    if not projects:
        print("ℹ️ No projects found.")
        return

    print(f"\n--- All Projects ({len(projects)}) ---")
    for project in projects:
        status_counts = project.get_tasks_by_status()
        print(f"\n📁 {project.name} (ID: {project.id})")
        print(f"   📝 {project.description}")
        print(
            f"   📊 Tasks: {project.get_task_count()} total | "
            f"⏳ Todo: {len(status_counts['todo'])} | "
            f"🔄 Doing: {len(status_counts['doing'])} | "
            f"✅ Done: {len(status_counts['done'])}"
        )


def handle_project_update(project_service: ProjectService) -> None:
    """Handle project update with user input."""
    try:
        print("\n--- Update Project ---")
        projects = project_service.list_projects()
        
        if not projects:
            print("❌ No projects available. Please create a project first.")
            return

        print("Available projects:")
        for project in projects:
            print(f"  {project.id}. {project.name}")

        project_id = get_validated_project_id(project_service)
        project = project_service.get_project(project_id)
        
        print(f"\nCurrent project details:")
        print(f"  Name: {project.name}")
        print(f"  Description: {project.description}")
        print("\nEnter new details (press Enter to keep current value):")
        
        new_name = input(f"New project name (current: {project.name}): ").strip()
        if not new_name:
            new_name = project.name
        
        new_description = input(f"New project description (current: {project.description}): ").strip()
        if not new_description:
            new_description = project.description

        updated_project = project_service.update_project(project_id, new_name, new_description)
        print(f"✅ Project updated successfully!")
        print(f"   ID: {updated_project.id}, Name: {updated_project.name}")

    except ToDoListError as e:
        print(f"❌ Error: {e}")


def handle_project_deletion(project_service: ProjectService) -> None:
    """Handle project deletion with user confirmation."""
    try:
        print("\n--- Delete Project ---")
        projects = project_service.list_projects()
        
        if not projects:
            print("❌ No projects available.")
            return

        print("Available projects:")
        for project in projects:
            print(f"  {project.id}. {project.name}")

        project_id = get_validated_project_id(project_service)
        project = project_service.get_project(project_id)
        
        print(f"\n⚠️ Warning: This will delete project '{project.name}' and all its tasks!")
        print(f"   Tasks in this project: {project.get_task_count()}")
        
        confirmation = input("Are you sure? Type 'yes' to confirm: ").strip().lower()
        
        if confirmation == "yes":
            project_service.delete_project(project_id)
            print(f"✅ Project '{project.name}' deleted successfully!")
        else:
            print("❌ Deletion cancelled.")

    except ToDoListError as e:
        print(f"❌ Error: {e}")


# ========================== TASK HANDLERS ========================== #

def handle_task_creation(
    project_service: ProjectService, task_service: TaskService
) -> None:
    """Handle task creation with user input."""
    try:
        print("\n--- Add New Task ---")

        projects = project_service.list_projects()
        if not projects:
            print("❌ No projects available. Please create a project first.")
            return

        print("Available projects:")
        for project in projects:
            print(f"  {project.id}. {project.name}")

        project_id = get_validated_project_id(project_service)
        title = get_validated_input(
            "Task title: ",
            lambda x: None if x.strip() else exec(
                'raise ValueError("Task title cannot be empty")'
            ),
            "Task title validation failed",
        )
        description = input("Task description: ").strip()

        print("Status options: todo, doing, done")
        status = get_validated_status()
        deadline = get_validated_date("Deadline (YYYY-MM-DD, optional): ")

        task = task_service.create_task(
            project_id, title, description, status, deadline
        )
        print(f"✅ Task '{task.title}' added successfully to project!")

    except ToDoListError as e:
        print(f"❌ Error: {e}")


def display_tasks_in_project(
    project_service: ProjectService, task_service: TaskService
) -> None:
    """Display all tasks in a specific project."""
    try:
        print("\n--- View Tasks in Project ---")
        projects = project_service.list_projects()

        if not projects:
            print("ℹ️ No projects available.")
            return

        print("Available projects:")
        for project in projects:
            print(f"  {project.id}. {project.name}")

        project_id = get_validated_project_id(project_service)
        project = project_service.get_project(project_id)

        tasks = task_service.list_tasks(project_id)
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


def handle_task_update(
    project_service: ProjectService, task_service: TaskService
) -> None:
    """Handle task update with user input."""
    try:
        print("\n--- Update Task ---")
        projects = project_service.list_projects()
        
        if not projects:
            print("❌ No projects available. Please create a project first.")
            return

        print("Available projects:")
        for project in projects:
            print(f"  {project.id}. {project.name}")

        project_id = get_validated_project_id(project_service)
        project = project_service.get_project(project_id)
        
        tasks = task_service.list_tasks(project_id)
        if not tasks:
            print(f"❌ No tasks found in project '{project.name}'.")
            return

        print(f"\nTasks in project '{project.name}':")
        for task in tasks:
            deadline_str = f" | 📅 {task.deadline}" if task.deadline else ""
            status_icons = {"todo": "⏳", "doing": "🔄", "done": "✅"}
            icon = status_icons.get(task.status, "📝")
            print(f"  {task.id}. {icon} {task.title} - {task.status}{deadline_str}")

        task_id = get_validated_task_id(task_service, project_id)
        task = task_service.get_task(project_id, task_id)
        
        print(f"\nCurrent task details:")
        print(f"  Title: {task.title}")
        print(f"  Description: {task.description}")
        print(f"  Status: {task.status}")
        print(f"  Deadline: {task.deadline if task.deadline else 'Not set'}")
        print("\nEnter new details (press Enter to keep current value):")
        
        new_title = input(f"New task title (current: {task.title}): ").strip()
        new_description = input(f"New task description (current: {task.description}): ").strip()
        
        print("Status options: todo, doing, done")
        new_status_input = input(f"New status (current: {task.status}): ").strip().lower()
        new_status = new_status_input if new_status_input in ("todo", "doing", "done") else None
        
        new_deadline_input = input(f"New deadline YYYY-MM-DD (current: {task.deadline if task.deadline else 'Not set'}): ").strip()
        new_deadline = None
        if new_deadline_input:
            try:
                new_deadline = datetime.strptime(new_deadline_input, "%Y-%m-%d").date()
            except ValueError:
                print("⚠️ Invalid date format. Keeping current deadline.")
                new_deadline = None  # Don't update if invalid

        # Only update fields that were provided
        updated_task = task_service.update_task(
            project_id,
            task_id,
            title=new_title if new_title else None,
            description=new_description if new_description else None,
            status=new_status if new_status else None,
            deadline=new_deadline if new_deadline_input else None,
        )
        print(f"✅ Task '{updated_task.title}' updated successfully!")

    except ToDoListError as e:
        print(f"❌ Error: {e}")


def handle_task_status_change(
    project_service: ProjectService, task_service: TaskService
) -> None:
    """Handle task status change with user input."""
    try:
        print("\n--- Change Task Status ---")
        projects = project_service.list_projects()
        
        if not projects:
            print("❌ No projects available. Please create a project first.")
            return

        print("Available projects:")
        for project in projects:
            print(f"  {project.id}. {project.name}")

        project_id = get_validated_project_id(project_service)
        project = project_service.get_project(project_id)
        
        tasks = task_service.list_tasks(project_id)
        if not tasks:
            print(f"❌ No tasks found in project '{project.name}'.")
            return

        print(f"\nTasks in project '{project.name}':")
        for task in tasks:
            status_icons = {"todo": "⏳", "doing": "🔄", "done": "✅"}
            icon = status_icons.get(task.status, "📝")
            print(f"  {task.id}. {icon} {task.title} - {task.status}")

        task_id = get_validated_task_id(task_service, project_id)
        task = task_service.get_task(project_id, task_id)
        
        print(f"\nCurrent task: {task.title}")
        print(f"Current status: {task.status}")
        print("Available statuses: todo, doing, done")
        
        new_status = get_validated_status()
        
        if new_status == task.status:
            print(f"⚠️ Task is already in '{new_status}' status.")
            return

        task_service.change_task_status(project_id, task_id, new_status)
        print(f"✅ Task status changed to '{new_status}' successfully!")

    except ToDoListError as e:
        print(f"❌ Error: {e}")


def handle_task_deletion(
    project_service: ProjectService, task_service: TaskService
) -> None:
    """Handle task deletion with user confirmation."""
    try:
        print("\n--- Delete Task ---")
        projects = project_service.list_projects()
        
        if not projects:
            print("❌ No projects available. Please create a project first.")
            return

        print("Available projects:")
        for project in projects:
            print(f"  {project.id}. {project.name}")

        project_id = get_validated_project_id(project_service)
        project = project_service.get_project(project_id)
        
        tasks = task_service.list_tasks(project_id)
        if not tasks:
            print(f"❌ No tasks found in project '{project.name}'.")
            return

        print(f"\nTasks in project '{project.name}':")
        for task in tasks:
            status_icons = {"todo": "⏳", "doing": "🔄", "done": "✅"}
            icon = status_icons.get(task.status, "📝")
            print(f"  {task.id}. {icon} {task.title} - {task.status}")

        task_id = get_validated_task_id(task_service, project_id)
        task = task_service.get_task(project_id, task_id)
        
        print(f"\n⚠️ Warning: This will delete task '{task.title}' from project '{project.name}'!")
        
        confirmation = input("Are you sure? Type 'yes' to confirm: ").strip().lower()
        
        if confirmation == "yes":
            task_service.delete_task(project_id, task_id)
            print(f"✅ Task '{task.title}' deleted successfully!")
        else:
            print("❌ Deletion cancelled.")

    except ToDoListError as e:
        print(f"❌ Error: {e}")


# ========================== REPORTS ========================== #

def show_project_statistics(project_service: ProjectService) -> None:
    """Display comprehensive project statistics."""
    try:
        stats = project_service.get_project_statistics()

        print("\n" + "=" * 50)
        print("📈 PROJECT STATISTICS")
        print("=" * 50)
        print(f"📁 Total Projects: {stats['total_projects']}/{stats['max_projects']}")
        print(f"📝 Total Tasks: {stats['total_tasks']}")
        print("📊 Task Status Distribution:")
        print(f"   ⏳ Todo: {stats['tasks_by_status']['todo']}")
        print(f"   🔄 Doing: {stats['tasks_by_status']['doing']}")
        print(f"   ✅ Done: {stats['tasks_by_status']['done']}")
        print("=" * 50)

    except Exception as e:
        print(f"❌ Error generating statistics: {e}")


# ========================== MAIN LOOP ========================== #

def main() -> None:
    """Main application loop."""
    # Initialize storage and services
    storage = InMemoryStorage()
    project_service = ProjectService(storage)
    task_service = TaskService(storage)

    print("🚀 Welcome to ToDoList CLI!")
    print("Managing your projects and tasks made easy.")

    try:
        while True:
            print_main_menu()
            choice = input("Select an option (1-4): ").strip()

            if choice == "1":
                while True:
                    print_project_menu()
                    sub_choice = input("Select an option (1-5): ").strip()

                    if sub_choice == "1":
                        handle_project_creation(project_service)
                    elif sub_choice == "2":
                        handle_project_listing(project_service)
                    elif sub_choice == "3":
                        handle_project_update(project_service)
                    elif sub_choice == "4":
                        handle_project_deletion(project_service)
                    elif sub_choice == "5":
                        break
                    else:
                        print("❌ Invalid option. Please choose 1–5.")

            elif choice == "2":
                while True:
                    print_task_menu()
                    sub_choice = input("Select an option (1-6): ").strip()

                    if sub_choice == "1":
                        handle_task_creation(project_service, task_service)
                    elif sub_choice == "2":
                        display_tasks_in_project(project_service, task_service)
                    elif sub_choice == "3":
                        handle_task_update(project_service, task_service)
                    elif sub_choice == "4":
                        handle_task_status_change(project_service, task_service)
                    elif sub_choice == "5":
                        handle_task_deletion(project_service, task_service)
                    elif sub_choice == "6":
                        break
                    else:
                        print("❌ Invalid option. Please choose 1–6.")

            elif choice == "3":
                while True:
                    print_reports_menu()
                    sub_choice = input("Select an option (1-4): ").strip()

                    if sub_choice == "1":
                        show_project_statistics(project_service)
                    elif sub_choice == "2":
                        handle_project_listing(project_service)
                    elif sub_choice == "3":
                        print("🛠️ Status filtering feature coming soon...")
                    elif sub_choice == "4":
                        break
                    else:
                        print("❌ Invalid option. Please choose 1–4.")

            elif choice == "4":
                print("\n👋 Thank you for using ToDoList CLI! Goodbye!")
                break

            else:
                print("❌ Invalid option. Please choose 1–4.")

    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user. Goodbye! 👋")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")


if __name__ == "__main__":
    main()
