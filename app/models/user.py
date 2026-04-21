import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash

from app.database import get_connection
from app.models.base import Base

class User(Base):
	FILE_NAME = 'users.json'

	def __init__(self, username, password):
		self.username = username.strip()
		self.password = password

	def to_dict(self):
		return {
			'username': self.username,
			'password_hash': generate_password_hash(self.password)
		}

	def register(self):
		try:
			with get_connection() as conn:
				with conn.cursor() as cursor:
					cursor.execute(
						'INSERT INTO users (username, password_hash) VALUES (%s, %s)',
						(self.username, generate_password_hash(self.password))
					)
					conn.commit()
			return True, 'Usuari registrat correctament'
		except mysql.connector.IntegrityError:
			return False, 'Usuari ja existeix'

	def login(self):
		with get_connection() as conn:
			with conn.cursor(dictionary=True) as cursor:
				cursor.execute(
					'SELECT password_hash FROM users WHERE username = %s',
					(self.username,)
				)
				user = cursor.fetchone()
		if user and check_password_hash(user['password_hash'], self.password):
			return True, 'Login correcte'
		return False, 'Usuari o contrasenya incorrectes'
