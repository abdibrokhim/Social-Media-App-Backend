from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    get_jwt_identity
)
import sqlite3
from datetime import datetime
from handler.query_helpers import execute_query

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()


@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    try:
        existing_user = execute_query("SELECT id FROM Users WHERE email = ?", (data['email'],), fetchone=True)
        if existing_user:
            return jsonify({'error': 'User with this email already exists'}), 409
        
        existing_user = execute_query("SELECT id FROM Users WHERE username = ?", (data['username'],), fetchone=True)
        if existing_user:
            return jsonify({'error': 'User with this username already exists'}), 409

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
            access_token = create_access_token(identity=data['username'], fresh=True, expires_delta=False)
            refresh_token = create_refresh_token(identity=data['username'])
            return jsonify(access_token=access_token, refresh_token=refresh_token), 200

        return jsonify({'error': 'Invalid username or password'}), 401
    
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500


# TODO: Implement api endpoint to update sensitive info: email or password
# @auth_bp.route('/api/users', methods=['POST'])
# def update_sensitive_info():
#     data = request.json

#     try:
#         user = execute_query("SELECT * FROM Users WHERE username = ?", (data['username'],), fetchone=True)
#         if user and bcrypt.check_password_hash(user['password'], data['password']):
#             access_token = create_access_token(identity=data['username'], fresh=True, expires_delta=False)
#             refresh_token = create_refresh_token(identity=data['username'])
#             return jsonify(access_token=access_token, refresh_token=refresh_token), 200

#         return jsonify({'error': 'Invalid username or password'}), 401
    
#     except sqlite3.Error as e:
#         return jsonify({'error': str(e)}), 500


@auth_bp.route("/api/new_access_token", methods=["GET"])
@jwt_required(refresh=True)
def refresh_access():
    try:
        identity = get_jwt_identity()
        new_access_token = create_access_token(identity=identity)
        return jsonify(access_token=new_access_token), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/api/logout', methods=['GET'])
@jwt_required(verify_type=False)
def logout_user():
    try:
        jti = get_jwt()['jti']
        execute_query("INSERT INTO RevokedTokens (jti, revoked_at) VALUES (?, ?)", (jti, datetime.now()), commit=True)
        return jsonify({"message": "Token revoked successfully"}), 200

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route("/api/me", methods=["GET"])
@jwt_required()
def whoami():
    try:
        user_identity = get_jwt_identity()

        return jsonify({"user": user_identity})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_revoked_token(jti):

    try:
        token = execute_query("SELECT * FROM RevokedTokens WHERE jti = ?", (jti,), fetchone=True)
        return token
    
    except Exception as e:
        print(jsonify({'error': str(e)})), 500
        return None
