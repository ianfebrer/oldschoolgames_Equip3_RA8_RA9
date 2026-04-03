import json

from app.models.base import Base

class User(Base):
	FILE_NAME = 'users.json'

	def __init__(self, username, password):
		self.username = username
		self.password = password

	def to_dict(self):
		return {
			'username': self.username,
			'password': self.password
		}

	def register(self):
		users = self.get_all()
		for user in users:
			if user['username'] == self.username:
				return False, 'Usuari ja existeix'
		users.append(self.to_dict())
		self.save_items(users)
		return True, 'Usuari registrat correctament'

	def login(self):
		users = self.get_all()
		for user in users:
			if user['username'] == self.username and user['password'] == self.password:
				return True, 'Login correcte'
		return False, 'Usuari o contranya incorrectes'
