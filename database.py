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

def get_employee_by_id(employee_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM employees WHERE id = ?",
        (employee_id,),
    ).fetchone()
    conn.close()
    if row is None:
        return None
    return dict(row)

def update_employee(employee_id, name, email, department, salary, joining_date):
    conn = get_connection()
    cursor = conn.execute(
        """
        UPDATE employees
        SET name = ?, email = ?, department = ?, salary = ?, joining_date = ?
        WHERE id = ?
        """,
        (name, email, department, salary, joining_date, employee_id),
    )
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated 

def delete_employee(employee_id):
    conn = get_connection()
    cursor = conn.execute(
        "DELETE FROM employees WHERE id = ?",
        (employee_id,),
    )
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted 

def search_employees(keyword):
    conn = get_connection()
    pattern = f"%{keyword}%"
    rows = conn.execute(
        "SELECT * FROM employees WHERE name LIKE ? OR department LIKE ? ORDER BY id",
        (pattern, pattern),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_summary():
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
    departments = conn.execute(
        "SELECT COUNT(DISTINCT department) FROM employees WHERE department != ''"
    ).fetchone()[0]
    conn.close()
    return {"total": total, "departments": departments}