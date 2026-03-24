import json

from app.models.base import Base

class GameSession(Base):
	FILE_NAME = 'game_sessions.json'

	def __init__(self, game_id, username, start_time, end_time, score):
		self.game_id = game_id
		self.username = username
		self.start_time = start_time
		self.end_time = end_time
		self.score = score

	def to_dict(self):
		return {
			'game_id': self.game_id,
			'username': self.username,
			'start_time': self.start_time,
			'end_time': self.end_time,
			'score': self.score
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
				if score > score_actual:
					millors[user] = sessio

		def puntuacio(sessio):
			return sessio.get('score')

		llista_millors = list(millors.values())
		llista_ordenada = sorted(llista_millors, key=puntuacio, reverse=True)
		return llista_ordenada[:limit]


	def save(self):
		game_sessions = self.get_all()
		user_found = False

		for game in game_sessions:
			if game['game_id'] == self.game_id and game['username'] == self.username:
				user_found = True
				if game['score'] < self.score:
					game['score'] = self.score
					game['end_time'] = self.end_time
				break

		if not user_found:
			game_sessions.append(self.to_dict())

		return self.save_items(game_sessions)
