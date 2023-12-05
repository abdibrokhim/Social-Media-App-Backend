from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from flask import Blueprint, jsonify, request
from datetime import datetime
from handler.query_helpers import execute_query

user_bp = Blueprint('user', __name__)
bcrypt = Bcrypt()

@user_bp.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):

    try:

        # Fetch user details
        user = execute_query("SELECT * FROM Users WHERE id = ?", (user_id,), fetchone=True)

        if user is None:
            return jsonify({'message': 'User not found'}), 404
        
        user_data = dict(user)

        # Fetch user meta info
        user_meta_info = execute_query("""
            SELECT mi.* FROM MetaInfo mi
            JOIN UserMetaInfo umi ON mi.id = umi.metaInfoId
            WHERE umi.userId = ?
        """, (user_id,), fetchone=True)
        user_data['userMetaInfo'] = dict(user_meta_info) if user_meta_info else {}

        # Fetch social media links
        cursor = execute_query("""
            SELECT sml.* FROM SocialMediaLinks sml
            JOIN UserSocialMediaLinks usml ON sml.id = usml.socialMediaLinkId
            WHERE usml.userId = ?
        """, (user_id,))
        social_media_links = [dict(link) for link in cursor.fetchall()]
        user_data['socialMediaLinks'] = social_media_links

        # Fetch posts
        cursor = execute_query("""
            SELECT p.* FROM Posts p
            JOIN UserPosts up ON p.id = up.postId
            WHERE up.userId = ? AND isDeleted = 0
        """, (user_id,))
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
        user = execute_query("SELECT * FROM Users WHERE username = ?", (username,), fetchone=True)

        if user is None:
            return jsonify({'message': 'User not found'}), 404
        
        user_id = user['id']
        user_data = dict(user)

        # Fetch user meta info
        user_meta_info = execute_query("""
            SELECT mi.* FROM MetaInfo mi
            JOIN UserMetaInfo umi ON mi.id = umi.metaInfoId
            WHERE umi.userId = ?
        """, (user_id,), fetchone=True)
        user_data['userMetaInfo'] = dict(user_meta_info) if user_meta_info else {}

        # Fetch social media links
        cursor = execute_query("""
            SELECT sml.* FROM SocialMediaLinks sml
            JOIN UserSocialMediaLinks usml ON sml.id = usml.socialMediaLinkId
            WHERE usml.userId = ?
        """, (user_id,))
        social_media_links = [dict(link) for link in cursor.fetchall()]
        user_data['socialMediaLinks'] = social_media_links

        # Fetch posts
        cursor = execute_query("""
            SELECT p.* FROM Posts p
            JOIN UserPosts up ON p.id = up.postId
            WHERE up.userId = ? AND isDeleted = 0
        """, (user_id,))
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


# API endpoint to update a user
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


# API endpoint to delete a user
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


# API endpoint to get all deleted users
@user_bp.route('/api/users/deleted', methods=['GET'])
def get_all_deleted_users():
    
        try:
            cursor = execute_query("SELECT * FROM Users WHERE isDeleted = 1")
            users = [dict(row) for row in cursor.fetchall()]
    
            return jsonify(users)
    
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        

# API endpoint to get all users (including deleted users)
@user_bp.route('/api/users/all', methods=['GET'])
def get_all_users():

    try:
        cursor = execute_query("SELECT * FROM Users")
        users = [dict(row) for row in cursor.fetchall()]

        return jsonify(users)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API endpoint to get all alive users (isDeleted = false)
@user_bp.route('/api/users/alive', methods=['GET'])
def get_all_alive_users():

    try:
        cursor = execute_query("SELECT * FROM Users WHERE isDeleted = 0")
        users = [dict(row) for row in cursor.fetchall()]

        return jsonify(users)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API endpoint to get user's all non deleted posts
