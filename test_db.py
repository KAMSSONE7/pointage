import mysql.connector
from mysql.connector import Error

def test_connection():
    try:
        conn = mysql.connector.connect(
            host="yamanote.proxy.rlwy.net",
            database="railway",
            user="root",
            password="oAEycvrWsPdjBfkQnEhqbSLoggHAadRt",
            port=13208
        )
        print("✅ Connexion réussie à la base de données!")
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        print("Tables existantes:", cursor.fetchall())
    except Error as e:
        print(f"❌ Erreur de connexion: {e}")
    finally:
        if conn.is_connected():
            conn.close()

test_connection()