from database.connections import get_connection, get_cursor
from faker import Faker
import requests
from database.table.user import *
from database.table.posts import *
from database.table.categories import *

import requests
import json


def create_tables():
    # if create_user_table():
    #     print("User table created successfully")
    # if create_user_meta_info_table():
    #     print("User meta info table created successfully")
    # if create_meta_info_table():
    #     print("Meta info table created successfully")
    # if create_user_interests_table():
    #     print("User interests table created successfully")
    # if create_social_media_links_table():
    #     print("Social media links table created successfully")
    # if create_user_social_media_links_table():
    #     print("User social media links table created successfully")
    # if create_revoked_tokens_table():
    #     print("Revoked tokens table created successfully")
    # if create_categories_table():
    #     print("Categories table created successfully")
    # if create_posts_table():
    #     print("Posts table created successfully")
    # if create_post_likes_table():
    #     print("Post likes table created successfully")
    # if create_post_categories_table():
    #     print("Post categories table created successfully")
    # if create_user_follow_table():
    #     print("User follow table created successfully")
    # if create_user_posts_table():
    #     print("User posts table created successfully")
    if create_user_post_views_table():
        print("User post views table created successfully")
    
    pass




def create_user():
    url = "http://0.0.0.0:8000/api/register"

    limit = 10

    for _ in range(limit):
        fake = Faker()
        payload = json.dumps({
            "username": fake.user_name(),
            "email": fake.email(),
            "password": "yourpassword"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)


def login():
    url = "http://0.0.0.0:8000/api/login"

    payload = json.dumps({
        "username": "ibrohim",
        "password": "ibrohim"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def update_user_info():
    limit = 10

    for i in range(limit):
        url = f"http://0.0.0.0:8000/api/users/{i + 1}"

        fake = Faker()
        payload = json.dumps({
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "profileImage": fake.image_url()
        })

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNzAxODA1MTE4LCJqdGkiOiJjZDliNDBiOS02NjdiLTRhMzMtYmMyYS0wODY4OTM3NDMwNjQiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiaWJyb2hpbSIsIm5iZiI6MTcwMTgwNTExOH0.RChfUdxHicidiaIEyPcNfaepXI3_rnRIAeooeO4i-BI'
        }

        response = requests.request("PATCH", url, headers=headers, data=payload)

        print(response.text)


def user_filter():
    url = "http://0.0.0.0:8000/api/users/autocomplete"

    payload = json.dumps({
        "query": "test"
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNzAxODA1MTE4LCJqdGkiOiJjZDliNDBiOS02NjdiLTRhMzMtYmMyYS0wODY4OTM3NDMwNjQiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiaWJyb2hpbSIsIm5iZiI6MTcwMTgwNTExOH0.RChfUdxHicidiaIEyPcNfaepXI3_rnRIAeooeO4i-BI'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


def create_categories():
    url = "http://0.0.0.0:8000/api/categories"

    limit = 10

    for _ in range(limit):
        fake = Faker()
        payload = json.dumps({
            "name": fake.word()
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)


def create_post():
    url = "http://0.0.0.0:8000/api/posts"
    limit = 10

    for _ in range(limit):
        fake = Faker()
        category_ids = set()
        while len(category_ids) < 5:
            category_ids.add(fake.random_int(min=1, max=10))

        categories = [{"categoryId": id} for id in category_ids]

        payload = json.dumps({
            "title": fake.sentence(),
            "description": fake.text(),
            "image": "https://picsum.photos/1016/759",
            "categories": categories
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNzAxOTY5MDQ4LCJqdGkiOiJjNzU4MzQ3Ni04OTg5LTRjNjctYjRjMi00Njk3YTA5NzcwNjMiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiaWJyb2hpbSIsIm5iZiI6MTcwMTk2OTA0OH0.x583dCYfJ-8YZpIBVww_TKXr-tIyWFw2JmmYHbETaFE' # TEST token
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)




def follow_user():

    limit = 10

    for i in range(limit):

        url = f"http://0.0.0.0:8000/api/users/{i+1}/follow"

        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNzAxODA1MTE4LCJqdGkiOiJjZDliNDBiOS02NjdiLTRhMzMtYmMyYS0wODY4OTM3NDMwNjQiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiaWJyb2hpbSIsIm5iZiI6MTcwMTgwNTExOH0.RChfUdxHicidiaIEyPcNfaepXI3_rnRIAeooeO4i-BI'  # TEST token
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)


def unfollow_user():

    url = "http://0.0.0.0:8000/api/users/4/unfollow"

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNzAxODA1MTE4LCJqdGkiOiJjZDliNDBiOS02NjdiLTRhMzMtYmMyYS0wODY4OTM3NDMwNjQiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiaWJyb2hpbSIsIm5iZiI6MTcwMTgwNTExOH0.RChfUdxHicidiaIEyPcNfaepXI3_rnRIAeooeO4i-BI'  # TEST token
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)

    print(response.text)


def like_post():
    pass


def get_all_users():
    url = "http://0.0.0.0:8000/api/users/all"

    payload = {}

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNzAxOTY5MDQ4LCJqdGkiOiJjNzU4MzQ3Ni04OTg5LTRjNjctYjRjMi00Njk3YTA5NzcwNjMiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiaWJyb2hpbSIsIm5iZiI6MTcwMTk2OTA0OH0.x583dCYfJ-8YZpIBVww_TKXr-tIyWFw2JmmYHbETaFE' # TEST token
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


def get_all_posts():

    url = "http://0.0.0.0:8000/api/posts/all"

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNzAxOTY5MDQ4LCJqdGkiOiJjNzU4MzQ3Ni04OTg5LTRjNjctYjRjMi00Njk3YTA5NzcwNjMiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiaWJyb2hpbSIsIm5iZiI6MTcwMTk2OTA0OH0.x583dCYfJ-8YZpIBVww_TKXr-tIyWFw2JmmYHbETaFE'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)



def main():
    # create_tables()
    # create_user()
    # update_user_info()
    # user_filter()
    # create_categories()
    create_post()
    # follow_user()
    # unfollow_user()
    # like_post()
    # get_all_users()
    # get_all_posts()

    pass


if __name__ == "__main__":
    main()
