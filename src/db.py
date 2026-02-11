import os
import dotenv

from pathlib import Path
dotenv.load_dotenv(Path(__file__).parent.parent / ".env")

from pymongo import MongoClient


def get_client() -> MongoClient:
    uri = os.environ.get("MONGODB_URI")
    return MongoClient(uri)


def get_collection(client: MongoClient):
    db_name = os.environ.get("MONGODB_DATABASE")
    return client[db_name]["assistant_usage_logs"]
