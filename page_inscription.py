import flet as ft
import mysql.connector
from mysql.connector import Error
import bcrypt
import time
from db_config import get_db_connection

# Fonction pour récupérer les utilisateurs depuis la base de données
def liste_utilisateur(table_name):
    connection = get_db_connection()
    if not connection:
        return []
        
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Erreur lors de la récupération des données de {table_name}: {e}")
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
        return "N/A"
        
    try:
        cursor = connection.cursor()
        
        if profession == 'Etudiant':
            cursor.execute("SELECT Adresse FROM etudiant WHERE Numero_carte_etu = %s", (user_id,))
        elif profession == 'Enseignant':
            cursor.execute("SELECT Adresse FROM enseignant WHERE Id_ens = %s", (user_id,))
        elif profession == 'Administration':
            cursor.execute("SELECT Adresse FROM administration WHERE Id_adm = %s", (user_id,))
        
        result = cursor.fetchone()
        return result[0] if result and result[0] else "N/A"
    except Error as e:
        print(f"Erreur lors de la récupération de l'adresse: {e}")
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
def page_inscription (page: ft.Page):
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

    # Récupérer les utilisateurs déjà inscrits
    inscrit = liste_utilisateur("utilisateurs")
    nom_inscrit = [normalize_text(str(user[1])) for user in inscrit]
    prenom_inscrit = [normalize_text(str(user[2])) for user in inscrit]

    # Récupérer les listes des étudiants, enseignants et administrateurs
    list_et = liste_utilisateur("etudiant")
    list_ens = liste_utilisateur("enseignant")
    list_admin = liste_utilisateur("administration")

    # Extraire les informations nécessaires et les normaliser
    list_nom_et = [normalize_text(str(et[3])) for et in list_et]
    list_prenom_et = [normalize_text(str(et[4])) for et in list_et]
    list_cart_etudiant = [str(et[1]) for et in list_et]
    list_email_et = [normalize_text(str(et[6])) for et in list_et]
    list_numero_et = [str(et[7]) for et in list_et]

    list_nom_ens = [normalize_text(str(ens[2])) for ens in list_ens]
    list_prenom_ens = [normalize_text(str(ens[3])) for ens in list_ens]
    list_Id_ens = [ens[0] for ens in list_ens]
    list_email_ens = [normalize_text(str(ens[4])) for ens in list_ens]
    list_numero_ens = [str(ens[5]) for ens in list_ens]

    list_nom_admin = [normalize_text(str(admin[1])) for admin in list_admin]
    list_prenom_admin = [normalize_text(str(admin[2])) for admin in list_admin]
    list_Id_adm = [admin[0] for admin in list_admin]
    list_email_admin = [normalize_text(str(admin[3])) for admin in list_admin]
    list_numero_admin = [str(admin[4]) for admin in list_admin]

    # Fonction pour vérifier si l'utilisateur est déjà inscrit
    def inscrits(name, prenom, nom_inscrit, prenom_inscrit):
        return name not in nom_inscrit and prenom not in prenom_inscrit

    # Fonction pour vérifier les informations de l'utilisateur
    def verification(id, name, prenom, numero, email, profession):
        name = normalize_text(name)
        prenom = normalize_text(prenom)
        email = normalize_text(email)
        
        if profession == "Administration":
            if (id in list_Id_adm and name in list_nom_admin and 
                prenom in list_prenom_admin and email in list_email_admin and 
                numero in list_numero_admin):
                return 1
        elif profession == "Enseignant":
            if (id in list_Id_ens and name in list_nom_ens and 
                prenom in list_prenom_ens and email in list_email_ens and 
                numero in list_numero_ens):
                return 2
        elif profession == "Etudiant":
            if (id in list_cart_etudiant and name in list_nom_et and 
                prenom in list_prenom_et and email in list_email_et and 
                numero in list_numero_et):
                return 3
        return 0

    # Fonction pour enregistrer un nouvel utilisateur
    def enregistrer_insrit(name, prenom, numero, profession, mot_passe, email):
        connection = get_db_connection()
        if not connection:
            return False
            
        try:
            cursor = connection.cursor()
            hashed_password = bcrypt.hashpw(mot_passe.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Vérifier si l'utilisateur existe déjà
            check_query = "SELECT * FROM utilisateurs WHERE nom = %s AND prenom = %s"
            cursor.execute(check_query, (name, prenom))
            existing_user = cursor.fetchone()

            if not existing_user:
                # Insérer le nouvel utilisateur
                insert_query = """
                INSERT INTO utilisateurs (nom, prenom, numero, email, profession, mot_passe)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (name, prenom, numero, email, profession, hashed_password))
                connection.commit()
                print("Utilisateur enregistré avec succès.")
                return True
            else:
                print("L'utilisateur existe déjà.")
                return False
                
        except Error as e:
            print(f"Erreur lors de l'enregistrement de l'utilisateur: {e}")
            return False
            
        finally:
            if 'cursor' in locals():
                cursor.close()
            if connection.is_connected():
                connection.close()

    # Fonction pour afficher les messages avec style
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
        
        # Mise à jour des labels en fonction de la profession
        if profession.value == "Administration":
            num_carte.label = "ID Administration"
            num_carte.hint_text = "Entrez votre ID d'administration"
        elif profession.value == "Enseignant":
            num_carte.label = "ID Enseignant"
            num_carte.hint_text = "Entrez votre ID d'enseignant"
        
        page.update()

    # Bouton pour revenir à la page précédente
    def retour(e):
        page.go("/page_connexion")

    # Bouton pour valider le formulaire
    def VALIDER(e):
        # Désactiver le bouton pendant le traitement
        valider.disabled = True
        valider.text = "Inscription..."
        page.update()
        
        id_value = carte.value if profession.value == "Etudiant" else num_carte.value
        if not all([id_value, nom.value, prenom.value, numero.value, email.value, mot_de_passe.value, conf_mot_de_passe.value, profession.value]):
            show_message("⚠ Veuillez remplir tous les champs", "red")
            valider.disabled = False
            valider.text = "VALIDER"
            page.update()
            return

        if mot_de_passe.value != conf_mot_de_passe.value:
            show_message("❌ Les mots de passe ne correspondent pas", "red")
            valider.disabled = False
            valider.text = "VALIDER"
            page.update()
            return

        verification_result = verification(id_value, nom.value, prenom.value, numero.value, email.value, profession.value)

        if verification_result == 0:
            show_message("❌ Échec de l'inscription, veuillez vérifier vos informations", "red")
            valider.disabled = False
            valider.text = "VALIDER"
            page.update()
            return

        if inscrits(nom.value, prenom.value, nom_inscrit, prenom_inscrit):
            enregistrer_insrit(nom.value, prenom.value, numero.value, profession.value, mot_de_passe.value, email.value)
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
            show_message("⚠ Vous êtes déjà inscrit", "red")
        
        # Réactiver le bouton
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

    # Créer une copie du style sans la hauteur pour le Dropdown
    dropdown_style = field_style.copy()
    if 'height' in dropdown_style:
        del dropdown_style['height']
    
    # Composants de l'interface utilisateur avec style amélioré
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
        hint_text="Entrez votre identifiant",
        **field_style
    )

    carte = ft.TextField(
        label="Numéro carte étudiante",
        hint_text="Entrez votre numéro de carte",
        visible=False,
        **field_style
    )

    nom = ft.TextField(
        label="Nom",
        hint_text="Entrez votre nom",
        **field_style
    )

    prenom = ft.TextField(
        label="Prénom",
        hint_text="Entrez votre prénom",
        **field_style
    )

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
        options=[ft.dropdown.Option(str(i)) for i in range(1, 5)] + 
                [ft.dropdown.Option("SI"), ft.dropdown.Option("Mecanique")],
        visible=False,
        **dropdown_style
    )

    numero = ft.TextField(
        label="Numéro de téléphone",
        hint_text="Entrez votre numéro",
        **field_style
    )

    email = ft.TextField(
        label="Adresse email",
        hint_text="Entrez votre email",
        **field_style
    )

    mot_de_passe = ft.TextField(
        label="Mot de passe",
        hint_text="Entrez votre mot de passe",
        password=True,
        can_reveal_password=True,
        **field_style
    )

    conf_mot_de_passe = ft.TextField(
        label="Confirmer le mot de passe",
        hint_text="Confirmez votre mot de passe",
        password=True,
        can_reveal_password=True,
        **field_style
    )

    # Boutons avec style amélioré
    valider = ft.ElevatedButton(
        "VALIDER",
        bgcolor='#90EE90',
        color='black',
        width=160,
        height=45,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD)
        ),
        on_click=VALIDER
    )

    revenir = ft.ElevatedButton(
        "← RETOUR",
        bgcolor='lightblue',
        color='black',
        width=160,
        height=45,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            text_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_500)
        ),
        on_click=retour
    )

    # Container principal avec design amélioré
    registration_container = ft.Container(
        content=ft.Column([
            # En-tête
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.PERSON_ADD, size=50, color='white'),
                    ft.Text(
                        "Inscription",
                        size=26,
                        weight=ft.FontWeight.BOLD,
                        color='white',
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Créez votre compte pour accéder à la plateforme",
                        size=14,
                        color='white',
                        text_align=ft.TextAlign.CENTER
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                margin=ft.margin.only(bottom=25)
            ),
            
            # Zone de saisie - TOUS LES CHAMPS EN VERTICAL
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "⚠ Veuillez choisir votre profession en premier",
                        size=12,
                        color='#ff9800',
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.W_500
                    ),
                    ft.Container(height=10),
                    
                    # Tous les champs disposés verticalement
                    profession,
                    ft.Container(height=8),
                    num_carte,
                    carte,
                    ft.Container(height=8),
                    nom,
                    ft.Container(height=8),
                    prenom,
                    ft.Container(height=8),
                    niveau,
                    groupe_td,
                    ft.Container(height=8),
                    numero,
                    ft.Container(height=8),
                    email,
                    ft.Container(height=8),
                    mot_de_passe,
                    ft.Container(height=8),
                    conf_mot_de_passe,
                    
                    ft.Container(height=20),
                    ft.Row([revenir, valider], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                    ft.Container(height=15),
                    message,
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor='rgba(255, 255, 255, 0.1)',
                border_radius=20,
                padding=25,
                border=ft.border.all(1, 'rgba(255, 255, 255, 0.2)')
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=20,
        expand=True
    )

    # Ajouter le conteneur d'inscription au conteneur défilant
    scroll_container.content.controls = [
        ft.Container(height=20),  # Espacement en haut
        registration_container,
        ft.Container(height=20)   # Espacement en bas
    ]
    
    # Layout final avec défilement
    return [
        ft.Container(
            content=scroll_container,
            expand=True,
            padding=0,
            margin=0,
        )
    ]