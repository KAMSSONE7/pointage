from db_config import DB_CONFIG
import mysql.connector

def check_tables():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Test 1: Vérifie la connexion
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()[0]
        print(f"[SUCCES] Connecté à la base: {db_name}")  # Remplacement du ✅
        
        # Test 2: Liste les tables
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        print(f"[INFO] Tables disponibles: {tables or 'Aucune table trouvée!'}")
        
        # Test 3: Exemple de requête
        if 'utilisateurs' in tables:
            cursor.execute("SELECT COUNT(*) FROM utilisateurs")
            count = cursor.fetchone()[0]
            print(f"[DATA] Nombre d'utilisateurs: {count}")
            
    except Exception as e:
        print(f"[ERREUR] {e}")  # Remplacement du ❌
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

check_tables()