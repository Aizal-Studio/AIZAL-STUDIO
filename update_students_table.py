import sqlite3

connection = sqlite3.connect("database/aizalstudio.db")
cursor = connection.cursor()

columns = [
    ("phone", "TEXT"),
    ("email", "TEXT"),
    ("city", "TEXT")
]

for column_name, column_type in columns:
    try:
        cursor.execute(
            f"ALTER TABLE students ADD COLUMN {column_name} {column_type}"
        )
        print(f"{column_name} column added.")
    except sqlite3.OperationalError:
        print(f"{column_name} column already exists.")

connection.commit()
connection.close()

print("Students table updated successfully!")