from flask import Blueprint, jsonify, request
from datetime import datetime
from handler.query_helpers import execute_query

from handler.category.category_service import (
    get_categories_service,
    get_category_by_id_service,
    create_category_service,
    update_category_service,
    delete_category_service,
    get_deleted_categories_service
)

category_bp = Blueprint('category', __name__)


@category_bp.route('/api/categories', methods=['GET'])
def get_categories():
    try:
        categories = get_categories_service()
        if categories:
            return jsonify(categories)
        return jsonify({'message': 'No categories found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@category_bp.route('/api/categories/<int:category_id>', methods=['GET'])
def get_category_by_id(category_id):
    try:
        category = get_category_by_id_service(category_id=category_id)
        if category:
            return jsonify(category)
        return jsonify({'message': 'Category not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@category_bp.route('/api/categories', methods=['POST'])
def create_category():
    new_category = request.json
    try:
        message, status_code = create_category_service(new_category=new_category)
        return jsonify({'message': message}), status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@category_bp.route('/api/categories/<int:category_id>', methods=['PATCH'])
def update_category(category_id):
    updated_category = request.json
    try:
        message, status_code = update_category_service(category_id=category_id, updated_category=updated_category)
        return jsonify({'message': message}), status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@category_bp.route('/api/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        message, status_code = delete_category_service(category_id=category_id)
        return jsonify({'message': message}), status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@category_bp.route('/api/categories/deleted', methods=['GET'])
def get_deleted_categories():
    try:
        categories = get_deleted_categories_service()
        return jsonify(categories)
    except Exception as e:
        return jsonify({'error': str(e)}), 500