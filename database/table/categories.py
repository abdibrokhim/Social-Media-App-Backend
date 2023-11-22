from database.connections import get_cursor
from database.constants import *


def create_categories_table():
    try:
        get_cursor().execute('''
                                CREATE TABLE IF NOT EXISTS Categories (
                                    id INTEGER PRIMARY KEY,
                                    createdAt DATETIME NOT NULL,
                                    name TEXT NOT NULL,
                                    isDeleted BOOLEAN NOT NULL
                                );
                            ''')
        get_cursor().close()
        return True
    except Exception as e:
        print(e)
        return False
