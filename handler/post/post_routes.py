from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from handler.post.post_service import (
    get_all_alive_posts_service,
    get_all_posts_service,
    get_post_by_id_service,
    create_post_service,
    update_post_service,
    toggle_like_post_service,
    get_post_likes_service,
    get_post_liked_users_service,
    delete_post_service,
    get_deleted_posts_service,
    get_posts_by_category_service,
    get_explore_posts_service,
    fetch_trending_posts,
    fetch_new_posts,
    fetch_diverse_posts,
    get_made_for_you_posts_service
)

post_bp = Blueprint('post', __name__)

@post_bp.route('/api/posts', methods=['GET'])
def get_all_alive_posts():
    try:
        posts = get_all_alive_posts_service()
        return jsonify(posts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@post_bp.route('/api/posts', methods=['GET'])
def get_all_posts():

    try:
        posts = get_all_posts_service()
        return jsonify(posts)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@post_bp.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post_by_id(post_id):

    try:
        post = get_post_by_id_service(post_id=post_id)
        if post:
            return jsonify(post)
        return jsonify({'message': 'Post not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@post_bp.route('/api/posts', methods=['POST'])
@jwt_required()
def create_post():
    new_post = request.json
    username = get_jwt_identity()
    print(f"LOG: user {username} is creating a post")

    try:
        message, status_code = create_post_service(new_post=new_post, username=username)
        return jsonify({'message': message}), status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to like or dislike a post (toggle)
@post_bp.route('/api/posts/<int:post_id>/toggle-like', methods=['POST'])
@jwt_required()
def toggle_like_post(post_id):
        
    username = get_jwt_identity()

    try:
        message, status_code = toggle_like_post_service(post_id=post_id, username=username)
        return jsonify({'message': message}), status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@post_bp.route('/api/posts/<post_id>', methods=['PATCH'])
@jwt_required()
def update_post(post_id):
    updated_post = request.json
    try:
        message, status_code = update_post_service(post_id=post_id, updated_post=updated_post)
        return jsonify({'message': message}), status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@post_bp.route('/api/posts/<int:post_id>/likes', methods=['GET'])
def get_post_likes(post_id):
    try:
        likes = get_post_likes_service(post_id)
        return jsonify({'likes': likes})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@post_bp.route('/api/posts/<int:post_id>/liked-users', methods=['GET'])
def get_post_liked_users(post_id):
    try:
        users = get_post_liked_users_service(post_id)
        return jsonify({"users": users})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@post_bp.route('/api/posts/<post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    try:
        message = delete_post_service(post_id)
        return jsonify({'message': message})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@post_bp.route('/api/posts/deleted', methods=['GET'])
def get_deleted_posts():
    try:
        posts = get_deleted_posts_service()
        return jsonify(posts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@post_bp.route('/api/posts/category/<int:category_id>', methods=['GET'])
def get_posts_by_category(category_id):
    try:
        posts = get_posts_by_category_service(category_id)
        return jsonify(posts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@post_bp.route('/api/posts/explore', methods=['GET'])
def get_explore_posts():
    # Accessing query parameters
    trending_posts_limit = request.args.get('trending', type=int)
    new_posts_limit = request.args.get('new', type=int)
    diverse_posts_limit = request.args.get('diverse', type=int)

    try:
        explore_posts = get_explore_posts_service(trending_posts_limit, new_posts_limit, diverse_posts_limit)
        return jsonify(explore_posts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@post_bp.route('/api/posts/explore/trending', methods=['GET'])
def get_explore_trending_posts():
    # Accessing query parameters
    limit = request.args.get('limit', type=int)
    excluded_ids = []

    try:
        explore_posts = fetch_trending_posts(limit, excluded_ids)
        return jsonify(explore_posts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@post_bp.route('/api/posts/explore/new', methods=['GET'])
def get_explore_new_posts():
    # Accessing query parameters
    limit = request.args.get('limit', type=int)
    excluded_ids = []

    try:
        explore_posts = fetch_new_posts(limit, excluded_ids)
        return jsonify(explore_posts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@post_bp.route('/api/posts/explore/diverse', methods=['GET'])
def get_explore_diverse_posts():
    # Accessing query parameters
    limit = request.args.get('limit', type=int)
    excluded_ids = []

    try:
        explore_posts = fetch_diverse_posts(limit, excluded_ids)
        return jsonify(explore_posts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@post_bp.route('/api/posts/made-for-you', methods=['GET'])
@jwt_required()
def get_made_for_you_posts():
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', type=int)  # Use offset for pagination

    try:
        username = get_jwt_identity()
        posts = get_made_for_you_posts_service(username=username, limit=limit, offset=offset)
        return jsonify(posts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
