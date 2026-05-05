from pymongo import MongoClient
import os

_mongo_client = None

def get_mongo_db():
    global _mongo_client
    if _mongo_client is None:
        uri = os.getenv('MONGODB_URL', os.getenv('MONGO_URI', 'mongodb://localhost:27017/oldschoolgames'))
        _mongo_client = MongoClient(uri)
    
    try:
        return _mongo_client.get_default_database()
    except Exception:
        return _mongo_client['oldschoolgames']
