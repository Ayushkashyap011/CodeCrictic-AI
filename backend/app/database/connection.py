"""
app/database/connection.py
Async MongoDB connection manager using Motor — configured for MongoDB Atlas.

Atlas connection strings use the mongodb+srv:// scheme which automatically
enables TLS and DNS-based replica set discovery. Motor handles this natively.
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)


class Database:
    client: AsyncIOMotorClient | None = None
    db: AsyncIOMotorDatabase | None = None


_db = Database()


async def connect_db() -> None:
    """Open the Motor connection pool to MongoDB Atlas."""
    settings = get_settings()
    logger.info("Connecting to MongoDB Atlas...")

    _db.client = AsyncIOMotorClient(
        settings.mongodb_url,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=10000,
        socketTimeoutMS=10000,
        maxPoolSize=10,
        retryWrites=True,
    )
    _db.db = _db.client[settings.database_name]

    # Verify connectivity (raises if credentials or network are wrong)
    await _db.client.admin.command("ping")
    logger.info("✅ MongoDB Atlas connected — database: %s", settings.database_name)


async def close_db() -> None:
    """Close the Motor connection pool."""
    if _db.client:
        _db.client.close()
        logger.info("MongoDB connection closed")


def get_db() -> AsyncIOMotorDatabase:
    """Return the active database instance (dependency-injectable)."""
    if _db.db is None:
        raise RuntimeError("Database not initialised. Did connect_db() run?")
    return _db.db
