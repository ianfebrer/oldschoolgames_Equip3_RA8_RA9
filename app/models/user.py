import json

class User:
	def __init__(self, username, password):
		self.username = username
		self.password = password

	def to_dict(self):
		return {
			'username': self.username,
			'password': self.password
		}

	def obtenirtots(self):
		with open('users.json', 'r') as f:
			users = json.load(f)
		return users

	def register(self):
		users = self.obtenirtots()
		users.append(self.to_dict())
		with open('users.json', 'w') as f:
			json.dump(users, f)

	def login(self):
		users = self.obtenirtots()
		for user in users:
			if user['username'] == self.username and user['password'] == self.password:
				return True
		return False
