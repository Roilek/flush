import os
from typing import Any, Mapping

import pymongo

from dotenv import load_dotenv
from pymongo import MongoClient

mongo_client: MongoClient[Mapping[str, Any] | Any] = None


def setup() -> None:
    load_dotenv()
    global mongo_client
    mongo_client = pymongo.MongoClient(os.getenv("MONGO_URI"))
