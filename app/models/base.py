import json
from abc import ABC, abstractmethod

class Base(ABC):
	DATA_DIR = 'app/data'
	FILE_NAME =None

	@classmethod
	def get_all(cls):
		"""Llegeix tots els registres del fitxer JSON. Les subclasses l'hereten."""
		with open(f'{cls.DATA_DIR}/{cls.FILE_NAME}', 'r', encoding='utf-8') as f:
			try:
				return json.load(f)
			except json.JSONDecodeError:
				return []
	@classmethod
	def save_items(cls, items):
		try:
			with open(f'{cls.DATA_DIR}/{cls.FILE_NAME}', 'w', encoding='utf-8') as f:
				json.dump(items, f, ensure_ascii=False, indent=4)
			return True, 'Items creados correctamente'
		except Exception as e:
			return False, f'Error al guardar els items: {str(e)}'

	@abstractmethod
	def to_dict(self):
		pass
