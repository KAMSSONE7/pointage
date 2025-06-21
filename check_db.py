"""
Script pour vérifier la connexion à la base de données et le contenu des tables.
"""
import mysql.connector
from mysql.connector import Error
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_database():
    """Vérifie la connexion à la base de données et le contenu des tables."""
    config = {
        'host': '127.0.0.1',
        'database': 'railway',
        'user': 'root',
        'password': '',
        'port': 13208,
        'charset': 'utf8mb4',
        'autocommit': True,
        'auth_plugin': 'mysql_native_password'
    }
    
    try:
        # Connexion au serveur MySQL
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            
            # Vérifier les bases de données disponibles
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print("\nBases de données disponibles:")
            for db in databases:
                print(f"- {db['Database']}")
            
            # Vérifier les tables dans railway
            cursor.execute("USE railway")
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("\nTables dans railway:")
            for table in tables:
                table_name = table[f'Tables_in_{config["database"]}']
                print(f"\nTable: {table_name}")
                
                # Afficher la structure de la table
                try:
                    cursor.execute(f"DESCRIBE {table_name}")
                    structure = cursor.fetchall()
                    print("\nStructure:")
                    for col in structure:
                        print(f"- {col['Field']}: {col['Type']} ({col['Null']})")
                    
                    # Afficher les 5 premières lignes
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
                    rows = cursor.fetchall()
                    print(f"\nDonnées (max 5 lignes):")
                    for row in rows:
                        print(row)
                        
                except Exception as e:
                    print(f"Erreur lors de la lecture de la table {table_name}: {e}")
            
    except Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("\nConnexion à la base de données fermée.")

if __name__ == "__main__":
    print("Début de la vérification de la base de données...")
    check_database()
