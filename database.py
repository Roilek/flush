import os
from typing import Any, Mapping

import pymongo
from dotenv import load_dotenv

from Enigma import Enigma

# Constants

DATABASE_NAME = "flush"
USERS_COLLECTION_NAME = "users"
ENIGMAS_COLLECTION_NAME = "enigmas"
AUTHENTICATED_USERS_COLLECTION_NAME = "authenticated_users"
ATTEMPTS_COLLECTION_NAME = "attempts"

mongo_client: pymongo.MongoClient = None


# Functions

def setup() -> None:
    """Connects to the client."""
    load_dotenv()
    global mongo_client
    mongo_client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    return


# --- USERS ---

def is_admin(user_id: int) -> bool:
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
        "current_enigma": 0,
        "is_admin": False,
    }
    collection.insert_one(user)
    return


# --- ENIGMAS ---

def add_enigma(enigma: Enigma) -> None:
    """Add an enigma."""
    db = mongo_client[DATABASE_NAME]
    collection = db[ENIGMAS_COLLECTION_NAME]
    collection.insert_one(enigma.to_dict())
    return


def user_has_enigma(user_id: int) -> bool:
    """Return True if the user has an enigma."""
    db = mongo_client[DATABASE_NAME]
    collection = db[USERS_COLLECTION_NAME]
    user = collection.find_one({"telegram_id": user_id})
    return user["current_enigma"] != 0


def get_user_enigma(user_id: int) -> Enigma:
    """Return the enigma of the user."""
    db = mongo_client[DATABASE_NAME]
    collection = db[USERS_COLLECTION_NAME]
    user = collection.find_one({"telegram_id": user_id})
    return get_enigma(user["current_enigma"])


def update_user_enigma(user_id: int, enigma_id: int) -> None:
    """Update the enigma of the user."""
    db = mongo_client[DATABASE_NAME]
    collection = db[USERS_COLLECTION_NAME]
    collection.update_one({"telegram_id": user_id}, {"$set": {"current_enigma": enigma_id}})
    return


def reset_user_enigma(user_id: int) -> None:
    """Reset the enigma of the user."""
    update_user_enigma(user_id, enigma_id=0)
    return


def enigma_exists(enigma_id: int) -> bool:
    """Return True if the enigma exists."""
    db = mongo_client[DATABASE_NAME]
    collection = db[ENIGMAS_COLLECTION_NAME]
    return collection.find_one({"id": enigma_id}) is not None


def get_enigma(enigma_id: int) -> Enigma:
    """Return the enigma."""
    db = mongo_client[DATABASE_NAME]
    collection = db[ENIGMAS_COLLECTION_NAME]
    enigma = collection.find_one({"id": enigma_id})
    return Enigma.from_dict(enigma)


def user_solved_enigma(user_id, enigma_id) -> bool:
    """Return True if the user solved the enigma."""
    db = mongo_client[DATABASE_NAME]
    collection = db[ATTEMPTS_COLLECTION_NAME]
    return collection.find_one({"user_id": user_id, "enigma_id": enigma_id, "correct": True}) is not None


# --- ATTEMPTS RELATION ---

def add_attempt(user_id: int, enigma_id: int, attempt: str, correct: bool) -> None:
    """Add an attempt."""
    db = mongo_client[DATABASE_NAME]
    collection = db[ATTEMPTS_COLLECTION_NAME]
    attempt = {
        "user_id": user_id,
        "enigma_id": enigma_id,
        "attempt": attempt,
        "correct": correct,
    }
    collection.insert_one(attempt)
    return
