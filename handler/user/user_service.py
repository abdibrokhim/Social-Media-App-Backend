from httpx import get
from handler.post.post_service import fetch_post_categories
from handler.query_helpers import execute_query
from datetime import datetime


def get_user_by_id_service(user_id):
    # Fetch user details
    user = execute_query("""SELECT
                                id,
                                firstName,
                                lastName,
                                username,
                                profileImage,
                                email,
                                activityLevel,
                                isDeleted,
                                isEmailValidated,
                                createdAt,
                                updatedAt
                            FROM Users WHERE id = ?""", (user_id,), fetchone=True)

    if user is None:
        return None
    
    user_data = dict(user)

    # Fetch user meta info
    user_meta_info = execute_query("""
        SELECT mi.* FROM MetaInfo mi
        JOIN UserMetaInfo umi ON mi.id = umi.metaInfoId
        WHERE umi.userId = ?
    """, (user_id,), fetchone=True)
    user_data['userMetaInfo'] = dict(user_meta_info) if user_meta_info else {}

    # Fetch social media links
    cursor = execute_query("""
        SELECT sml.* FROM SocialMediaLinks sml
        JOIN UserSocialMediaLinks usml ON sml.id = usml.socialMediaLinkId
        WHERE usml.userId = ?
    """, (user_id,))
    social_media_links = [dict(link) for link in cursor.fetchall()]
    user_data['socialMediaLinks'] = social_media_links

    # Fetch posts
    cursor = execute_query("""
        SELECT p.* FROM Posts p
        JOIN UserPosts up ON p.id = up.postId
        WHERE up.userId = ? AND isDeleted = 0
    """, (user_id,))
    posts = [dict(post) for post in cursor.fetchall()]
    user_data['posts'] = posts

    # Fetch post categories
    for post in user_data['posts']:
        categories_cursor = execute_query("""
            SELECT c.* FROM PostCategories pc
            JOIN Categories c ON pc.categoryId = c.id
            WHERE pc.postId = ? AND c.isDeleted = 0
        """, (post['id'],))
        post['categories'] = [dict(row) for row in categories_cursor.fetchall()]

    # Fetch interests
    cursor = execute_query("""
        SELECT c.* FROM Categories c
        JOIN UserInterests ui ON c.id = ui.categoryId
        WHERE ui.userId = ? AND c.isDeleted = 0
    """, (user_id,))
    interests = [dict(interest) for interest in cursor.fetchall()]
    user_data['interests'] = interests

    # Increment the activity level count
    execute_query("UPDATE Users SET activityLevel = activityLevel + 1 WHERE id = ?", (user_id,), commit=True)

    return user_data


def get_user_by_id_small_service(user_id):
    # Fetch user details
    user = execute_query("""SELECT
                                id,
                                firstName,
                                lastName,
                                username,
                                profileImage,
                                email,
                                activityLevel,
                                isDeleted,
                                isEmailValidated,
                                createdAt,
                                updatedAt
                            FROM Users WHERE id = ?""", (user_id,), fetchone=True)

    if user is None:
        return None
    return dict(user)


def get_user_by_username_service(username):
    # Fetch user details
    user = execute_query("SELECT * FROM Users WHERE username = ?", (username,), fetchone=True)

    if user is None:
        return None
    
    user_id = user['id']
    user_data = dict(user)

    # Fetch user meta info
    user_meta_info = execute_query("""
        SELECT mi.* FROM MetaInfo mi
        JOIN UserMetaInfo umi ON mi.id = umi.metaInfoId
        WHERE umi.userId = ?
    """, (user_id,), fetchone=True)
    user_data['userMetaInfo'] = dict(user_meta_info) if user_meta_info else {}

    # Fetch social media links
    cursor = execute_query("""
        SELECT sml.* FROM SocialMediaLinks sml
        JOIN UserSocialMediaLinks usml ON sml.id = usml.socialMediaLinkId
        WHERE usml.userId = ?
    """, (user_id,))
    social_media_links = [dict(link) for link in cursor.fetchall()]
    user_data['socialMediaLinks'] = social_media_links

    # Fetch posts
    cursor = execute_query("""
        SELECT p.* FROM Posts p
        JOIN UserPosts up ON p.id = up.postId
        WHERE up.userId = ? AND isDeleted = 0
    """, (user_id,))
    posts = [dict(post) for post in cursor.fetchall()]
    user_data['posts'] = posts

    # Fetch interests
    cursor = execute_query("""
        SELECT c.* FROM Categories c
        JOIN UserInterests ui ON c.id = ui.categoryId
        WHERE ui.userId = ? AND c.isDeleted = 0
    """, (user_id,))
    interests = [dict(interest) for interest in cursor.fetchall()]
    user_data['interests'] = interests
    
    # Increment the activity level count
    execute_query("UPDATE Users SET activityLevel = activityLevel + 1 WHERE username = ?", (username,), commit=True)

    return user_data

