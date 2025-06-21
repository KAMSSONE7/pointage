"""
Configuration centralisée pour la base de données.
"""
import logging
import os

# Configuration du logging
logger = logging.getLogger(__name__)


DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'switchback.proxy.rlwy.net'),  # Fallback option
    'database': os.getenv('DB_NAME', 'donnee_app'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'IowFRbmQYlvxWwLrMLalevEQqhQtWvYN'),
    'port': int(os.getenv('DB_PORT', 55321)),  # Convertit en entier
    'charset': 'utf8mb4',
    'autocommit': True,
    'connection_timeout': 10
}

def get_db_connection():
    """
    Crée et retourne une nouvelle connexion à la base de données.
    """
    import mysql.connector
    from mysql.connector import Error, errorcode
    
    logger.info("Tentative de connexion à la base de données...")
    logger.debug(f"Paramètres de connexion: host={DB_CONFIG['host']}, port={DB_CONFIG['port']}, database={DB_CONFIG['database']}")
    
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            db_info = connection.get_server_info()
            logger.info(f"Connecté à MySQL Server version {db_info}")
            return connection
        else:
            logger.error("La connexion à la base de données a échoué")
            return None
            
    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger.error("Erreur d'authentification: Vérifiez le nom d'utilisateur et le mot de passe")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger.error(f"La base de données {DB_CONFIG['database']} n'existe pas")
        elif isinstance(err, mysql.connector.errors.InterfaceError):
            logger.error(f"Impossible de se connecter au serveur MySQL sur {DB_CONFIG['host']}:{DB_CONFIG['port']}")
        else:
            logger.error(f"Erreur de connexion à la base de données: {err}")
        return None
    except Exception as e:
        logger.error(f"Erreur inattendue lors de la connexion: {str(e)}")
        return None
