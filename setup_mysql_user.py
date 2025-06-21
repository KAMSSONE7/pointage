import mysql.connector
from mysql.connector import Error

def setup_database_user():
    try:
        # Connexion en tant que root (sans mot de passe dans ce cas)
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port=55321,
            user='root',
            password='IowFRbmQYlvxWwLrMLalevEQqhQtWvYN',
            auth_plugin='mysql_native_password'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Paramètres du nouvel utilisateur
            db_name = 'donnee_app'
            db_user = 'app_user'
            db_password = 'MonMotDePasseSecurise123!'  # À changer en production !
            
            print("Création de l'utilisateur et configuration des privilèges...")
            
            # Création de l'utilisateur s'il n'existe pas
            cursor.execute(f"CREATE USER IF NOT EXISTS '{db_user}'@'switchback.proxy.rlwy.net' IDENTIFIED BY '{db_password}'")
            
            # Création de la base de données si elle n'existe pas
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            
            # Attribution des privilèges
            cursor.execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'switchback.proxy.rlwy.net'")
            cursor.execute("FLUSH PRIVILEGES")
            
            # Vérification
            cursor.execute(f"SHOW GRANTS FOR '{db_user}'@'switchback.proxy.rlwy.net'")
            print("\nPrivilèges accordés :")
            for priv in cursor:
                print(f"- {priv[0]}")
            
            print("\n✅ Configuration terminée avec succès !")
            print(f"\nVoici les informations de connexion à utiliser dans db_config.py :")
            print(f"- Utilisateur: {db_user}")
            print(f"- Mot de passe: {db_password}")
            print(f"- Base de données: {db_name}")
            print("\n⚠️  N'oubliez pas de mettre à jour le fichier db_config.py avec ces informations !")
            
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"❌ Erreur lors de la configuration : {e}")
        if "Access denied" in str(e):
            print("\nVeuillez vérifier que vous avez les droits d'administration sur MySQL.")
        elif "using password: YES" in str(e):
            print("\nLe mot de passe root semble incorrect. Veuillez vérifier votre configuration.")

if __name__ == "__main__":
    print("=== Configuration de l'utilisateur MySQL ===\n")
    print("Ce script va :")
    print("1. Créer un nouvel utilisateur 'app_user'")
    print("2. Créer la base de données 'donnee_app' si elle n'existe pas")
    print("3. Accorder tous les privilèges sur cette base au nouvel utilisateur\n")
    
    confirm = input("Voulez-vous continuer ? (o/n): ")
    if confirm.lower() == 'o':
        setup_database_user()
    else:
        print("Opération annulée.")
