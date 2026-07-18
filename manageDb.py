# ORM

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


def insertData(conn, data):
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Tasks (title, desc, status) VALUES (?, ?, ?)",
        data
    )
    conn.commit()

    return True


def getData(conn):
    cursor = conn.cursor()

    cursor.execute("SELECT title, desc, id, status FROM Tasks")
    conn.commit()

    rows = cursor.fetchall()
    result = []

    for row in rows:
        result.append(list(row))

    print(result)
    return result


def editRow(conn, updatedData, id):
    cursor = conn.cursor()
    print("Updating row...")
    for k, v in updatedData.items():
        cursor.execute(f"UPDATE Tasks SET {k} = ? WHERE id = ?", (v, id))
        conn.commit()

    print("Row updated")

    return True