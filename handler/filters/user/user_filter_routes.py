from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from flask import Blueprint, jsonify, request
from handler.filters.user.user_filter_service import (
    get_filter_users_service,
    get_autocomplete_users_service
)

filter_users_bp = Blueprint('user_filter', __name__)
bcrypt = Bcrypt()

@filter_users_bp.route('/api/filter/users', methods=['POST'])
# @jwt_required()
def get_filter_users():
    user_r = request.json
    
    try:
        query = f"%{user_r['query']}%"
        users = get_filter_users_service(query=query)

        return jsonify({'users': users})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@filter_users_bp.route('/api/autocomplete/users', methods=['POST'])
# @jwt_required()
def get_autocomplete_users():
    user_r = request.json
    
    try:
        query = f"%{user_r['query']}%"
        users = get_autocomplete_users_service(query=query)

        return jsonify({'users': users})

    except Exception as e:
        return jsonify({'error': str(e)}), 500