from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from flask import Blueprint, jsonify, request
from handler.subscription.subscription_service import (
    get_user_subscription_service,
    subscribe_service,
    udpdate_user_subscription,
    unsubscribe_service,

)

subscription_bp = Blueprint('subscription', __name__)
bcrypt = Bcrypt()


@subscription_bp.route('/api/subscription', methods=['GET'])
@jwt_required()
def get_subscription():
    try:
        username = get_jwt_identity()
        subscription = get_user_subscription_service(username=username)
        return jsonify(subscription)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@subscription_bp.route('/api/subscription', methods=['POST'])
@jwt_required()
def subscribe():
    try:
        username = get_jwt_identity()
        subscription = subscribe_service(username=username)
        return jsonify(subscription)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@subscription_bp.route('/api/subscription', methods=['PATCH'])
@jwt_required()
def update_subscription():
    try:
        username = get_jwt_identity()
        subscription = udpdate_user_subscription(username=username)
        return jsonify(subscription)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@subscription_bp.route('/api/subscription', methods=['DELETE'])
@jwt_required()
def unsubscribe():
    try:
        username = get_jwt_identity()
        subscription = unsubscribe_service(username=username)
        return jsonify(subscription)
    except Exception as e:
        return jsonify({'error': str(e)}), 500