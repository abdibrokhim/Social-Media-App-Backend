from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from flask import Blueprint, jsonify, request
from datetime import datetime
from handler.query_helpers import execute_query

user_filter_bp = Blueprint('user_filter', __name__)
bcrypt = Bcrypt()

@user_filter_bp.route('/api/users/filter', methods=['GET'])
@jwt_required()
def get_user_filter():
    user_r = request.json
    
    try:
        query = f"%{user_r['query']}%"

        users_cursor = execute_query("""
            SELECT id, username, profileImage 
            FROM Users
            WHERE (username LIKE ? OR firstName LIKE ? OR lastName LIKE ? OR email LIKE ?) AND isDeleted = 0 ORDER BY activityLevel DESC
        """, (query, query, query, query))

        users = [dict(row) for row in users_cursor.fetchall()]

        return jsonify({'users': users})

    except Exception as e:
        return jsonify({'error': str(e)}), 500