"""
Configuration centralisée et optimisée pour la base de données avec variables d’environnement personnalisées.
"""
import logging
import mysql.connector
from mysql.connector import Error, errorcode, pooling
import os

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lecture des variables d’environnement
DB_CONFIG = {
    'host': os.environ.get("DB_HOST", "localhost"),
    'port': int(os.environ.get("DB_PORT", 3306)),
    'user': os.environ.get("DB_USER", "root"),
    'password': os.environ.get("DB_PASSWORD", ""),
    'database': os.environ.get("DB_NAME", "railway"),
    'autocommit': True,
    'pool_size': 5,
    'connect_timeout': 10,
    'raise_on_warnings': True
}

# Initialisation du pool de connexions
try:
    connection_pool = pooling.MySQLConnectionPool(**DB_CONFIG)
    logger.info("✅ Pool de connexions MySQL initialisé avec succès")
except Error as err:
    logger.error(f"❌ Erreur lors de l'initialisation du pool : {err}")
    connection_pool = None

def get_db_connection():
    """
    Récupère une connexion depuis le pool.
    """
    if not connection_pool:
        logger.error("❌ Le pool de connexions n’est pas initialisé.")
        return None

    try:
        connection = connection_pool.get_connection()
        if connection.is_connected():
            logger.debug("✅ Connexion obtenue depuis le pool")
            return connection
    except Error as err:
        logger.error(f"❌ Erreur de connexion : {err}")
        return None

def close_db_resources(cursor=None, connection=None):
    """
    Ferme proprement les ressources.
    """
    try:
        if cursor:
            cursor.close()
    except Exception as e:
        logger.warning(f"⚠️ Erreur fermeture curseur : {e}")

    try:
        if connection and connection.is_connected():
            connection.close()
            logger.debug("✅ Connexion libérée")
    except Exception as e:
        logger.warning(f"⚠️ Erreur fermeture connexion : {e}")

# Test de connexion
if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE()")
            db = cursor.fetchone()[0]
            logger.info(f"🎯 Connecté à la base : {db}")
        finally:
            close_db_resources(cursor, conn)
