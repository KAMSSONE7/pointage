import flet as ft
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector
from mysql.connector import Error
import time
from random import randint

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

# Variables globales pour stocker le code de récupération et l'heure d'envoi
recovery_code = None
code_sent_time = None

# Fonction pour générer un code de récupération
def generate_recovery_code():
    return str(randint(100000, 999999))

# Fonction pour envoyer un email
def send_email(to_email, subject, body):
    try:
        # Configuration du serveur SMTP
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        from_email = "gnetoschiphra@gmail.com"  # Remplacez par votre email
        password = "iqrxihbpznmlsekl"  # Remplacez par votre mot de passe d'application

        # Création du message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Connexion au serveur SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Activation du chiffrement TLS
        server.login(from_email, password)  # Connexion avec le mot de passe d'application

        # Envoi de l'email
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Email envoyé avec succès.")
        return True
    except smtplib.SMTPException as e:
        print(f"Erreur SMTP lors de l'envoi de l'email : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue lors de l'envoi de l'email : {e}")
        return False

# Fonction pour vérifier si l'email existe dans la base de données
def check_email_exists(email):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM utilisateurs WHERE email = %s", (email,))
        result = cursor.fetchone()
        return result is not None
    except Error as e:
        print(f"Erreur lors de la vérification de l'email : {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Fonction pour mettre à jour le code de récupération dans la base de données
def update_recovery_code(email, recovery_code):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Mettre à jour le code de récupération dans la table
        update_query = "UPDATE utilisateurs SET recovery_code = %s WHERE email = %s"
        cursor.execute(update_query, (recovery_code, email))
        connection.commit()
        print(f"Code de récupération mis à jour pour l'email : {email}")
        return True
    except Error as e:
        print(f"Erreur lors de la mise à jour du code de récupération : {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Fonction pour afficher les messages avec style
def show_message(message, text, color, page, is_success=False):
    message.value = text
    message.color = color
    page.update()
    if is_success:
        time.sleep(1.5)

# Page de récupération de mot de passe
def page_recup_mot_passe(page: ft.Page):
    page.title = 'RÉCUPÉRATION DE MOT DE PASSE'
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    page.padding = 20

    # Message pour afficher les erreurs ou les succès
    message = ft.Text("", size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    def ENVOYER(e):
        global recovery_code, code_sent_time

        # Désactiver le bouton pendant le traitement
        envoyer.disabled = True
        envoyer.text = "Envoi en cours..."
        page.update()

        if not email.value:
            show_message(message, "⚠️ Veuillez entrer votre email", "red", page)
            envoyer.disabled = False
            envoyer.text = "ENVOYER"
            page.update()
            return

        if not check_email_exists(email.value):
            show_message(message, "❌ Email non trouvé dans notre base de données", "red", page)
            envoyer.disabled = False
            envoyer.text = "ENVOYER"
            page.update()
            return

        # Générer et enregistrer le code de récupération
        recovery_code = generate_recovery_code()
        code_sent_time = time.time()
        
        if update_recovery_code(email.value, recovery_code):
            # Stocker l'email dans la session pour page_renit_mot_passe
            page.session.set("recovery_email", email.value)
            
            # Sujet et corps de l'email
            subject = "Code de récupération de mot de passe"
            body = (
                f"Bonjour cher utilisateur,\n\n"
                f"Voici votre code pour réinitialiser votre mot de passe : {recovery_code}.\n"
                f"Ce code est valable pendant 5 minutes et ne doit pas être partagé.\n"
                f"Si vous n'avez pas initié cette demande, contactez immédiatement notre support à contact@application.com.\n"
                f"Merci, l'équipe [Nom de l'application]."
            )

            # Envoyer l'email
            if send_email(email.value, subject, body):
                show_message(message, "✅ Code de récupération envoyé à votre email", "#90EE90", page, True)
                # Rediriger vers la page de confirmation après un délai
                time.sleep(1)
                page.go('/page_renit_mot_passe')
            else:
                show_message(message, "❌ Erreur lors de l'envoi du code de récupération", "red", page)
        else:
            show_message(message, "❌ Erreur lors de la génération du code de récupération", "red", page)
        
        # Réactiver le bouton
        envoyer.disabled = False
        envoyer.text = "ENVOYER"
        page.update()

    def RETOUR(e):
        page.go('/page_connexion')

    # Style pour les champs (adapté de la page 2)
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

    # Création des champs avec style amélioré
    email = ft.TextField(
        label="Adresse email",
        hint_text="Entrez votre adresse email",
        prefix_icon=ft.Icons.EMAIL,
        **field_style
    )

    # Boutons avec style amélioré
    envoyer = ft.ElevatedButton(
        "ENVOYER",
        bgcolor='#90EE90',
        color='black',
        width=160,
        height=45,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD)
        ),
        on_click=ENVOYER
    )

    retour = ft.ElevatedButton(
        "← RETOUR",
        bgcolor='lightblue',
        color='black',
        width=160,
        height=45,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            text_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_500)
        ),
        on_click=RETOUR
    )

    # Container principal avec design moderne (inspiré de la page 2)
    recovery_container = ft.Container(
        content=ft.Column([
            # En-tête avec icône et texte
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.LOCK_RESET, size=50, color='white'),
                    ft.Text(
                        "Récupération de mot de passe",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color='white',
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Entrez votre email pour recevoir un code de récupération",
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
                        "📧 Un code de récupération sera envoyé à votre adresse email",
                        size=12,
                        color='#ff9800',
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.W_500
                    ),
                    ft.Container(height=20),
                    
                    email,
                    ft.Container(height=25),
                    
                    ft.Row([retour, envoyer], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                    ft.Container(height=15),
                    message,
                    
                    ft.Container(height=10),
                    ft.Text(
                        "💡 Astuce: Vérifiez également votre dossier spam",
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
            content=ft.Row([recovery_container], alignment=ft.MainAxisAlignment.CENTER),
            expand=True,
            alignment=ft.alignment.center,
            padding=20
        )
    ]