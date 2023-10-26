import sqlite3
from flask import Blueprint, jsonify
from database.connections import get_cursor, get_connection

user_bp = Blueprint('user', __name__)


@user_bp.route('/api/users', methods=['GET'])
def get_users():
    try:
        cursor = get_cursor()

        cursor.execute("SELECT * FROM your_table_name")
        users = [dict(row) for row in cursor.fetchall()]

        return jsonify(users)

    except Exception as e:
        return jsonify({'error': str(e)})

    finally:
        cursor.close()
        get_connection().close()


@user_bp.route('/api/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    try:
        cursor = get_cursor()

        cursor.execute("SELECT * FROM posts WHERE user_id = ?", (user_id,))
        user_posts = [dict(row) for row in cursor.fetchall()]

        return jsonify(user_posts)

    except Exception as e:
        return jsonify({'error': str(e)})

    finally:
        cursor.close()
        get_connection().close()
