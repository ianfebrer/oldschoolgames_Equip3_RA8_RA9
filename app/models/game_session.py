import json

data_dir = "app/data"

class GameSession:
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

	def get_all(self):
		with open(f'{data_dir}/game_sessions.json', 'r', encoding='utf-8') as f:
			try:
				game_sessions = json.load(f)
			except json.JSONDecodeError:
				game_sessions = []
		return game_sessions

	def create(self):
		game_sessions = self.get_all()
		game_sessions.append(self.to_dict())
		with open(f'{data_dir}/game_sessions.json', 'w', encoding='utf-8') as f:
			json.dump(game_sessions, f, ensure_ascii=False, indent=4)
		return True, 'Sesión de juego creada correctamente'
