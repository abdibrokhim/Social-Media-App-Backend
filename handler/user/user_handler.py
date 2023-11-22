from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    current_user,
    get_jwt_identity,
)
from flask import Blueprint, jsonify, request
import sqlite3
from database.connections import get_cursor, get_connection
from datetime import datetime
from handler.query_helpers import execute_query

user_bp = Blueprint('user', __name__)
bcrypt = Bcrypt()

@user_bp.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):

    try:

        # Fetch user details
        user = execute_query("SELECT * FROM Users WHERE id = ? AND isDeleted = 0", (user_id,), fetchone=True)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        user_data = dict(user)

        # Fetch user meta info
        user_meta_info = execute_query("SELECT * FROM UserMetaInfo WHERE userId = ?", (user_id,), fetchone=True)
        user_data['userMetaInfo'] = dict(user_meta_info) if user_meta_info else {}

        # Fetch social media links
        cursor = execute_query("SELECT * FROM SocialMediaLinks WHERE userId = ?", (user_id,))
        social_media_links = [dict(link) for link in cursor.fetchall()]
        user_data['socialMediaLinks'] = social_media_links

        # Fetch posts
        cursor = execute_query("SELECT * FROM Posts WHERE userId = ? AND isDeleted = 0", (user_id,))
        posts = [dict(post) for post in cursor.fetchall()]
        user_data['posts'] = posts

        # Fetch interests
        cursor = execute_query("""
            SELECT c.* FROM Categories c
            JOIN UserInterests ui ON c.id = ui.categoryId
            WHERE ui.userId = ? AND c.isDeleted = 0
        """, (user_id,))
        interests = [dict(interest) for interest in cursor.fetchall()]
        user_data['interests'] = interests

        # Increment the activity level count
        execute_query("UPDATE Users SET activityLevel = activityLevel + 1 WHERE id = ?", (user_id,), commit=True)

        return jsonify(user_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/api/users/<username>', methods=['GET'])
def get_user_by_username(username):

    try:

        # Fetch user details
        user = execute_query("SELECT * FROM Users WHERE username = ? AND isDeleted = 0", (username,), fetchone=True)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        user_id = user['id']
        user_data = dict(user)

        # Fetch user meta info
        user_meta_info = execute_query("SELECT * FROM UserMetaInfo WHERE userId = ?", (user_id,), fetchone=True)
        user_data['userMetaInfo'] = dict(user_meta_info) if user_meta_info else {}

        # Fetch social media links
        cursor = execute_query("SELECT * FROM SocialMediaLinks WHERE userId = ?", (user_id,))
        social_media_links = [dict(link) for link in cursor.fetchall()]
        user_data['socialMediaLinks'] = social_media_links

        # Fetch posts
        cursor = execute_query("SELECT * FROM Posts WHERE userId = ? AND isDeleted = 0", (user_id,))
        posts = [dict(post) for post in cursor.fetchall()]
        user_data['posts'] = posts

        # Fetch interests
        cursor = execute_query("""
            SELECT c.* FROM Categories c
            JOIN UserInterests ui ON c.id = ui.categoryId
            WHERE ui.userId = ? AND c.isDeleted = 0
        """, (user_id,))
        interests = [dict(interest) for interest in cursor.fetchall()]
        user_data['interests'] = interests
        
        # Increment the activity level count
        execute_query("UPDATE Users SET activityLevel = activityLevel + 1 WHERE username = ?", (username,), commit=True)

        return jsonify(user_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# TODO: Check whether user exists before updating
@user_bp.route('/api/users/<int:user_id>', methods=['PATCH'])
@jwt_required()
def update_user(user_id):

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
        execute_query(update_query, tuple(update_values), commit=True)
        return jsonify({'message': 'User updated successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):

    try:
        cursor = execute_query("UPDATE Users SET isDeleted = 1 WHERE id = ?", (user_id,), commit=True)

        if cursor.rowcount == 0:
            return jsonify({'message': 'User not found'}), 404

        return jsonify({'message': 'User deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# TODO: Implement api endpoint to get all deleted posts

@user_bp.route('/api/users', methods=['GET'])
def get_all_users():

    try:
        cursor = execute_query("SELECT * FROM Users WHERE isDeleted = 0")
        users = [dict(row) for row in cursor.fetchall()]

        return jsonify(users)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/api/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):

    try:
        cursor = execute_query("SELECT * FROM Posts WHERE userId = ? AND isDeleted = 0", (user_id,))
        posts = [dict(row) for row in cursor.fetchall()]

        return jsonify(posts)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/api/users/<int:user_id>/user-meta-info', methods=['GET'])
def get_user_meta_info(user_id):

    try:
        user_meta_info = execute_query("SELECT * FROM UserMetaInfo WHERE userId = ?", (user_id,), fetchone=True)

        if user_meta_info:
            return jsonify(dict(user_meta_info))
        return jsonify({'message': 'UserMetaInfo not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/api/users/<int:user_id>/social-media-links', methods=['GET'])
def get_user_social_media_links(user_id):

    try:
        social_media_links = execute_query("SELECT * FROM SocialMediaLinks WHERE userId = ?", (user_id,), fetchone=True)

        if social_media_links:
            return jsonify(dict(social_media_links))
        return jsonify({'message': 'SocialMediaLinks not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/api/users/<int:user_id>/social-media-links/<int:link_id>', methods=['PATCH'])
@jwt_required()
def update_specific_social_media_link(user_id, link_id):

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
        cursor = execute_query(update_query, tuple(update_values), commit=True)

        if cursor.rowcount == 0:
            return jsonify({'message': 'Social media link not found or no update needed'}), 404

        return jsonify({'message': 'Social media link updated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/api/users/<int:user_id>/social-media-links/<int:link_id>', methods=['DELETE'])
@jwt_required()
def delete_specific_social_media_link(user_id, link_id):

    try:
        cursor = execute_query("""
            DELETE FROM SocialMediaLinks 
            WHERE id = ? AND userId = ?
        """, (link_id, user_id), commit=True)

        if cursor.rowcount == 0:
            return jsonify({'message': 'Social media link not found'}), 404

        return jsonify({'message': 'Social media link deleted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/api/users/<int:user_id>/social-media-links', methods=['POST'])
@jwt_required()
def add_social_media_link(user_id):
    socials_data = request.json  # Expecting a list of dictionaries with 'categoryId'

    try:
        # Check if user exists
        user_exists = execute_query("SELECT id FROM Users WHERE id = ? AND isDeleted = 0", (user_id,), fetchone=True)
        if user_exists is None:
            return jsonify({'error': 'User not found'}), 404

        for social in socials_data:
            icon = social.get('icon')
            name = social.get('name')
            url = social.get('url')

            if url is None:
                return jsonify({'error': 'URL is required'}), 400

            execute_query("""
                INSERT INTO SocialMediaLinks (icon, name, url, userId) 
                VALUES (?, ?, ?, ?)
            """, (icon, name, url, user_id), commit=True)

        return jsonify({'message': 'Social media link added successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/api/users/<int:user_id>/interests', methods=['POST'])
@jwt_required()
def add_interest(user_id):
    interest_data = request.json  # Expecting a list of dictionaries with 'categoryId'

    try:
        for interest in interest_data:
            category_id = interest.get('categoryId')
            if category_id is not None:
                execute_query("INSERT INTO UserInterests (userId, categoryId) VALUES (?, ?)", (user_id, category_id), commit=True)

        return jsonify({'message': 'Interests added successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/api/users/<int:user_id>/interests/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_interest(user_id, category_id):

    try:
        cursor = execute_query("DELETE FROM UserInterests WHERE userId = ? AND categoryId = ?", (user_id, category_id), commit=True)

        if cursor.rowcount == 0:
            return jsonify({'message': 'Interest not found'}), 404

        return jsonify({'message': 'Interest deleted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
