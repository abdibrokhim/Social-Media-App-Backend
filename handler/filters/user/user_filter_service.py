from datetime import datetime
from handler.query_helpers import execute_query

def get_filter_users_service(query):

    users_cursor = execute_query("""
        SELECT id AS userId, username, profileImage
        FROM Users
        WHERE (username LIKE ? OR firstName LIKE ? OR lastName LIKE ? OR email LIKE ?) AND isDeleted = 0 ORDER BY activityLevel DESC
    """, (query, query, query, query))

    return [dict(row) for row in users_cursor.fetchall()]