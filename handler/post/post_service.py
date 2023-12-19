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

        post_data['categories'] = fetch_post_categories(post_id)

        return post_data
    return None


def fetch_post_categories(post_id):
    categories_cursor = execute_query("""
        SELECT c.* FROM PostCategories pc
        JOIN Categories c ON pc.categoryId = c.id
        WHERE pc.postId = ? AND c.isDeleted = 0
    """, (post_id,))
    return [dict(row) for row in categories_cursor.fetchall()]


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

        # return created post id
        return post_id
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


def like_post_service(username, post_id):
    user_id = execute_query(
        "SELECT id FROM Users WHERE username = ?", (username,), fetchone=True)['id']
    
    print('user_id: ', user_id)

    execute_query("INSERT INTO PostLikes (postId, userId) VALUES (?, ?)",
                  (post_id, user_id), commit=True)

    print('Post liked successfully', 200)
    # return likes count
    likes_count = get_post_likes_service(post_id)
    liked_users = get_post_liked_users_service(post_id)
    return {'likes': likes_count, 'likedUsers': liked_users}


def unlike_post_service(username, post_id):
    user_id = execute_query(
        "SELECT id FROM Users WHERE username = ?", (username,), fetchone=True)['id']

    execute_query("DELETE FROM PostLikes WHERE postId = ? AND userId = ?",
                  (post_id, user_id), commit=True)

    print('Post unliked successfully', 200)
    # return likes count
    likes_count = get_post_likes_service(post_id)
    liked_users = get_post_liked_users_service(post_id)
    return {'likes': likes_count, 'likedUsers': liked_users}


def is_liked_service(post_id, username):
    user_id = execute_query(
        "SELECT id FROM Users WHERE username = ?", (username,), fetchone=True)['id']

    is_liked = execute_query("SELECT * FROM PostLikes WHERE postId = ? AND userId = ?", (post_id, user_id), fetchone=True)

    if is_liked:
        return 1
    return 0


def get_post_likes_service(post_id):
    cursor = execute_query(
        "SELECT COUNT(*) AS likes FROM PostLikes WHERE postId = ?", (post_id,), fetchone=True)
    return cursor['likes']


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
    return post_id

def get_deleted_posts_service():
    cursor = execute_query("SELECT * FROM Posts WHERE isDeleted = 1")
    return [dict(row) for row in cursor.fetchall()]


