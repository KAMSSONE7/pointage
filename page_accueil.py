import flet as ft
from datetime import datetime

# Définition des couleurs
BG = "#041955"   # Bleu foncé
FWG = "#FFFFFF"  # Blanc
FG = "#3450a1"   # Bleu clair
PINK = "#eb06ff" # Rose
def page_accueil(page: ft.Page):
    # Définir la couleur de fond de la page
    page.bgcolor = BG 
    
    # Page de menu
    menu_items = [
        ft.PopupMenuItem(icon=ft.Icons.HOME, text="Accueil", on_click=lambda _: page.go('/page_accueil')),
        ft.PopupMenuItem(icon=ft.Icons.WIDGETS, text="À propos de", on_click=lambda _: page.go('/page_a_propos')),
        ft.PopupMenuItem(icon=ft.Icons.PERSON, text="Profil", on_click=lambda _: page.go('/page_profil')),
    ]
    # Barre d'application (AppBar)
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.appbar = ft.AppBar(
        leading=ft.PopupMenuButton(
            icon=ft.Icons.MENU,  
            icon_color="white", 
            items=menu_items,  
        ),
        leading_width=40,
        bgcolor=ft.Colors.INDIGO,
        actions=[
        
            ft.IconButton(ft.Icons.NOTIFICATION_ADD_OUTLINED, icon_color="WHITE",on_click=lambda _: page.go('/page_notif')),
        ],
    )
    # Fonction pour gérer les clics sur la barre de navigation
    def navigation_changed(e):
        if e.control.selected_index == 0:
            page.go("/page_accueil")  # Accueil
        elif e.control.selected_index == 1:
            page.go("/page_emploi_temps")  # Emploi du temps
        elif e.control.selected_index == 2:
            page.go("/page_statistiques")  # Statistiques
        elif e.control.selected_index == 3: 
            page.go("/page_profil")
    # Barre de navigation
    navigation_bar = ft.CupertinoNavigationBar(
        bgcolor=ft.Colors.WHITE,
        inactive_color=ft.Colors.BLACK,
        active_color=ft.Colors.BLUE,
        on_change=navigation_changed,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.Icons.HOME_ROUNDED, color="black"),
                selected_icon=ft.Icon(ft.Icons.HOME_ROUNDED, color="BLUE"),
                label="Accueil"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.Icons.CALENDAR_TODAY, color="black"),
                selected_icon=ft.Icon(ft.Icons.CALENDAR_TODAY, color="BLUE"),
                label="Emploi du temps"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.Icons.SHOW_CHART, color="black"),
                selected_icon=ft.Icon(ft.Icons.SHOW_CHART, color="BLUE"),
                label="Statistiques"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.Icons.PERSON_2, color="black"),
                selected_icon=ft.Icon(ft.Icons.PERSON_2, color="BLUE"),
                label="Profil"
            ),
        ],
    )
    # Contenu de la page d'accueil
    content1 = ft.Column(
        controls=[
            ft.Text(
                spans=[
                    ft.TextSpan(
                        "PAGE D'ACCUEIL",
                        ft.TextStyle(
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            foreground=ft.Paint(
                                gradient=ft.PaintLinearGradient(
                                    (0, 20), (150, 20), [ft.Colors.PURPLE, ft.Colors.WHITE]
                                )
                            ),
                        ),
                    )
                ],
            ),
            ft.Text("TACHES", color="WHITE", size=20, weight=ft.FontWeight.BOLD),
            ft.Row(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("BOITE DE RECEPTION", color="WHITE", size=12, weight=ft.FontWeight.BOLD),
                                ft.Container(
                                    width=160,
                                    height=5,
                                    bgcolor=PINK,
                                    border_radius=20,
                                    padding=ft.Padding(5, 5, 5, 5),
                                    content=ft.Container(bgcolor=PINK)
                                )
                            ]
                        ),
                        border_radius=20,
                        bgcolor=BG,
                        height=171,
                        width=170,
                        padding=15,
                        ink=True,
                        on_click=lambda _: page.go('/page_boite_de_reception')
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("VOIR LISTE DE PRESENCE", color="WHITE", size=12, weight=ft.FontWeight.BOLD),
                                ft.Container(
                                    width=160,
                                    height=5,
                                    bgcolor=PINK,
                                    border_radius=20,
                                    padding=ft.Padding(5, 5, 5, 5),
                                    content=ft.Container(bgcolor=PINK)
                                ),
                            ]
                        ),
                        border_radius=20,
                        bgcolor=BG,
                        height=171,
                        width=170,
                        padding=15,
                        ink=True,
                        on_click=lambda _: page.go('/page_liste_de_presence')
                    ),
                    
                ], expand=True
            ),
            ft.Text("GENERER LA LISTE DE PRESENCE", color="WHITE", size=12, weight=ft.FontWeight.BOLD),
            ft.FloatingActionButton(
                icon=ft.Icons.ADD,
                bgcolor=ft.Colors.WHITE,
                on_click=lambda _: page.go('/page_generer_liste')
            )
        ]
    )
    # Retourner une liste de widgets
    return [content1, navigation_bar, page.appbar]
