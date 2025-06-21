"""
Configuration centralisée et optimisée pour la base de données avec gestion de pool de connexions.
"""
import logging
import mysql.connector
from mysql.connector import Error, errorcode, pooling
import os

# Configuration avancée du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration de la base de données avec variables d'environnement de Render
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'yamanote.proxy.rlwy.net'),
    'port': int(os.getenv('DB_PORT', 13208)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'oAEycvrWsPdjBfkQnEhqbSLoggHAadRt'),
    'database': os.getenv('DB_NAME', 'railway'),
    'autocommit': True,
    'pool_size': 5,
    'connect_timeout': 10,
    'raise_on_warnings': True,
    'ssl_ca': '/path/to/ca-cert.pem',  # Ajoute si SSL requis
    'ssl_verify_cert': True
}

# Initialisation du pool de connexions
try:
    connection_pool = pooling.MySQLConnectionPool(**DB_CONFIG)
    logger.info("Pool de connexions MySQL initialisé avec succès")
except Error as err:
    logger.error(f"Erreur lors de l'initialisation du pool: {err}")
    connection_pool = None

def get_db_connection():
    if not connection_pool:
        logger.error("Pool de connexions non initialisé")
        return None
    try:
        connection = connection_pool.get_connection()
        if connection.is_connected():
            logger.debug("Connexion obtenue depuis le pool")
            return connection
    except Error as err:
        logger.error(f"Erreur lors de l'obtention de la connexion: {err}")
        return None

def close_db_resources(cursor=None, connection=None):
    try:
        if cursor:
            cursor.close()
    except Exception as e:
        logger.warning(f"Erreur lors de la fermeture du curseur: {e}")
    try:
        if connection and connection.is_connected():
            connection.close()
            logger.debug("Connexion libérée dans le pool")
    except Exception as e:
        logger.warning(f"Erreur lors de la fermeture de la connexion: {e}")

if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()[0]
            logger.info(f"Connecté avec succès à la base: {db_name}")
        finally:
            close_db_resources(cursor, conn)