import mysql.connector
from mysql.connector import Error
import hashlib
from datetime import datetime

# === Connection ===
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='employee'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()

# === Utilities ===
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# === Auth ===
def register_user(email, username, password):
    connection = create_connection()
    if not connection:
        return False, "Failed to connect to database"

    cursor = connection.cursor()
    try:
        email = email.strip().lower()
        username = username.strip()
        hashed_pw = hash_password(password)

        print(f"[DEBUG] Trying to insert: {email}, {username}, {hashed_pw}")
        sql = "INSERT INTO users (email, username, password) VALUES (%s, %s, %s)"
        cursor.execute(sql, (email, username, hashed_pw))
        connection.commit()
        return True, "User registered successfully"
    except mysql.connector.Error as err:
        print(f"[ERROR] {err}")
        if err.errno == 1062:
            if "email" in str(err).lower():
                return False, "Email already registered"
            elif "username" in str(err).lower():
                return False, "Username already taken"
        return False, f"Database error: {err}"
    finally:
        cursor.close()
        close_connection(connection)

def login_user(email, password):
    connection = create_connection()
    if not connection:
        return False, "Failed to connect to database"

    cursor = connection.cursor()
    try:
        hashed_pw = hash_password(password)
        sql = "SELECT id, username FROM users WHERE email = %s AND password = %s"
        cursor.execute(sql, (email, hashed_pw))
        result = cursor.fetchone()
        if result:
            return True, {"id": result[0], "username": result[1]}
        else:
            return False, "Email or password incorrect"
    except mysql.connector.Error as err:
        return False, f"Database error: {err}"
    finally:
        cursor.close()
        close_connection(connection)

# === Employee ===
def get_all_employees():
    connection = create_connection()
    if not connection:
        return []

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM employees")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"[ERROR] {err}")
        return []
    finally:
        cursor.close()
        close_connection(connection)

def add_employee(name, position, department, status):
    connection = create_connection()
    if not connection:
        return False

    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO employees (name, position, department, status) VALUES (%s, %s, %s, %s)",
            (name, position, department, status)
        )
        connection.commit()
        return True
    except mysql.connector.Error as err:
        print(f"[ERROR] {err}")
        return False
    finally:
        cursor.close()
        close_connection(connection)

def delete_employee(emp_id):
    connection = create_connection()
    if not connection:
        return False

    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM employees WHERE id = %s", (emp_id,))
        connection.commit()
        return True
    except mysql.connector.Error as err:
        print(f"[ERROR] {err}")
        return False
    finally:
        cursor.close()
        close_connection(connection)

def update_employee(emp_id, name, position, department, status):
    connection = create_connection()
    if not connection:
        return False

    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE employees SET name=%s, position=%s, department=%s, status=%s WHERE id=%s",
            (name, position, department, status, emp_id)
        )
        connection.commit()
        return True
    except mysql.connector.Error as err:
        print(f"[ERROR] {err}")
        return False
    finally:
        cursor.close()
        close_connection(connection)

# === Departments ===
def get_all_departments():
    connection = create_connection()
    if not connection:
        return []

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM departments")
        return cursor.fetchall()
    except Error as e:
        print(f"[ERROR] {e}")
        return []
    finally:
        cursor.close()
        close_connection(connection)

