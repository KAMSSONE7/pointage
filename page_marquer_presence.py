import flet as ft
from db_config import DB_CONFIG
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import logging
import sys

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

def get_db_connection():
    """Établit une connexion à la base de données MySQL"""
    try:
        connection = mysql.connector.connect(
            host='switchback.proxy.rlwy.net',
            database='donnee_app',
            user='root',
            password='IowFRbmQYlvxWwLrMLalevEQqhQtWvYN',  # Mot de passe vide
            port=55321,
            connection_timeout=5
        )
        if connection.is_connected():
            logger.info("Connexion à la base de données réussie")
            return connection
    except Error as e:
        logger.error(f"Erreur de connexion à la base de données: {e}")
        return None
    except Exception as e:
        logger.error(f"Erreur inattendue lors de la connexion: {e}")
        return None

def page_marquer_presence(page: ft.Page, etudiant_connecte):
    """Affiche la page de marquage de présence"""
    
    # Création des contrôles d'interface utilisateur
    t = ft.Text()
    checkbox = ft.Checkbox(
        label="Marquer ma présence",
        value=False,
        disabled=True  # Désactivé par défaut jusqu'à la vérification
    )
    
    def on_checkbox_changed(e):
        """Gère le changement d'état de la case à cocher"""
        if not checkbox.value:  # Si on décoche, on ne fait rien
            return
            
        connection = None
        cursor = None
        try:
            # Connexion à la base de données
            connection = get_db_connection()
            if not connection:
                raise Exception("Impossible de se connecter à la base de données")

            cursor = connection.cursor(dictionary=True)
            numero_etudiant = etudiant_connecte.get('numero')
            
            # Vérification du numéro d'étudiant
            if not numero_etudiant:
                raise ValueError("Numéro d'étudiant non trouvé dans la session")

            # Récupération des informations de l'étudiant
            cursor.execute("SELECT IP, Id_gpe_td FROM Etudiant WHERE Numero = %s", (numero_etudiant,))
            etudiant = cursor.fetchone()
            
            if not etudiant:
                raise ValueError(f"Aucun étudiant trouvé avec le numéro {numero_etudiant}")

            ip_etudiant = etudiant.get('IP')
            if not ip_etudiant:
                raise ValueError("Aucune adresse IP trouvée pour cet étudiant")

            # Récupération de la date et de l'heure actuelles
            maintenant = datetime.now()
            date_aujourdhui = maintenant.date()
            heure_actuelle = maintenant.time().strftime('%H:%M:%S')

            # Vérification des cours du jour avec enseignant présent
            query = """
                SELECT 
                    e.Id_cours, e.Id_salle, c.Libelle, 
                    e.heure_deb, e.heure_fin, p.Id_pres, 
                    p.Id_ens, p.Heure_debut, p.Heure_fin, 
                    ens.Nom, ens.Prenoms
                FROM Emploi_du_temps e
                JOIN Cours c ON e.Id_cours = c.Id_cours
                JOIN Enseignant ens ON ens.Id_cours = c.Id_cours
                LEFT JOIN Presence_ens p ON p.Id_ens = ens.Id_ens 
                    AND DATE(p.Date_presence) = %s
                    AND p.Id_Salle = e.Id_salle
                WHERE e.Date_cours = %s
                    AND p.Id_pres IS NOT NULL
                LIMIT 1
            """
            
            cursor.execute(query, (date_aujourdhui, date_aujourdhui))
            cours = cursor.fetchone()
            
            if not cours:
                raise Exception("Aucun cours avec enseignant présent n'est prévu aujourd'hui")

            # Vérification si l'étudiant a déjà marqué sa présence
            cursor.execute("""
                SELECT 1 
                FROM Presence_etu 
                WHERE IP = %s 
                AND DATE(Date_presence) = %s
                LIMIT 1
            """, (ip_etudiant, date_aujourdhui))
            
            if cursor.fetchone():
                raise Exception("Vous avez déjà marqué votre présence pour aujourd'hui")

            # Enregistrement de la présence
            cursor.execute("""
                INSERT INTO Presence_etu (IP, Date_presence, Heure_debut, Heure_fin)
                VALUES (%s, %s, %s, %s)
            """, (ip_etudiant, date_aujourdhui, heure_actuelle, cours['Heure_fin']))
            
            connection.commit()
            t.value = f"Présence enregistrée pour le cours de {cours['Libelle']} !"
            t.color = "green"
            t.weight = ft.FontWeight.BOLD
            checkbox.disabled = True

        except Exception as e:
            t.value = f"Erreur : {str(e)}"
            t.color = "red"
            t.weight = ft.FontWeight.BOLD
            logger.error(f"Erreur lors du marquage de présence : {e}", exc_info=True)
            checkbox.value = False  # Décocher en cas d'erreur
            
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
            page.update()
    
    # Assigner le gestionnaire d'événements
    checkbox.on_change = on_checkbox_changed
    
    # Fonction d'initialisation
    def initialize():
        connection = None
        cursor = None
        try:
            # Connexion à la base de données
            connection = get_db_connection()
            if not connection:
                raise Exception("Impossible de se connecter à la base de données")

            cursor = connection.cursor(dictionary=True)
            numero_etudiant = etudiant_connecte.get('numero')
            
            # Vérification du numéro d'étudiant
            if not numero_etudiant:
                raise ValueError("Numéro d'étudiant non trouvé dans la session")

            # Récupération des informations de l'étudiant
            cursor.execute("SELECT IP, Id_gpe_td FROM Etudiant WHERE Numero = %s", (numero_etudiant,))
            etudiant = cursor.fetchone()
            
            if not etudiant:
                raise ValueError(f"Aucun étudiant trouvé avec le numéro {numero_etudiant}")

            ip_etudiant = etudiant.get('IP')
            if not ip_etudiant:
                raise ValueError("Aucune adresse IP trouvée pour cet étudiant")


            # Vérification si l'étudiant a déjà marqué sa présence aujourd'hui
            date_aujourdhui = datetime.now().date()
            cursor.execute("""
                SELECT 1 
                FROM Presence_etu 
                WHERE IP = %s 
                AND DATE(Date_presence) = %s
                LIMIT 1
            """, (ip_etudiant, date_aujourdhui))
            
            if cursor.fetchone():
                t.value = "Vous avez déjà marqué votre présence aujourd'hui"
                t.color = "orange"
                t.weight = ft.FontWeight.BOLD
                checkbox.disabled = True
            else:
                # Vérification s'il y a un cours aujourd'hui
                query = """
                    SELECT 1 
                    FROM Emploi_du_temps e
                    JOIN Cours c ON e.Id_cours = c.Id_cours
                    JOIN Enseignant ens ON ens.Id_cours = c.Id_cours
                    LEFT JOIN Presence_ens p ON p.Id_ens = ens.Id_ens 
                        AND DATE(p.Date_presence) = %s
                        AND p.Id_Salle = e.Id_salle
                    WHERE e.Date_cours = %s
                        AND p.Id_pres IS NOT NULL
                    LIMIT 1
                """
                cursor.execute(query, (date_aujourdhui, date_aujourdhui))
                
                if cursor.fetchone():
                    t.value = "Cochez la case pour marquer votre présence"
                    t.color = "blue"
                    t.weight = ft.FontWeight.BOLD
                    checkbox.disabled = False
                else:
                    t.value = "Aucun cours avec enseignant présent n'est prévu aujourd'hui"
                    t.color = "orange"
                    t.weight = ft.FontWeight.BOLD
                    checkbox.disabled = True

        except Exception as e:
            t.value = f"Erreur : {str(e)}"
            t.color = "red"
            t.weight = ft.FontWeight.BOLD
            checkbox.disabled = True
            logger.error(f"Erreur lors de l'initialisation : {e}", exc_info=True)
            
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
            page.update()
    
    # Appeler l'initialisation
    initialize()

    # Retourner l'interface utilisateur
    return [
        ft.Row(
            controls=[
                ft.IconButton(
                    icon="arrow_back",
                    icon_color="white",
                    on_click=lambda _: page.go('/page_etu_acc')
                ),
                ft.Text(
                    value="MARQUER MA PRÉSENCE",
                    color="white",
                    weight=ft.FontWeight.BOLD,
                    size=18,
                    expand=True,
                    text_align=ft.TextAlign.CENTER
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        ft.Container(
            content=ft.Column(
                controls=[
                    checkbox,
                    t
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            margin=ft.margin.only(top=40),
            alignment=ft.alignment.center
        )
    ]