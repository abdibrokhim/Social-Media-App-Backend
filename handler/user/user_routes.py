from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from flask import Blueprint, jsonify, request
from handler.user.user_service import (
    get_user_by_id_service,
    get_user_by_id_small_service,
    get_user_by_username_service,
    update_user_service,
    delete_user_service,
    get_all_deleted_users_service,
    get_all_users_service,
    get_all_alive_users_service,
    get_user_posts_service,
    get_user_meta_info_service,
    get_user_social_media_links_service,
    get_user_interests_service,
    update_specific_social_media_link_service,
    add_social_media_link_service,
    delete_specific_social_media_link_service,
    add_interest_service,
    delete_interest_service,
    toggle_follow_user_service,
    follow_user_service,
    unfollow_user_service,
    is_following_service,
    get_updated_user_service
)

user_bp = Blueprint('user', __name__)
bcrypt = Bcrypt()


@user_bp.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_by_id(user_id):
    try:
        user_data = get_user_by_id_service(user_id=user_id)
        if user_data:
            return jsonify(user_data)
        return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/api/users/<int:user_id>/small', methods=['GET'])
@jwt_required()
def get_user_by_id_small(user_id):
    try:
        user_data = get_user_by_id_small_service(user_id=user_id)
        if user_data:
            return jsonify(user_data)
        return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/api/users/<username>', methods=['GET'])
@jwt_required()
def get_user_by_username(username):
    try:
        user_data = get_user_by_username_service(username=username)
        if user_data:
            return jsonify(user_data)
        return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/api/users/<int:user_id>', methods=['PATCH'])
@jwt_required()
def update_user(user_id):
    try:
        updated_user = request.json
        user = update_user_service(user_id=user_id, updated_user=updated_user)
        return jsonify(user)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@user_bp.route('/api/users/<int:user_id>/updated', methods=['GET'])
@jwt_required()
def get_updated_user(user_id):
    try:
        user = get_updated_user_service(user_id=user_id)
        return jsonify(user)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        message, status_code = delete_user_service(user_id=user_id)
        return jsonify({'message': message}), status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to get all deleted users
@user_bp.route('/api/users/deleted', methods=['GET'])
@jwt_required()
def get_all_deleted_users():
    try:
        users = get_all_deleted_users_service()
        return jsonify({'users': users})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to get all users (including deleted users)
@user_bp.route('/api/users/all', methods=['GET'])
@jwt_required()
def get_all_users():

    try:
        users = get_all_users_service()
        return jsonify(users)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to get all alive users (isDeleted = false)
@user_bp.route('/api/users/live', methods=['GET'])
@jwt_required()
def get_all_alive_users():

    try:
        users = get_all_alive_users_service()

        return jsonify(users)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to get user's all non deleted posts
@user_bp.route('/api/users/<int:user_id>/posts', methods=['GET'])
@jwt_required()
def get_user_posts(user_id):

    try:
        posts = get_user_posts_service(user_id=user_id)

        return jsonify(posts)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to get user's meta info
@user_bp.route('/api/users/<int:user_id>/user-meta-info', methods=['GET'])
@jwt_required()
def get_user_meta_info(user_id):

    try:
        user_meta_info = get_user_meta_info_service(user_id=user_id)

        if user_meta_info:
            return jsonify(user_meta_info)
        return jsonify({'message': 'UserMetaInfo not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to get user's social media links
@user_bp.route('/api/users/<int:user_id>/social-media-links', methods=['GET'])
@jwt_required()
def get_user_social_media_links(user_id):

    try:
        social_media_links = get_user_social_media_links_service(user_id=user_id)

        if social_media_links:
            return jsonify(social_media_links)
        return jsonify({'message': 'SocialMediaLinks not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to get user's interests
@user_bp.route('/api/users/<int:user_id>/interests', methods=['GET'])
@jwt_required()
def get_user_interests(user_id):

    try:
        interests = get_user_interests_service(user_id=user_id)

        if interests:
            return jsonify(interests)
        return jsonify({'message': 'Interests not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/api/users/<int:user_id>/social-media-links/<int:link_id>', methods=['PATCH'])
@jwt_required()
def update_specific_social_media_link(user_id, link_id):
    try:
        updated_link = request.json
        sml = update_specific_social_media_link_service(user_id=user_id, link_id=link_id, updated_link=updated_link)
        return jsonify({'social_media_links': sml})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to add a social media link and link it to a specific user
@user_bp.route('/api/users/<int:user_id>/social-media-links', methods=['POST'])
@jwt_required()
def add_social_media_link(user_id):
    try:
        socials_data = request.json
        sml = add_social_media_link_service(user_id=user_id, socials_data=socials_data)
        return jsonify({'social_media_links': sml})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to delete user's specific social media link
@user_bp.route('/api/users/<int:user_id>/social-media-links/<int:link_id>', methods=['DELETE'])
@jwt_required()
def delete_specific_social_media_link(user_id, link_id):
    try:
        sml = delete_specific_social_media_link_service(user_id=user_id, link_id=link_id)
        return jsonify({'social_media_links': sml})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to add user's interests
@user_bp.route('/api/users/<int:user_id>/interests', methods=['POST'])
@jwt_required()
def add_interest(user_id):
    interest_data = request.json

    try:
        interests = add_interest_service(user_id=user_id, interest_data=interest_data)
        return jsonify({'interests': interests})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to delete user's specific interest
@user_bp.route('/api/users/<int:user_id>/interests/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_interest(user_id, category_id):

    try:
        interests = delete_interest_service(user_id=user_id, category_id=category_id)
        return jsonify({'interests': interests})

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
        message, status_code = toggle_follow_user_service(user_id=user_id, username=username)
        return jsonify({'message': message}), status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/api/users/<int:user_id>/follow', methods=['POST'])
@jwt_required()
def follow_user(user_id):
    # user_id => user being followed
    # follower_id => user following

    username = get_jwt_identity()

    try:
        message, status_code = follow_user_service(user_id=user_id, username=username)
        return jsonify({'message': message}), status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/api/users/<int:user_id>/unfollow', methods=['POST'])
@jwt_required()
def unfollow_user(user_id):
    # user_id => user being followed
    # follower_id => user following

    username = get_jwt_identity()

    try:
        message, status_code = unfollow_user_service(user_id=user_id, username=username)
        return jsonify({'message': message}), status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/api/users/<int:user_id>/is-following', methods=['GET'])
@jwt_required()
def is_following(user_id):
    # user_id => user being followed
    # follower_id => user following

    username = get_jwt_identity()

    try:
        is_following = is_following_service(user_id=user_id, username=username)
        return jsonify({'is_following': is_following})

    except Exception as e:
        return jsonify({'error': str(e)}), 500