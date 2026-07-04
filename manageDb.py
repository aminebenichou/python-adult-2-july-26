import sqlite3


def createDb():
    print("Creating Database...")
    conn = sqlite3.connect("Todo.db")
    print("DB Created")

    return conn



def createTable(conn):
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            desc TEXT,
            status TEXT
        )
    """)

    conn.commit()
    print("Table created Successfully...")
    return True


def insertData():
    pass