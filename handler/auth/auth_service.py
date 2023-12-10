from handler.query_helpers import execute_query
from datetime import datetime
import sqlite3
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token

bcrypt = Bcrypt()


def register_user_service(username, email, password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    try:
        # Check if email or username already exists
        if user_exists(email, username):
            return 'User with this email or username already exists', 409

        user_id = create_user(username, email, hashed_password)
        meta_info_id = create_meta_info()

        link_user_with_meta_info(user_id, meta_info_id)

        print({'message': 'User registered successfully', 'on': 'register_user_service','timestamp': datetime.now()})
        return 'User registered successfully', 201

    except sqlite3.Error as e:
        return str(e), 500

def user_exists(email, username):
    if execute_query("SELECT id FROM Users WHERE email = ?", (email,), fetchone=True):
        return True
    if execute_query("SELECT id FROM Users WHERE username = ?", (username,), fetchone=True):
        return True
    return False

def create_user(username, email, hashed_password):
    return execute_query("""
        INSERT INTO Users (username, email, password, activityLevel, isDeleted, isEmailValidated, createdAt) 
        VALUES (?, ?, ?, 1, 0, 0, ?)
    """, (username, email, hashed_password, datetime.now()), commit=True).lastrowid

def create_meta_info():
    return execute_query("""
        INSERT INTO MetaInfo (followers, following, likes)
        VALUES (0, 0, 0)
    """, commit=True).lastrowid

def link_user_with_meta_info(user_id, meta_info_id):
    execute_query("""
        INSERT INTO UserMetaInfo (userId, metaInfoId)
        VALUES (?, ?)
    """, (user_id, meta_info_id), commit=True)


def get_revoked_token_service(jti):
    token = execute_query("SELECT * FROM RevokedTokens WHERE jti = ?", (jti,), fetchone=True)
    
    print({'message': 'returning revoked token', 'on': 'get_revoked_token_service','timestamp': datetime.now()})
    return token


def login_user_service(username, password):
    try:
        user = execute_query("SELECT * FROM Users WHERE username = ?", (username,), fetchone=True)
        user_data = {}
        
        if user and bcrypt.check_password_hash(user['password'], password):
            access_token = create_access_token(identity=username, fresh=True, expires_delta=False)
            refresh_token = create_refresh_token(identity=username)

            user_dict = {key: user[key] for key in user.keys()}
            user_data['user'] = user_dict
            user_data['access_token'] = access_token
            user_data['refresh_token'] = refresh_token
            
            print({'message': 'returning user data', 'on': 'login_user_service','timestamp': datetime.now()})
            return user_data, 200
        print({'message': 'Invalid username or password', 'on': 'login_user_service','timestamp': datetime.now()})
        return {'error': 'Invalid username or password'}, 401

    except sqlite3.Error as e:
        return {'error': str(e)}, 500


def forgot_password_service(email):

    user = execute_query("SELECT * FROM Users WHERE email = ?", (email,), fetchone=True)
    if user:
        print({'message': 'Email sent successfully', 'on': 'forgot_password_service', 'timestamp': datetime.now()})
        return 'Email sent successfully', 200
    
    print({'message': 'User with this email does not exist', 'on': 'forgot_password_service', 'timestamp': datetime.now()})
    return 'User with this email does not exist', 404


def logout_user_service(jti):
    execute_query("INSERT INTO RevokedTokens (jti, revoked_at) VALUES (?, ?)", (jti, datetime.now()), commit=True)
    
    print({'message': 'Token revoked successfully', 'on': 'logout_user_service', 'timestamp': datetime.now()})
    return "Token revoked successfully", 200

   