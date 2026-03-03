import json

data_dir = "app/data"

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
		with open(f'{data_dir}/users.json', 'r', encoding='utf-8') as f:
			try:
				users = json.load(f)
			except json.JSONDecodeError:
				users = []
		return users

	def register(self):
		users = self.obtenirtots()
		users.append(self.to_dict())
		with open(f'{data_dir}/users.json', 'w', encoding='utf-8') as f:
			json.dump(users, f, ensure_ascii=False, indent=4)

	def login(self):
		users = self.obtenirtots()
		for user in users:
			if user['username'] == self.username and user['password'] == self.password:
				return True
		return False
