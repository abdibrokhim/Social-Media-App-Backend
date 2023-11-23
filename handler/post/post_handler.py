from flask import Blueprint, jsonify, request
from database.connections import get_cursor, get_connection
import sqlite3
from datetime import datetime
from flask_jwt_extended import (
    current_user,
    jwt_required,
    get_jwt,
    get_jwt_identity
)
from handler.query_helpers import execute_query

post_bp = Blueprint('post', __name__)

@post_bp.route('/api/posts', methods=['GET'])
def get_posts():

    try:
        cursor = execute_query("SELECT * FROM Posts WHERE isDeleted = 0")
        posts = [dict(row) for row in cursor.fetchall()]
        return jsonify(posts)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@post_bp.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post_by_id(post_id):


    try:
        # Increment the activity level count
        execute_query("UPDATE Posts SET activityLevel = activityLevel + 1 WHERE id = ?", (post_id,), commit=True)

        post = execute_query("SELECT * FROM Posts WHERE id = ? AND isDeleted = 0", (post_id,), fetchone=True)
        if post:
            return jsonify(dict(post))
        return jsonify({'message': 'Post not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@post_bp.route('/api/posts', methods=['POST'])
@jwt_required()
def create_post():

    new_post = request.json
    username = get_jwt_identity()

    try:
        user_id = execute_query("SELECT id FROM Users WHERE username = ?", (username,), fetchone=True)['id']

        post_id = execute_query("""
            INSERT INTO Posts (createdAt, description, image, activityLevel, isDeleted, title, userId) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (datetime.now(), new_post['description'], new_post['image'], 1, 0, new_post['title'], user_id), commit=True).lastrowid

        # Add post categories
        for category in new_post['categories']:
            category_id = category['categoryId']
            execute_query("""
                INSERT INTO PostCategories (postId, categoryId)
                VALUES (?, ?)
            """, (post_id, category_id), commit=True)

        return jsonify({'message': 'Post created successfully'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@post_bp.route('/api/posts/<post_id>', methods=['PATCH'])
@jwt_required()
def update_post(post_id):

    updated_post = request.json
    update_fields = []
    update_values = []

    if 'description' in updated_post:
        update_fields.append("description = ?")
        update_values.append(updated_post['description'])

    if 'image' in updated_post:
        update_fields.append("image = ?")
        update_values.append(updated_post['image'])

    if 'title' in updated_post:
        update_fields.append("title = ?")
        update_values.append(updated_post['title'])

    # Always update activityLevel and updatedAt
    update_fields.append("activityLevel = activityLevel + 0.1")
    update_fields.append("updatedAt = ?")
    update_values.append(datetime.now())

    update_values.append(post_id)  # Add post_id at the end for the WHERE clause

    update_query = "UPDATE Posts SET " + ", ".join(update_fields) + " WHERE id = ?"

    try:
        execute_query(update_query, tuple(update_values), commit=True)
        return jsonify({'message': 'Post updated successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@post_bp.route('/api/posts/<int:post_id>/like', methods=['POST'])
@jwt_required()
def like_post(post_id):

    username = get_jwt_identity()

    try:
        user_id = execute_query("SELECT id FROM Users WHERE username = ?", (username,), fetchone=True)['id']

        execute_query("INSERT INTO PostLikes (postId, userId) VALUES (?, ?)", (post_id, user_id), commit=True)

        return jsonify({'message': 'Post liked successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@post_bp.route('/api/posts/<int:post_id>/unlike', methods=['POST'])
@jwt_required()
def unlike_post(post_id):
    
        username = get_jwt_identity()
    
        try:
            user_id = execute_query("SELECT id FROM Users WHERE username = ?", (username,), fetchone=True)['id']
    
            execute_query("DELETE FROM PostLikes WHERE postId = ? AND userId = ?", (post_id, user_id), commit=True)
    
            return jsonify({'message': 'Post unliked successfully'})
    
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@post_bp.route('/api/posts/<int:post_id>/likes', methods=['GET'])
def get_post_likes(post_id):
    
        try:
            cursor = execute_query("SELECT COUNT(*) AS likes FROM PostLikes WHERE postId = ?", (post_id,))
            likes = cursor.fetchone()['likes']
            return jsonify({'likes': likes})

        except Exception as e:
            return jsonify({'error': str(e)}), 500


@post_bp.route('/api/posts/<int:post_id>/liked-users', methods=['GET'])
def get_post_liked_users(post_id):
    try:
        # Query to get the list of users who liked the post along with their username and profile image
        users_cursor = execute_query("""
            SELECT u.id AS userId, u.username, u.profileImage FROM PostLikes pl
            JOIN Users u ON pl.userId = u.id
            WHERE pl.postId = ?
        """, (post_id,))
        users = [dict(row) for row in users_cursor.fetchall()]

        return jsonify({"users": users})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@post_bp.route('/api/posts/<post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):

    try:
        execute_query("UPDATE Posts SET isDeleted = 1 WHERE id = ?", (post_id,), commit=True)
        return jsonify({'message': 'Post deleted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@post_bp.route('/api/posts/deleted', methods=['GET'])
def get_deleted_posts():
    
        try:
            cursor = execute_query("SELECT * FROM Posts WHERE isDeleted = 1")
            posts = [dict(row) for row in cursor.fetchall()]
            return jsonify(posts)
    
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@post_bp.route('/api/posts/category/<int:category_id>', methods=['GET'])
def get_posts_by_category(category_id):


    try:
        # A many-to-many relationship with a junction table named PostCategories
        cursor = execute_query("""
            SELECT p.* FROM Posts p
            JOIN PostCategories pc ON p.id = pc.postId
            WHERE pc.categoryId = ? AND p.isDeleted = 0
        """, (category_id,))
        posts = [dict(row) for row in cursor.fetchall()]
        return jsonify(posts)


    except Exception as e:
        return jsonify({'error': str(e)}), 500

# TODO: refactor this endpoint. It should return a list of posts every time except that already was returned
@post_bp.route('/api/posts/made-for-you', methods=['GET'])
@jwt_required()
def get_made_for_you_posts():
    limit = request.args.get('limit', 10, type=int)
    last_post_id = request.args.get('last_post_id', type=int)

    try:
        # Fetch user
        username = get_jwt_identity()
        user_id = execute_query("SELECT id FROM Users WHERE username = ?", (username,), fetchone=True)['id']

        # Fetch user interests
        cursor = execute_query("""
            SELECT categoryId FROM UserInterests WHERE userId = ?
        """, (user_id,))
        interests = cursor.fetchall()

        # If user has no interests, return an empty list
        if not interests:
            return get_explore_posts(limit=limit)

        # Convert interests to a list of category IDs
        category_ids = [interest['categoryId'] for interest in interests]

        # Prepare the SQL query
        query = """
            SELECT p.* FROM Posts p
            JOIN PostCategories pc ON p.id = pc.postId
            JOIN Users u ON p.userId = u.id
            WHERE pc.categoryId IN ({}) AND p.activityLevel > 0 AND u.activityLevel > 0 AND p.isDeleted = 0
        """.format(','.join('?' * len(category_ids)))

        # Add condition for pagination
        if last_post_id:
            query += " AND p.id > ?"
            category_ids.append(last_post_id)

        # Add ordering and limit
        query += " ORDER BY p.activityLevel DESC, u.activityLevel DESC LIMIT ?"
        category_ids.append(limit)

        cursor = execute_query(query, category_ids)
        posts = [dict(row) for row in cursor.fetchall()]

        return jsonify(posts)

    except Exception as e:
        return jsonify({'error': str(e)}), 500




@post_bp.route('/api/posts/explore/<int:limit>', methods=['GET'])
def get_explore_posts(limit):


    try:
        # Fetch trending posts based on likes and activity level
        cursor = execute_query("""
            SELECT p.* FROM Posts p
            WHERE p.activityLevel > 0 AND p.isDeleted = 0
            ORDER BY p.likes DESC, p.activityLevel DESC
            LIMIT = ?
        """, (limit,))
        trending_posts = [dict(row) for row in cursor.fetchall()]

        # Fetch new content
        cursor = execute_query("""
            SELECT * FROM Posts
            WHERE activityLevel > 0 AND isDeleted = 0
            ORDER BY createdAt DESC
            LIMIT = ?
        """, (limit,))
        new_posts = [dict(row) for row in cursor.fetchall()]

        # Fetch posts from diverse categories
        cursor = execute_query("""
            SELECT p.*, c.name AS category_name FROM Posts p
            JOIN PostCategories pc ON p.id = pc.postId
            JOIN Categories c ON pc.categoryId = c.id
            WHERE p.activityLevel > 0 AND p.isDeleted = 0
            GROUP BY c.id
            ORDER BY RANDOM()
            LIMIT = ?
        """, (limit,))
        diverse_posts = [dict(row) for row in cursor.fetchall()]

        # Combine all posts into a single list
        explore_posts = trending_posts + new_posts + diverse_posts

        return jsonify(explore_posts)


    except Exception as e:
        return jsonify({'error': str(e)}), 500


