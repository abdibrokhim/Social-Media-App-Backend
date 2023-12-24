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
                                    userId INTEGER,
                                    metaInfoId INTEGER,
                                    PRIMARY KEY (userId, metaInfoId),
                                    FOREIGN KEY (userId) REFERENCES Users(id),
                                    FOREIGN KEY (metaInfoId) REFERENCES MetaInfo(id)
                                );
                            ''')
        get_cursor().close()
        return True
    except Exception as e:
        print(e)
        return False
    

def create_user_social_media_links_table():
    try:
        get_cursor().execute('''
                                CREATE TABLE IF NOT EXISTS UserSocialMediaLinks (
                                    userId INTEGER,
                                    socialMediaLinkId INTEGER,
                                    PRIMARY KEY (userId, socialMediaLinkId),
                                    FOREIGN KEY (userId) REFERENCES Users(id),
                                    FOREIGN KEY (socialMediaLinkId) REFERENCES SocialMediaLinks(id)
                                );
                            ''')
        get_cursor().close()
        return True
    except Exception as e:
        print(e)
        return False


def create_meta_info_table():
    try:
        get_cursor().execute('''
                                CREATE TABLE IF NOT EXISTS MetaInfo (
                                    id INTEGER PRIMARY KEY,
                                    followers INTEGER,
                                    following INTEGER,
                                    likes INTEGER
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
                                    url TEXT NOT NULL
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
                                CREATE TABLE IF NOT EXISTS RevokedTokens (
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


def create_user_posts_table():
    try:
        get_cursor().execute('''
                                CREATE TABLE IF NOT EXISTS UserPosts (
                                    userId INTEGER,
                                    postId INTEGER,
                                    PRIMARY KEY (userId, postId),
                                    FOREIGN KEY (userId) REFERENCES Users(id),
                                    FOREIGN KEY (postId) REFERENCES Posts(id)
                                );
                            ''')
        get_cursor().close()
        return True
    except Exception as e:
        print(e)
        return False


def create_user_post_views_table():
    try:
        get_cursor().execute('''
                                CREATE TABLE IF NOT EXISTS UserPostViews (
                                    id INTEGER PRIMARY KEY,
                                    userId INTEGER,
                                    postId INTEGER,
                                    FOREIGN KEY (userId) REFERENCES Users(id),
                                    FOREIGN KEY (postId) REFERENCES Posts(id)
                                );
                            ''')
        get_cursor().close()
        return True
    except Exception as e:
        print(e)
        return False
    

def create_user_subscription_table():
    try:
        get_cursor().execute('''
                                CREATE TABLE IF NOT EXISTS UserSubscriptions (
                                    id INTEGER PRIMARY KEY,
                                    userId INTEGER,
                                    subscribedDate DATETIME,
                                    expirationDate DATETIME,
                                    expired BOOLEAN NOT NULL,
                                    FOREIGN KEY (userId) REFERENCES Users(id)
                                );
                            ''')
        get_cursor().close()
        return True
    except Exception as e:
        print(e)
        return False
