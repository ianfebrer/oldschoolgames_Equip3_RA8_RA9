from datetime import datetime
from app.mongo import get_mongo_db

class GameEvent:
    def __init__(self, game_id, username, event_type, data):
        self.game_id = game_id
        self.username = username
        self.event_type = event_type
        self.timestamp = datetime.utcnow()
        self.data = data

    def save_to_mongo(self):
        db = get_mongo_db()
        result = db.game_events.insert_one(self.to_dict())
        return result.inserted_id

    def to_dict(self):
        return {
            'game_id': self.game_id,
            'username': self.username,
            'event_type': self.event_type,
            'timestamp': self.timestamp,
            'data': self.data
        }
