# 📝 ToDoList CLI (In-Memory Application)

A lightweight **command-line ToDoList manager** built with Python — designed to help you organize projects and tasks easily, all stored **in-memory** (no database required).

---

## 🚀 Features

✅ Create, list, and manage projects  
✅ Add, update, and track tasks  
✅ Task statuses: `todo`, `doing`, `done`  
✅ View detailed project statistics  
✅ Fully in-memory storage (no external DB)  
✅ Configurable limits via `.env` file  
✅ Clean, PEP 8–compliant architecture

---

## 🧩 Project Structure

```

todolist/
│
├── .venv/                      # Virtual environment
│
├── todolist/                   # Main source code package
│   ├── cli/
│   │   ├── **init**.py
│   │   └── main.py             # CLI entrypoint
│   │
│   ├── core/
│   │   ├── **init**.py
│   │   ├── config.py           # Environment configuration
│   │   ├── exception.py        # Custom exceptions
│   │   ├── project.py          # Project model
│   │   └── task.py             # Task model
│   │
│   ├── storage/
│   │   ├── **init**.py
│   │   └── in_memory.py        # In-memory data storage
│   │
│   ├── **init**.py
│   └── **main**.py             # Poetry run entrypoint
│
├── .env                        # Environment variables
├── .env.example                # Example config file
├── .gitignore
├── poetry.lock
├── pyproject.toml
└── README.md

````

---

## ⚙️ Configuration

You can configure the maximum number of projects and tasks in the `.env` file:

```bash
MAX_NUMBER_OF_PROJECT=10
MAX_NUMBER_OF_TASK=100
````

These limits help prevent exceeding memory usage.

---

## 💻 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yasamin8331/todolist.git
cd todolist
```

### 2️⃣ (Optional) Create a virtual environment

```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3️⃣ Install dependencies

If you’re using Poetry:

```bash
poetry install
```

If you’re using pip:

```bash
pip install -r requirements.txt
```

### 4️⃣ Set up environment variables

Create a `.env` file in the project root:

```bash
echo "MAX_NUMBER_OF_PROJECT=10" >> .env
echo "MAX_NUMBER_OF_TASK=100" >> .env
```

### 5️⃣ Run the application

With Poetry:

```bash
poetry run run-project
```

Or directly with Python:

```bash
python -m todolist.cli.main
```

---

## 📊 Example Usage

### ➕ Create a new project

```
📁 Project name: Portfolio Website
📝 Description: Build personal portfolio
✅ Project created successfully!
```

### ➕ Add a task

```
📝 Task title: Design homepage
📅 Deadline: 2025-10-30
✅ Task added successfully!
```

---

## ⚡ Error Handling

| Exception            | Description                     |
| -------------------- | ------------------------------- |
| `ValidationError`    | Invalid input or format         |
| `NotFoundError`      | Project or task not found       |
| `LimitExceededError` | Max project/task limit exceeded |
| `DuplicateError`     | Duplicate project name          |
| `ToDoListError`      | Generic app-level error         |

---

## 🧭 Future Enhancements

* Persistent storage (SQLite / JSON)
* Task filtering and search
* Deadline reminders and alerts
* Project archiving
* Rich TUI (Text UI)

---

## 👩‍💻 Author

**Fatemeh Tahery**
GitHub: [yasamin8331](https://github.com/yasamin8331)

---



⭐ **If you like this project, give it a star on GitHub!** 🌟
