import sqlite3

connection = sqlite3.connect("database/aizalstudio.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS admissions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    full_name TEXT,

    father_name TEXT,

    email TEXT,

    phone TEXT,

    city TEXT,

    qualification TEXT,

    course TEXT,

    status TEXT,

    apply_date TEXT

)
""")

connection.commit()

connection.close()

print("Admissions table created successfully!")