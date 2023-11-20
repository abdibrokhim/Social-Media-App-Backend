from database.connections import get_cursor
from database.constants import *


def create_posts_table():
    try:
        get_cursor().execute(f'''
                                CREATE TABLE IF NOT EXISTS {posts_table_name} (
                                    id TEXT PRIMARY KEY,
                                    createdAt DATETIME NOT NULL,
                                    description TEXT,
                                    image TEXT,
                                    activityLevel REAL NOT NULL,
                                    isDeleted BOOLEAN NOT NULL,
                                    title TEXT NOT NULL,
                                    updatedAt DATETIME,
                                    userId INTEGER,
                                    FOREIGN KEY (userId) REFERENCES User(id)
                                );
                            ''')
        get_cursor().close()
        return True
    except Exception as e:
        print(e)
        return False


def create_post_likes_table():
    try:
        get_cursor().execute(f'''
                                CREATE TABLE IF NOT EXISTS {post_likes_table_name} (
                                    postId INTEGER,
                                    userId INTEGER,
                                    PRIMARY KEY (postId, userId),
                                    FOREIGN KEY (postId) REFERENCES Posts(id),
                                    FOREIGN KEY (userId) REFERENCES User(id)
                                );
                            ''')
        get_cursor().close()
        return True
    except Exception as e:
        print(e)
        return False
    

def create_post_categories_table():
    try:
        get_cursor().execute(f'''
                                CREATE TABLE IF NOT EXISTS {post_categories_table_name} (
                                    postId INTEGER,
                                    categoryId INTEGER,
                                    PRIMARY KEY (postId, categoryId),
                                    FOREIGN KEY (postId) REFERENCES Posts(id),
                                    FOREIGN KEY (categoryId) REFERENCES Category(id)
                                );
                            ''')
        get_cursor().close()
        return True
    except Exception as e:
        print(e)
        return False
