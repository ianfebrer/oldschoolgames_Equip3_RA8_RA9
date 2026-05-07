from pymongo import MongoClient
import os
import time

_mongo_client = None

# Circuit breaker per a MongoDB: igual que per a MySQL
_mongo_unavailable_until = 0
_MONGO_RETRY_COOLDOWN_SECONDS = 30


def get_mongo_db():
    global _mongo_client, _mongo_unavailable_until

    # Si el circuit breaker està actiu, llancem error immediatament
    if time.monotonic() < _mongo_unavailable_until:
        raise ConnectionError("MongoDB no disponible (circuit breaker actiu)")

    if _mongo_client is None:
        try:
            uri = os.getenv('MONGODB_URL', os.getenv('MONGO_URI', 'mongodb://localhost:27017/oldschoolgames'))
            # serverSelectionTimeoutMS: temps màxim per trobar un servidor Mongo (2s)
            # connectTimeoutMS: temps màxim per establir la connexió TCP (2s)
            _mongo_client = MongoClient(
                uri,
                serverSelectionTimeoutMS=2000,
                connectTimeoutMS=2000,
                socketTimeoutMS=3000
            )
            # Comprovem que la connexió funciona realment
            _mongo_client.admin.command('ping')
        except Exception as e:
            _mongo_client = None
            _mongo_unavailable_until = time.monotonic() + _MONGO_RETRY_COOLDOWN_SECONDS
            print(f"[Mongo] MongoDB no disponible, circuit breaker actiu durant {_MONGO_RETRY_COOLDOWN_SECONDS}s: {e}")
            raise

    try:
        return _mongo_client.get_default_database()
    except Exception:
        return _mongo_client['oldschoolgames']
