import sqlite3

connection = sqlite3.connect("database/aizalstudio.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    certificate_id TEXT UNIQUE,

    student_name TEXT,

    father_name TEXT,

    phone TEXT,

    email TEXT,

    city TEXT,

    course TEXT,

    duration TEXT,

    grade TEXT,

    issue_date TEXT,

    status TEXT

)
""")

connection.commit()

connection.close()

print("Database Created Successfully")