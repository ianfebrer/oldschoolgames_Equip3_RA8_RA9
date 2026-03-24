from app.models.base import Base

class Game(Base):
	FILE_NAME = 'games.json'

	def __init__(self, nom, descripcio):
		self.nom = nom
		self.descripcio = descripcio

	def to_dict(self):
		return {
			'nom': self.nom,
			'descripcio': self.descripcio
		}

	@classmethod
	def get_all_main(cls):
		raw_games = cls.get_all()
		result = []
		for game in raw_games:
			nom = game.get('nom').lower()
			descripcio = game.get('descripcio')
			result.append(
				{
					'nom': nom,
					'descripcio': descripcio
				}
			)
		return result

	def save(self):
		games = self.get_all()
		games.append(self.to_dict())
		self.save(games)
		return True, 'Juego creado correctamente'
