import pymongo
import os
from datetime import datetime
from app.database import get_connection # Utilitzem la connexió que ja teniu configurada

class GameResult:
    def __init__(self, user_id, game_slug, score, duration_ms, details=None):
        self.user_id = user_id
        self.game_slug = game_slug
        self.score = score
        self.duration_ms = duration_ms
        self.details = details if details else {}  # Dades dinàmiques per a MongoDB
        self.timestamp = datetime.now()

    def save(self):
        """Mètode principal que orquestra el guardat a les dues DBs."""
        sql_ok = self._save_to_mariadb()
        mongo_ok = self._save_to_mongodb()
        return sql_ok and mongo_ok

    def _save_to_mariadb(self):
        """Guarda les dades estructurades per al Top 10."""
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = """INSERT INTO scores (user_id, game_slug, score, duration_ms, played_at) 
                             VALUES (%s, %s, %s, %s, %s)"""
                    cursor.execute(sql, (self.user_id, self.game_slug, self.score, self.duration_ms, self.timestamp))
                    conn.commit()
            return True
        except Exception as e:
            print(f"❌ Error MariaDB: {e}")
            return False

    def _save_to_mongodb(self):
        """Guarda totes les dades variables (intents, moviments, etc.)."""
        try:
            # Connectem a MongoDB (pots posar la URI al .env)
            client = pymongo.MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
            db = client["oldschoolgames_logs"]
            collection = db["game_details"]
            
            document = {
                "user_id": self.user_id,
                "game_slug": self.game_slug,
                "score": self.score,
                "duration_ms": self.duration_ms,
                "timestamp": self.timestamp,
                "extended_data": self.details # Aquí va la informació que no cap al SQL
            }
            collection.insert_one(document)
            return True
        except Exception as e:
            print(f"❌ Error MongoDB: {e}")
            return False