# todo: return updated user
def update_user_service(user_id, updated_user):
    update_fields = []
    update_values = []

    if 'firstName' in updated_user:
        update_fields.append("firstName = ?")
        update_values.append(updated_user['firstName'])

    if 'lastName' in updated_user:
        update_fields.append("lastName = ?")
        update_values.append(updated_user['lastName'])

    if 'profileImage' in updated_user:
        update_fields.append("profileImage = ?")
        update_values.append(updated_user['profileImage'])

    # Always update activityLevel and updatedAt
    update_fields.append("activityLevel = activityLevel + 0.1")
    update_fields.append("updatedAt = ?")
    update_values.append(datetime.now())

    update_values.append(user_id)  # Add user_id at the end for the WHERE clause

    update_query = "UPDATE Users SET " + ", ".join(update_fields) + " WHERE id = ?"

    execute_query(update_query, tuple(update_values), commit=True)

    print('User updated successfully', 200)
    return get_updated_user_info(user_id)


def get_updated_user_info(user_id):
    # Fetch user firstName, lastName, profileImage, updatedAt
    user = execute_query("SELECT firstName, lastName, profileImage, updatedAt FROM Users WHERE id = ?", (user_id,), fetchone=True)

    if user is None:
        return None
    
    return dict(user)


def delete_user_service(user_id):
    cursor = execute_query("UPDATE Users SET isDeleted = 1 WHERE id = ?", (user_id,), commit=True)

    if cursor.rowcount == 0:
        return 'User not found', 404
    return 'User deleted successfully', 200


def get_all_deleted_users_service():
    cursor = execute_query("SELECT * FROM Users WHERE isDeleted = 1")
    return [dict(user) for user in cursor.fetchall()]
    

def get_all_users_service():
    cursor = execute_query("SELECT * FROM Users")
    return [dict(row) for row in cursor.fetchall()]


def get_all_alive_users_service():
    cursor = execute_query("SELECT * FROM Users WHERE isDeleted = 0")
    return [dict(row) for row in cursor.fetchall()]


def get_user_posts_service(user_id):
    cursor = execute_query("""
        SELECT p.id AS postId, p.image, p.title FROM Posts p
        JOIN UserPosts up ON p.id = up.postId
        WHERE up.userId = ? AND isDeleted = 0
    """, (user_id,))
    posts = [dict(post) for post in cursor.fetchall()]
    
    #fetch categories
    for post in posts:
        post['categories'] = fetch_post_categories(post['postId'])

    return posts


def get_user_meta_info_service(user_id):
    user_meta_info = execute_query("""
        SELECT mi.* FROM MetaInfo mi
        JOIN UserMetaInfo umi ON mi.id = umi.metaInfoId
        WHERE umi.userId = ?
    """, (user_id,), fetchone=True)
    return dict(user_meta_info) if user_meta_info else None


def get_user_social_media_links_service(user_id):
    cursor = execute_query("""
        SELECT sml.* FROM SocialMediaLinks sml
        JOIN UserSocialMediaLinks usml ON sml.id = usml.socialMediaLinkId
        WHERE usml.userId = ?
    """, (user_id,))
    return [dict(link) for link in cursor.fetchall()]


