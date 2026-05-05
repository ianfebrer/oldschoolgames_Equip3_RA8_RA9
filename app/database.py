import os

import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

_connection_pool = None

def get_connection():
	global _connection_pool
	if _connection_pool is None:
		_connection_pool = mysql.connector.pooling.MySQLConnectionPool(
			pool_name="oldschool_pool",
			pool_size=5,
			host=os.getenv('DB_HOST', 'localhost'),
			port=int(os.getenv('DB_PORT', '3306')),
			user=os.getenv('DB_USER', 'root'),
			password=os.getenv('DB_PASSWORD', ''),
			database=os.getenv('DB_NAME', 'oldschoolgames')
		)
	return _connection_pool.get_connection()
