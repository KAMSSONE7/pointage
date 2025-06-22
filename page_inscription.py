import flet as ft
from db_config import get_db_connection
import mysql.connector
from mysql.connector import Error
import bcrypt
import time
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Fonction pour récupérer les utilisateurs depuis la base de données
def liste_utilisateur(table_name, id_column):
    connection = get_db_connection()
    if not connection:
        logger.error(f"Connexion échouée pour liste_utilisateur ({table_name})")
        return []
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT {id_column}, Nom, Prenoms, Email, Numero, Adresse FROM {table_name}")
        result = cursor.fetchall()
        logger.debug(f"Données récupérées de {table_name}: {result[:5]}")
        return result
    except Error as e:
        logger.error(f"Erreur lors de la récupération des données de {table_name}: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if connection.is_connected():
            connection.close()

# Fonction pour récupérer l'adresse depuis les tables spécialisées
def get_address_from_specialized_table(profession, user_id):
    connection = get_db_connection()
    if not connection:
        logger.error("Connexion échouée pour get_address_from_specialized_table")
        return "N/A"
    try:
        cursor = connection.cursor()
        if profession == 'Etudiant':
            cursor.execute("SELECT Adresse FROM Etudiant WHERE IP = %s", (user_id,))
        elif profession == 'Enseignant':
            cursor.execute("SELECT Adresse FROM Enseignant WHERE Id_ens = %s", (user_id,))
        elif profession == 'Administration':
            cursor.execute("SELECT Adresse FROM Administration WHERE Id_adm = %s", (user_id,))
        result = cursor.fetchone()
        return result[0] if result and result[0] else "N/A"
    except Error as e:
        logger.error(f"Erreur lors de la récupération de l'adresse: {e}")
        return "N/A"
    finally:
        if 'cursor' in locals():
            cursor.close()
        if connection.is_connected():
            connection.close()

# Fonction pour normaliser une chaîne
def normalize_text(text):
    if text:
        return text.lower().strip()
    return text

# Fonction principale pour la page d'inscription
def page_inscription(page: ft.Page):
    page.title = "PAGE D'INSCRIPTION"
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    page.padding = 20
    
    # Conteneur principal avec défilement
    scroll_container = ft.Container(
        expand=True,
        content=ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        ),
    )

    # Message pour afficher les erreurs ou les succès
    message = ft.Text("", size=16, weight='bold', text_align=ft.TextAlign.CENTER)

    # Récupérer les utilisateurs déjà inscrits dans utilisateurs
    inscrit = liste_utilisateur("utilisateurs", "id")
    nom_inscrit = [normalize_text(str(user[1])) for user in inscrit if len(user) > 1]
    prenom_inscrit = [normalize_text(str(user[2])) for user in inscrit if len(user) > 2]

    # Récupérer les listes des étudiants, enseignants et administrateurs
    list_et = liste_utilisateur("Etudiant", "IP")
    list_ens = liste_utilisateur("Enseignant", "Id_ens")
    list_admin = liste_utilisateur("Administration", "Id_adm")

    # Extraire les informations nécessaires et les normaliser
    list_ip_et = [str(et[0]) for et in list_et if len(et) > 0]  # IP
    list_nom_et = [normalize_text(str(et[1])) for et in list_et if len(et) > 1]
    list_prenom_et = [normalize_text(str(et[2])) for et in list_et if len(et) > 2]
    list_email_et = [normalize_text(str(et[3])) for et in list_et if len(et) > 3]
    list_numero_et = [str(et[4]) for et in list_et if len(et) > 4]

    list_id_ens = [str(ens[0]) for ens in list_ens if len(ens) > 0]  # Id_ens
    list_nom_ens = [normalize_text(str(ens[2])) for ens in list_ens if len(ens) > 2]
    list_prenom_ens = [normalize_text(str(ens[3])) for ens in list_ens if len(ens) > 3]
    list_email_ens = [normalize_text(str(ens[4])) for ens in list_ens if len(ens) > 4]
    list_numero_ens = [str(ens[5]) for ens in list_ens if len(ens) > 5]

    list_id_adm = [str(admin[0]) for admin in list_admin if len(admin) > 0]  # Id_adm
    list_nom_admin = [normalize_text(str(admin[1])) for admin in list_admin if len(admin) > 1]
    list_prenom_admin = [normalize_text(str(admin[2])) for admin in list_admin if len(admin) > 2]
    list_email_admin = [normalize_text(str(admin[3])) for admin in list_admin if len(admin) > 3]
    list_numero_admin = [str(admin[4]) for admin in list_admin if len(admin) > 4]

    # Fonction pour vérifier si l'utilisateur est déjà inscrit
    def inscrits(name, prenom, nom_inscrit, prenom_inscrit):
        return name not in nom_inscrit and prenom not in prenom_inscrit

    # Fonction pour vérifier les informations de l'utilisateur
    def verification(id, name, prenom, numero, email, profession):
        name = normalize_text(name)
        prenom = normalize_text(prenom)
        email = normalize_text(email)
        logger.debug(f"Vérification - ID: {id}, Name: {name}, Prenom: {prenom}, Numero: {numero}, Email: {email}, Profession: {profession}")
        logger.debug(f"Listes - Admin: {list_id_adm[:5]}, {list_nom_admin[:5]}, Etudiant: {list_ip_et[:5]}, {list_nom_et[:5]}")
        
        if profession == "Administration":
            if (id in list_id_adm and name in list_nom_admin and 
                prenom in list_prenom_admin and email in list_email_admin and 
                numero in list_numero_admin):
                logger.debug("Validation Administration réussie")
                return 1
        elif profession == "Enseignant":
            if (id in list_id_ens and name in list_nom_ens and 
                prenom in list_prenom_ens and email in list_email_ens and 
                numero in list_numero_ens):
                logger.debug("Validation Enseignant réussie")
                return 2
        elif profession == "Etudiant":
            if (id in list_ip_et and name in list_nom_et and 
                prenom in list_prenom_et and email in list_email_et and 
                numero in list_numero_et):
                logger.debug("Validation Etudiant réussie")
                return 3
        logger.debug("Validation échouée - Aucune correspondance trouvée")
        return 0

    # Fonction pour enregistrer un nouvel utilisateur
    def enregistrer_insrit(name, prenom, numero, profession, mot_passe, email):
        connection = get_db_connection()
        if not connection:
            logger.error("Connexion échouée pour enregistrer_insrit")
            return False
        try:
            cursor = connection.cursor()
            hashed_password = bcrypt.hashpw(mot_passe.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            check_query = "SELECT * FROM utilisateurs WHERE email = %s"
            cursor.execute(check_query, (email,))
            existing_user = cursor.fetchone()

            if not existing_user:
                insert_query = """
                INSERT INTO utilisateurs (nom, prenom, numero, email, profession, mot_passe)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (name, prenom, numero, email, profession, hashed_password))
                connection.commit()
                logger.info(f"Utilisateur {name} {prenom} enregistré avec succès.")
                return True
            else:
                logger.warning(f"Utilisateur avec email {email} existe déjà.")
                return False
        except Error as e:
            logger.error(f"Erreur lors de l'enregistrement: {e}")
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()
            if connection.is_connected():
                connection.close()

    # Fonction pour afficher les messages
    def show_message(text, color, is_success=False):
        message.value = text
        message.color = color
        page.update()
        if is_success:
            time.sleep(1.5)

    # Gestion du changement de profession
    def on_profession_change(e):
        is_student = profession.value == "Etudiant"
        niveau.visible = is_student
        groupe_td.visible = is_student
        carte.visible = is_student
        num_carte.visible = not is_student
        
        if profession.value == "Administration":
            num_carte.label = "ID Administration"
            num_carte.hint_text = "Entrez votre ID (ex: ADM001)"
        elif profession.value == "Enseignant":
            num_carte.label = "ID Enseignant"
            num_carte.hint_text = "Entrez votre ID (ex: ENS001)"
        page.update()

    # Bouton pour revenir
    def retour(e):
        page.go("/page_connexion")

    # Bouton pour valider
    def VALIDER(e):
        valider.disabled = True
        valider.text = "Inscription..."
        page.update()
        
        id_value = carte.value if profession.value == "Etudiant" else num_carte.value
        if not all([id_value, nom.value, prenom.value, numero.value, email.value, mot_de_passe.value, conf_mot_de_passe.value, profession.value]):
            show_message("⚠ Veuillez remplir tous les champs", "red")
        elif mot_de_passe.value != conf_mot_de_passe.value:
            show_message("❌ Les mots de passe ne correspondent pas", "red")
        else:
            verification_result = verification(id_value, nom.value, prenom.value, numero.value, email.value, profession.value)
            if verification_result == 0:
                show_message(f"❌ Échec de l'inscription. Vérifiez : ID={id_value}, Name={nom.value}, Email={email.value}", "red")
            elif inscrits(nom.value, prenom.value, nom_inscrit, prenom_inscrit):
                if enregistrer_insrit(nom.value, prenom.value, numero.value, profession.value, mot_de_passe.value, email.value):
                    adresse = get_address_from_specialized_table(profession.value, id_value)
                    page.session.set("user", {
                        "nom": nom.value,
                        "prenom": prenom.value,
                        "email": email.value,
                        "profession": profession.value,
                        "numero": numero.value,
                        "adresse": adresse
                    })
                    show_message(f"✅ Inscription réussie ! Bienvenue {nom.value}", "green", True)
                    if profession.value == 'Etudiant':
                        page.go('/page_etu_acc')
                    elif profession.value == 'Enseignant':
                        page.go('/page_accueil')
                    elif profession.value == 'Administration':
                        page.go('/page_admins')
                else:
                    show_message("⚠ Erreur lors de l'enregistrement", "red")
            else:
                show_message("⚠ Vous êtes déjà inscrit", "red")
        
        valider.disabled = False
        valider.text = "VALIDER"
        page.update()

    # Style commun pour les champs
    field_style = {
        "width": 350,
        "height": 55,
        "border_radius": 12,
        "border_color": '#e0e0e0',
        "focused_border_color": 'white',
        "bgcolor": "white12",
        "color": 'black',
        "text_size": 14,
        "label_style": ft.TextStyle(color='black', size=15),
        "content_padding": ft.padding.symmetric(horizontal=15, vertical=12)
    }

    # Style pour Dropdown
    dropdown_style = field_style.copy()
    if 'height' in dropdown_style:
        del dropdown_style['height']
    
    # Composants de l'interface
    profession = ft.Dropdown(
        label="Profession",
        hint_text="Sélectionnez votre profession",
        options=[
            ft.dropdown.Option("Administration"),
            ft.dropdown.Option("Enseignant"),
            ft.dropdown.Option("Etudiant")
        ],
        on_change=on_profession_change,
        **dropdown_style
    )

    num_carte = ft.TextField(
        label="ID (Enseignant/Administration)",
        hint_text="Entrez votre ID (ex: ADM001 ou ENS001)",
        **field_style
    )

    carte = ft.TextField(
        label="IP ou Numéro carte étudiante",
        hint_text="Entrez votre IP (ex: YEOH0612860001) ou carte",
        visible=False,
        **field_style
    )

    nom = ft.TextField(label="Nom", hint_text="Entrez votre nom", **field_style)
    prenom = ft.TextField(label="Prénom", hint_text="Entrez votre prénom", **field_style)
    niveau = ft.Dropdown(
        label="Niveau d'études",
        hint_text="Sélectionnez votre niveau",
        options=[ft.dropdown.Option(f"Licence {i}") for i in range(1, 4)] + 
                [ft.dropdown.Option(f"Master {i}") for i in range(1, 3)],
        visible=False,
        **dropdown_style
    )

    groupe_td = ft.Dropdown(
        label="Groupe de TD",
        hint_text="Sélectionnez votre groupe",
        options=[ft.dropdown.Option(str(i)) for i in range(1, 6)] + 
                [ft.dropdown.Option("SI"), ft.dropdown.Option("Mecanique")],
        visible=False,
        **dropdown_style
    )

    numero = ft.TextField(label="Numéro de téléphone", hint_text="Entrez votre numéro", **field_style)
    email = ft.TextField(label="Adresse email", hint_text="Entrez votre email", **field_style)
    mot_de_passe = ft.TextField(
        label="Mot de passe", hint_text="Entrez votre mot de passe", password=True, can_reveal_password=True, **field_style
    )
    conf_mot_de_passe = ft.TextField(
        label="Confirmer le mot de passe", hint_text="Confirmez votre mot de passe", password=True, can_reveal_password=True, **field_style
    )

    # Boutons
    valider = ft.ElevatedButton(
        "VALIDER", bgcolor='#90EE90', color='black', width=160, height=45,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12), text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD)),
        on_click=VALIDER
    )

    revenir = ft.ElevatedButton(
        "← RETOUR", bgcolor='lightblue', color='black', width=160, height=45,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12), text_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_500)),
        on_click=retour
    )

    # Conteneur d'inscription
    registration_container = ft.Container(
        content=ft.Column([
            ft.Container(content=ft.Column([
                ft.Icon(ft.Icons.PERSON_ADD, size=50, color='white'),
                ft.Text("Inscription", size=26, weight=ft.FontWeight.BOLD, color='white', text_align=ft.TextAlign.CENTER),
                ft.Text("Créez votre compte pour accéder à la plateforme", size=14, color='white', text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER), margin=ft.margin.only(bottom=25)),
            ft.Container(content=ft.Column([
                ft.Text("⚠ Veuillez choisir votre profession en premier", size=12, color='#ff9800', text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.W_500),
                ft.Container(height=10),
                profession, ft.Container(height=8),
                num_carte, carte, ft.Container(height=8),
                nom, ft.Container(height=8),
                prenom, ft.Container(height=8),
                niveau, groupe_td, ft.Container(height=8),
                numero, ft.Container(height=8),
                email, ft.Container(height=8),
                mot_de_passe, ft.Container(height=8),
                conf_mot_de_passe, ft.Container(height=20),
                ft.Row([revenir, valider], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                ft.Container(height=15),
                message,
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER), bgcolor='rgba(255, 255, 255, 0.1)', border_radius=20, padding=25, border=ft.border.all(1, 'rgba(255, 255, 255, 0.2)'))
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=20,
        expand=True
    )

    # Ajouter au conteneur défilant
    scroll_container.content.controls = [ft.Container(height=20), registration_container, ft.Container(height=20)]
    return [ft.Container(content=scroll_container, expand=True, padding=0, margin=0)]

# Assure-toi que db_config.py est configuré comme suggéré précédemment