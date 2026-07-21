import sqlite3

DATABASE = "database/aizalstudio.db"

def get_connection():

    connection = sqlite3.connect(
        DATABASE,
        timeout=30,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection