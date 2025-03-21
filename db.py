# CHOSEN SCRUM BETA
# All code and functions are by Chosen
# Handles all database initialization and ensures required tables exist.
# PSUDOCODE:
#Define create_database():
#    Connect to SQLite database
#    Create 'users' table if it doesn't exist
#    Create 'logs' table if it doesn't exist
#    Commit changes and close connection
#############################################################################


import sqlite3

def create_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
