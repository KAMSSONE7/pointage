import flet as ft
from db_config import DB_CONFIG
import mysql.connector
from mysql.connector import Error
import bcrypt
from fonction import *
import time
from db_config import get_db_connection as create_connection

# Fonction pour récupérer l'adresse depuis les tables spécialisées
def get_address_from_specialized_table(profession, user_id):
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            
            if profession == 'Etudiant':
                cursor.execute("SELECT adresse FROM etudiant WHERE Numero_carte_etu = %s", (user_id,))
            elif profession == 'Enseignant':
                cursor.execute("SELECT adresse FROM enseignant WHERE Id_ens = %s", (user_id,))
            elif profession == 'Administration':
                cursor.execute("SELECT adresse FROM administration WHERE Id_adm = %s", (user_id,))
            
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            
            return result[0] if result and result[0] else "N/A"
    except Error as e:
        print(f"Erreur lors de la récupération de l'adresse: {e}")
    return "N/A"

# Page de connexion
def page_connexion(page: ft.Page):
    page.title = "PAGE DE CONNEXION"
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    page.padding = 20
    page.auto_scroll = True

    # Conteneur principal avec défilement
    main_container = ft.Container(
        expand=True,
        content=ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )
    
    # Message pour afficher les erreurs ou les succès
    message = ft.Text("", size=16, weight='bold', text_align=ft.TextAlign.CENTER)

    # Navigation vers les autres pages
    def s_inscrire(e):
        page.go("/page_inscription")

    def oublier(e):
        page.go('/page_recup_mot_passe')

    # Récupérer les utilisateurs depuis la table utilisateurs
    def get_users():
        try:
            connection = create_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT nom, prenom, numero, email, profession, mot_passe FROM utilisateurs")
                result = cursor.fetchall()
                cursor.close()
                connection.close()
                return result
            return []
        except Error as e:
            print(f"Erreur lors de la récupération des utilisateurs: {e}")
            return []

    list_users = get_users()
    list_numero = [str(user[2]) for user in list_users]
    list_mot_passe = [user[5] for user in list_users]  # Hashed passwords
    list_profession = [str(user[4]) for user in list_users]
    list_nomComplet = [f"{user[0]} {user[1]}" for user in list_users]
    list_email = [str(user[3]) for user in list_users]
    list_user_id = [user[6] if len(user) > 6 else None for user in list_users]  # ID spécialisé

    # Vérification des identifiants
    def identite(numero, mot_passe):
        if numero in list_numero:
            index = list_numero.index(numero)
            # Vérifier le mot de passe haché
            stored_password = list_mot_passe[index].encode('utf-8')
            if bcrypt.checkpw(mot_passe.encode('utf-8'), stored_password):
                return index
        return None

    # Fonction pour afficher les messages avec animation
    def show_message(text, color, is_success=False):
        message.value = text
        message.color = color
        page.update()
        if is_success:
            time.sleep(1.5)

    # Gestion de la connexion
    def connexion(e):
        # Désactiver le bouton pendant le traitement
        btn_connexion.disabled = True
        btn_connexion.text = "Connexion..."
        page.update()
        
        num = numero.value.strip()
        mdp = mot_de_passe.value.strip()
        adresse = "N/A"
        ip = "N/A"
        
        if not num or not mdp:
            show_message("⚠ Veuillez remplir tous les champs.", "red")
        else:
            index = identite(num, mdp)
            if index is not None:
                # Récupérer l'adresse et l'IP depuis la table spécialisée
                user_profession = list_profession[index]
                user_id = list_user_id[index] if list_user_id[index] else num
                try:
                    connection = create_connection()
                    if not connection or not connection.is_connected():
                        show_message("❌ Erreur de connexion à la base de données", "red")
                        return
                        
                    cursor = connection.cursor()
                    
                    if user_profession == 'Etudiant':
                        # D'abord, essayer de trouver par Numero_carte_etu
                        cursor.execute("SELECT Adresse, IP, Numero FROM etudiant WHERE Numero_carte_etu = %s OR Numero = %s LIMIT 1", (user_id, user_id))
                        result = cursor.fetchone()
                        if result:
                            adresse = result[0] if result[0] else "N/A"
                            ip = result[1] if result[1] else "N/A"
                            # Mettre à jour le numéro de carte si nécessaire
                            if not result[2] or result[2] != user_id:
                                cursor.execute("UPDATE etudiant SET Numero = %s WHERE IP = %s", (user_id, ip))
                                connection.commit()
                        else:
                            # Si aucun étudiant n'est trouvé, essayer de trouver par IP
                            cursor.execute("SELECT Adresse, IP, Numero FROM etudiant WHERE IP = %s LIMIT 1", (user_id,))
                            result = cursor.fetchone()
                            if result:
                                adresse = result[0] if result[0] else "N/A"
                                ip = result[1] if result[1] else "N/A"
                                # Mettre à jour le numéro de carte si nécessaire
                                if not result[2] or result[2] != user_id:
                                    cursor.execute("UPDATE etudiant SET Numero = %s WHERE IP = %s", (user_id, ip))
                                    connection.commit()
                            else:
                                adresse = "N/A"
                                ip = "N/A"
                    elif user_profession == 'Enseignant':
                        cursor.execute("SELECT Id_ens, adresse FROM enseignant WHERE Id_ens = %s", (user_id,))
                        result = cursor.fetchone()
                        if result:
                            user_id = result[0]
                            adresse = result[1] if result[1] else "N/A"
                        else:
                            cursor.execute("SELECT Id_ens, adresse FROM enseignant WHERE Numero = %s", (num,))
                            result = cursor.fetchone()
                            if result:
                                user_id = result[0]
                                adresse = result[1] if result[1] else "N/A"
                            else:
                                adresse = "N/A"
                    elif user_profession == 'Administration':
                        cursor.execute("SELECT adresse, Id_adm FROM administration WHERE Id_adm = %s", (user_id,))
                        result = cursor.fetchone()
                        if result:
                            adresse = result[0] if result[0] else "N/A"
                        else:
                            adresse = "N/A"
                    
                    cursor.close()
                    connection.close()
                        
                except Error as e:
                    print(f"Erreur lors de la récupération des données: {e}")
                    adresse = "N/A"
                    ip = "N/A"
                
                # Stocker toutes les informations de l'utilisateur dans la session
                user_data = {
                    "nom": list_users[index][0],
                    "prenom": list_users[index][1],
                    "email": list_users[index][3],
                    "profession": list_users[index][4],
                    "numero": list_users[index][2],
                    "adresse": adresse,
                    "IP": ip,
                    "id": user_id
                }
                page.session.set("user", user_data)
                
                show_message(f"✅ Connexion réussie ! Bienvenue {list_users[index][0]}", "green", True)
                
                # Redirection selon le profil
                if list_profession[index] == 'Etudiant':
                    page.go('/page_etu_acc')
                elif list_profession[index] == 'Enseignant':
                    page.go('/page_accueil')
                elif list_profession[index] == 'Administration':
                    page.go('/page_admins')
            else:
                show_message("❌ Numéro ou mot de passe incorrect.", "red")
        
        # Réactiver le bouton
        btn_connexion.disabled = False
        btn_connexion.text = "SE CONNECTER"
        page.update()

    # Champs de saisie avec style amélioré
    numero = ft.TextField(
        label="Numéro d'identification",
        hint_text="Entrez votre numéro",
        border_radius=15,
        border_color='#e0e0e0',
        focused_border_color='#90EE90',
        bgcolor="white",
        width=350,
        height=60,
        color='black',
        text_size=16,
        label_style=ft.TextStyle(color='#666666', size=14),
        content_padding=ft.padding.symmetric(horizontal=20, vertical=15)
    )
    
    mot_de_passe = ft.TextField(
        label="Mot de passe",
        hint_text="Entrez votre mot de passe",
        password=True,
        border_radius=15,
        border_color='#e0e0e0',
        focused_border_color='#90EE90',
        can_reveal_password=True,
        bgcolor='white',
        width=350,
        height=60,
        color='black',
        text_size=16,
        label_style=ft.TextStyle(color='#666666', size=14),
        content_padding=ft.padding.symmetric(horizontal=20, vertical=15)
    )

    # Boutons avec style amélioré
    btn_connexion = ft.ElevatedButton(
        "SE CONNECTER",
        bgcolor='#90EE90',
        color='black',
        width=350,
        height=50,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=15),
            text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
        ),
        on_click=connexion
    )
    
    btn_inscrire = ft.ElevatedButton(
        "CRÉER UN COMPTE",
        bgcolor='lightblue',
        color='black',
        width=350,
        height=45,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=15),
            text_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_500)
        ),
        on_click=s_inscrire
    )
    
    btn_oublier = ft.TextButton(
        "Mot de passe oublié ?",
        style=ft.ButtonStyle(
            color='white',
            text_style=ft.TextStyle(size=14)
        ),
        on_click=oublier
    )
    
    btn_retour = ft.ElevatedButton(
        "← RETOUR",
        bgcolor='white',
        color='black',
        width=120,
        height=40,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            text_style=ft.TextStyle(size=14)
        ),
        on_click=lambda _: page.go("/page_bienvenue")
    )

    # Container principal avec design amélioré
    login_container = ft.Container(
        content=ft.Column([
            # En-tête
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.PERSON, size=60, color='white'),
                    ft.Text(
                        "Connexion",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color='white',
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Connectez-vous pour accéder à votre compte",
                        size=16,
                        color='white',
                        text_align=ft.TextAlign.CENTER
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                margin=ft.margin.only(bottom=30)
            ),
            
            # Zone de saisie
            ft.Container(
                content=ft.Column([
                    numero,
                    ft.Container(height=15),  # Espacement
                    mot_de_passe,
                    ft.Container(height=25),  # Espacement
                    btn_connexion,
                    ft.Container(height=15),  # Espacement
                    btn_inscrire,
                    ft.Container(height=10),  # Espacement
                    btn_oublier,
                    ft.Container(height=20),  # Espacement
                    message,
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor='rgba(255, 255, 255, 0.1)',
                border_radius=20,
                padding=30,
                border=ft.border.all(1, 'rgba(255, 255, 255, 0.2)')
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=20,
        expand=True
    )

    # Ajouter le conteneur de connexion au conteneur principal
    main_container.content.controls = [
        ft.Container(height=20),  # Espacement en haut
        login_container,
        ft.Container(height=20)   # Espacement en bas
    ]
    
    # Layout final avec bouton retour en haut à gauche
    stack = ft.Stack([
        main_container,
        ft.Container(
            content=btn_retour,
            top=20,
            left=20,
            padding=ft.padding.only(left=10, top=10)
        )
    ], expand=True)
    
    # Retourner une liste contenant le Stack avec défilement
    return [
        ft.Container(
            content=stack,
            expand=True,
            padding=0,
            margin=0,
        )
    ]