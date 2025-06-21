import mysql.connector
from mysql.connector import Error
from db_config import get_db_connection

def create_table_if_not_exists():
    print("3.1. Dans create_table_if_not_exists()")
    connection = None
    cursor = None
    try:
        # Connexion à la base de données
        print("3.2. Tentative de connexion à la base de données...")
        connection = get_db_connection()
        
        if connection and connection.is_connected():
            print("3.3. Connexion à la base de données établie")
            cursor = connection.cursor()
        else:
            print("3.3. Échec de la connexion à la base de données")
            return False
            
            # Créer la table Etudiant
            create_etudiant_query = """
            CREATE TABLE IF NOT EXISTS Etudiant (
                Numero_carte_etu VARCHAR(20) PRIMARY KEY,
                Nom VARCHAR(50) NOT NULL,
                Prenoms VARCHAR(100) NOT NULL,
                IP VARCHAR(20) NOT NULL UNIQUE,
                Adresse VARCHAR(200),
                Email VARCHAR(100),
                Date_inscription DATE NOT NULL,
                INDEX idx_ip (IP)
            )
            """
            cursor.execute(create_etudiant_query)
            
            # Créer la table presence_etu_archive
            create_table_query = """
            CREATE TABLE IF NOT EXISTS presence_etu_archive (
                IP VARCHAR(20) NOT NULL,
                Date_presence DATE NOT NULL,
                Heure_debut TIME NOT NULL,
                Heure_fin TIME NOT NULL,
                PRIMARY KEY (IP, Date_presence),
                FOREIGN KEY (IP) REFERENCES Etudiant(IP)
            )
            """
            cursor.execute(create_table_query)
            
            # Créer la table notification_professeur
            create_notification_table_query = """
            CREATE TABLE IF NOT EXISTS notification_professeur (
                Id_notification INT PRIMARY KEY AUTO_INCREMENT,
                Id_ens VARCHAR(20) NOT NULL,
                IP_etudiant VARCHAR(20) NOT NULL,
                Nom_etudiant VARCHAR(50) NOT NULL,
                Prenoms_etudiant VARCHAR(50),
                Message TEXT NOT NULL,
                Date_notification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                Lu BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (Id_ens) REFERENCES Enseignant(Id_ens),
                FOREIGN KEY (IP_etudiant) REFERENCES Etudiant(IP)
            )
            """
            cursor.execute(create_notification_table_query)
            
            # Créer la table liste_presence
            create_liste_presence_query = """
            CREATE TABLE IF NOT EXISTS liste_presence (
                Id_liste INT PRIMARY KEY AUTO_INCREMENT,
                Id_ens VARCHAR(20) NOT NULL,
                Date_liste DATE NOT NULL,
                Heure_creation TIME NOT NULL,
                Nombre_etudiants INT NOT NULL,
                FOREIGN KEY (Id_ens) REFERENCES Enseignant(Id_ens)
            )
            """
            cursor.execute(create_liste_presence_query)
            
            # Créer la table detail_presence
            create_detail_presence_query = """
            CREATE TABLE IF NOT EXISTS detail_presence (
                Id_liste INT NOT NULL,
                IP_etudiant VARCHAR(20) NOT NULL,
                Heure_arrivee TIME NOT NULL,
                PRIMARY KEY (Id_liste, IP_etudiant),
                FOREIGN KEY (Id_liste) REFERENCES liste_presence(Id_liste),
                FOREIGN KEY (IP_etudiant) REFERENCES Etudiant(IP)
            )
            """
            cursor.execute(create_detail_presence_query)
            
            connection.commit()

    except Error as e:
        print(f"Erreur lors de la création des tables: {e}")
    
    finally:
        if cursor and connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion MySQL fermée")
