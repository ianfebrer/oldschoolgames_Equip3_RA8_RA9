from app.models.base import Base

class GameSession(Base):
    FILE_NAME = 'game_sessions.json'

    def __init__(self, game_id, username, start_time, end_time, score, duration_ms=None):
        self.game_id = str(game_id)
        self.username = str(username)
        self.start_time = float(start_time)
        self.end_time = float(end_time)
        self.score = int(score)
        self.duration_ms = float(duration_ms) if duration_ms is not None else 0.0

    def to_dict(self):
        return {
            'game_id': self.game_id,
            'username': self.username,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'score': self.score,
            'duration_ms': self.duration_ms
        }

    @classmethod
    def get_leaderboard(cls, game_id, limit=10):
        from app.database import get_connection
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    # Fem un JOIN amb la taula d'usuaris (feina de l'Adrià) 
                    # per mostrar el nom i no només l'ID
                    sql = """
                        SELECT u.username, s.score, s.duration_ms, s.played_at 
                        FROM scores s
                        JOIN users u ON s.user_id = u.id
                        WHERE s.game_slug = %s
                        ORDER BY s.score DESC, s.duration_ms ASC
                        LIMIT %s
                    """
                    cursor.execute(sql, (game_id, limit))
                    return cursor.fetchall()
        except Exception as e:
            print(f"❌ Error al rànquing de Ian: {e}")
            return []

    def save(self):
        game_sessions = self.get_all()
        user_found = False

        for game in game_sessions:
            if game['game_id'] == self.game_id and game['username'] == self.username:
                user_found = True
                if int(game['score']) < int(self.score):
                    game['score'] = int(self.score)
                    game['end_time'] = float(self.end_time)
                    game['duration_ms'] = float(self.duration_ms)
                break

        if not user_found:
            game_sessions.append(self.to_dict())

        return self.save_items(game_sessions)