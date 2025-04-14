# import sqlite3
# import bcrypt

# def create_users_table():
#     conn = sqlite3.connect("users.db")
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS users (
#                     username TEXT PRIMARY KEY,
#                     password TEXT
#                 )''')
#     conn.commit()
#     conn.close()

# def add_user(username, password):
#     conn = sqlite3.connect("users.db")
#     c = conn.cursor()
#     hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
#     c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
#     conn.commit()
#     conn.close()

# def validate_user(username, password):
#     conn = sqlite3.connect("users.db")
#     c = conn.cursor()
#     c.execute("SELECT password FROM users WHERE username = ?", (username,))
#     data = c.fetchone()
#     conn.close()
#     if data and bcrypt.checkpw(password.encode(), data[0]):
#         return True
#     return False





























# import sqlite3

# def create_users_table():
#     conn = sqlite3.connect("users.db")
#     c = conn.cursor()
#     c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)')
#     conn.commit()
#     conn.close()

# def add_user(username, password):
#     conn = sqlite3.connect("users.db")
#     c = conn.cursor()
#     c.execute('INSERT INTO users(username, password) VALUES (?, ?)', (username, password))
#     conn.commit()
#     conn.close()

# def validate_user(username, password):
#     conn = sqlite3.connect("users.db")
#     c = conn.cursor()
#     c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
#     result = c.fetchone()
#     conn.close()
#     return result is not None



# def user_exists(username):
#     conn = sqlite3.connect("users.db")
#     c = conn.cursor()
#     c.execute("SELECT * FROM users WHERE username = ?", (username,))
#     data = c.fetchone()
#     conn.close()
#     return data is not None


# def get_all_users():
#     conn = sqlite3.connect("users.db")
#     c = conn.cursor()
#     c.execute("SELECT username, password FROM users")
#     users = c.fetchall()
#     conn.close()
#     return users














import sqlite3
from datetime import datetime


def create_users_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY, 
            password TEXT, 
            role TEXT DEFAULT 'user'
        )
    ''')
    conn.commit()
    conn.close()


def add_user(username, password, role='user'):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('INSERT INTO users(username, password, role) VALUES (?, ?, ?)', 
              (username, password, role))
    conn.commit()
    conn.close()


def validate_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
              (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None


def user_exists(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    data = c.fetchone()
    conn.close()
    return data is not None


def get_user_role(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None


def get_all_users():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT username, role FROM users")
    users = c.fetchall()
    conn.close()
    return users



def create_login_logs_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS login_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            login_time TEXT
        )
    ''')
    conn.commit()
    conn.close()






def log_user_login(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO login_logs (username, login_time) VALUES (?, ?)", (username, login_time))
    conn.commit()
    conn.close()





def get_login_logs():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT username, login_time FROM login_logs ORDER BY login_time DESC")
    logs = c.fetchall()
    conn.close()
    return logs
