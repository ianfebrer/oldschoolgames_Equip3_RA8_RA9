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

	@classmethod
	def get_by_slug(cls, slug):
		try:
			with get_connection() as conn:
				with conn.cursor(dictionary=True) as cursor:
					cursor.execute(
						'SELECT slug, name, description, image FROM games WHERE slug = %s',
						(slug,)
					)
					row = cursor.fetchone()
					if row:
						return cls(
							slug=row['slug'],
							name=row.get('name', row['slug']),
							description=row['description'],
							image=row['image']
						)
			return None
		except Exception:
			# Fallback a JSON
			games = cls.get_all()
			for g in games:
				if g.get('slug') == slug or g.get('nom') == slug:
					return cls(
						slug=g.get('slug', g.get('nom')),
						name=g.get('nom', g.get('slug')),
						description=g.get('descripcio'),
						image=g.get('imatge')
					)
			return None

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
