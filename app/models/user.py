import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash

from app.database import get_connection


class User:
	def __init__(self, username, password):
		self.username = username.strip()
		self.password = password

	def register(self):
		try:
			with get_connection() as conn:
				with conn.cursor() as cursor:
					cursor.execute(
						'INSERT INTO users (username, password_hash) VALUES (%s, %s)',
						(self.username, generate_password_hash(self.password))
					)
					conn.commit()
			return True, 'Usuari registrat correctament.'
		except mysql.connector.IntegrityError:
			return False, 'Aquest nom d\'usuari ja existeix.'
		except Exception:
			return False, 'No s\'ha pogut connectar amb la base de dades.'

	def login(self):
		try:
			with get_connection() as conn:
				with conn.cursor(dictionary=True) as cursor:
					cursor.execute(
						'SELECT password_hash FROM users WHERE username = %s',
						(self.username,)
					)
					user = cursor.fetchone()
			if user and check_password_hash(user['password_hash'], self.password):
				return True, 'Login correcte.'
			return False, 'Usuari o contrasenya incorrectes.'
		except Exception:
			return False, 'No s\'ha pogut connectar amb la base de dades.'
