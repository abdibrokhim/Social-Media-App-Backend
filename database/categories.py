from database.connections import get_connection, get_cursor
from database.constants import *


def create_categories_table():
    try:
        get_cursor().execute(f'''
                                CREATE TABLE IF NOT EXISTS {categories_table_name} (
                                    id TEXT PRIMARY KEY,
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
