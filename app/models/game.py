from app.database import get_connection


class Game:
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
						'SELECT slug, name, description, image FROM games ORDER BY id'
					)
					raw_games = cursor.fetchall()

			return [
				{
					'nom': game['slug'],
					'descripcio': game['description'],
					'imatge': game['image'],
					'tag': 'REFLEX'
				}
				for game in raw_games
			]
		except Exception:
			return []

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
							name=row['name'],
							description=row['description'],
							image=row['image']
						)
			return None
		except Exception:
			return None

	def save(self):
		with get_connection() as conn:
			with conn.cursor() as cursor:
				cursor.execute(
					'''
					INSERT INTO games (slug, name, description, image)
					VALUES (%s, %s, %s, %s)
					''',
					(self.slug, self.name, self.description, self.image)
				)
				conn.commit()
		return True, 'Joc creat correctament.'
