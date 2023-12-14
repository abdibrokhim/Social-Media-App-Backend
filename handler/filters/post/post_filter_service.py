from datetime import datetime
from handler.query_helpers import execute_query
from handler.post.post_service import fetch_post_categories


def get_filter_posts_service(query):
    post_cursor = execute_query("""
        SELECT id AS postId, image, title
        FROM Posts 
        WHERE (title LIKE ? OR description LIKE ?) AND isDeleted = 0 ORDER BY activityLevel DESC
    """, (query, query))

    posts = [dict(row) for row in post_cursor.fetchall()]

    #fetch categories
    for post in posts:
        post['categories'] = fetch_post_categories(post['postId'])

    return posts


def get_autocomplete_posts_service(query):
    post_cursor = execute_query("""
        SELECT id, title, description
        FROM Posts 
        WHERE (title LIKE ? OR description LIKE ?) AND isDeleted = 0 ORDER BY activityLevel DESC
    """, (query, query))

    posts = [dict(row) for row in post_cursor.fetchall()]

    return posts
        
