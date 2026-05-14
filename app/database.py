import os
import time

import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

_connection_pool = None

# Circuit breaker: si la BD falla, esperem un temps mínim
# abans de tornar a intentar-ho, per evitar bloquejar cada petició.
_db_unavailable_until = 0
_DB_RETRY_COOLDOWN_SECONDS = 30


def get_connection():
    global _connection_pool, _db_unavailable_until

    # Si el circuit breaker està actiu, llancem error immediatament
    # sense esperar cap timeout de xarxa.
    if time.monotonic() < _db_unavailable_until:
        raise ConnectionError("MySQL no disponible (circuit breaker actiu)")

    if _connection_pool is None:
        try:
            _connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="oldschool_pool",
                pool_size=5,
                host=os.getenv('DB_HOST', 'localhost'),
                port=int(os.getenv('DB_PORT', '3306')),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', ''),
                database=os.getenv('DB_NAME', 'oldschoolgames'),
                connect_timeout=2  # Reduït a 2s per fallback ràpid
            )
        except Exception as e:
            # Activem el circuit breaker: no tornarem a provar durant 30s
            _db_unavailable_until = time.monotonic() + _DB_RETRY_COOLDOWN_SECONDS
            print(f"[DB] MySQL no disponible, circuit breaker actiu durant {_DB_RETRY_COOLDOWN_SECONDS}s: {e}")
            raise

    try:
        return _connection_pool.get_connection()
    except Exception as e:
        # Si el pool existeix però no pot donar connexions, resetegem
        _connection_pool = None
        _db_unavailable_until = time.monotonic() + _DB_RETRY_COOLDOWN_SECONDS
        print(f"[DB] Error al pool de connexions, circuit breaker actiu: {e}")
        raise
