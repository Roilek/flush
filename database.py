import os
from typing import Any, Mapping

import pymongo

from dotenv import load_dotenv

# Constants

DATABASE_NAME = "flush"
ENIGMAS_COLLECTION_NAME = "enigmas"
AUTHENTICATED_USERS_COLLECTION_NAME = "authenticated_users"

mongo_client: pymongo.MongoClient = None


def is_authenticated(user_id: int) -> bool:
    """Return True if the user is authenticated."""
    db = mongo_client[DATABASE_NAME]
    collection = db[AUTHENTICATED_USERS_COLLECTION_NAME]
    return collection.find_one({"telegram_id": user_id}) is not None


def setup() -> None:
    """Connects to the client."""
    load_dotenv()
    global mongo_client
    mongo_client = pymongo.MongoClient(os.getenv("MONGO_URI"))
