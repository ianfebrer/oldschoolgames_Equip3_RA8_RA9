from app.database import get_connection
from app.models.base import Base

class Game(Base):
	FILE_NAME = 'games.json'

	def __init__(self, slug, name, description, image=None, max_score=10):
		self.slug = slug
		self.name = name
		self.description = description
		self.image = image
		self.max_score = max_score

	def to_dict(self):
		return {
			'slug': self.slug,
			'name': self.name,
			'description': self.description,
			'image': self.image,
			'max_score': self.max_score
		}

	@classmethod
	def get_all_main(cls):
		try:
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
		except Exception:
			# Fallback a JSON si no hi ha base de dades
			return cls.get_all()

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
