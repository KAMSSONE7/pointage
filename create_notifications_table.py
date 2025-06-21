import mysql.connector
from mysql.connector import Error
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def execute_sql_file(filename):
    """
    Exécute un fichier SQL sur la base de données.
    """
    try:
        # Lire le contenu du fichier SQL
        with open(filename, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        
        # Se connecter à la base de données
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='IowFRbmQYlvxWwLrMLalevEQqhQtWvYN',
            port=55321,
            database='railway'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Exécuter chaque commande SQL séparément
            for statement in sql_script.split(';'):
                if statement.strip():
                    try:
                        cursor.execute(statement)
                        logger.info(f"Commande exécutée avec succès: {statement[:50]}...")
                    except Error as e:
                        logger.error(f"Erreur lors de l'exécution de la commande: {e}")
            
            # Valider les modifications
            connection.commit()
            logger.info("Toutes les commandes ont été exécutées avec succès.")
            
    except Error as e:
        logger.error(f"Erreur de connexion à la base de données: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            logger.info("Connexion à la base de données fermée.")

if __name__ == "__main__":
    # Exécuter le script SQL
    execute_sql_file("ajouter_table_notifications.sql")
    print("Création de la table des notifications terminée.")