def get_user_interests_service(user_id):
    cursor = execute_query("""
        SELECT c.* FROM Categories c
        JOIN UserInterests ui ON c.id = ui.categoryId
        WHERE ui.userId = ? AND c.isDeleted = 0
    """, (user_id,))
    return [dict(interest) for interest in cursor.fetchall()]

# todo: return user social media link (updated link)
def update_specific_social_media_link_service(user_id, link_id, updated_link):
    update_fields = []
    update_values = []

    if 'icon' in updated_link:
        update_fields.append("icon = ?")
        update_values.append(updated_link['icon'])

    if 'name' in updated_link:
        update_fields.append("name = ?")
        update_values.append(updated_link['name'])

    if 'url' in updated_link:
        update_fields.append("url = ?")
        update_values.append(updated_link['url'])

    if not update_fields:
        return 'No fields provided for update', 400

    # Ensure that the link being updated belongs to the specified user
    link_exists_query = """
        SELECT 1 FROM SocialMediaLinks
        WHERE id = ? AND EXISTS (
            SELECT 1 FROM UserSocialMediaLinks
            WHERE userId = ? AND socialMediaLinkId = ?
        )
    """
    link_exists_params = (link_id, user_id, link_id)

    link_exists_cursor = execute_query(link_exists_query, link_exists_params)
    if link_exists_cursor.fetchone() is None:
        return 'Social media link not found or does not belong to the specified user', 404

    # Update the social media link
    update_query = f"UPDATE SocialMediaLinks SET {', '.join(update_fields)} WHERE id = ?"
    update_values.append(link_id)

    cursor = execute_query(update_query, tuple(update_values), commit=True)
    if cursor.rowcount == 0:
        print('No update needed', 200)
        return get_user_social_media_links_service(user_id)

    print('Social media link updated successfully', 200)
    return get_user_social_media_links_service(user_id)


# todo: return user social media links (list)
def add_social_media_link_service(user_id, socials_data):

    for social in socials_data:
        icon = social.get('icon')
        name = social.get('name')
        url = social.get('url')

        if url is None:
            return 'URL is required', 400

        link_id = execute_query("""
            INSERT INTO SocialMediaLinks (icon, name, url) 
            VALUES (?, ?, ?)
        """, (icon, name, url), commit=True).lastrowid

        # Link social media links to the user
        execute_query("""
            INSERT INTO UserSocialMediaLinks (userId, socialMediaLinkId) 
            VALUES (?, ?)
        """, (user_id, link_id), commit=True)

    print('Social media links added successfully', 201)
    return get_user_social_media_links_service(user_id)


def delete_specific_social_media_link_service(link_id, user_id):
    # Check if the social media link exists and belongs to the specified user
    link_exists_query = """
        SELECT 1 
        FROM SocialMediaLinks 
        WHERE id = ? AND EXISTS (SELECT 1 FROM UserSocialMediaLinks WHERE userId = ? AND socialMediaLinkId = ?)
    """
    link_exists_params = (link_id, user_id, link_id)

    link_exists_cursor = execute_query(link_exists_query, link_exists_params)

    if link_exists_cursor.fetchone() is None:
        return 'Social media link not found or does not belong to the specified user', 404

    # Delete the social media link
    delete_query = "DELETE FROM UserSocialMediaLinks WHERE socialMediaLinkId = ? AND userId = ?"
    delete_params = (link_id, user_id)

    cursor = execute_query(delete_query, delete_params, commit=True)

    if cursor.rowcount == 0:
        return 'Social media link not found', 404

    print('Social media link deleted successfully', 200)
    return get_user_social_media_links_service(user_id)

# todo: return user interests
def add_interest_service(user_id, interest_data):
    for interest in interest_data:
        category_id = interest.get('categoryId')
        if category_id is not None:
            execute_query("INSERT INTO UserInterests (userId, categoryId) VALUES (?, ?)", (user_id, category_id), commit=True)

    print('Interests added successfully', 201)
    return get_user_interests_service(user_id)


def delete_interest_service(user_id, category_id):
    cursor = execute_query("DELETE FROM UserInterests WHERE userId = ? AND categoryId = ?", (user_id, category_id), commit=True)

    if cursor.rowcount == 0:
        return 'Interest not found', 404

    print('Interest deleted successfully', 200)
    return get_user_interests_service(user_id)


