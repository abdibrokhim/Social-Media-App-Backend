from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from flask import Blueprint, jsonify, request
from handler.filters.post.post_filter_service import (
    get_filter_posts_service,
    get_autocomplete_posts_service
)

filter_posts_bp = Blueprint('post_filter', __name__)
bcrypt = Bcrypt()

@filter_posts_bp.route('/api/filter/posts', methods=['POST'])
# @jwt_required()
def get_filter_posts():
    post_r = request.json
    
    try:
        query = f"%{post_r['query']}%"
        posts = get_filter_posts_service(query=query)

        return jsonify({'posts': posts})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@filter_posts_bp.route('/api/autocomplete/posts', methods=['POST'])
# @jwt_required()
def get_autocomplete_posts():
    post_r = request.json
    
    try:
        query = f"%{post_r['query']}%"
        posts = get_autocomplete_posts_service(query=query)

        return jsonify({'posts': posts})

    except Exception as e:
        return jsonify({'error': str(e)}), 500