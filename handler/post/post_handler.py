from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from database.connections import get_cursor, get_connection
import sqlite3
from datetime import datetime

post_bp = Blueprint('post', __name__)

@post_bp.route('/api/posts', methods=['GET'])
def get_posts():
    conn = get_connection()
    cursor = get_cursor()

    try:
        cursor.execute("SELECT * FROM posts WHERE isDeleted = 0")
        posts = [dict(row) for row in cursor.fetchall()]
        return jsonify(posts)

    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@post_bp.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post_by_id(post_id):
    conn = get_connection()
    cursor = get_cursor()

    try:
        # Increment the activity level count
        cursor.execute("UPDATE Posts SET activityLevel = activityLevel + 1 WHERE id = ?", (post_id,))
        conn.commit()

        cursor.execute("SELECT * FROM Posts WHERE id = ? AND isDeleted = 0", (post_id,))
        post = cursor.fetchone()
        if post:
            return jsonify(dict(post))
        return jsonify({'message': 'Post not found'}), 404

    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@post_bp.route('/api/posts', methods=['POST'])
@jwt_required()
def create_post():
    conn = get_connection()
    cursor = get_cursor()

    new_post = request.json
    try:
        cursor.execute("""
            INSERT INTO posts (id, createdAt, description, image, activityLevel, isDeleted, title, userId) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (new_post['id'], datetime.now(), new_post['description'], new_post['image'], 1, 0, new_post['title'], new_post['userId']))
        conn.commit()
        return jsonify({'message': 'Post created successfully'}), 201
    
    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@post_bp.route('/api/posts/<post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    conn = get_connection()
    cursor = get_cursor()

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

    update_query = "UPDATE posts SET " + ", ".join(update_fields) + " WHERE id = ?"

    try:
        cursor.execute(update_query, tuple(update_values))
        conn.commit()
        return jsonify({'message': 'Post updated successfully'})
    
    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@post_bp.route('/api/posts/<post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    conn = get_connection()
    cursor = get_cursor()

    try:
        cursor.execute("UPDATE posts SET isDeleted = 1 WHERE id = ?", (post_id,))
        conn.commit()
        return jsonify({'message': 'Post deleted successfully'})

    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@post_bp.route('/api/posts/category/<category_id>', methods=['GET'])
def get_posts_by_category(category_id):
    conn = get_connection()
    cursor = get_cursor()

    try:
        # A many-to-many relationship with a junction table named PostCategories
        cursor.execute("""
            SELECT p.* FROM Posts p
            JOIN PostCategories pc ON p.id = pc.postId
            WHERE pc.categoryId = ? AND p.isDeleted = 0
        """, (category_id,))
        posts = [dict(row) for row in cursor.fetchall()]
        return jsonify(posts)

    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@post_bp.route('/api/posts/made-for-you/<int:user_id>', methods=['GET'])
def get_made_for_you_posts(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Fetch user interests
        cursor.execute("""
            SELECT categoryId FROM UserInterests WHERE userId = ?
        """, (user_id,))
        interests = cursor.fetchall()

        # If user has no interests, return an empty list
        if not interests:
            return jsonify([])

        # Convert interests to a list of category IDs
        category_ids = [interest['categoryId'] for interest in interests]

        # Fetch posts related to these interests and sort by activity level
        query = """
            SELECT p.* FROM Posts p
            JOIN PostCategories pc ON p.id = pc.postId
            JOIN Users u ON p.userId = u.id
            WHERE pc.categoryId IN ({}) AND p.activityLevel > 0 AND u.activityLevel > 0
            ORDER BY p.activityLevel DESC, u.activityLevel DESC
        """.format(','.join('?' * len(category_ids)))

        cursor.execute(query, category_ids)
        posts = [dict(row) for row in cursor.fetchall()]

        return jsonify(posts)
    
    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@post_bp.route('/api/posts/explore', methods=['GET'])
def get_explore_posts():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Fetch trending posts based on likes and activity level
        cursor.execute("""
            SELECT p.* FROM Posts p
            WHERE p.activityLevel > 0
            ORDER BY p.likes DESC, p.activityLevel DESC
            LIMIT 10
        """)
        trending_posts = [dict(row) for row in cursor.fetchall()]

        # Fetch new content
        cursor.execute("""
            SELECT * FROM Posts
            WHERE activityLevel > 0
            ORDER BY createdAt DESC
            LIMIT 10
        """)
        new_posts = [dict(row) for row in cursor.fetchall()]

        # Fetch posts from diverse categories
        cursor.execute("""
            SELECT p.*, c.name AS category_name FROM Posts p
            JOIN PostCategories pc ON p.id = pc.postId
            JOIN Categories c ON pc.categoryId = c.id
            WHERE p.activityLevel > 0
            GROUP BY c.id
            ORDER BY RANDOM()
            LIMIT 10
        """)
        diverse_posts = [dict(row) for row in cursor.fetchall()]

        # Combine all posts into a single list
        explore_posts = trending_posts + new_posts + diverse_posts

        return jsonify(explore_posts)

    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()
