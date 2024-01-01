
from handler.query_helpers import execute_query
from datetime import datetime, timedelta

def get_user_subscription_service(username):
    user_id = execute_query("SELECT id FROM Users WHERE username = ?", (username,), fetchone=True)['id']

    if user_id is None:
        return {"message": "User not found", "statusCode": 404}

    subscription = execute_query("SELECT * FROM UserSubscriptions WHERE userId = ? AND expired = 0", (user_id,), fetchone=True)
    return {"statusCode": 200, "subscription": [dict(subscription)]} if subscription else {"subscription": [], "statusCode": 404}

def get_user_subscription_by_id_service(user_id):
    subscription = execute_query("SELECT * FROM UserSubscriptions WHERE userId = ? AND expired = 0", (user_id,), fetchone=True)
    return {"statusCode": 200, "subscription": [dict(subscription)]} if subscription else {"message": "User is not subscribed", "statusCode": 404}


def subscribe_service(username):
    user_id = execute_query("SELECT id FROM Users WHERE username = ?", (username,), fetchone=True)['id']

    if user_id is None:
        return {"message": "User not found", "statusCode": 404}
    
    subscribed_date = datetime.now()
    expiration_date = subscribed_date + timedelta(days=30)
    execute_query("INSERT INTO UserSubscriptions (userId, subscribedDate, expirationDate, expired) VALUES (?, ?, ?, 0)", (user_id, subscribed_date, expiration_date), commit=True)
    return get_user_subscription_by_id_service(user_id)


def udpdate_user_subscription(username):
    user_id = execute_query("SELECT id FROM Users WHERE username = ?", (username,), fetchone=True)['id']

    if user_id is None:
        return {"message": "User not found", "statusCode": 404}
    
    subscribedDate = datetime.now()
    expirationDate = subscribedDate + timedelta(days=30)
    execute_query("UPDATE UserSubscriptions SET subscribedDate = ?, expirationDate = ?, expired = 0 WHERE userId = ?", (subscribedDate, expirationDate, user_id), commit=True)
    return get_user_subscription_by_id_service(user_id)


def unsubscribe_service(username):
    user_id = execute_query("SELECT id FROM Users WHERE username = ?", (username,), fetchone=True)['id']

    if user_id is None:
        return {"message": "User not found", "statusCode": 404}

    execute_query("UPDATE UserSubscriptions SET expired = 1 WHERE userId = ?", (user_id,), commit=True)
    return {"statusCode": 200, "message": "User unsubscribed successfully"}