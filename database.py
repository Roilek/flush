import os
from typing import Any, Mapping

import pymongo

from dotenv import load_dotenv

# Constants

DATABASE_NAME = "flush"
USERS_COLLECTION_NAME = "users"
ENIGMAS_COLLECTION_NAME = "enigmas"
AUTHENTICATED_USERS_COLLECTION_NAME = "authenticated_users"

mongo_client: pymongo.MongoClient = None


def is_authenticated(user_id: int) -> bool:
    """Return True if the user is authenticated."""
    db = mongo_client[DATABASE_NAME]
    collection = db[AUTHENTICATED_USERS_COLLECTION_NAME]
    return collection.find_one({"telegram_id": user_id}) is not None


def user_exists(user_id: int) -> bool:
    """Return True if the user exists."""
    db = mongo_client[DATABASE_NAME]
    collection = db[USERS_COLLECTION_NAME]
    return collection.find_one({"telegram_id": user_id}) is not None


def register_user(user_id: int, first_name: str, last_name: str = None, username: str = None) -> None:
    """Register a user."""
    db = mongo_client[DATABASE_NAME]
    collection = db[USERS_COLLECTION_NAME]
    user = {
        "telegram_id": user_id,
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "score": 0,
        "current_enigma": 0,
        "is_admin": False,
    }
    collection.insert_one(user)
    return


def setup() -> None:
    """Connects to the client."""
    load_dotenv()
    global mongo_client
    mongo_client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    return