def toggle_follow_user_service(user_id, username):
    follower_id = execute_query("SELECT id FROM Users WHERE username = ?", (username,), fetchone=True)['id']

    # Check if user is already followed
    is_followed = execute_query("SELECT * FROM UserFollowers WHERE followingId = ? AND followerId = ?", (user_id, follower_id), fetchone=True)

    if is_followed:
        # Unfollow user, here followingId is the user being followed and followerId is the user following
        execute_query("DELETE FROM UserFollowers WHERE followingId = ? AND followerId = ?", (user_id, follower_id), commit=True)

        # Decrement the follower count for the user being followed
        execute_query("UPDATE MetaInfo SET followers = followers - 1 WHERE id = (SELECT metaInfoId FROM UserMetaInfo WHERE userId = ?)", (user_id,), commit=True)

        # Decrement the following count for the follower user
        execute_query("UPDATE MetaInfo SET following = following - 1 WHERE id = (SELECT metaInfoId FROM UserMetaInfo WHERE userId = ?)", (follower_id,), commit=True)

        return 'User unfollowed successfully', 200

    # Follow user, here user_id is the user being following's id and follower_id is the follower's id
    execute_query("INSERT INTO UserFollowers (followingId, followerId) VALUES (?, ?)", (user_id, follower_id), commit=True)

    # Increment the follower count for the user being followed
    execute_query("UPDATE MetaInfo SET followers = followers + 1 WHERE id = (SELECT metaInfoId FROM UserMetaInfo WHERE userId = ?)", (user_id,), commit=True)

    # Increment the following count for the follower user
    execute_query("UPDATE MetaInfo SET following = following + 1 WHERE id = (SELECT metaInfoId FROM UserMetaInfo WHERE userId = ?)", (follower_id,), commit=True)

    return 'User followed successfully', 200


def is_following_service(user_id, username):
    follower_id = execute_query("SELECT id FROM Users WHERE username = ?", (username,), fetchone=True)['id']

    # Check if user is already followed
    is_followed = execute_query("SELECT * FROM UserFollowers WHERE followingId = ? AND followerId = ?", (user_id, follower_id), fetchone=True)

    if is_followed:
        return 1
    return 0


def follow_user_service(user_id, username):
    follower_id = execute_query("SELECT id FROM Users WHERE username = ?", (username,), fetchone=True)['id']

    # Follow user, here user_id is the user being following's id and follower_id is the follower's id
    execute_query("INSERT INTO UserFollowers (followingId, followerId) VALUES (?, ?)", (user_id, follower_id), commit=True)

    # Increment the follower count for the user being followed
    execute_query("UPDATE MetaInfo SET followers = followers + 1 WHERE id = (SELECT metaInfoId FROM UserMetaInfo WHERE userId = ?)", (user_id,), commit=True)

    # Increment the following count for the follower user
    execute_query("UPDATE MetaInfo SET following = following + 1 WHERE id = (SELECT metaInfoId FROM UserMetaInfo WHERE userId = ?)", (follower_id,), commit=True)

    return 'User followed successfully', 200


def unfollow_user_service(user_id, username):
    follower_id = execute_query("SELECT id FROM Users WHERE username = ?", (username,), fetchone=True)['id']

    # Unfollow user, here followingId is the user being followed and followerId is the user following
    execute_query("DELETE FROM UserFollowers WHERE followingId = ? AND followerId = ?", (user_id, follower_id), commit=True)

    # Decrement the follower count for the user being followed
    execute_query("UPDATE MetaInfo SET followers = followers - 1 WHERE id = (SELECT metaInfoId FROM UserMetaInfo WHERE userId = ?)", (user_id,), commit=True)

    # Decrement the following count for the follower user
    execute_query("UPDATE MetaInfo SET following = following - 1 WHERE id = (SELECT metaInfoId FROM UserMetaInfo WHERE userId = ?)", (follower_id,), commit=True)

    return 'User unfollowed successfully', 200