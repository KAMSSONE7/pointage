import flet as ft
from db_config import DB_CONFIG
import mysql.connector
from mysql.connector import Error
from db_config import get_db_connection
import logging

# Définition des couleurs
BG = "#041955"   # Bleu foncé
FWG = "#FFFFFF"  # Blanc
FG = "#3450a1"   # Bleu clair
PINK = "#eb06ff" # Rose

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_presence_stats():
    """Récupère les statistiques de présence depuis la base de données"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn or not conn.is_connected():
            logger.error("Impossible de se connecter à la base de données")
            return {}
            
        cursor = conn.cursor(dictionary=True)
        
        # Récupérer le nombre total d'enseignants
        cursor.execute("SELECT COUNT(*) as total FROM Enseignant")
        total_teachers = cursor.fetchone()['total']
        
        # Récupérer le nombre d'enseignants présents aujourd'hui
        cursor.execute("""
            SELECT COUNT(DISTINCT p.Id_ens) as present_today 
            FROM Presence_ens p
            JOIN Enseignant e ON p.Id_ens = e.Id_ens
            WHERE DATE(p.Date_presence) = CURDATE()
        """)
        present_today = cursor.fetchone()['present_today']
        
        # Récupérer le nombre d'enseignants actifs cette semaine
        cursor.execute("""
            SELECT COUNT(DISTINCT p.Id_ens) as active_this_week 
            FROM Presence_ens p
            JOIN Enseignant e ON p.Id_ens = e.Id_ens
            WHERE YEARWEEK(p.Date_presence, 1) = YEARWEEK(CURDATE(), 1)
        """)
        active_this_week = cursor.fetchone()['active_this_week']
        
        # Calculer les pourcentages
        present_percent = round((present_today / total_teachers * 100) if total_teachers > 0 else 0, 1)
        absent_percent = max(0, 100 - present_percent)
        
        return {
            'total_teachers': total_teachers,
            'present_today': present_today,
            'active_this_week': active_this_week,
            'present_percent': present_percent,
            'absent_percent': absent_percent
        }
        
    except Error as e:
        logger.error(f"Erreur lors de la récupération des statistiques: {e}")
        return {}
    except Exception as e:
        logger.error(f"Erreur inattendue: {e}")
        return {}
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

# La fonction get_db_connection est maintenant importée depuis db_config

def page_stat2(page: ft.Page, teacher_id=None):
    # Configuration de la page
    page.title = "Statistiques de présence"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    
    # Récupérer les statistiques
    stats = fetch_presence_stats()
    
    # Vérifier si les statistiques ont été récupérées avec succès
    if not stats:
        page.add(
            ft.Text(
                "Erreur lors de la récupération des statistiques. Veuillez réessayer plus tard.",
                color=FWG,
                size=18,
                weight=ft.FontWeight.BOLD
            )
        )
        return
    
    # Créer l'en-tête avec les boutons de navigation
    header = ft.Row([
        ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_color=FWG,
            on_click=lambda _: page.go("/page_accueil"),
            tooltip="Retour"
        ),
        ft.Container(expand=True),
        ft.IconButton(
            icon=ft.Icons.REFRESH,
            icon_color=FWG,
            on_click=lambda _: page.update(),
            tooltip="Rafraîchir"
        ),
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    # Créer le graphique en secteurs
    chart = ft.PieChart(
        sections=[
            ft.PieChartSection(
                stats.get('present_percent', 0),
                title=f"{stats.get('present_percent', 0)}%\nPrésents",
                title_style=ft.TextStyle(
                    size=14,
                    color=FWG,
                    weight=ft.FontWeight.BOLD
                ),
                color="#4CAF50",
                radius=80
            ),
            ft.PieChartSection(
                stats.get('absent_percent', 100),
                title=f"{stats.get('absent_percent', 100)}%\nAbsents",
                title_style=ft.TextStyle(
                    size=14,
                    color=FWG,
                    weight=ft.FontWeight.BOLD
                ),
                color="#EF5350",
                radius=80
            ),
        ],
        sections_space=2,
        center_space_radius=40,
        height=300,
        width=300,
    )
    
    # Suppression du doublon de l'en-tête
    
    # Créer la mise en page
    content = ft.Container(
        content=ft.Column(
            [
                header,
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(
                                        f"{stats.get('total_teachers', 0)}",
                                        size=32,
                                        weight=ft.FontWeight.BOLD,
                                        color=FG
                                    ),
                                    ft.Text("Enseignants au total", color=FWG),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=5,
                            ),
                            padding=20,
                            bgcolor=ft.Colors.with_opacity(0.1, FWG),
                            border_radius=10,
                            width=200,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(
                                        f"{stats.get('present_today', 0)}",
                                        size=32,
                                        weight=ft.FontWeight.BOLD,
                                        color="#4CAF50"
                                    ),
                                    ft.Text("Présents aujourd'hui", color=FWG),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=5,
                            ),
                            padding=20,
                            bgcolor=ft.Colors.with_opacity(0.1, FWG),
                            border_radius=10,
                            width=200,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(
                                        f"{stats.get('active_this_week', 0)}",
                                        size=32,
                                        weight=ft.FontWeight.BOLD,
                                        color="#FF9800"
                                    ),
                                    ft.Text("Actifs cette semaine", color=FWG),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=5,
                            ),
                            padding=20,
                            bgcolor=ft.Colors.with_opacity(0.1, FWG),
                            border_radius=10,
                            width=200,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    wrap=True,
                ),
                ft.Container(
                    content=chart,
                    padding=20,
                    bgcolor=ft.Colors.with_opacity(0.1, FWG),
                    border_radius=10,
                    margin=ft.margin.only(top=20),
                    alignment=ft.alignment.center,
                ),
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        ),
        padding=20,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[BG, FG],
        ),
        expand=True,
    )
    
    # Gestion du redimensionnement de la fenêtre
    def on_resize(e):
        if page.width < 768:  # Mobile
            content.content.width = page.width - 40
        page.update()
    
    page.on_resize = on_resize
    
    return [content]
