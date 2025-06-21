import flet as ft
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import asyncio
from db_config import get_db_connection

BG = "#041955"
CARD_BG = "#1e3a8a"
ACCENT_COLOR = "#3b82f6"
SUCCESS_COLOR = "#10b981"
WARNING_COLOR = "#f59e0b"
ERROR_COLOR = "#ef4444"

def page_notif(page: ft.Page):
    # Configuration responsive
    page.adaptive = True
    
    # État des notifications
    notifications_data = []
    selected_notification = None
    
    # Titre principal avec style moderne
    title = ft.Text(
        "📬 Centre de Notifications", 
        size=32, 
        color="WHITE", 
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )
    
    # Sous-titre avec compteur
    subtitle = ft.Text(
        "Toutes vos notifications en un coup d'œil",
        size=16,
        color="#94a3b8",
        text_align=ft.TextAlign.CENTER
    )
    
    # Bannière moderne avec gradient
    banner = ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.NOTIFICATIONS_ACTIVE, size=60, color="WHITE"),
            title,
            subtitle
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.padding.all(30),
        margin=ft.margin.only(bottom=20),
        bgcolor=ft.Colors.BLUE_700,
        border_radius=20,
        gradient=ft.LinearGradient(
            colors=[ACCENT_COLOR, "#1e40af"],
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right
        )
    )
    
    # Barre d'actions
    refresh_button = ft.IconButton(
        icon=ft.Icons.REFRESH,
        tooltip="Actualiser",
        icon_color="WHITE",
        bgcolor=SUCCESS_COLOR,
        on_click=lambda _: fetch_notifications()
    )
    
    mark_all_read_button = ft.ElevatedButton(
        "Tout marquer comme lu",
        icon=ft.Icons.MARK_EMAIL_READ,
        bgcolor=WARNING_COLOR,
        color="WHITE",
        on_click=lambda _: mark_all_as_read()
    )
    
    back_button = ft.ElevatedButton(
        "← Retour à l'accueil",
        icon=ft.Icons.HOME,
        bgcolor=CARD_BG,
        color="WHITE",
        on_click=lambda _: page.go("/page_accueil")
    )
    
    action_bar = ft.ResponsiveRow([
        ft.Column([back_button], col={"xs": 12, "sm": 4}),
        ft.Column([refresh_button], col={"xs": 6, "sm": 4}, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Column([mark_all_read_button], col={"xs": 6, "sm": 4}, horizontal_alignment=ft.CrossAxisAlignment.END)
    ], spacing=10)
    
    # Statistiques des notifications
    stats_container = ft.ResponsiveRow([
        ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.MAIL, size=30, color=ACCENT_COLOR),
                    ft.Text("Total", size=12, color="#94a3b8"),
                    ft.Text("0", size=24, weight=ft.FontWeight.BOLD, color="WHITE", ref=ft.Ref[ft.Text]())
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=15,
                bgcolor=CARD_BG,
                border_radius=10,
                width=120,
                height=100
            )
        ], col={"xs": 6, "sm": 3}),
        ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.MARK_EMAIL_UNREAD, size=30, color=WARNING_COLOR),
                    ft.Text("Non lues", size=12, color="#94a3b8"),
                    ft.Text("0", size=24, weight=ft.FontWeight.BOLD, color="WHITE", ref=ft.Ref[ft.Text]())
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=15,
                bgcolor=CARD_BG,
                border_radius=10,
                width=120,
                height=100
            )
        ], col={"xs": 6, "sm": 3}),
        ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.TODAY, size=30, color=SUCCESS_COLOR),
                    ft.Text("Aujourd'hui", size=12, color="#94a3b8"),
                    ft.Text("0", size=24, weight=ft.FontWeight.BOLD, color="WHITE", ref=ft.Ref[ft.Text]())
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=15,
                bgcolor=CARD_BG,
                border_radius=10,
                width=120,
                height=100
            )
        ], col={"xs": 6, "sm": 3}),
        ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.PRIORITY_HIGH, size=30, color=ERROR_COLOR),
                    ft.Text("Importantes", size=12, color="#94a3b8"),
                    ft.Text("0", size=24, weight=ft.FontWeight.BOLD, color="WHITE", ref=ft.Ref[ft.Text]())
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=15,
                bgcolor=CARD_BG,
                border_radius=10,
                width=120,
                height=100
            )
        ], col={"xs": 6, "sm": 3})
    ], spacing=10)
    
    # Références pour les statistiques
    total_ref = stats_container.controls[0].controls[0].content.controls[2]
    unread_ref = stats_container.controls[1].controls[0].content.controls[2]
    today_ref = stats_container.controls[2].controls[0].content.controls[2]
    important_ref = stats_container.controls[3].controls[0].content.controls[2]
    
    # Conteneur pour les notifications
    notifications_list = ft.Column(spacing=10)
    
    # Conteneur scrollable pour les notifications
    notifications_scroll = ft.Container(
        content=notifications_list,
        padding=10,
        height=400,
        bgcolor=ft.Colors.TRANSPARENT,
        border_radius=10,
    )
    
    # Indicateur de chargement
    loading_indicator = ft.ProgressRing(
        width=50,
        height=50,
        color=ACCENT_COLOR,
        visible=False
    )
    
    # Message d'état vide
    empty_state = ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.NOTIFICATIONS_OFF, size=80, color="#64748b"),
            ft.Text("Aucune notification", size=20, color="#64748b", weight=ft.FontWeight.BOLD),
            ft.Text("Vous êtes à jour ! 🎉", size=14, color="#94a3b8")
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=40,
        visible=False
    )
    
    def get_notification_icon(notification_type):
        """Retourne l'icône appropriée selon le type de notification"""
        Icons_map = {
            'info': ft.Icons.INFO,
            'warning': ft.Icons.WARNING,
            'error': ft.Icons.ERROR,
            'success': ft.Icons.CHECK_CIRCLE,
            'message': ft.Icons.MESSAGE,
            'email': ft.Icons.EMAIL,
            'system': ft.Icons.COMPUTER,
            'security': ft.Icons.SECURITY,
            'update': ft.Icons.SYSTEM_UPDATE
        }
        return Icons_map.get(notification_type.lower(), ft.Icons.NOTIFICATIONS)
    
    def get_notification_color(notification_type, is_read=False):
        """Retourne la couleur appropriée selon le type et l'état"""
        if is_read:
            return "#64748b"
        
        Colors_map = {
            'info': ACCENT_COLOR,
            'warning': WARNING_COLOR,
            'error': ERROR_COLOR,
            'success': SUCCESS_COLOR,
            'message': "#8b5cf6",
            'email': "#06b6d4",
            'system': "#6b7280",
            'security': ERROR_COLOR,
            'update': SUCCESS_COLOR
        }
        return Colors_map.get(notification_type.lower(), ACCENT_COLOR)
    
    def format_time_ago(date_str):
        """Formate le temps écoulé depuis la notification"""
        try:
            if isinstance(date_str, str):
                notif_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            else:
                notif_date = date_str
            
            now = datetime.now()
            diff = now - notif_date
            
            if diff.days > 0:
                return f"Il y a {diff.days} jour{'s' if diff.days > 1 else ''}"
            elif diff.seconds > 3600:
                hours = diff.seconds // 3600
                return f"Il y a {hours}h"
            elif diff.seconds > 60:
                minutes = diff.seconds // 60
                return f"Il y a {minutes}min"
            else:
                return "À l'instant"
        except:
            return "Date inconnue"
    
    def create_notification_card(notification):
        """Crée une carte de notification moderne"""
        notif_id, message, date_str, is_read, notif_type, priority = notification
        
        # Indicateur de lecture
        read_indicator = ft.Container(
            width=8,
            height=8,
            bgcolor=get_notification_color(notif_type, is_read) if not is_read else ft.Colors.TRANSPARENT,
            border_radius=4,
            margin=ft.margin.only(right=10)
        )
        
        # Icône de notification
        icon = ft.Icon(
            get_notification_icon(notif_type),
            size=24,
            color=get_notification_color(notif_type, is_read)
        )
        
        # Contenu principal
        main_content = ft.Column([
            ft.Text(
                message,
                size=14,
                color="WHITE" if not is_read else "#94a3b8",
                weight=ft.FontWeight.BOLD if not is_read else ft.FontWeight.NORMAL,
                max_lines=2,
                overflow=ft.TextOverflow.ELLIPSIS,
                expand=True
            ),
            ft.Text(
                format_time_ago(date_str),
                size=12,
                color="#64748b"
            )
        ], spacing=5, expand=True)
        
        # Actions
        actions = ft.Row([
            ft.IconButton(
                icon=ft.Icons.MARK_EMAIL_READ if not is_read else ft.Icons.MARK_EMAIL_UNREAD,
                tooltip="Marquer comme lu" if not is_read else "Marquer comme non lu",
                icon_size=18,
                icon_color="#64748b",
                on_click=lambda _, nid=notif_id: toggle_read_status(nid)
            ),
            ft.IconButton(
                icon=ft.Icons.DELETE_OUTLINE,
                tooltip="Supprimer",
                icon_size=18,
                icon_color=ERROR_COLOR,
                on_click=lambda _, nid=notif_id: delete_notification(nid)
            )
        ], spacing=0)
        
        # Badge de priorité
        priority_badge = None
        if priority == 'high':
            priority_badge = ft.Container(
                content=ft.Text("!", size=12, color="WHITE", weight=ft.FontWeight.BOLD),
                width=20,
                height=20,
                bgcolor=ERROR_COLOR,
                border_radius=10,
                alignment=ft.alignment.center,
                margin=ft.margin.only(left=5)
            )
        
        # Carte complète
        card = ft.Container(
            content=ft.Row([
                read_indicator,
                icon,
                main_content,
                priority_badge,
                actions
            ], alignment=ft.MainAxisAlignment.START, spacing=10),
            padding=15,
            margin=ft.margin.only(bottom=5),
            bgcolor=CARD_BG if not is_read else "#1e293b",
            border_radius=10,
            border=ft.border.all(1, get_notification_color(notif_type, is_read)) if not is_read else None,
            animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT),
            on_click=lambda _, nid=notif_id: mark_as_read_and_expand(nid)
        )
        
        return card
    
    def mark_as_read_and_expand(notification_id):
        """Marque une notification comme lue et l'ouvre"""
        mark_notification_read(notification_id)
        # Ici vous pourriez ajouter une logique pour afficher les détails
    
    def toggle_read_status(notification_id):
        """Inverse l'état de lecture d'une notification"""
        connection = None
        try:
            connection = get_db_connection()
            if not connection or not connection.is_connected():
                print("Erreur: Impossible de se connecter à la base de données")
                return
            
            if connection.is_connected():
                cursor = connection.cursor()
                # Inverser l'état de lecture
                cursor.execute(
                    "UPDATE notifications SET is_read = NOT is_read WHERE id = %s",
                    (notification_id,)
                )
                connection.commit()
                fetch_notifications()
                
        except Error as e:
            print(f"Erreur lors de la mise à jour: {e}")
            show_snackbar(f"Erreur: {e}", ERROR_COLOR)
        finally:
            if connection is not None and connection.is_connected():
                cursor.close()
                connection.close()
    
    def mark_notification_read(notification_id):
        """Marque une notification comme lue"""
        connection = None
        try:
            connection = get_db_connection()
            if not connection or not connection.is_connected():
                print("Erreur: Impossible de se connecter à la base de données")
                return
            
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(
                    "UPDATE notifications SET is_read = TRUE WHERE id = %s",
                    (notification_id,)
                )
                connection.commit()
                fetch_notifications()
                
        except Error as e:
            print(f"Erreur lors de la mise à jour: {e}")
    
    def delete_notification(notification_id):
        """Supprime une notification"""
        connection = None
        try:
            connection = get_db_connection()
            if not connection or not connection.is_connected():
                print("Erreur: Impossible de se connecter à la base de données")
                return
            
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("DELETE FROM notifications WHERE id = %s", (notification_id,))
                connection.commit()
                fetch_notifications()
                show_snackbar("Notification supprimée", SUCCESS_COLOR)
                
        except Error as e:
            print(f"Erreur lors de la suppression: {e}")
            show_snackbar(f"Erreur: {e}", ERROR_COLOR)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def mark_all_as_read():
        """Marque toutes les notifications comme lues"""
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            if not connection or not connection.is_connected():
                print("Erreur: Impossible de se connecter à la base de données")
                show_snackbar("Erreur de connexion à la base de données", ERROR_COLOR)
                return
                
            cursor = connection.cursor()
            cursor.execute("UPDATE notifications SET is_read = TRUE")
            connection.commit()
            fetch_notifications()
            show_snackbar("Toutes les notifications marquées comme lues", SUCCESS_COLOR)
                
        except Error as e:
            print(f"Erreur lors de la mise à jour: {e}")
            show_snackbar(f"Erreur: {e}", ERROR_COLOR)
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
    
    def show_snackbar(message, color):
        """Affiche un message de confirmation"""
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color="WHITE"),
            bgcolor=color
        )
        page.snack_bar.open = True
        page.update()
    
    def update_stats():
        """Met à jour les statistiques"""
        total = len(notifications_data)
        unread = sum(1 for n in notifications_data if not n[3])  # is_read = False
        today = sum(1 for n in notifications_data if is_today(n[2]))
        important = sum(1 for n in notifications_data if n[5] == 'high')  # priority = high
        
        total_ref.current.value = str(total)
        unread_ref.current.value = str(unread)
        today_ref.current.value = str(today)
        important_ref.current.value = str(important)
    
    def is_today(date_str):
        """Vérifie si une date est aujourd'hui"""
        try:
            if isinstance(date_str, str):
                notif_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            else:
                notif_date = date_str
            return notif_date.date() == datetime.now().date()
        except:
            return False
    
    def fetch_notifications():
        """Récupère les notifications depuis la base de données"""
        loading_indicator.visible = True
        empty_state.visible = False
        page.update()
        
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            if not connection or not connection.is_connected():
                print("Erreur: Impossible de se connecter à la base de données")
                show_snackbar("Erreur de connexion à la base de données", ERROR_COLOR)
                empty_state.visible = True
                return
                
            cursor = connection.cursor()
            # Requête avec plus de champs pour une meilleure gestion
            cursor.execute("""
                SELECT id, message, date, is_read, type, priority 
                FROM notifications 
                ORDER BY date DESC, is_read ASC
            """)
            notifications = cursor.fetchall()
            
            # Mettre à jour les données globales
            global notifications_data
            notifications_data = notifications
            
            # Vider la liste actuelle
            notifications_list.controls.clear()
            
            if notifications:
                # Ajouter chaque notification
                for notification in notifications:
                    card = create_notification_card(notification)
                    notifications_list.controls.append(card)
                empty_state.visible = False
            else:
                empty_state.visible = True
            
            # Mettre à jour les statistiques
            update_stats()
                
        except Error as e:
            print(f"Erreur lors de la connexion à MySQL: {e}")
            show_snackbar(f"Erreur de connexion: {e}", ERROR_COLOR)
            empty_state.visible = True
            
        finally:
            loading_indicator.visible = False
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
            page.update()
    
    # Chargement initial
    fetch_notifications()
    
    # Mise en page principale
    main_content = ft.Column([
        banner,
        action_bar,
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        stats_container,
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        ft.Text("📧 Boîte de réception", size=20, color="WHITE", weight=ft.FontWeight.BOLD),
        ft.Stack([
            notifications_scroll,
            ft.Container(
                content=loading_indicator,
                alignment=ft.alignment.center,
                height=400
            ),
            ft.Container(
                content=empty_state,
                alignment=ft.alignment.center,
                height=400
            )
        ])
    ], spacing=15, expand=True)
    
    # Conteneur principal responsive
    responsive_container = ft.Container(
        content=main_content,
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        bgcolor=BG,
        expand=True
    )
    
    return [responsive_container]


# Script SQL pour créer/mettre à jour la table notifications si nécessaire
"""
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE,
    type VARCHAR(50) DEFAULT 'info',
    priority VARCHAR(20) DEFAULT 'normal',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Exemples de données de test
INSERT INTO notifications (message, type, priority, is_read) VALUES
('Bienvenue dans votre nouvelle application!', 'success', 'normal', FALSE),
('Mise à jour de sécurité disponible', 'warning', 'high', FALSE),
('Votre profil a été mis à jour avec succès', 'success', 'normal', TRUE),
('Nouvelle fonctionnalité disponible', 'info', 'normal', FALSE),
('Sauvegarde automatique effectuée', 'system', 'normal', TRUE),
('Attention: Tentative de connexion suspecte détectée', 'security', 'high', FALSE);
"""