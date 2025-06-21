import flet as ft
import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager
from typing import List, Tuple, Optional
import logging
from db_config import get_db_connection as db_connection

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@contextmanager
def get_db_connection():
    """Gestionnaire de contexte pour les connexions à la base de données"""
    connection = None
    try:
        connection = db_connection()
        if not connection or not connection.is_connected():
            raise Error("Impossible de se connecter à la base de données")
        yield connection
    except Error as e:
        logger.error(f"Erreur de connexion à la base de données: {e}")
        raise
    finally:
        if connection and connection.is_connected():
            connection.close()
            logger.info("Connexion MySQL fermée")

def fetch_schedule_data() -> List[Tuple]:
    """Récupère les données de l'emploi du temps depuis la base de données"""
    query = """
        SELECT 
            e.jours, 
            TIME_FORMAT(e.heure_deb, '%H:%i') as heure_deb,
            TIME_FORMAT(e.heure_fin, '%H:%i') as heure_fin,
            c.Libelle as cours, 
            s.Libelle as salle
        FROM 
            Emploi_du_temps e
        JOIN 
            Cours c ON e.Id_cours = c.Id_cours
        JOIN 
            Salle s ON e.Id_salle = s.Id_salle
        ORDER BY 
            FIELD(e.jours, 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'),
            e.heure_deb
    """
    
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()
    except Error as e:
        logger.error(f"Erreur lors de la récupération des données: {e}")
        return []

def create_schedule_table() -> ft.DataTable:
    """Crée et configure le tableau de l'emploi du temps"""
    return ft.DataTable(
        columns=[
            ft.DataColumn(
                ft.Text("Jour", color="WHITE", weight=ft.FontWeight.BOLD),
                numeric=False
            ),
            ft.DataColumn(
                ft.Text("Début", color="WHITE", weight=ft.FontWeight.BOLD),
                numeric=False
            ),
            ft.DataColumn(
                ft.Text("Fin", color="WHITE", weight=ft.FontWeight.BOLD),
                numeric=False
            ),
            ft.DataColumn(
                ft.Text("Cours", color="WHITE", weight=ft.FontWeight.BOLD),
                numeric=False
            ),
            ft.DataColumn(
                ft.Text("Salle", color="WHITE", weight=ft.FontWeight.BOLD),
                numeric=False
            ),
        ],
        rows=[],
        border=ft.border.all(2, ft.Colors.BLUE_400),
        border_radius=12,
        bgcolor=ft.Colors.BLUE_800,
        heading_row_color=ft.Colors.BLUE_900,
        heading_row_height=50,
        data_row_min_height=45,
        column_spacing=20,
        horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLUE_300),
        show_checkbox_column=False,
    )

def create_responsive_schedule_display(schedule_data: List[Tuple]) -> ft.Control:
    """Crée un affichage responsive de l'emploi du temps"""
    if not schedule_data:
        return ft.Container(
            content=ft.Text(
                "Aucune donnée disponible",
                color="WHITE",
                size=16,
                text_align=ft.TextAlign.CENTER
            ),
            padding=20,
            alignment=ft.alignment.center
        )
    
    # Version tableau avec scroll horizontal
    schedule_table = create_schedule_table()
    populate_schedule_table(schedule_table, schedule_data)
    
    # Conteneur avec scroll horizontal
    horizontal_scroll_container = ft.Container(
        content=schedule_table,
        width=None,  # Laisse le tableau prendre sa taille naturelle
        padding=10,
    )
    
    # Row avec scroll horizontal
    scrollable_row = ft.Row(
        controls=[horizontal_scroll_container],
        scroll=ft.ScrollMode.ALWAYS,  # Active le scroll horizontal
        expand=True,
    )
    
    # Version liste pour mobile (alternative)
    mobile_cards = create_mobile_schedule_cards(schedule_data)
    
    return ft.Column([
        # Indicateur de scroll pour les utilisateurs
        ft.Container(
            content=ft.Text(
                "👈 Faites glisser horizontalement pour voir toutes les colonnes",
                color=ft.Colors.BLUE_300,
                size=12,
                text_align=ft.TextAlign.CENTER,
                italic=True
            ),
            padding=ft.padding.only(bottom=10)
        ),
        # Tableau avec scroll horizontal
        ft.Container(
            content=scrollable_row,
            border_radius=12,
            margin=ft.margin.symmetric(vertical=10),
            height=400,  # Hauteur fixe pour le conteneur du tableau
        ),
        # Espacement
        ft.Container(height=20),
        # Version cartes pour mobile (optionnelle)
        ft.Text(
            "Version cartes (plus lisible sur mobile) :",
            color="WHITE",
            size=16,
            weight=ft.FontWeight.BOLD
        ),
        ft.Container(height=10),
        mobile_cards
    ])

