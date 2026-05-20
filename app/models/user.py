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
			return True, 'register_success'
		except mysql.connector.IntegrityError:
			return False, 'username_exists'
		except Exception:
			# Fallback a JSON
			users = self.get_all()
			if any(u['username'] == self.username for u in users):
				return False, 'username_exists'
			users.append({
				'username': self.username,
				'password': self.password # Guardem en pla com sembla estar el JSON original
			})
			self.save_items(users)
			return True, 'register_success_local'

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
				return True, 'login_success'
			return False, 'invalid_credentials'
		except Exception:
			# Fallback a JSON
			users = self.get_all()
			for u in users:
				if u['username'] == self.username:
					# Comprovem tant hashed com pla (pel format del JSON original)
					if u.get('password') == self.password or \
					   (u.get('password_hash') and check_password_hash(u['password_hash'], self.password)):
						return True, 'login_success_local'
			return False, 'invalid_credentials'
