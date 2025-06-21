import mysql.connector

def main():
    try:
        # Connexion en tant que root
        conn = mysql.connector.connect(
            host='127.0.0.1',
            port=55321,
            user='root',
            password='IowFRbmQYlvxWwLrMLalevEQqhQtWvYN',
            auth_plugin='mysql_native_password'
        )
        
        cursor = conn.cursor()
        
        # Paramètres
        db_name = 'railway'
        db_user = 'app_user'
        db_password = 'MonMotDePasseSecurise123!'  # À changer en production
        
        # Création utilisateur
        cursor.execute(f"CREATE USER IF NOT EXISTS '{db_user}'@'switchback.proxy.rlwy.net' IDENTIFIED BY '{db_password}'")
        
        # Création base de données
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        
        # Attribution des droits
        cursor.execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'switchback.proxy.rlwy.net'")
        cursor.execute("FLUSH PRIVILEGES")
        
        print("✅ Configuration réussie!")
        print(f"Utilisateur: {db_user}")
        print(f"Mot de passe: {db_password}")
        print(f"Base de données: {db_name}")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    main()
