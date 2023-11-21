from database.connections import get_connection, get_cursor
from faker import Faker
import requests
from database.table.user import *
from database.table.posts import *
from database.table.categories import *

import requests
import json


def create_tables():
    if create_user_table():
        print("User table created successfully")
    if create_user_meta_info_table():
        print("User meta info table created successfully")
    if create_user_interests_table():
        print("User interests table created successfully")
    if create_social_media_links_table():
        print("Social media links table created successfully")
    if create_revoked_tokens_table():
        print("Revoked tokens table created successfully")
    if create_categories_table():
        print("Categories table created successfully")
    if create_posts_table():
        print("Posts table created successfully")
    if create_post_likes_table():
        print("Post likes table created successfully")
    if create_post_categories_table():
        print("Post categories table created successfully")
    pass



def create_user():
    url = "http://0.0.0.0:8000/api/register"

    payload = json.dumps({
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "yourpassword"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def main():
    create_tables()
    # create_user()
    pass


if __name__ == "__main__":
    main()
