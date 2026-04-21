from app.database import get_connection
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
		with get_connection() as conn:
			with conn.cursor(dictionary=True) as cursor:
				cursor.execute(
					'SELECT slug, description, image FROM games ORDER BY id'
				)
				raw_games = cursor.fetchall()

		return [
			{
				'nom': game['slug'],
				'descripcio': game['description'],
				'imatge': game['image']
			}
			for game in raw_games
		]

	def save(self):
		with get_connection() as conn:
			with conn.cursor() as cursor:
				cursor.execute(
					'''
					INSERT INTO games (slug, name, description, image)
					VALUES (%s, %s, %s, %s)
					''',
					(self.nom.lower(), self.nom, self.descripcio, self.imatge)
				)
				conn.commit()
		return True, 'Juego creado correctamente'