@user_bp.route('/api/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):

    try:
        # Fetch user posts
        cursor = execute_query("""
            SELECT p.* FROM Posts p
            JOIN UserPosts up ON p.id = up.postId
            WHERE up.userId = ? AND isDeleted = 0
        """, (user_id,))
        posts = [dict(post) for post in cursor.fetchall()]

        return jsonify(posts)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API endpoint to get user's meta info
@user_bp.route('/api/users/<int:user_id>/user-meta-info', methods=['GET'])
def get_user_meta_info(user_id):

    try:
        # Fetch user meta info
        user_meta_info = execute_query("""
            SELECT mi.* FROM MetaInfo mi
            JOIN UserMetaInfo umi ON mi.id = umi.metaInfoId
            WHERE umi.userId = ?
        """, (user_id,), fetchone=True)

        if user_meta_info:
            return jsonify(dict(user_meta_info))
        return jsonify({'message': 'UserMetaInfo not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API endpoint to get user's social media links
@user_bp.route('/api/users/<int:user_id>/social-media-links', methods=['GET'])
def get_user_social_media_links(user_id):

    try:
        # Fetch social media links
        cursor = execute_query("""
            SELECT sml.* FROM SocialMediaLinks sml
            JOIN UserSocialMediaLinks usml ON sml.id = usml.socialMediaLinkId
            WHERE usml.userId = ?
        """, (user_id,))
        social_media_links = [dict(link) for link in cursor.fetchall()]

        if social_media_links:
            return jsonify(dict(social_media_links))
        return jsonify({'message': 'SocialMediaLinks not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API endpoint to get user's interests
@user_bp.route('/api/users/<int:user_id>/interests', methods=['GET'])
def get_user_interests(user_id):

    try:
        # Fetch interests
        cursor = execute_query("""
            SELECT c.* FROM Categories c
            JOIN UserInterests ui ON c.id = ui.categoryId
            WHERE ui.userId = ? AND c.isDeleted = 0
        """, (user_id,))
        interests = [dict(interest) for interest in cursor.fetchall()]

        if interests:
            return jsonify(dict(interests))
        return jsonify({'message': 'Interests not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API endpoint to update user's social media links
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

    # Ensure that the link being updated belongs to the specified user
    link_exists_query = "SELECT 1 FROM SocialMediaLinks WHERE id = ? AND EXISTS (SELECT 1 FROM UserSocialMediaLinks WHERE userId = ? AND socialMediaLinkId = ?)"
    link_exists_params = (link_id, user_id, link_id)

    try:
        link_exists_cursor = execute_query(link_exists_query, link_exists_params)

        if link_exists_cursor.fetchone() is None:
            return jsonify({'message': 'Social media link not found or does not belong to the specified user'}), 404

        # Update the social media link
        update_query = f"UPDATE SocialMediaLinks SET {', '.join(update_fields)} WHERE id = ?"
        update_values.append(link_id)

        cursor = execute_query(update_query, tuple(update_values), commit=True)

        if cursor.rowcount == 0:
            return jsonify({'message': 'No update needed'}), 200

        return jsonify({'message': 'Social media link updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API endpoint to delete user's specific social media link
@user_bp.route('/api/users/<int:user_id>/social-media-links/<int:link_id>', methods=['DELETE'])
@jwt_required()
def delete_specific_social_media_link(user_id, link_id):
    try:
        # Check if the social media link exists and belongs to the specified user
        link_exists_query = """
            SELECT 1 
            FROM SocialMediaLinks 
            WHERE id = ? AND EXISTS (SELECT 1 FROM UserSocialMediaLinks WHERE userId = ? AND socialMediaLinkId = ?)
        """
        link_exists_params = (link_id, user_id, link_id)

        link_exists_cursor = execute_query(link_exists_query, link_exists_params)

        if link_exists_cursor.fetchone() is None:
            return jsonify({'message': 'Social media link not found or does not belong to the specified user'}), 404

        # Delete the social media link
        delete_query = "DELETE FROM SocialMediaLinks WHERE socialMediaLinkId = ? AND userId = ?"
        delete_params = (link_id, user_id)

        cursor = execute_query(delete_query, delete_params, commit=True)

        if cursor.rowcount == 0:
            return jsonify({'message': 'Social media link not found'}), 404

        return jsonify({'message': 'Social media link deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to add a social media link and link it to a specific user
@user_bp.route('/api/users/<int:user_id>/social-media-links', methods=['POST'])
@jwt_required()
def add_social_media_link(user_id):
    socials_data = request.json

    try:
        for social in socials_data:
            icon = social.get('icon')
            name = social.get('name')
            url = social.get('url')

            if url is None:
                return jsonify({'error': 'URL is required'}), 400

            link_id = execute_query("""
                INSERT INTO SocialMediaLinks (icon, name, url) 
                VALUES (?, ?, ?)
            """, (icon, name, url), commit=True).lastrowid

            # Link social media links to the user
            execute_query("""
                INSERT INTO UserSocialMediaLinks (userId, socialMediaLinkId) 
                VALUES (?, ?)
            """, (user_id, link_id), commit=True)

        return jsonify({'message': 'Social media links added successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API endpoint to add user's interests
@user_bp.route('/api/users/<int:user_id>/interests', methods=['POST'])
@jwt_required()
def add_interest(user_id):
    interest_data = request.json

    try:
        for interest in interest_data:
            category_id = interest.get('categoryId')
            if category_id is not None:
                execute_query("INSERT INTO UserInterests (userId, categoryId) VALUES (?, ?)", (user_id, category_id), commit=True)

        return jsonify({'message': 'Interests added successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API endpoint to delete user's specific interest
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


# API endpoint to follow a user
@user_bp.route('/api/users/<int:user_id>/follow', methods=['POST'])
@jwt_required()
def follow_user(user_id):
    # user_id => user being followed
    # follower_id => user following

    username = get_jwt_identity()

    try:
        follower_id = execute_query("SELECT id FROM Users WHERE username = ?", (username,), fetchone=True)['id']

        # Check if user is already followed
        is_followed = execute_query("SELECT * FROM UserFollowers WHERE followingId = ? AND followerId = ?", (user_id, follower_id), fetchone=True)
        if is_followed:
            return jsonify({'error': 'User is already followed'}), 400

        # Follow user, here user_id is the user being following's id and follower_id is the follower's id
        execute_query("INSERT INTO UserFollowers (followingId, followerId) VALUES (?, ?)", (user_id, follower_id), commit=True)

        # Increment the follower count for the user being followed
        execute_query("UPDATE MetaInfo SET followers = followers + 1 WHERE id = (SELECT metaInfoId FROM UserMetaInfo WHERE userId = ?)", (user_id,), commit=True)

        # Increment the following count for the follower user
        execute_query("UPDATE MetaInfo SET following = following + 1 WHERE id = (SELECT metaInfoId FROM UserMetaInfo WHERE userId = ?)", (follower_id,), commit=True)

        return jsonify({'message': 'User followed successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@user_bp.route('/api/users/<int:user_id>/unfollow', methods=['DELETE'])
@jwt_required()
def unfollow_user(user_id):
    
    username = get_jwt_identity()

    try:
        follower_id = execute_query("SELECT id FROM Users WHERE username = ?", (username,), fetchone=True)['id']
        
        # Check if user is already followed
        is_followed = execute_query("SELECT * FROM UserFollowers WHERE followingId = ? AND followerId = ?", (user_id, follower_id), fetchone=True)
        if not is_followed:
            return jsonify({'error': 'User is not followed'}), 400

        # Unfollow user, here followingId is the user being followed and followerId is the user following
        execute_query("DELETE FROM UserFollowers WHERE followingId = ? AND followerId = ?", (user_id, follower_id), commit=True)

        # Decrement the follower count for the user being followed
        execute_query("UPDATE MetaInfo SET followers = followers - 1 WHERE id = (SELECT metaInfoId FROM UserMetaInfo WHERE userId = ?)", (user_id,), commit=True)

        # Decrement the following count for the follower user
        execute_query("UPDATE MetaInfo SET following = following - 1 WHERE id = (SELECT metaInfoId FROM UserMetaInfo WHERE userId = ?)", (follower_id,), commit=True)

        return jsonify({'message': 'User unfollowed successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# API endpoint to follow or unfollow a user (toggle)
@user_bp.route('/api/users/<int:user_id>/toggle-follow', methods=['POST'])
@jwt_required()
def toggle_follow_user(user_id):
    # user_id => user being followed
    # follower_id => user following

    username = get_jwt_identity()

    try:
        follower_id = execute_query("SELECT id FROM Users WHERE username = ?", (username,), fetchone=True)['id']

        # Check if user is already followed
        is_followed = execute_query("SELECT * FROM UserFollowers WHERE followingId = ? AND followerId = ?", (user_id, follower_id), fetchone=True)

        if is_followed:
            # Unfollow user, here followingId is the user being followed and followerId is the user following
            execute_query("DELETE FROM UserFollowers WHERE followingId = ? AND followerId = ?", (user_id, follower_id), commit=True)

            # Decrement the follower count for the user being followed
            execute_query("UPDATE MetaInfo SET followers = followers - 1 WHERE id = (SELECT metaInfoId FROM UserMetaInfo WHERE userId = ?)", (user_id,), commit=True)

            # Decrement the following count for the follower user
            execute_query("UPDATE MetaInfo SET following = following - 1 WHERE id = (SELECT metaInfoId FROM UserMetaInfo WHERE userId = ?)", (follower_id,), commit=True)

            return jsonify({'message': 'User unfollowed successfully'})

        # Follow user, here user_id is the user being following's id and follower_id is the follower's id
        execute_query("INSERT INTO UserFollowers (followingId, followerId) VALUES (?, ?)", (user_id, follower_id), commit=True)

        # Increment the follower count for the user being followed
        execute_query("UPDATE MetaInfo SET followers = followers + 1 WHERE id = (SELECT metaInfoId FROM UserMetaInfo WHERE userId = ?)", (user_id,), commit=True)

        # Increment the following count for the follower user
        execute_query("UPDATE MetaInfo SET following = following + 1 WHERE id = (SELECT metaInfoId FROM UserMetaInfo WHERE userId = ?)", (follower_id,), commit=True)

        return jsonify({'message': 'User followed successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
