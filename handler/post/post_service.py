from datetime import datetime
from handler.query_helpers import execute_query


def get_all_alive_posts_service():
    cursor = execute_query("SELECT * FROM Posts WHERE isDeleted = 0")
    return [dict(row) for row in cursor.fetchall()]


def get_all_posts_service():
    cursor = execute_query("SELECT * FROM Posts")
    return [dict(row) for row in cursor.fetchall()]


def get_post_by_id_service(post_id):

    post = execute_query(
        "SELECT * FROM Posts WHERE id = ? AND isDeleted = 0", (post_id,), fetchone=True)

    if post:
        post_data = dict(post)
        # Increment the activity level count
        execute_query(
            "UPDATE Posts SET activityLevel = activityLevel + 1 WHERE id = ?", (post_id,), commit=True)
        # Fetch post categories
        categories_cursor = execute_query("""
            SELECT c.* FROM PostCategories pc
            JOIN Categories c ON pc.categoryId = c.id
            WHERE pc.postId = ? AND c.isDeleted = 0
        """, (post_id,))
        post_data['categories'] = [dict(row)
                                   for row in categories_cursor.fetchall()]

        return post_data
    return None


def create_post_service(new_post, username):
    user_id = execute_query(
        "SELECT id FROM Users WHERE username = ?", (username,), fetchone=True)['id']

    result = execute_query("""
        INSERT INTO Posts (createdAt, description, image, activityLevel, isDeleted, title) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (datetime.now(), new_post['description'], new_post['image'], 1, 0, new_post['title']), commit=True)

    if result is not None:
        post_id = result.lastrowid

        # Add post categories
        for category in new_post['categories']:
            category_id = category['categoryId']
            execute_query("""
                INSERT INTO PostCategories (postId, categoryId)
                VALUES (?, ?)
            """, (post_id, category_id), commit=True)

        # Link post to user
        execute_query("""
            INSERT INTO UserPosts (postId, userId)
            VALUES (?, ?)
        """, (post_id, user_id), commit=True)

        print('Post created successfully', 201)

        # return created post
        return get_post_by_id_service(post_id)
    print('Failed to insert post', 500)
    return None


def update_post_service(post_id, updated_post):
    update_fields = []
    update_values = []

    if 'description' in updated_post:
        update_fields.append("description = ?")
        update_values.append(updated_post['description'])

    if 'image' in updated_post:
        update_fields.append("image = ?")
        update_values.append(updated_post['image'])

    if 'title' in updated_post:
        update_fields.append("title = ?")
        update_values.append(updated_post['title'])

    # Always update activityLevel and updatedAt
    update_fields.append("activityLevel = activityLevel + 0.1")
    update_fields.append("updatedAt = ?")
    update_values.append(datetime.now())

    # Add post_id at the end for the WHERE clause
    update_values.append(post_id)

    update_query = "UPDATE Posts SET " + \
        ", ".join(update_fields) + " WHERE id = ?"

    execute_query(update_query, tuple(update_values), commit=True)

    print('Post updated successfully', 200)
    return get_post_by_id_service(post_id)


def toggle_like_post_service(username, post_id):

    user_id = execute_query(
        "SELECT id FROM Users WHERE username = ?", (username,), fetchone=True)['id']

    # Check if user is already liked the post
    if execute_query("SELECT * FROM PostLikes WHERE postId = ? AND userId = ?", (post_id, user_id), fetchone=True):
        execute_query("DELETE FROM PostLikes WHERE postId = ? AND userId = ?",
                      (post_id, user_id), commit=True)
        return 'Post unliked successfully', 200

    execute_query("INSERT INTO PostLikes (postId, userId) VALUES (?, ?)",
                  (post_id, user_id), commit=True)

    return 'Post liked successfully', 200


def get_post_likes_service(post_id):
    cursor = execute_query(
        "SELECT COUNT(*) AS likes FROM PostLikes WHERE postId = ?", (post_id,))
    return cursor.fetchone()['likes']


def get_post_liked_users_service(post_id):
    users_cursor = execute_query("""
        SELECT u.id AS userId, u.username, u.profileImage FROM PostLikes pl
        JOIN Users u ON pl.userId = u.id
        WHERE pl.postId = ?
    """, (post_id,))
    return [dict(row) for row in users_cursor.fetchall()]


def get_post_owner_service(post_id):

    owner_cursor = execute_query("""
        SELECT u.id AS userId, u.username, u.profileImage FROM UserPosts up
        JOIN Users u ON up.userId = u.id
        WHERE up.postId = ?
    """, (post_id,), fetchone=True)

    if owner_cursor:
        return dict(owner_cursor)
    return None


def delete_post_service(post_id):
    execute_query("UPDATE Posts SET isDeleted = 1 WHERE id = ?",
                  (post_id,), commit=True)
    print('Post deleted successfully', 200)
    # return post_id
    return post_id, 200

def get_deleted_posts_service():
    cursor = execute_query("SELECT * FROM Posts WHERE isDeleted = 1")
    return [dict(row) for row in cursor.fetchall()]


def get_posts_by_category_service(category_id):
    cursor = execute_query("""
        SELECT p.* FROM Posts p
        JOIN PostCategories pc ON p.id = pc.postId
        WHERE pc.categoryId = ? AND p.isDeleted = 0
    """, (category_id,))
    return [dict(row) for row in cursor.fetchall()]


def get_explore_posts_service(trending_limit, new_limit, diverse_limit):
    included_post_ids = set()

    # Fetch trending posts
    trending_posts = fetch_trending_posts(trending_limit, included_post_ids)

    # Fetch new posts, excluding already included posts
    new_posts = fetch_new_posts(new_limit, included_post_ids)

    # Fetch diverse posts, excluding already included posts
    diverse_posts = fetch_diverse_posts(diverse_limit, included_post_ids)

    # Combine all posts into a single list
    return trending_posts + new_posts + diverse_posts


def fetch_trending_posts(limit, excluded_ids):
    query = """
        SELECT p.*, COUNT(pl.userId) AS likes FROM Posts p
        JOIN PostLikes pl ON p.id = pl.postId
        WHERE p.isDeleted = 0 AND p.id NOT IN ({})
        GROUP BY p.id
        ORDER BY likes DESC, p.activityLevel DESC
        LIMIT ?
    """.format(','.join('?' for _ in excluded_ids))

    cursor = execute_query(query, tuple(excluded_ids) + (limit,))
    trending_posts = [dict(row) for row in cursor.fetchall()]

    excluded_ids.update(post['id'] for post in trending_posts)

    # Fetch post categories
    for post in trending_posts:
        categories_cursor = execute_query("""
            SELECT c.* FROM PostCategories pc
            JOIN Categories c ON pc.categoryId = c.id
            WHERE pc.postId = ? AND c.isDeleted = 0
        """, (post['id'],))
        post['categories'] = [dict(row) for row in categories_cursor.fetchall()]

    return trending_posts


def fetch_new_posts(limit, excluded_ids):
    query = """
        SELECT * FROM Posts
        WHERE isDeleted = 0 AND id NOT IN ({})
        ORDER BY createdAt DESC
        LIMIT ?
    """.format(','.join('?' for _ in excluded_ids))

    cursor = execute_query(query, tuple(excluded_ids) + (limit,))
    new_posts = [dict(row) for row in cursor.fetchall()]
    excluded_ids.update(post['id'] for post in new_posts)
    
    # Fetch post categories
    for post in new_posts:
        categories_cursor = execute_query("""
            SELECT c.* FROM PostCategories pc
            JOIN Categories c ON pc.categoryId = c.id
            WHERE pc.postId = ? AND c.isDeleted = 0
        """, (post['id'],))
        post['categories'] = [dict(row) for row in categories_cursor.fetchall()]
    return new_posts


def fetch_diverse_posts(limit, excluded_ids):
    query = """
        SELECT DISTINCT p.*, c.name AS category_name FROM Posts p
        JOIN PostCategories pc ON p.id = pc.postId
        JOIN Categories c ON pc.categoryId = c.id
        WHERE p.activityLevel > 0 AND p.isDeleted = 0 AND p.id NOT IN ({})
        GROUP BY p.id
        ORDER BY RANDOM()
        LIMIT ?
    """.format(','.join('?' for _ in excluded_ids))

    cursor = execute_query(query, tuple(excluded_ids) + (limit,))
    diverse_posts = [dict(row) for row in cursor.fetchall()]
    excluded_ids.update(post['id'] for post in diverse_posts)
    
    # Fetch post categories
    for post in diverse_posts:
        categories_cursor = execute_query("""
            SELECT c.* FROM PostCategories pc
            JOIN Categories c ON pc.categoryId = c.id
            WHERE pc.postId = ? AND c.isDeleted = 0
        """, (post['id'],))
        post['categories'] = [dict(row) for row in categories_cursor.fetchall()]

    return diverse_posts


def get_made_for_you_posts_service(username, limit, offset):
    # Fetch user ID
    user_id = execute_query(
        "SELECT id FROM Users WHERE username = ?", (username,), fetchone=True)['id']

    # Fetch user interests
    interests_cursor = execute_query(
        "SELECT categoryId FROM UserInterests WHERE userId = ?", (user_id,))
    interests = interests_cursor.fetchall()

    # If user has no interests, return explore posts (or an empty list)
    if not interests:
        return []  # Or call a function to return explore posts

    # Convert interests to a list of category IDs
    category_ids = [interest['categoryId'] for interest in interests]

    # Building the query for personalized posts
    query = """
        SELECT p.* FROM Posts p
        JOIN PostCategories pc ON p.id = pc.postId
        WHERE pc.categoryId IN ({})
        AND p.isDeleted = 0
        ORDER BY p.activityLevel DESC
        LIMIT ? OFFSET ?
    """.format(','.join('?' * len(category_ids)))

    parameters = category_ids + [limit, offset]

    posts_cursor = execute_query(query, parameters)
    return [dict(row) for row in posts_cursor.fetchall()]
