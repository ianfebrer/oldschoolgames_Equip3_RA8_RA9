import os
import mysql.connector
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Connexió a MariaDB
def get_mariadb_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        # Ara agafarà correctament el port 3308 del teu .env
        port=int(os.getenv('DB_PORT', '3306')), 
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'oldschoolgames')
    )

# Connexió a MongoDB
def get_mongodb_db():
    try:
        # Canviat a 'MONGODB_URL' per coincidir amb el teu .env
        mongo_uri = os.getenv('MONGODB_URL', 'mongodb://localhost:27017/')
        client = MongoClient(mongo_uri)
        
        # Utilitzem 'DB_NAME' que és la variable que tens al .env
        db_name = os.getenv('DB_NAME', 'oldschoolgames')
        return client[db_name]
    except Exception as e:
        print(f"Error connectant a MongoDB: {e}")
        return None