def add_department(department_name, manager):
    connection = create_connection()
    if not connection:
        return False

    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO departments (department_name, manager) VALUES (%s, %s)",
            (department_name, manager)
        )
        connection.commit()
        return True
    except Error as e:
        print(f"[ERROR] {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)

def update_department(dep_id, department_name, manager):
    connection = create_connection()
    if not connection:
        return False

    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE departments SET department_name=%s, manager=%s WHERE id=%s",
            (department_name, manager, dep_id)
        )
        connection.commit()
        return True
    except Error as e:
        print(f"[ERROR] {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)

def delete_department(dep_id):
    connection = create_connection()
    if not connection:
        return False

    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM departments WHERE id=%s", (dep_id,))
        connection.commit()
        return True
    except Error as e:
        print(f"[ERROR] {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)

# === Attendance ===
def get_all_attendance():
    connection = create_connection()
    if not connection:
        return []

    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT a.id, e.name, a.status, a.checkin_time, a.checkout_time, a.notes, a.date
            FROM attendance a
            JOIN employees e ON a.employee_id = e.id
            ORDER BY a.date DESC
        """)
        return cursor.fetchall()
    except Error as e:
        print(f"[ERROR] {e}")
        return []
    finally:
        cursor.close()
        close_connection(connection)

def add_attendance(name, status, checkin, checkout, notes, date):
    connection = create_connection()
    if not connection:
        return False

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM employees WHERE name = %s", (name,))
        result = cursor.fetchone()
        if not result:
            print("[ERROR] Employee not found")
            return False
        employee_id = result[0]
        cursor.execute("""
            INSERT INTO attendance (employee_id, status, checkin_time, checkout_time, notes, date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (employee_id, status, checkin, checkout, notes, date))
        connection.commit()
        return True
    except Error as e:
        print(f"[ERROR] {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)

def delete_attendance_by_id(att_id):
    connection = create_connection()
    if not connection:
        return False

    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM attendance WHERE id = %s", (att_id,))
        connection.commit()
        return True
    except Error as e:
        print(f"[ERROR] {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)

def get_all_employee_names():
    connection = create_connection()
    if not connection:
        return []

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT name FROM employees")
        return [row[0] for row in cursor.fetchall()]
    except Error as e:
        print(f"[ERROR] {e}")
        return []
    finally:
        cursor.close()
        close_connection(connection)

# === Payroll ===
def get_all_payroll():
    conn = create_connection()
    if conn is None:
        print("Database connection failed!")
        return []
    cursor = conn.cursor()
    query = """SELECT p.id, p.period, e.name, p.base_salary, p.bonus, p.deductions, p.net_pay, p.status
               FROM payroll p
               JOIN employees e ON p.employee_id = e.id
               ORDER BY p.period DESC"""
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def calculate_net_pay(base_salary, bonus, deductions):
    return base_salary + bonus - deductions

def insert_payroll(employee_id, period, base_salary, bonus, deductions, net_pay, status):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO payroll (employee_id, period, base_salary, bonus, deductions, net_pay, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (employee_id, period, base_salary, bonus, deductions, net_pay, status))
    conn.commit()
    conn.close()

def update_payroll(payroll_id, employee_id, period, base_salary, bonus, deductions, net_pay, status):
    connection = create_connection()
    if not connection:
        return False
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE payroll
            SET employee_id=%s, period=%s, base_salary=%s, bonus=%s, deductions=%s, net_pay=%s, status=%s
            WHERE id=%s
        """, (employee_id, period, base_salary, bonus, deductions, net_pay, status, payroll_id))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print("Error updating payroll:", e)
        return False
    finally:
        cursor.close()
        connection.close()

def get_payroll_by_id(payroll_id):
    connection = create_connection()
    if not connection:
        return None
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT p.id, p.employee_id, p.period, p.base_salary, p.bonus, 
                   p.deductions, p.net_pay, p.status, e.name
            FROM payroll p
            JOIN employees e ON p.employee_id = e.id
            WHERE p.id = %s
        """, (payroll_id,))
        row = cursor.fetchone()
        if row:
            return (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        return None
    except Exception as e:
        print(f"Error fetching payroll by ID: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def get_payroll_summary_by_period(period):
    conn = create_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.name, p.base_salary, p.bonus, p.deductions, p.net_pay
            FROM payroll p
            JOIN employees e ON p.employee_id = e.id
            WHERE p.period = %s
            ORDER BY e.name ASC
        """, (period,))
        return cursor.fetchall()
    except Exception as e:
        print(f"[ERROR] get_payroll_summary_by_period: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# === Audit Logs ===
def get_audit_logs():
    conn = create_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.timestamp, u.username, a.action
            FROM audit_logs a
            JOIN users u ON a.user_id = u.id
            ORDER BY a.timestamp DESC
        """)
        return cursor.fetchall()
    except Exception as e:
        print("[ERROR] get_audit_logs:", e)
        return []
    finally:
        cursor.close()
        conn.close()

def log_action(user_id, action):
    conn = create_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO audit_logs (user_id, action, timestamp)
            VALUES (%s, %s, NOW())
        """, (user_id, action))
        conn.commit()
    except Exception as e:
        print("[ERROR] log_action:", e)
    finally:
        cursor.close()
        conn.close()
