import sqlite3
import getpass
import hashlib

def create_user_table():
    with sqlite3.connect('user_db.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')

def signup():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    try:
        with sqlite3.connect('user_db.db') as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_hash))
            connection.commit()
        print("Signup successful!")
    except sqlite3.Error as e:
        print(f"An error occurred during signup: {str(e)}")