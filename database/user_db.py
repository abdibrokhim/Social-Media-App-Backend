from database.connections import get_connection, get_cursor
from database.constants import *


def create_user_table():
    try:
        get_cursor().execute(f'''
                                CREATE TABLE IF NOT EXISTS {user_table_name} (
                                    id INTEGER PRIMARY KEY,
                                    firstName TEXT NOT NULL,
                                    lastName TEXT NOT NULL,
                                    username TEXT NOT NULL UNIQUE,
                                    profileImage TEXT,
                                    email TEXT NOT NULL UNIQUE,
                                    isActive BOOLEAN NOT NULL,
                                    isDeleted BOOLEAN NOT NULL,
                                    isEmailValidated BOOLEAN NOT NULL,
                                    createdAt DATETIME NOT NULL,
                                    updatedAt DATETIME
                                );
                            ''')
        get_cursor().close()
        return True
    except Exception as e:
        print(e)
        return False



def create_user_meta_info_table():
    try:
        get_cursor().execute(f'''
                                CREATE TABLE IF NOT EXISTS {user_meta_info_table_name} (
                                    id TEXT PRIMARY KEY,
                                    userId INTEGER,
                                    FOREIGN KEY (userId) REFERENCES User(id)
                                );
                            ''')
        get_cursor().close()
        return True
    except Exception as e:
        print(e)
        return False
    

def create_social_media_links_table():
    try:
        get_cursor().execute(f'''
                                CREATE TABLE IF NOT EXISTS {social_media_links_table_name} (
                                    id TEXT PRIMARY KEY,
                                    icon TEXT,
                                    name TEXT NOT NULL,
                                    url TEXT NOT NULL,
                                    userId INTEGER,
                                    FOREIGN KEY (userId) REFERENCES User(id)
                                );
                            ''')
        get_cursor().close()
        return True
    except Exception as e:
        print(e)
        return False
    

def create_user_interests_table():
    try:
        get_cursor().execute(f'''
                                CREATE TABLE IF NOT EXISTS {user_interests_table_name} (
                                    userId INTEGER,
                                    categoryId TEXT,
                                    PRIMARY KEY (userId, categoryId),
                                    FOREIGN KEY (userId) REFERENCES User(id),
                                    FOREIGN KEY (categoryId) REFERENCES Category(id)
                                );
                            ''')
        get_cursor().close()
        return True
    except Exception as e:
        print(e)
        return False
