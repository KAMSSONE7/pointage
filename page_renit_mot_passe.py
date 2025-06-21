import flet as ft
from db_config import DB_CONFIG
import mysql.connector
from mysql.connector import Error
import bcrypt
import time

from db_config import get_db_connection

# Configuration de la base de données
db_config = {
    'host': 'switchback.proxy.rlwy.net',
    'database': 'donnee_app',
    'user': 'root',
    'password': 'IowFRbmQYlvxWwLrMLalevEQqhQtWvYN',
    'port': 55321,
    'charset': 'utf8mb4'
}

# Fonction pour créer les colonnes si elles n'existent pas
def create_columns_if_not_exist():
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Vérifier et ajouter la colonne 'mot_de_passe' si elle n'existe pas
        cursor.execute("SHOW COLUMNS FROM utilisateurs LIKE 'mot_de_passe'")
        result = cursor.fetchone()
        if not result:
            cursor.execute("ALTER TABLE utilisateurs ADD COLUMN mot_de_passe VARCHAR(255)")
            print("Colonne 'mot_de_passe' ajoutée à la table 'utilisateurs'.")

        # Vérifier et ajouter la colonne 'recovery_code' si elle n'existe pas
        cursor.execute("SHOW COLUMNS FROM utilisateurs LIKE 'recovery_code'")
        result = cursor.fetchone()
        if not result:
            cursor.execute("ALTER TABLE utilisateurs ADD COLUMN recovery_code VARCHAR(6)")
            print("Colonne 'recovery_code' ajoutée à la table 'utilisateurs'.")

        connection.commit()
    except Error as e:
        print(f"Erreur lors de la modification de la table : {e}")
    finally:
        try:
            if cursor is not None:
                cursor.close()
            if connection is not None and hasattr(connection, 'is_connected') and connection.is_connected():
                connection.close()
        except Exception as e:
            print(f"Erreur lors de la fermeture des ressources : {e}")

# Appeler la fonction pour créer les colonnes si elles n'existent pas
try:
    create_columns_if_not_exist()
except Exception as e:
    print(f"Erreur lors de l'exécution de create_columns_if_not_exist: {e}")

# Fonction pour réinitialiser le mot de passe dans la base de données
def reset_password(email, entered_code, new_password):
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        # Vérifier le code de récupération
        cursor.execute("SELECT recovery_code FROM utilisateurs WHERE email = %s", (email,))
        result = cursor.fetchone()
        
        if not result or not result[0]:
            return False, "Aucun code de récupération trouvé pour cet email."
            
        stored_code = result[0]
        
        if stored_code != entered_code:
            return False, "Code de récupération invalide."
            
        # Mettre à jour le mot de passe
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute(
            "UPDATE utilisateurs SET mot_passe = %s, recovery_code = NULL WHERE email = %s",
            (hashed_password, email)
        )
        connection.commit()
        return True, "Mot de passe réinitialisé avec succès."
        
    except Error as e:
        return False, f"Erreur lors de la réinitialisation du mot de passe : {e}"
    finally:
        try:
            if cursor is not None:
                cursor.close()
            if connection is not None and hasattr(connection, 'is_connected') and connection.is_connected():
                connection.close()
        except Exception as e:
            print(f"Erreur lors de la fermeture des ressources : {e}")

# Fonction pour afficher les messages avec style
def show_message(message, text, color, page, is_success=False):
    message.value = text
    message.color = color
    page.update()
    if is_success:
        time.sleep(1.5)

