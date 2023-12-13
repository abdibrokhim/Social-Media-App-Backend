from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    get_jwt_identity
)
from handler.auth.auth_service import (
    register_user_service,
    get_revoked_token_service,
    login_user_service,
    forgot_password_service,
    logout_user_service
)

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.json

    try:
        message, status = register_user_service(data['username'], data['email'], data['password'])
        return jsonify({'message': message})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route("/api/new-access-token", methods=["GET"])
@jwt_required(refresh=True)
def refresh_access():
    try:
        identity = get_jwt_identity()
        new_access_token = create_access_token(identity=identity)
        return jsonify(access_token=new_access_token), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route("/api/me", methods=["GET"])
@jwt_required()
def whoami():
    try:
        user_identity = get_jwt_identity()

        return jsonify({"username": user_identity})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def get_revoked_token(jti):

    try:
        revoked_token = get_revoked_token_service(jti=jti)
        return revoked_token
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.json

    try:
        result, status = login_user_service(data['username'], data['password'])
        return jsonify(result), status
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route("/api/forgot-password", methods=["POST"])
def forgot_password():
    data = request.json

    try:
        message, status = forgot_password_service(data['email'])
        return jsonify({'message': message}), status
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/api/logout', methods=['GET'])
@jwt_required(verify_type=False)
def logout_user():
    try:
        jti = get_jwt()['jti']
        message, status = logout_user_service(jti=jti)
        return jsonify({"message": message})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500