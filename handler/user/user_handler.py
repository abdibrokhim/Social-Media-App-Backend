from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask import Blueprint, jsonify, request
import sqlite3
from database.connections import get_cursor, get_connection
from datetime import datetime

user_bp = Blueprint('user', __name__)
bcrypt = Bcrypt()

@user_bp.route('/api/register', methods=['POST'])
def register():
    conn = get_connection()
    cursor = conn.cursor()

    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        cursor.execute("""
            INSERT INTO Users (username, email, password, activityLevel, isDeleted, isEmailValidated, createdAt) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (username, email, hashed_password, 1, 0, 0, datetime.now()))
        conn.commit()
        return jsonify({'message': 'User registered successfully'}), 201

    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@user_bp.route('/api/login', methods=['POST'])
def login():
    conn = get_connection()
    cursor = conn.cursor()

    username = request.json.get('username')
    password = request.json.get('password')

    try:
        cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user and bcrypt.check_password_hash(user['password'], password):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token)

        return jsonify({'error': 'Invalid username or password'}), 401
    
    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@user_bp.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Increment the activity level count
        cursor.execute("UPDATE Users SET activityLevel = activityLevel + 1 WHERE id = ?", (user_id,))
        conn.commit()

        # Fetch user details
        cursor.execute("SELECT * FROM Users WHERE id = ? AND isDeleted = 0", (user_id,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        user_data = dict(user)

        # Fetch user meta info
        cursor.execute("SELECT * FROM UserMetaInfo WHERE userId = ?", (user_id,))
        user_meta_info = cursor.fetchone()
        user_data['userMetaInfo'] = dict(user_meta_info) if user_meta_info else {}

        # Fetch social media links
        cursor.execute("SELECT * FROM SocialMediaLinks WHERE userId = ?", (user_id,))
        social_media_links = [dict(link) for link in cursor.fetchall()]
        user_data['socialMediaLinks'] = social_media_links

        # Fetch posts
        cursor.execute("SELECT * FROM Posts WHERE userId = ? AND isDeleted = 0", (user_id,))
        posts = [dict(post) for post in cursor.fetchall()]
        user_data['posts'] = posts

        # Fetch interests
        cursor.execute("""
            SELECT c.* FROM Categories c
            JOIN UserInterests ui ON c.id = ui.categoryId
            WHERE ui.userId = ? AND c.isDeleted = 0
        """, (user_id,))
        interests = [dict(interest) for interest in cursor.fetchall()]
        user_data['interests'] = interests

        return jsonify(user_data)

    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@user_bp.route('/api/users/<username>', methods=['GET'])
def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Increment the activity level count
        cursor.execute("UPDATE Users SET activityLevel = activityLevel + 1 WHERE username = ?", (username,))
        conn.commit()

        # Fetch user details
        cursor.execute("SELECT * FROM Users WHERE username = ? AND isDeleted = 0", (username,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        user_id = user['id']
        user_data = dict(user)

        # Fetch user meta info
        cursor.execute("SELECT * FROM UserMetaInfo WHERE userId = ?", (user_id,))
        user_meta_info = cursor.fetchone()
        user_data['userMetaInfo'] = dict(user_meta_info) if user_meta_info else {}

        # Fetch social media links
        cursor.execute("SELECT * FROM SocialMediaLinks WHERE userId = ?", (user_id,))
        social_media_links = [dict(link) for link in cursor.fetchall()]
        user_data['socialMediaLinks'] = social_media_links

        # Fetch posts
        cursor.execute("SELECT * FROM Posts WHERE userId = ? AND isDeleted = 0", (user_id,))
        posts = [dict(post) for post in cursor.fetchall()]
        user_data['posts'] = posts

        # Fetch interests
        cursor.execute("""
            SELECT c.* FROM Categories c
            JOIN UserInterests ui ON c.id = ui.categoryId
            WHERE ui.userId = ? AND c.isDeleted = 0
        """, (user_id,))
        interests = [dict(interest) for interest in cursor.fetchall()]
        user_data['interests'] = interests

        return jsonify(user_data)

    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@user_bp.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    conn = get_connection()
    cursor = get_cursor()

    updated_user = request.json
    update_fields = []
    update_values = []

    if 'firstName' in updated_user:
        update_fields.append("firstName = ?")
        update_values.append(updated_user['firstName'])

    if 'lastName' in updated_user:
        update_fields.append("lastName = ?")
        update_values.append(updated_user['lastName'])

    if 'profileImage' in updated_user:
        update_fields.append("profileImage = ?")
        update_values.append(updated_user['profileImage'])

    # Always update activityLevel and updatedAt
    update_fields.append("activityLevel = activityLevel + 0.1")
    update_fields.append("updatedAt = ?")
    update_values.append(datetime.now())

    update_values.append(user_id)  # Add user_id at the end for the WHERE clause

    update_query = "UPDATE Users SET " + ", ".join(update_fields) + " WHERE id = ?"

    try:
        cursor.execute(update_query, tuple(update_values))
        conn.commit()
        return jsonify({'message': 'User updated successfully'})
    
    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@user_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()  # Assign the cursor to a variable

    try:
        cursor.execute("UPDATE Users SET isDeleted = 1 WHERE id = ?", (user_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'message': 'User not found'}), 404

        return jsonify({'message': 'User deleted successfully'}), 200

    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()


@user_bp.route('/api/users', methods=['GET'])
def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Users WHERE isDeleted = 0")
        users = [dict(row) for row in cursor.fetchall()]

        return jsonify(users)

    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@user_bp.route('/api/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Posts WHERE user_id = ? AND isDeleted = 0", (user_id,))
        posts = [dict(row) for row in cursor.fetchall()]

        return jsonify(posts)

    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@user_bp.route('/api/users/<int:user_id>/user-meta-info', methods=['GET'])
def get_user_meta_info(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM UserMetaInfo WHERE userId = ?", (user_id,))
        user_meta_info = cursor.fetchone()

        if user_meta_info:
            return jsonify(dict(user_meta_info))
        return jsonify({'message': 'UserMetaInfo not found'}), 404

    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@user_bp.route('/api/users/<int:user_id>/social-media-links', methods=['GET'])
def get_user_social_media_links(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM SocialMediaLinks WHERE userId = ?", (user_id,))
        user_meta_info = cursor.fetchone()

        if user_meta_info:
            return jsonify(dict(user_meta_info))
        return jsonify({'message': 'SocialMediaLinks not found'}), 404

    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@user_bp.route('/api/users/<int:user_id>/social-media-links/<int:link_id>', methods=['PUT'])
@jwt_required()
def update_specific_social_media_link(user_id, link_id):
    conn = get_connection()
    cursor = conn.cursor()

    updated_link = request.json
    update_fields = []
    update_values = []

    if 'icon' in updated_link:
        update_fields.append("icon = ?")
        update_values.append(updated_link['icon'])

    if 'name' in updated_link:
        update_fields.append("name = ?")
        update_values.append(updated_link['name'])

    if 'url' in updated_link:
        update_fields.append("url = ?")
        update_values.append(updated_link['url'])

    if not update_fields:
        return jsonify({'message': 'No fields provided for update'}), 400

    update_values.extend([link_id, user_id])

    update_query = "UPDATE SocialMediaLinks SET " + ", ".join(update_fields) + " WHERE id = ? AND userId = ?"

    try:
        cursor.execute(update_query, tuple(update_values))

        if cursor.rowcount == 0:
            return jsonify({'message': 'Social media link not found or no update needed'}), 404

        conn.commit()
        return jsonify({'message': 'Social media link updated successfully'})

    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()


@user_bp.route('/api/users/<int:user_id>/social-media-links/<int:link_id>', methods=['DELETE'])
@jwt_required()
def delete_specific_social_media_link(user_id, link_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM SocialMediaLinks 
            WHERE id = ? AND userId = ?
        """, (link_id, user_id))

        if cursor.rowcount == 0:
            return jsonify({'message': 'Social media link not found'}), 404

        conn.commit()
        return jsonify({'message': 'Social media link deleted successfully'})

    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@user_bp.route('/api/users/<int:user_id>/social-media-links', methods=['POST'])
@jwt_required()
def add_social_media_link(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    icon = request.json.get('icon')
    name = request.json.get('name')
    url = request.json.get('url')

    try:
        cursor.execute("""
            INSERT INTO SocialMediaLinks (icon, name, url, userId) 
            VALUES (?, ?, ?, ?)
        """, (icon, name, url, user_id))
        conn.commit()

        return jsonify({'message': 'Social media link added successfully'}), 201

    except sqlite3.IntegrityError:
        return jsonify({'error': 'This social media link already exists for the user'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@user_bp.route('/api/users/<int:user_id>/interests', methods=['POST'])
@jwt_required()
def add_interest(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    category_id = request.json.get('category_id')

    try:
        cursor.execute("INSERT INTO UserInterests (userId, categoryId) VALUES (?, ?)", (user_id, category_id))
        conn.commit()
        return jsonify({'message': 'Interest added successfully'}), 201

    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Interest already exists or invalid category'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@user_bp.route('/api/users/<int:user_id>/interests/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_interest(user_id, category_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM UserInterests WHERE userId = ? AND categoryId = ?", (user_id, category_id))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'message': 'Interest not found'}), 404

        return jsonify({'message': 'Interest deleted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()
