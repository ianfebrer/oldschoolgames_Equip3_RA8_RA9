from app.models.base import Base

class Game(Base):
	FILE_NAME = 'games.json'

	def __init__(self, nom, descripcio, imatge=None):
		self.nom = nom
		self.descripcio = descripcio
		self.imatge = imatge

	def to_dict(self):
		return {
			'nom': self.nom,
			'descripcio': self.descripcio,
			'imatge': self.imatge
		}

	@classmethod
	def get_all_main(cls):
		raw_games = cls.get_all()
		result = []
		for game in raw_games:
			nom = game.get('nom').lower()
			descripcio = game.get('descripcio')
			imatge = game.get('imatge')
			result.append(
				{
					'nom': nom,
					'descripcio': descripcio,
					'imatge': imatge
				}
			)
		return result

	def save(self):
		games = self.get_all()
		games.append(self.to_dict())
		self.save(games)
		return True, 'Juego creado correctamente'
