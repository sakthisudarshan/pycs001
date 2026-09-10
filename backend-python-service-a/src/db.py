"""
MongoDB connection helper — mirrors MongoDB.Driver usage in C# service.
Covers: Statement Coverage, Definition Coverage
"""
import os
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB: str = os.getenv("MONGO_DB", "ceplatform")

_client: MongoClient | None = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client


def get_database() -> Database:
    return get_client()[MONGO_DB]


def get_collection(name: str) -> Collection:
    return get_database()[name]


def close_client() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None
