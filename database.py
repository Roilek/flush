import os
from typing import Any, Mapping

import pymongo

from dotenv import load_dotenv


# Constants

DATABASE_NAME = "flush"
ENIGMAS_COLLECTION_NAME = "enigmas"
AUTHENTICATED_USERS_COLLECTION_NAME = "authenticated_users"

mongo_client: pymongo.MongoClient = None


def get_authenticated_users() -> list:
    """Return a list of all the authenticated telegram ids."""
    users = []
    for x in mongo_client[DATABASE_NAME][AUTHENTICATED_USERS_COLLECTION_NAME].find({}, {"_id": 0, "telegram_id": 1}):
        users.append(x["telegram_id"])
    return users


def setup() -> None:
    """Connects to the client."""
    load_dotenv()
    global mongo_client
    mongo_client = pymongo.MongoClient(os.getenv("MONGO_URI"))
