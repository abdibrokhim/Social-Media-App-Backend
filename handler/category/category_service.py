from handler.query_helpers import execute_query
from datetime import datetime

def get_categories_service():
    cursor = execute_query("SELECT * FROM Categories WHERE isDeleted = 0")
    return [dict(row) for row in cursor.fetchall()]

def get_category_by_id_service(category_id):
    category = execute_query("SELECT * FROM Categories WHERE id = ? AND isDeleted = 0", (category_id,), fetchone=True)
    return dict(category) if category else None

def create_category_service(new_category):
    category_exists = execute_query("SELECT id FROM Categories WHERE name = ?", (new_category['name'],), fetchone=True)
    if category_exists:
        return 'Category with this name already exists', 409

    execute_query("""
        INSERT INTO Categories (createdAt, name, isDeleted) 
        VALUES (?, ?, ?)
    """, (datetime.now(), new_category['name'], 0), commit=True)
    return 'Category created successfully', 201

def update_category_service(category_id, updated_category):
    category_exists = execute_query("SELECT id FROM Categories WHERE id = ? AND isDeleted = 0", (category_id,), fetchone=True)
    if not category_exists:
        return 'Category with this id does not exist', 404

    execute_query("""
        UPDATE Categories SET name = ? WHERE id = ?
    """, (updated_category['name'], category_id), commit=True)
    return 'Category updated successfully', 200

def delete_category_service(category_id):
    execute_query("UPDATE Categories SET isDeleted = 1 WHERE id = ?", (category_id,), commit=True)
    return 'Category deleted successfully', 200

def get_deleted_categories_service():
    cursor = execute_query("SELECT * FROM Categories WHERE isDeleted = 1")
    return [dict(row) for row in cursor.fetchall()]