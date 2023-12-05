from database.connections import get_cursor
from database.constants import *


def create_posts_table():
    try:
        get_cursor().execute('''
                                CREATE TABLE IF NOT EXISTS Posts (
                                    id INTEGER PRIMARY KEY,
                                    createdAt DATETIME NOT NULL,
                                    description TEXT,
                                    image TEXT,
                                    activityLevel REAL NOT NULL,
                                    isDeleted BOOLEAN NOT NULL,
                                    title TEXT NOT NULL,
                                    updatedAt DATETIME
                                );
                            ''')
        get_cursor().close()
        return True
    except Exception as e:
        print(e)
        return False


def create_post_likes_table():
    try:
        get_cursor().execute('''
                                CREATE TABLE IF NOT EXISTS PostLikes (
                                    postId INTEGER,
                                    userId INTEGER,
                                    PRIMARY KEY (postId, userId),
                                    FOREIGN KEY (postId) REFERENCES Posts(id),
                                    FOREIGN KEY (userId) REFERENCES Users(id)
                                );
                            ''')
        get_cursor().close()
        return True
    except Exception as e:
        print(e)
        return False
    

def create_post_categories_table():
    try:
        get_cursor().execute('''
                                CREATE TABLE IF NOT EXISTS PostCategories (
                                    postId INTEGER,
                                    categoryId INTEGER,
                                    PRIMARY KEY (postId, categoryId),
                                    FOREIGN KEY (postId) REFERENCES Posts(id),
                                    FOREIGN KEY (categoryId) REFERENCES Categories(id)
                                );
                            ''')
        get_cursor().close()
        return True
    except Exception as e:
        print(e)
        return False
