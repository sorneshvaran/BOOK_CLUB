import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # backend/
DB_DIR = os.path.join(BASE_DIR, 'db')
SCHEMA_PATH = os.path.join(DB_DIR, 'schema.sql')
DB_PATH = os.path.join(DB_DIR, 'book_club.db')

os.makedirs(DB_DIR, exist_ok=True)

if not os.path.exists(SCHEMA_PATH):
    print(f"Schema file not found: {SCHEMA_PATH}")
    raise SystemExit(1)

# Create DB if missing and apply schema (safe to run multiple times)
conn = sqlite3.connect(DB_PATH)
with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
    schema = f.read()
conn.executescript(schema)
conn.close()
print(f"Initialized database at: {DB_PATH}")