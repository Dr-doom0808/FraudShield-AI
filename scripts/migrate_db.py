import sqlite3
import os

db_path = "fraud_detection.db"

def migrate():
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found. No migration needed.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Checking for missing columns...")

    # Check claims table
    cursor.execute("PRAGMA table_info(claims)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'created_at' not in columns:
        print("Adding created_at to claims table...")
        # Add without default to avoid "non-constant default" error
        cursor.execute("ALTER TABLE claims ADD COLUMN created_at DATETIME")
        # Update existing rows with a timestamp
        cursor.execute("UPDATE claims SET created_at = CURRENT_TIMESTAMP")
    else:
        print("created_at already exists in claims table.")

    # Check predictions table
    cursor.execute("PRAGMA table_info(predictions)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'created_at' not in columns:
        print("Adding created_at to predictions table...")
        cursor.execute("ALTER TABLE predictions ADD COLUMN created_at DATETIME")
        cursor.execute("UPDATE predictions SET created_at = CURRENT_TIMESTAMP")
    else:
        print("created_at already exists in predictions table.")

    conn.commit()
    conn.close()
    print("Migration completed.")

if __name__ == "__main__":
    migrate()
