from flask import Blueprint, jsonify, request
from database.connections import get_cursor, get_connection
from datetime import datetime
import sqlite3

category_bp = Blueprint('category', __name__)

@category_bp.route('/api/categories', methods=['GET'])
def get_categories():
    conn = get_connection()
    cursor = get_cursor()

    try:
        cursor.execute("SELECT * FROM Category WHERE isDeleted = 0")
        categories = [dict(row) for row in cursor.fetchall()]
        return jsonify(categories)

    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@category_bp.route('/api/categories/<int:category_id>', methods=['GET'])
def get_category_by_id(category_id):
    conn = get_connection()
    cursor = get_cursor()

    try:
        cursor.execute("SELECT * FROM Category WHERE id = ? AND isDeleted = 0", (category_id,))
        category = cursor.fetchone()
        if category:
            return jsonify(dict(category))
        return jsonify({'message': 'Category not found'}), 404

    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@category_bp.route('/api/categories', methods=['POST'])
def create_category():
    conn = get_connection()
    cursor = get_cursor()

    new_category = request.json
    try:
        cursor.execute("""
            INSERT INTO Category (id, createdAt, name, isDeleted) 
            VALUES (?, ?, ?, ?)
        """, (new_category['id'], datetime.now(), new_category['name'], 0))
        conn.commit()
        return jsonify({'message': 'Category created successfully'}), 201

    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@category_bp.route('/api/categories/<category_id>', methods=['PUT'])
def update_category(category_id):
    conn = get_connection()
    cursor = get_cursor()

    updated_category = request.json
    try:
        cursor.execute("""
            UPDATE Category SET name = ? WHERE id = ?
        """, (updated_category['name'], category_id))
        conn.commit()
        return jsonify({'message': 'Category updated successfully'})

    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@category_bp.route('/api/categories/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    conn = get_connection()
    cursor = get_cursor()

    try:
        cursor.execute("UPDATE Category SET isDeleted = 1 WHERE id = ?", (category_id,))
        conn.commit()
        return jsonify({'message': 'Category deleted successfully'})

    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()
