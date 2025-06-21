from db_config import get_db_connection

def check_etudiant_table():
    try:
        connection = get_db_connection()
        if not connection or not connection.is_connected():
            print("Impossible de se connecter à la base de données")
            return
            
        cursor = connection.cursor()
        
        # Vérifier la structure de la table etudiant
        cursor.execute("DESCRIBE etudiant")
        print("Structure de la table 'etudiant':")
        for column in cursor.fetchall():
            print(column)
            
        # Vérifier si la colonne IP existe
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'railway' 
            AND TABLE_NAME = 'etudiant' 
            AND COLUMN_NAME = 'IP';
        """)
        
        if cursor.fetchone():
            print("\nLa colonne 'IP' existe dans la table 'etudiant'")
        else:
            print("\nLa colonne 'IP' n'existe pas dans la table 'etudiant'")
            
        # Afficher quelques enregistrements pour vérifier les données
        print("\nQuelques enregistrements de la table 'etudiant':")
        cursor.execute("SELECT Numero, IP FROM etudiant LIMIT 5")
        for row in cursor.fetchall():
            print(f"Numero: {row[0]}, IP: {row[1]}")
            
    except Exception as e:
        print(f"Erreur lors de la vérification de la table: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("\nConnexion à la base de données fermée")

if __name__ == "__main__":
    check_etudiant_table()
