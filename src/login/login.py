import sqlite3
import hashlib
import getpass

class User:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username

def clean_database():
    try:
        connection = sqlite3.connect('user_db.db')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users")
        connection.commit()
        print("Database cleaned successfully!")
    except sqlite3.Error as e:
        print("Error cleaning the database:", e)
    finally:
        connection.close()

def login():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    connection = sqlite3.connect('user_db.db')
    cursor = connection.cursor()
    cursor.execute("SELECT id, username FROM users WHERE username = ? AND password = ?", (username, password_hash))
    user = cursor.fetchone()
    connection.close()

    if user:
        user_id, username = user
        logged_in_user = User(user_id, username)
        print("Login successful!")
        return logged_in_user
    else:
        print("Login failed fucking dumbass")
        clean_database()
        return None

