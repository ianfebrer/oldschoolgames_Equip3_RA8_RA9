from datetime import datetime
from app.mongo import get_mongo_db

class GameLog:
    def __init__(self, game_id, username, session_id):
        self.game_id = game_id
        self.username = username
        self.session_id = session_id
        self.started_at = datetime.utcnow()
        self.events = []
        self.closed = False
        self.final_score = None

    def add_event(self, event_dict):
        self.events.append(event_dict)

    def close_log(self, final_score):
        self.closed = True
        self.final_score = final_score
        self.ended_at = datetime.utcnow()

    def save_to_mongo(self):
        db = get_mongo_db()
        doc = {
            'game_id': self.game_id,
            'username': self.username,
            'session_id': self.session_id,
            'started_at': self.started_at,
            'events': self.events,
            'closed': self.closed,
            'final_score': self.final_score
        }
        if self.closed:
            doc['ended_at'] = self.ended_at

        # Si el document ja existeix, l'actualitzem (upsert)
        result = db.game_logs.update_one(
            {'session_id': self.session_id},
            {'$set': doc},
            upsert=True
        )
        return result.upserted_id or self.session_id
