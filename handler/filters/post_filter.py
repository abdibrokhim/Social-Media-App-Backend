from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from flask import Blueprint, jsonify, request
from datetime import datetime
from handler.query_helpers import execute_query

post_filter_bp = Blueprint('post_filter', __name__)
bcrypt = Bcrypt()

@post_filter_bp.route('/api/posts/filter', methods=['GET'])
@jwt_required()
def get_post_filter():
    post_r = request.json
    
    try:
        query = f"%{post_r['query']}%"

        post_cursor = execute_query("""
            SELECT * FROM Posts WHERE (title LIKE ? OR description LIKE ?) AND isDeleted = 0 ORDER BY activityLevel DESC
        """, (query, query))

        posts = [dict(row) for row in post_cursor.fetchall()]

        return jsonify({'posts': posts})

    except Exception as e:
        return jsonify({'error': str(e)}), 500