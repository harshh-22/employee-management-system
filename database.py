import sqlite3

DB_NAME = "employees.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn 

def create_table():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            department TEXT,
            salary REAL,
            joining_date TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_employee(name, email, department, salary, joining_date):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO employees (name, email, department, salary, joining_date)
        VALUES (?, ?, ?, ?, ?)
         """,
         (name, email, department, salary, joining_date),
    )
    conn.commit()
    conn.close() 

def get_all_employees():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM employees ORDER by id"
    ).fetchall()
    conn.close()
    return[dict(row) for row in rows] 