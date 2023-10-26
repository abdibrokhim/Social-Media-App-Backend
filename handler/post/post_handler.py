import sqlite3
from flask import Blueprint, jsonify
from database.connections import get_cursor, get_connection

post_bp = Blueprint('post', __name__)


@post_bp.route('/api/posts', methods=['GET'])
def get_posts():
    conn = get_connection()
    cursor = get_cursor()

    try:

        cursor.execute("SELECT * FROM posts")
        posts = [dict(row) for row in cursor.fetchall()]

        return jsonify(posts)

    except Exception as e:
        return jsonify({'error': str(e)})

    finally:
        cursor.close()
        conn.close()
