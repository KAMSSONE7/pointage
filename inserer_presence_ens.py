import mysql.connector
from datetime import datetime, timedelta

def inserer_presence_enseignant():
    try:
        connection = mysql.connector.connect(
            host='switchback.proxy.rlwy.net',
            database='donnee_app',
            user='root',
            password=' ',
            port='55321'
        )
        
        if not connection.is_connected():
            raise Exception("Impossible de se connecter à la base de données")
        
        cursor = connection.cursor()
        
        # Date d'aujourd'hui
        aujourdhui = datetime.now().date()
        heure_actuelle = datetime.now().time()
        heure_fin = (datetime.now() + timedelta(hours=2)).time()  # 2 heures plus tard
        
        # Insérer une présence pour un enseignant (par exemple, ENS004)
        cursor.execute(
            """
            INSERT INTO Presence_ens (Id_ens, Id_Salle, Date_presence, Heure_debut, Heure_fin)
            VALUES (%s, %s, %s, %s, %s)
            """,
            ('ENS004', 1, aujourdhui, heure_actuelle, heure_fin)
        )
        
        connection.commit()
        print(f"Présence de l'enseignant ENS004 enregistrée pour aujourd'hui à {heure_actuelle}")
        
    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")

if __name__ == "__main__":
    inserer_presence_enseignant()
