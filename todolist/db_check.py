"""Utility script to verify database connection for Phase 2.

Run with:

    poetry run python -m todolist.db_check
"""

from sqlalchemy import text

from todolist.db import engine


def main() -> None:
    """Test database connectivity and print current DB/user."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("✅ Connected to database successfully!")
            row = conn.execute(
                text("SELECT current_database() AS db, current_user AS usr;")
            ).mappings().one()
            print(f"🗃 DB: {row['db']} | 👤 User: {row['usr']}")
    except Exception as e:  # pragma: no cover - manual debug helper
        print("❌ Database connection failed:", e)


if __name__ == "__main__":
    main()


