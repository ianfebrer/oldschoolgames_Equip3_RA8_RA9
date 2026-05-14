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
		try:
			with get_connection() as conn:
				with conn.cursor(dictionary=True) as cursor:
					# Obtenim la millor puntuació de cada usuari per a aquest joc
					query = """
						SELECT u.username, MAX(s.score) as score, MIN(s.duration_ms) as duration_ms
						FROM scores s
						JOIN users u ON s.user_id = u.id
						WHERE s.game_slug = %s
						GROUP BY u.username
						ORDER BY score DESC, duration_ms ASC
						LIMIT %s
					"""
					cursor.execute(query, (game_id, limit))
					return cursor.fetchall()
		except Exception as e:
			print(f"Error al carregar el leaderboard des de MySQL: {e}")
			# Fallback a JSON (lògica original simplificada)
			try:
				sessions = cls.get_all()
				filtrades = [s for s in sessions if s.get('game_id') == game_id]
				millors = {}
				for s in filtrades:
					user = s.get('username')
					score = s.get('score', 0)
					duration = s.get('duration_ms', float('inf'))
					if user not in millors or score > millors[user]['score'] or (score == millors[user]['score'] and duration < millors[user]['duration_ms']):
						millors[user] = s
				
				llista_ordenada = sorted(millors.values(), key=lambda x: (-x.get('score', 0), x.get('duration_ms', float('inf'))))
				return llista_ordenada[:limit]
			except Exception:
				return []

	def save(self):
		# Primer intentem guardar a MySQL
		try:
			with get_connection() as conn:
				with conn.cursor() as cursor:
					# Necessitem l'ID de l'usuari
					cursor.execute("SELECT id FROM users WHERE username = %s", (self.username,))
					user = cursor.fetchone()
					if not user:
						return False, "Usuari no trobat a la base de dades"
					
					user_id = user[0]
					
					# Inserim la nova puntuació
					query = "INSERT INTO scores (user_id, game_slug, score, duration_ms) VALUES (%s, %s, %s, %s)"
					cursor.execute(query, (user_id, self.game_id, self.score, self.duration_ms))
					conn.commit()
					
			return True, "Puntuació guardada correctament a MySQL"
		except Exception as e:
			print(f"Error al guardar a MySQL, utilitzant fallback JSON: {e}")
			# Fallback a JSON (lògica original)
			try:
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
			except Exception as json_e:
				return False, f"Error al guardar la puntuació: {json_e}"
