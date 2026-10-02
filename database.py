import sqlite3


# Database se connection banane wala function
def get_connection():
    connection = sqlite3.connect("database.db")
    return connection