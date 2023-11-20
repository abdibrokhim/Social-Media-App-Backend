import sqlite3
from database.constants import db_path


def get_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def get_cursor():
    conn = get_connection()
    cursor = conn.cursor()
    return cursor
