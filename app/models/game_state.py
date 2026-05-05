from datetime import datetime
from app.mongo import get_mongo_db

class GameState:
    def __init__(self, game_id, username, state_data):
        self.game_id = game_id
        self.username = username
        self.state_data = state_data
        self.timestamp = datetime.utcnow()

    def save_to_mongo(self):
        db = get_mongo_db()
        result = db.game_states.insert_one(self.to_dict())
        return result.inserted_id

    def to_dict(self):
        return {
            'game_id': self.game_id,
            'username': self.username,
            'state_data': self.state_data,
            'timestamp': self.timestamp
        }
