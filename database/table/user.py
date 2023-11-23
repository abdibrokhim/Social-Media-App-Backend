from database.connections import get_cursor
from database.constants import *


def create_user_table():
    try:
        get_cursor().execute('''
                                CREATE TABLE IF NOT EXISTS Users (
                                    id INTEGER PRIMARY KEY,
                                    firstName TEXT,
                                    lastName TEXT,
                                    username TEXT NOT NULL UNIQUE,
                                    profileImage TEXT,
                                    email TEXT NOT NULL UNIQUE,
                                    password TEXT NOT NULL,
                                    activityLevel REAL NOT NULL,
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
        get_cursor().execute('''
                                CREATE TABLE IF NOT EXISTS UserMetaInfo (
                                    id INTEGER PRIMARY KEY,
                                    followers INTEGER,
                                    following INTEGER,
                                    likes INTEGER,
                                    userId INTEGER,
                                    FOREIGN KEY (userId) REFERENCES Users(id)
                                );
                            ''')
        get_cursor().close()
        return True
    except Exception as e:
        print(e)
        return False
    

def create_social_media_links_table():
    try:
        get_cursor().execute('''
                                CREATE TABLE IF NOT EXISTS SocialMediaLinks (
                                    id INTEGER PRIMARY KEY,
                                    icon TEXT,
                                    name TEXT NOT NULL,
                                    url TEXT NOT NULL,
                                    userId INTEGER,
                                    FOREIGN KEY (userId) REFERENCES Users(id)
                                );
                            ''')
        get_cursor().close()
        return True
    except Exception as e:
        print(e)
        return False
    

def create_user_interests_table():
    try:
        get_cursor().execute('''
                                CREATE TABLE IF NOT EXISTS UserInterests (
                                    userId INTEGER,
                                    categoryId INTEGER,
                                    PRIMARY KEY (userId, categoryId),
                                    FOREIGN KEY (userId) REFERENCES Users(id),
                                    FOREIGN KEY (categoryId) REFERENCES Categories(id)
                                );
                            ''')
        get_cursor().close()
        return True
    except Exception as e:
        print(e)
        return False

def create_revoked_tokens_table():
    try:
        get_cursor().execute('''
                                CREATE TABLE RevokedTokens (
                                    jti TEXT PRIMARY KEY,
                                    revoked_at DATETIME NOT NULL
                                );
                            ''')
        get_cursor().close()
        return True
    except Exception as e:
        print(e)
        return False

def create_user_follow_table():
    try:
        get_cursor().execute('''
                                CREATE TABLE IF NOT EXISTS UserFollowers (
                                    followerId INTEGER,
                                    followingId INTEGER,
                                    PRIMARY KEY (followerId, followingId),
                                    FOREIGN KEY (followerId) REFERENCES Users(id),
                                    FOREIGN KEY (followingId) REFERENCES Users(id)
                                );
                            ''')
        get_cursor().close()
        return True
    except Exception as e:
        print(e)
        return False