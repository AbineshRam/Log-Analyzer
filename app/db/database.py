from pymongo import MongoClient
from pymongo.database import Database
from typing import Optional

from app.core.config import settings


# =========================
# GLOBAL CLIENT
# =========================

_client: Optional[MongoClient] = None
_db: Optional[Database] = None


# =========================
# CONNECTION HANDLERS
# =========================

def connect_db() -> None:
    """
    Create MongoDB connection on app startup
    """
    global _client, _db

    _client = MongoClient(
        settings.MONGO_URI,
        maxPoolSize=10,
        serverSelectionTimeoutMS=5000
    )

    _db = _client[settings.MONGO_DB_NAME]

    # Simple ping to validate connection
    _client.admin.command("ping")
    print("✅ MongoDB connected")


def close_db() -> None:
    """
    Close MongoDB connection on app shutdown
    """
    global _client

    if _client:
        _client.close()
        print("🛑 MongoDB connection closed")


def get_db() -> Database:
    """
    Dependency-style DB accessor
    """
    if _db is None:
        raise RuntimeError("Database not initialized")
    return _db
