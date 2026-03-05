import json

data_dir = "app/data"

class Game:
	def __init__(self, name, description):
		self.name = name
		self.description = description

	def to_dict(self):
		return {
			'name': self.name,
			'description': self.description
		}

	def get_all(self):
		try:
			with open(f'{data_dir}/games.json', 'r', encoding='utf-8') as f:
				return json.load(f)
		except json.JSONDecodeError:
			return []

	def create(self):
		games = self.get_all()
		games.append(self.to_dict())
		with open(f'{data_dir}/games.json', 'w', encoding='utf-8') as f:
			json.dump(games, f, ensure_ascii=False, indent=4)
		return True, 'Juego creado correctamente'
