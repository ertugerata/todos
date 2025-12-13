import sqlite3
import json
import random
import string
import os
import time

DB_PATH = '/pb_data/data.db'

def generate_id(length=15):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def init_db():
    print(f"Checking database at {DB_PATH}...")
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}. Maybe PocketBase hasn't started yet?")
        return False

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check if todos collection exists
        cursor.execute("SELECT id FROM _collections WHERE name='todos'")
        if cursor.fetchone():
            print("'todos' collection already exists in DB.")
            conn.close()
            return True

        # Get users collection ID
        cursor.execute("SELECT id FROM _collections WHERE name='users'")
        row = cursor.fetchone()
        if not row:
            print("Error: 'users' collection not found in DB.")
            conn.close()
            return False

        users_id = row[0]
        print(f"Found 'users' collection ID: {users_id}")

        # Prepare fields JSON
        fields = [
            {
                "system": False,
                "id": generate_id(),
                "name": "title",
                "type": "text",
                "required": True,
                "presentable": True,
                "min": None,
                "max": None,
                "pattern": ""
            },
            {
                "system": False,
                "id": generate_id(),
                "name": "is_completed",
                "type": "bool",
                "required": False,
                "presentable": False
            },
            {
                "system": False,
                "id": generate_id(),
                "name": "user",
                "type": "relation",
                "required": True,
                "presentable": False,
                "collectionId": users_id,
                "cascadeDelete": False,
                "minSelect": None,
                "maxSelect": 1,
                "displayFields": []
            }
        ]

        fields_json = json.dumps(fields)
        collection_id = generate_id()

        # Read SQL template
        with open('init_schema.sql', 'r') as f:
            sql_template = f.read()

        # Format the SQL
        final_sql = sql_template.format(
            collection_id=collection_id,
            schema_json=fields_json
        )

        print("Executing SQL to create 'todos' collection...")
        cursor.executescript(final_sql)
        conn.commit()
        print("'todos' collection created successfully via SQL.")

        conn.close()
        return True

    except Exception as e:
        print(f"Error initializing DB: {e}")
        return False

if __name__ == "__main__":
    # Retry loop
    for i in range(30):
        if init_db():
            break
        print(f"Retrying in 2 seconds... ({i+1}/30)")
        time.sleep(2)
