from app.models.base import Base
from app.database import get_connection
import mysql.connector

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
        """Obté el Top 10 de MariaDB amb fallback a JSON."""
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    # LÒGICA: Millor puntuació per usuari en aquest joc,
                    # desfent empats per menor durada (duration_ms).
                    query = """
                        SELECT u.username, MAX(s.score) AS score, MIN(s.duration_ms) AS duration_ms
                        FROM scores s
                        JOIN users u ON s.user_id = u.id
                        WHERE s.game_slug = %s
                        GROUP BY u.id, u.username
                        ORDER BY score DESC, duration_ms ASC
                        LIMIT %s
                    """
                    cursor.execute(query, (game_id, limit))
                    return cursor.fetchall()
        except Exception as e:
            print(f"⚠️ Error obtenint leaderboard de MariaDB: {e}. Fent fallback a JSON.")
            
            # =========================================================
            # FALLBACK A JSON (Manté la mateixa lògica exacta que el SQL)
            # =========================================================
            try:
                all_sessions = cls.get_all()  # Mètode heretat de Base.py
                # Filtrem les sessions que pertanyen a aquest joc
                game_sessions = [s for s in all_sessions if s.get('game_id') == game_id]
                
                # Agrupem per usuari per agafar només la seva millor marca
                user_best = {}
                for s in game_sessions:
                    user = s.get('username')
                    score = int(s.get('score', 0))
                    duration = float(s.get('duration_ms', float('inf')))
                    
                    if user not in user_best:
                        user_best[user] = {'username': user, 'score': score, 'duration_ms': duration}
                    else:
                        # Si trobem una puntuació més alta, o mateixa puntuació en menys temps, la fitem
                        if score > user_best[user]['score']:
                            user_best[user]['score'] = score
                            user_best[user]['duration_ms'] = duration
                        elif score == user_best[user]['score'] and duration < user_best[user]['duration_ms']:
                            user_best[user]['duration_ms'] = duration
                
                # Convertim el diccionari a llista i ordenem: Puntuació DESC, Durada ASC
                leaderboard = list(user_best.values())
                leaderboard.sort(key=lambda x: (-x['score'], x['duration_ms']))
                
                return leaderboard[:limit]
            except Exception as json_err:
                print(f"❌ Error crític en el fallback de JSON: {json_err}")
                return []
    def save(self):
        """Guarda la sessió a MariaDB i manté el JSON com a còpia de seguretat."""
        success_sql = False
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    # 1. Necessitem l'ID de l'usuari (la taula scores usa user_id, no username)
                    cursor.execute("SELECT id FROM users WHERE username = %s", (self.username,))
                    user_row = cursor.fetchone()
                    
                    if user_row:
                        user_id = user_row[0]
                        # 2. Inserim la puntuació
                        query = """
                            INSERT INTO scores (user_id, game_slug, score, duration_ms)
                            VALUES (%s, %s, %s, %s)
                        """
                        cursor.execute(query, (user_id, self.game_id, self.score, self.duration_ms))
                        conn.commit()
                        success_sql = True
                    else:
                        print(f"⚠️ Usuari '{self.username}' no trobat a la DB.")
        except Exception as e:
            print(f"❌ Error guardant a MariaDB: {e}")

        # Fallback/Còpia a JSON (com fas a User.py)
        sessions = self.get_all()
        sessions.append(self.to_dict())
        self.save_items(sessions)
        
        return success_sql, "Sessió guardada correctament"