def get_posts_by_category_service(category_id):
    cursor = execute_query("""
        SELECT p.id AS postId, p.title, p.image FROM Posts p
        JOIN PostCategories pc ON postId = pc.postId
        WHERE pc.categoryId = ? AND p.isDeleted = 0
    """, (category_id,))
    
    posts = [dict(row) for row in cursor.fetchall()]
    
    # Fetch post categories
    for post in posts:
        post['categories'] = fetch_post_categories(post['postId'])

    return posts


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
        SELECT p.id AS postId, p.title, p.image, COUNT(pl.userId) AS likes 
        FROM Posts p
        JOIN PostLikes pl ON p.id = pl.postId
        WHERE p.isDeleted = 0 AND p.id NOT IN ({})
        GROUP BY p.id
        ORDER BY likes DESC, p.activityLevel DESC
        LIMIT ?
    """.format(','.join('?' for _ in excluded_ids))

    cursor = execute_query(query, tuple(excluded_ids) + (limit,))
    trending_posts = [dict(row) for row in cursor.fetchall()]

    excluded_ids.update(post['postId'] for post in trending_posts)

    # Fetch post categories
    for post in trending_posts:
        post['categories'] = fetch_post_categories(post['postId'])

    return trending_posts


def fetch_new_posts(limit, excluded_ids):
    query = """
        SELECT id AS postId, title, image 
        FROM Posts
        WHERE isDeleted = 0 AND id NOT IN ({})
        ORDER BY createdAt DESC
        LIMIT ?
    """.format(','.join('?' for _ in excluded_ids))

    cursor = execute_query(query, tuple(excluded_ids) + (limit,))
    new_posts = [dict(row) for row in cursor.fetchall()]
    excluded_ids.update(post['postId'] for post in new_posts)
    
    # Fetch post categories
    for post in new_posts:
        post['categories'] = fetch_post_categories(post['postId'])
    return new_posts


def fetch_diverse_posts(limit, excluded_ids):
    query = """
        SELECT DISTINCT p.id AS postId, p.title, p.image
        FROM Posts p
        JOIN PostCategories pc ON p.id = pc.postId
        JOIN Categories c ON pc.categoryId = c.id
        WHERE p.activityLevel > 0 AND p.isDeleted = 0 AND p.id NOT IN ({})
        GROUP BY p.id
        ORDER BY RANDOM()
        LIMIT ?
    """.format(','.join('?' for _ in excluded_ids))

    cursor = execute_query(query, tuple(excluded_ids) + (limit,))
    diverse_posts = [dict(row) for row in cursor.fetchall()]
    excluded_ids.update(post['postId'] for post in diverse_posts)
    
    # Fetch post categories
    for post in diverse_posts:
        
        post['categories'] = fetch_post_categories(post['postId'])

    return diverse_posts


def get_made_for_you_posts_service(username, page_size, page_number):
    # Fetch user ID
    user_id = execute_query(
        "SELECT id FROM Users WHERE username = ?", (username,), fetchone=True
    )['id']

    # Return empty list if no such user found
    if not user_id:
        return []

    # Fetch user interests
    interests_cursor = execute_query(
        "SELECT categoryId FROM UserInterests WHERE userId = ?", (user_id,)
    )
    interests = interests_cursor.fetchall()

    # Return explore posts (or an empty list) if the user has no interests
    if not interests:
        return get_explore_posts_service(trending_limit=page_size, new_limit=page_size, diverse_limit=page_size)

    # Convert interests to a list of category IDs
    category_ids = [interest['categoryId'] for interest in interests]

    # Calculate offset based on page number
    offset = (page_number - 1) * page_size

    # Building the query for personalized posts, excluding already viewed posts
    query = """
        SELECT DISTINCT p.id AS postId, p.title, p.image 
        FROM Posts p
        JOIN PostCategories pc ON p.id = pc.postId
        LEFT JOIN UserPostViews upv ON p.id = upv.postId AND upv.userId = ?
        WHERE pc.categoryId IN ({})
        AND p.isDeleted = 0
        AND upv.id IS NULL
        ORDER BY p.activityLevel DESC
        LIMIT ? OFFSET ?
    """.format(','.join('?' * len(category_ids)))

    parameters = [user_id] + category_ids + [page_size, offset]

    # Execute the query and return the results
    posts_cursor = execute_query(query, parameters)
    posts = [dict(row) for row in posts_cursor.fetchall()]
    
    # Fetch post categories
    for post in posts:
        post['categories'] = fetch_post_categories(post['postId'])
    
    return posts


def clear_high_activity_posts_for_user_service(username, activity_level_threshold):
    # Fetch user ID
    user_id = execute_query(
        "SELECT id FROM Users WHERE username = ?", (username,), fetchone=True
    )['id']

    # Return an error message if no such user found
    if not user_id:
        return "User not found"

    # Delete entries from UserPostViews for posts with high activity level
    delete_query = """
        DELETE FROM UserPostViews
        WHERE userId = ?
        AND postId IN (
            SELECT id FROM Posts
            WHERE activityLevel > ?
            AND isDeleted = 0
        )
    """

    # Execute the delete query
    execute_query(delete_query, (user_id, activity_level_threshold))

    return "High activity posts cleared from user's view history"


def get_all_from_user_post_views_service(username):
    # Fetch user ID
    user_id = execute_query(
        "SELECT id FROM Users WHERE username = ?", (username,), fetchone=True
    )['id']

    cursor = execute_query("SELECT * FROM UserPostViews WHERE userId = ?", (user_id,))
    
    return [dict(row) for row in cursor.fetchall()]