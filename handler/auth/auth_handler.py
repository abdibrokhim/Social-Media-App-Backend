from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    current_user,
    jwt_required,
    get_jwt,
    get_jwt_identity
)
import sqlite3
from database.connections import get_connection
from datetime import datetime
from service.wsgi import jwt

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()

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
        cursor.close()
        conn.close()

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    try:
        existing_user = execute_query("SELECT id FROM Users WHERE email = ?", (data['email'],), fetchone=True)
        if existing_user:
            return jsonify({'error': 'User with this email already exists'}), 409

        user_id = execute_query("""
            INSERT INTO Users (username, email, password, activityLevel, isDeleted, isEmailValidated, createdAt) 
            VALUES (?, ?, ?, 1, 0, 0, ?)
        """, (data['username'], data['email'], hashed_password, datetime.now()), commit=True).lastrowid

        execute_query("""
            INSERT INTO UserMetaInfo (followers, following, likes, userId)
            VALUES (0, 0, 0, ?)
        """, (user_id,), commit=True)

        return jsonify({'message': 'User registered successfully'}), 201

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.json

    try:
        user = execute_query("SELECT * FROM Users WHERE username = ?", (data['username'],), fetchone=True)
        if user and bcrypt.check_password_hash(user['password'], data['password']):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return jsonify(access_token=access_token, refresh_token=refresh_token), 200

        return jsonify({'error': 'Invalid username or password'}), 401
    
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.get("/api/new_access_token")
@jwt_required(refresh=True)
def refresh_access():
    try:
        identity = get_jwt_identity()
        new_access_token = create_access_token(identity=identity)
        return jsonify(access_token=new_access_token), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.get('/api/logout')
@jwt_required(verify_type=False)
def logout_user():
    try:
        jti = get_jwt()['jti']
        execute_query("INSERT INTO revoked_tokens (jti, revoked_at) VALUES (?, ?)", (jti, datetime.now()), commit=True)
        return jsonify({"message": "Token revoked successfully"}), 200

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    try:
        token = execute_query("SELECT * FROM revoked_tokens WHERE jti = ?", (jti,), fetchone=True)
        return token is not None
    except sqlite3.Error:
        return False

@auth_bp.get("/api/me")
@jwt_required()
def whoami():
    try:
        return jsonify({
                "user_details": {
                    "username": current_user.username,
                    "email": current_user.email,
                },
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500