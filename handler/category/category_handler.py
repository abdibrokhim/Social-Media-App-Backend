from flask import Blueprint, jsonify, request
from datetime import datetime
from handler.query_helpers import execute_query

category_bp = Blueprint('category', __name__)

@category_bp.route('/api/categories', methods=['GET'])
def get_categories():
    try:
        cursor = execute_query("SELECT * FROM Categories WHERE isDeleted = 0")
        categories = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        return jsonify(categories)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@category_bp.route('/api/categories/<int:category_id>', methods=['GET'])
def get_category_by_id(category_id):
    try:
        category = execute_query("SELECT * FROM Categories WHERE id = ? AND isDeleted = 0", (category_id,), fetchone=True)
        if category:
            return jsonify(dict(category))
        return jsonify({'message': 'Category not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@category_bp.route('/api/categories', methods=['POST'])
def create_category():
    new_category = request.json
    try:
        category_exists = execute_query("SELECT id FROM Categories WHERE name = ?", (new_category['name'],), fetchone=True)
        if category_exists:
            return jsonify({'error': 'Category with this name already exists'}), 409

        execute_query("""
            INSERT INTO Categories (createdAt, name, isDeleted) 
            VALUES (?, ?, ?)
        """, (datetime.now(), new_category['name'], 0), commit=True)
        return jsonify({'message': 'Category created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@category_bp.route('/api/categories/<int:category_id>', methods=['PATCH'])
def update_category(category_id):
    updated_category = request.json
    try:
        category_exists = execute_query("SELECT id FROM Categories WHERE id = ? AND isDeleted = 0", (category_id,), fetchone=True)
        if not category_exists:
            return jsonify({'error': 'Category not found'}), 404

        execute_query("""
            UPDATE Categories SET name = ? WHERE id = ?
        """, (updated_category['name'], category_id), commit=True)
        return jsonify({'message': 'Category updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@category_bp.route('/api/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        execute_query("UPDATE Categories SET isDeleted = 1 WHERE id = ?", (category_id,), commit=True)
        return jsonify({'message': 'Category deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# TODO: Implement api endpoint to get all deleted posts