def create_mobile_schedule_cards(schedule_data: List[Tuple]) -> ft.Column:
    """Crée une version en cartes pour mobile"""
    cards = []
    current_day = None
    
    for row in schedule_data:
        jour, heure_deb, heure_fin, cours, salle = row
        
        # Titre du jour si changement
        if jour != current_day:
            if current_day is not None:  # Espacement entre les jours
                cards.append(ft.Container(height=15))
            
            cards.append(
                ft.Container(
                    content=ft.Text(
                        jour,
                        size=18,
                        color="WHITE",
                        weight=ft.FontWeight.BOLD
                    ),
                    bgcolor=ft.Colors.BLUE_700,
                    padding=ft.padding.symmetric(horizontal=15, vertical=8),
                    border_radius=8,
                    margin=ft.margin.only(bottom=5)
                )
            )
            current_day = jour
        
        # Carte du cours
        card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.ACCESS_TIME, color=ft.Colors.BLUE_300, size=16),
                    ft.Text(f"{heure_deb} - {heure_fin}", color="WHITE", weight=ft.FontWeight.W_500)
                ], spacing=5),
                ft.Row([
                    ft.Icon(ft.Icons.BOOK, color=ft.Colors.GREEN_300, size=16),
                    ft.Text(cours, color="WHITE", size=16)
                ], spacing=5),
                ft.Row([
                    ft.Icon(ft.Icons.ROOM, color=ft.Colors.ORANGE_300, size=16),
                    ft.Text(salle, color="WHITE")
                ], spacing=5),
            ], spacing=5),
            bgcolor=ft.Colors.BLUE_800,
            padding=15,
            border_radius=8,
            border=ft.border.all(1, ft.Colors.BLUE_400),
            margin=ft.margin.only(bottom=8, left=20)
        )
        cards.append(card)
    
    return ft.Column(cards, spacing=0)

def populate_schedule_table(schedule_table: ft.DataTable, schedule_data: List[Tuple]):
    """Remplit le tableau avec les données de l'emploi du temps"""
    schedule_table.rows.clear()
    
    if not schedule_data:
        # Affiche un message si aucune donnée n'est disponible
        schedule_table.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Aucune donnée", color="WHITE", italic=True)),
                    ft.DataCell(ft.Text("", color="WHITE")),
                    ft.DataCell(ft.Text("", color="WHITE")),
                    ft.DataCell(ft.Text("", color="WHITE")),
                    ft.DataCell(ft.Text("", color="WHITE")),
                ]
            )
        )
        return
    
    # Groupement par jour pour une meilleure lisibilité
    current_day = None
    for row in schedule_data:
        jour, heure_deb, heure_fin, cours, salle = row
        
        # Highlight du premier cours de chaque jour
        row_color = ft.Colors.BLUE_700 if jour != current_day else None
        current_day = jour
        
        schedule_table.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(jour, color="WHITE", weight=ft.FontWeight.W_500)),
                    ft.DataCell(ft.Text(str(heure_deb), color="WHITE")),
                    ft.DataCell(ft.Text(str(heure_fin), color="WHITE")),
                    ft.DataCell(ft.Text(cours, color="WHITE")),
                    ft.DataCell(ft.Text(salle, color="WHITE")),
                ],
                color=row_color
            )
        )

def create_error_display(error_message: str) -> ft.Container:
    """Crée un affichage d'erreur stylisé"""
    return ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.RED_400, size=48),
            ft.Text(
                "Erreur de chargement",
                size=20,
                color=ft.Colors.RED_400,
                weight=ft.FontWeight.BOLD
            ),
            ft.Text(
                error_message,
                size=14,
                color=ft.Colors.RED_300,
                text_align=ft.TextAlign.CENTER
            ),
        ], 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
        ),
        padding=20,
        border_radius=10,
        bgcolor=ft.Colors.RED_900,
        border=ft.border.all(2, ft.Colors.RED_400),
        margin=ft.margin.symmetric(vertical=20)
    )

def create_loading_indicator() -> ft.Container:
    """Crée un indicateur de chargement"""
    return ft.Container(
        content=ft.Column([
            ft.ProgressRing(color=ft.Colors.BLUE_400),
            ft.Text("Chargement de l'emploi du temps...", color="WHITE", size=16)
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15
        ),
        padding=40,
        alignment=ft.alignment.center
    )

def page_emploi_temps(page: ft.Page):
    """Page principale de l'emploi du temps"""
    
    # Interface utilisateur
    title = ft.Text(
        "📅 Emploi du temps",
        size=32,
        color="WHITE",
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )
    
    back_button = ft.ElevatedButton(
        "← Retour à l'accueil",
        on_click=lambda _: page.go("/page_accueil"),
        bgcolor=ft.Colors.BLUE_600,
        color="white",
        height=45,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation=3
        )
    )
    
    refresh_button = ft.ElevatedButton(
        "🔄 Actualiser",
        on_click=lambda _: load_schedule(),
        bgcolor=ft.Colors.GREEN_600,
        color="white",
        height=45,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation=3
        )
    )
    
    # Conteneur pour le contenu principal
    main_content = ft.Container()
    
    def load_schedule():
        """Charge l'emploi du temps avec gestion des états"""
        # Affichage du loading
        main_content.content = create_loading_indicator()
        page.update()
        
        try:
            schedule_data = fetch_schedule_data()
            
            # Utilisation de l'affichage responsive
            main_content.content = create_responsive_schedule_display(schedule_data)
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement: {e}")
            main_content.content = create_error_display(
                "Impossible de charger l'emploi du temps. Vérifiez votre connexion à la base de données."
            )
        
        page.update()
    
    # Conteneur des boutons
    button_row = ft.Row([
        back_button,
        refresh_button
    ],
    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    spacing=10
    )
    
    # Layout principal avec ListView pour le défilement vertical
    scrollable_content = ft.ListView(
        controls=[
            ft.Container(height=10),  # Espacement supérieur
            title,
            ft.Container(height=20),
            button_row,
            ft.Container(height=20),
            main_content,
            ft.Container(height=20),  # Espacement inférieur
        ],
        expand=True,
        padding=ft.padding.all(20),
        spacing=0
    )
    
    content = ft.Column(
        controls=[scrollable_content],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
        spacing=0
    )
    
    # Chargement initial
    load_schedule()
    
    return [content]