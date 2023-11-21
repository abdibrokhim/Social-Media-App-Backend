import sqlite3
from database.connections import get_connection
from datetime import datetime

def execute_query(query, params=(), fetchone=False, commit=False):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        if commit:
            conn.commit()
        return cursor.fetchone() if fetchone else cursor
    except sqlite3.Error as e:
        raise e
    finally:
        if fetchone or commit:
            # Close the cursor only if we're not returning it for further use
            if cursor:
                cursor.close()
            if conn:
                conn.close()