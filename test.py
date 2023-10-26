from database.db import create_database
from database.connections import get_connection, get_cursor
from faker import Faker
import requests


def main():
    # if create_database():
        # print(f"Table created successfully!")

    # if insert_fake_users():
    #     print(f"Fake users inserted successfully!")
    # else:
    #     print(f"Failed to insert fake users!")

    get_users()


table_name = 'USERS'
num_fake_users = 4


def insert_fake_users():
    conn = get_connection()
    cursor = get_cursor()

    try:
        # Generate and insert fake user data
        fake = Faker()
        for _ in range(num_fake_users):
            user_data = {
                'name': fake.name(),
                'image': fake.image_url(),
                'likes': fake.random_int(min=0, max=1000),
                'posts': fake.random_int(min=0, max=100)
            }
            print('user_data: ', user_data)
            conn.execute(f'''
                INSERT INTO {table_name} (name, image, likes, posts)
                VALUES (? , ? , ? , ?);
            ''', (user_data['name'], user_data['image'], user_data['likes'], user_data['posts']))

            # Commit the changes to the database
            conn.commit()

        cursor.close()
        return True

    except Exception as e:
        print(e)
        return False


api_url = 'http://0.0.0.0:8000/api/users'

def get_users():
    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            users = response.json()
            print(f"users: \n {users}")
            print("Users:")
            for user in users:
                print(f"ID: {user['id']}, Name: {user['name']}, Image: {user['image']}, Likes: {user['likes']}, Posts: {user['posts']}")
            return True
        else:
            print(f"Failed to retrieve user data. Status code: {response.status_code}")
            print(response.text)
            return False

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()