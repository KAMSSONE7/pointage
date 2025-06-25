import flet as ft

def page_etu_acc(page: ft.Page):
    # Palette de couleurs moderne pour étudiant
    PRIMARY_COLOR = '#041955'  # Bleu-violet moderne
    ACCENT_COLOR = '#2BC2A9'  # Vert menthe
    CARD_COLOR = '#ffffff'  # Blanc
    CARD_SHADOW = '#516ec5'  # Gris clair pour ombres
    TEXT_PRIMARY = '#2d3748'  # Gris foncé
    TEXT_SECONDARY = '#718096'  # Gris moyen
    SUCCESS_COLOR = '#48bb78'  # Vert
    WARNING_COLOR = '#ed8936'  # Orange
    ERROR_COLOR = '#f56565'  # Rouge

    # Récupérer l'utilisateur actuel depuis la session
    user = page.session.get("user")
    
    # Vérifier les clés requises
    required_keys = ["nom", "prenom", "email", "profession", "numero", "adresse"]
    if not user or not all(key in user for key in required_keys):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(
                "Erreur: Données utilisateur incomplètes. Veuillez vous reconnecter.",
                color="white"
            ),
            bgcolor=ERROR_COLOR
        )
        page.snack_bar.open = True
        page.go('/page_connexion')
        return

    page.title = "Mon Espace Étudiant"
    page.bgcolor = "white"  # Fond blanc pour toute la page
    
    # État des composants
    search_visible = False
    notification_count = 5

    # Functions
    def toggle_search(e):
        nonlocal search_visible
        search_visible = not search_visible
        search_field.visible = search_visible
        if search_visible:
            search_field.focus()
        page.update()

    def search_query(e):
        query = e.control.value.lower()
        
        # Liste des mots-clés et leurs routes correspondantes
        keywords = {
            "accueil": "/page_etu_acc",
            "home": "/page_etu_acc",
            "espace": "/page_etu_acc",
            "profil": "/page_etu_profil",
            "compte": "/page_etu_profil",
            "parametres": "/page_etu_profil",
            "settings": "/page_etu_profil",
            "stats": "/page_etu_stats",
            "statistiques": "/page_etu_stats",
            "presence": "/page_etu_stats",
            "absence": "/page_etu_stats",
            "pointage": "/page_marquer_presence",
            "marquer": "/page_marquer_presence",
            "scanner": "/page_marquer_presence",
            "emploi": "/page_etu_emploi",
            "emploi du temps": "/page_etu_emploi",
            "emploi_temps": "/page_etu_emploi",
            "notes": "/page_etu_notes",
            "note": "/page_etu_notes",
            "resultats": "/page_etu_notes",
            "resultat": "/page_etu_notes",
            "aide": "/page_etu_propos",
            "help": "/page_etu_propos",
            "support": "/page_etu_propos",
            "contact": "/page_etu_propos"
        }
        
        for keyword, route in keywords.items():
            if keyword in query:
                page.go(route)
                break
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Aucun résultat trouvé pour cette recherche"),
                bgcolor=WARNING_COLOR,
                content_color=ft.Colors.WHITE
            )
            page.snack_bar.open = True
            page.update()

    def handle_logout(e):
        def close_dialog(e):
            page.dialog.open = False
            page.update()

        def confirm_logout(e):
            page.dialog.open = False
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Déconnexion réussie"),
                bgcolor=SUCCESS_COLOR,
                color="white"
            )
            page.snack_bar.open = True
            page.session.clear()
            page.go('/page_connexion')
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmation", color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
            content=ft.Text("Voulez-vous vraiment vous déconnecter ?", color=TEXT_SECONDARY),
            bgcolor=CARD_COLOR,
            actions=[
                ft.TextButton("Annuler", on_click=close_dialog),
                ft.ElevatedButton(
                    "Se déconnecter",
                    on_click=confirm_logout,
                    style=ft.ButtonStyle(bgcolor=ERROR_COLOR, color="white")
                )
            ],
        )
        page.dialog.open = True
        page.update()

    # Composants UI
    search_field = ft.TextField(
        label="Rechercher...",
        hint_text="Accueil, Profil, Stats, Pointage, Emploi du temps...",
        visible=search_visible,
        width=250,
        border_color=PRIMARY_COLOR,
        focused_border_color=ACCENT_COLOR,
        prefix_icon=ft.Icons.SEARCH,
        on_submit=search_query
    )

    header = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.PopupMenuButton(
                    icon=ft.Icons.MENU,
                    icon_color="white",
                    items=[
                        ft.PopupMenuItem(text="🏠 Accueil", on_click=lambda _: page.go("/page_etu_acc")),
                        ft.PopupMenuItem(text="👤 Mon Profil", on_click=lambda _: page.go("/page_etu_profil")),
                        ft.PopupMenuItem(text="📊 Stats", on_click=lambda _: page.go("/page_etu_stats")),
                        ft.PopupMenuItem(text="📚 Pointage", on_click=lambda _: page.go("/page_marquer_presence")),
                        ft.PopupMenuItem(text="⚙️ Paramètres", on_click=lambda _: page.go("/page_etu_propos")),
                        ft.PopupMenuItem(text="❓ Aide", on_click=lambda _: page.go("/page_etu_propos"))
                    ]
                ),
                ft.Row([
                    search_field,
                    ft.IconButton(
                        ft.Icons.SEARCH,
                        on_click=toggle_search,
                        icon_color="white",
                        tooltip="Rechercher"
                    ),
                    ft.Stack([
                        ft.IconButton(
                            ft.Icons.NOTIFICATIONS_OUTLINED,
                            icon_color="white",
                            tooltip="Notifications",
                            on_click=lambda _: page.go('/page_etu_notif')
                        ),
                        ft.Container(
                            content=ft.Text(str(notification_count), color="black", weight=ft.FontWeight.BOLD),
                            bgcolor=ERROR_COLOR,
                            padding=ft.padding.all(4),
                            border_radius=10,
                            right=8,
                            top=8,
                            width=18,
                            height=18,
                            alignment=ft.alignment.center
                        ) if notification_count > 0 else ft.Container()
                    ])
                ], spacing=5)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Container(height=20),
            
            ft.Column([
                ft.Text(
                    f"Bonjour {user.get('prenom', 'Étudiant')} ! 👋",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                    text_align=ft.TextAlign.CENTER
                ),
              
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ]),
        padding=ft.padding.all(20),
        height=200,
        bgcolor="#274192",
        border_radius=ft.border_radius.only(bottom_left=30, bottom_right=30)
    )

    def create_shortcut_card(title, subtitle, icon_name, color, route):
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Icon(icon_name, size=40, color=color),
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(bottom=10)
                ),
                ft.Text(title, color=CARD_COLOR, size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    width=page.width * 0.35,
                    height=5,
                    bgcolor=color,
                    border_radius=20,
                    padding=ft.padding.all(5),
                    content=ft.Container(bgcolor=color)
                ),
                ft.Text(subtitle, size=12, color=TEXT_SECONDARY, text_align=ft.TextAlign.CENTER)
            ], spacing=10),
            border_radius=20,
            bgcolor=PRIMARY_COLOR,
            height=171,
            width=page.width * 0.4,
            padding=15,
            ink=True,
            on_click=lambda _: page.go(route)
        )

    shortcuts_grid = ft.ResponsiveRow([
        create_shortcut_card(
            "Stats",
            "Voir vos statistiques",
            "bar_chart",
            SUCCESS_COLOR,
            "/page_etu_stats"
        ),
        create_shortcut_card(
            "Emploi du Temps",
            "Planning des cours",
            "calendar_today",
            SUCCESS_COLOR,
            "/page_etu_emploi"
        )
    ], spacing=15, alignment=ft.MainAxisAlignment.CENTER)

    shortcuts_grid2 = ft.ResponsiveRow([
        create_shortcut_card(
            "Profil",
            "Voir et modifier vos informations",
            "person",
            "#eb06ff",
            "/page_etu_profil"
        ),
        create_shortcut_card(
            "Pointage",
            "Voir vos pointages",
            "fingerprint",
            "#eb06ff",
            "/page_marquer_presence"
        )
    ], spacing=15, alignment=ft.MainAxisAlignment.CENTER)

    def create_announcement_card(title, content, date, priority="normal"):
        priority_Colors = {
            "high": ERROR_COLOR,
            "medium": WARNING_COLOR,
            "normal": ACCENT_COLOR
        }
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    width=4,
                    height=60,
                    bgcolor=priority_Colors.get(priority, ACCENT_COLOR),
                    border_radius=2
                ),
                ft.Column([
                    ft.Text(title, size=14, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                    ft.Text(content, size=12, color=TEXT_SECONDARY, max_lines=2),
                    ft.Text(date, size=10, color=TEXT_SECONDARY, italic=True)
                ], spacing=2, expand=True)
            ], spacing=10),
            bgcolor=CARD_COLOR,
            padding=ft.padding.all(15),
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=CARD_SHADOW,
                offset=ft.Offset(0, 1)
            ),
            margin=ft.margin.only(bottom=10)
        )

    announcements_section = ft.Column([
        ft.Text("📢 Actualités & Annonces", size=18, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
        ft.Container(height=10),
        create_announcement_card(
            "Examens de fin de semestre",
            "Les inscriptions aux examens sont ouvertes jusqu'au 15 décembre",
            "Il y a 2 heures",
            "high"
        ),
        create_announcement_card(
            "Nouvelle ressource disponible",
            "Cours de mathématiques avancées - Chapitre 5 ajouté",
            "Hier",
            "normal"
        ),
        create_announcement_card(
            "Rappel: Projet à rendre",
            "N'oubliez pas de rendre votre projet de programmation",
            "Il y a 3 jours",
            "medium"
        )
    ])

    def create_stat_card(value, label, icon, color):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=30, color=color),
                ft.Text(str(value), size=24, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                ft.Text(label, size=12, color=TEXT_SECONDARY, text_align=ft.TextAlign.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            bgcolor=CARD_COLOR,
            padding=ft.padding.all(15),
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=CARD_SHADOW,
                offset=ft.Offset(0, 1)
            ),
            width=page.width * 0.2
        )

    stats_row = ft.ResponsiveRow([
        create_stat_card("14.5", "Moyenne", "trending_up", SUCCESS_COLOR),
        create_stat_card("6", "Cours", "menu_book", PRIMARY_COLOR),
        create_stat_card("92%", "Assiduité", "assignment_turned_in", ACCENT_COLOR),
        create_stat_card("3", "Projets", "work", WARNING_COLOR)
    ], spacing=10, alignment=ft.MainAxisAlignment.SPACE_AROUND)

    main_content = ft.Column([
        header,
        ft.Container(height=20),
        ft.Container(
            content=ft.Column([
                ft.Text("🚀 Accès Rapide", size=18, weight=ft.FontWeight.BOLD, color="white"),
                ft.Container(height=10),
                shortcuts_grid,
                ft.Container(height=10),
                shortcuts_grid2
            ]),
            padding=ft.padding.symmetric(horizontal=20)
        ),
        ft.Container(height=20),
        ft.Container(
            content=ft.Column([
                ft.Text("📊 Aperçu", size=18, weight=ft.FontWeight.BOLD, color="white"),
                ft.Container(height=10),
                stats_row
            ]),
            padding=ft.padding.symmetric(horizontal=20)
        ),
        ft.Container(height=20),
        ft.Container(
            content=announcements_section,
            padding=ft.padding.symmetric(horizontal=20)
        ),
        ft.Container(height=20),
        ft.Container(height=100)
    ], scroll=ft.ScrollMode.AUTO, expand=True)

    def navigation_changed(e):
        routes = {
            0: "/page_etu_acc",
            1: "/page_marquer_presence",
            2: "/page_etu_stats",
            3: "/page_etu_profil"
        }
        selected_route = routes.get(e.control.selected_index)
        if selected_route:
            try:
                page.go(selected_route)
            except Exception as ex:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Erreur de navigation: {str(ex)}"),
                    bgcolor=ERROR_COLOR,
                    color="white"
                )
                page.snack_bar.open = True
                page.update()

    navigation_bar = ft.CupertinoNavigationBar(
        bgcolor=ft.Colors.WHITE,
        inactive_color=ft.Colors.BLACK,
        active_color=ft.Colors.BLUE,
        on_change=navigation_changed,
        destinations=[
            ft.NavigationBarDestination(
                icon="home_rounded",
                selected_icon="home_rounded",
                label="Accueil"
            ),
            ft.NavigationBarDestination(
                icon="fingerprint",
                selected_icon="fingerprint",
                label="Pointage"
            ),
            ft.NavigationBarDestination(
                icon="show_chart",
                selected_icon="show_chart",
                label="Statistiques"
            ),
            ft.NavigationBarDestination(
                icon="person_2",
                selected_icon="person_2",
                label="Profil"
            ),
        ],
    )
    
    return [
        ft.Stack([
            main_content,
            ft.Container(
                alignment=ft.alignment.bottom_center,
                bottom=0,
                left=0,
                right=0,
                content=navigation_bar
            )
        ], expand=True)
    ]