# Page de confirmation de mot de passe
def page_renit_mot_passe(page: ft.Page):
    page.title = "RÉINITIALISATION DU MOT DE PASSE"
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    page.padding = 20

    # Message pour afficher les erreurs ou les succès
    message = ft.Text("", size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    def on_confirm_click(e):
        # Désactiver le bouton pendant le traitement
        confirm_button.disabled = True
        confirm_button.text = "Validation..."
        page.update()

        if not code_input.value:
            show_message(message, "⚠️ Veuillez entrer le code de confirmation", "red", page)
            confirm_button.disabled = False
            confirm_button.text = "CONFIRMER"
            page.update()
            return
            
        if not new_password_input.value or not confirm_password_input.value:
            show_message(message, "⚠️ Veuillez remplir tous les champs du mot de passe", "red", page)
            confirm_button.disabled = False
            confirm_button.text = "CONFIRMER"
            page.update()
            return
            
        if new_password_input.value != confirm_password_input.value:
            show_message(message, "❌ Les mots de passe ne correspondent pas", "red", page)
            confirm_password_input.value = ""
            confirm_password_input.focus()
            confirm_button.disabled = False
            confirm_button.text = "CONFIRMER"
            page.update()
            return
            
        # Validation de la longueur du mot de passe
        if len(new_password_input.value) < 6:
            show_message(message, "⚠️ Le mot de passe doit contenir au moins 6 caractères", "red", page)
            confirm_button.disabled = False
            confirm_button.text = "CONFIRMER"
            page.update()
            return
            
        # Récupérer l'email depuis la session
        email = page.session.get("recovery_email")
        if not email:
            show_message(message, "❌ Erreur: session expirée, veuillez recommencer", "red", page)
            confirm_button.disabled = False
            confirm_button.text = "CONFIRMER"
            page.update()
            return
            
        success, result_message = reset_password(email, code_input.value, new_password_input.value)
        
        if success:
            show_message(message, "✅ " + result_message, "#90EE90", page, True)
            time.sleep(1)
            page.go("/page_connexion")  # Rediriger vers la page de connexion
        else:
            show_message(message, "❌ " + result_message, "red", page)
        
        # Réactiver le bouton
        confirm_button.disabled = False
        confirm_button.text = "CONFIRMER"
        page.update()

    def retour_click(e):
        page.go('/page_recup_mot_passe')

    # Style pour les champs (cohérent avec les autres pages)
    field_style = {
        "width": 350,
        "height": 55,
        "border_radius": 12,
        "border_color": '#e0e0e0',
        "focused_border_color": '#90EE90',
        "bgcolor": "white",
        "color": 'black',
        "text_size": 14,
        "label_style": ft.TextStyle(color='#666666', size=12),
        "content_padding": ft.padding.symmetric(horizontal=15, vertical=12)
    }

    # Création des champs de saisie avec style amélioré
    code_input = ft.TextField(
        label="Code de confirmation",
        hint_text="Entrez le code reçu par email",
        prefix_icon=ft.Icons.SECURITY,
        max_length=6,
        **field_style
    )
    
    new_password_input = ft.TextField(
        label="Nouveau mot de passe",
        hint_text="Minimum 6 caractères",
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK,
        **field_style
    )
    
    confirm_password_input = ft.TextField(
        label="Confirmer le mot de passe",
        hint_text="Répétez le nouveau mot de passe",
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        **field_style
    )
    
    # Boutons avec style amélioré
    confirm_button = ft.ElevatedButton(
        "CONFIRMER",
        bgcolor='#90EE90',
        color='black',
        width=160,
        height=45,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD)
        ),
        on_click=on_confirm_click
    )

    retour_button = ft.ElevatedButton(
        "← RETOUR",
        bgcolor='lightblue',
        color='black',
        width=160,
        height=45,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            text_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_500)
        ),
        on_click=retour_click
    )

    # Container principal avec design moderne
    reset_container = ft.Container(
        content=ft.Column([
            # En-tête avec icône et texte
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.KEY, size=50, color='white'),
                    ft.Text(
                        "Nouveau mot de passe",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color='white',
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Entrez le code reçu et définissez votre nouveau mot de passe",
                        size=14,
                        color='white',
                        text_align=ft.TextAlign.CENTER
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                margin=ft.margin.only(bottom=25)
            ),
            
            # Zone de saisie
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "🔐 Choisissez un mot de passe sécurisé (minimum 6 caractères)",
                        size=12,
                        color='#ff9800',
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.W_500
                    ),
                    ft.Container(height=20),
                    
                    code_input,
                    ft.Container(height=15),
                    
                    new_password_input,
                    ft.Container(height=15),
                    
                    confirm_password_input,
                    ft.Container(height=25),
                    
                    ft.Row([retour_button, confirm_button], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                    ft.Container(height=15),
                    message,
                    
                    ft.Container(height=10),
                    ft.Text(
                        "💡 Conseil: Utilisez un mélange de lettres, chiffres et symboles",
                        size=11,
                        color='rgba(255, 255, 255, 0.7)',
                        text_align=ft.TextAlign.CENTER,
                        italic=True
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor='rgba(255, 255, 255, 0.1)',
                border_radius=20,
                padding=30,
                border=ft.border.all(1, 'rgba(255, 255, 255, 0.2)')
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        width=450,
        padding=20,
    )

    # Layout final avec conteneur centré
    return [
        ft.Container(
            content=ft.Row([reset_container], alignment=ft.MainAxisAlignment.CENTER),
            expand=True,
            alignment=ft.alignment.center,
            padding=20
        )
    ]