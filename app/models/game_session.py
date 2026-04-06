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
	def get_leaderboard(cls, game_id, limit=5):
		# primer obtenim totes les sesions actuals
		sessions = cls.get_all()

		# després filtrem nomes les del joc
		filtrades = []
		for sessio in sessions:
			if sessio.get('game_id') == game_id:
				filtrades.append(sessio)

		# per cada usuario, només agafem la seua millor puntuació
		millors = {}
		for sessio in filtrades:
			user = sessio.get('username')
			score = sessio.get('score')
			if user not in millors:
				millors[user] = sessio
			else:
				score_actual = millors[user].get('score')
				duracio_actual = millors[user].get('duration_ms')
				duracio_nova = sessio.get('duration_ms')
				duracio_actual = float('inf') if duracio_actual is None else duracio_actual
				duracio_nova = float('inf') if duracio_nova is None else duracio_nova
				if score > score_actual:
					millors[user] = sessio
				elif score == score_actual and duracio_nova < duracio_actual:
					millors[user] = sessio

		def clau_ordenacio(sessio):
			score = sessio.get('score', 0)
			duracio = sessio.get('duration_ms')
			duracio = float('inf') if duracio is None else duracio
			return (-score, duracio)

		llista_millors = list(millors.values())
		llista_ordenada = sorted(llista_millors, key=clau_ordenacio)
		return llista_ordenada[:limit]


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
