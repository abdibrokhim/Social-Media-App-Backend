from datetime import datetime
from handler.query_helpers import execute_query

def get_filter_posts_service(query):
    post_cursor = execute_query("""
        SELECT * FROM Posts WHERE (title LIKE ? OR description LIKE ?) AND isDeleted = 0 ORDER BY activityLevel DESC
    """, (query, query))

    return [dict(row) for row in post_cursor.fetchall()]