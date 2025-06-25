import flet as ft

BG = "#041955"  # Bleu foncé
FWG = "#FFFFFF"  # Blanc
FG = "#3450a1"   # Bleu clair
PINK = "#eb06ff"  # Rose

def page_etu_propos(page: ft.Page, etudiant_connecte=None):
    page.title = "À propos"
    page.bgcolor = BG
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # Header avec bouton retour
    header = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK, 
                icon_color=FWG, 
                on_click=lambda _: page.go('/page_etu_acc'),
                tooltip="Retour"
            ),
            ft.Text("À propos de l'application", 
                   size=24, 
                   weight=ft.FontWeight.BOLD,
                   color=FWG,
                   expand=True,
                   text_align=ft.TextAlign.CENTER),
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Carte pour chaque section
    def create_card(title, content, color=BG):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            title=ft.Text(title, 
                                        weight=ft.FontWeight.BOLD,
                                        color=FWG),
                        ),
                        ft.Divider(height=1, color="white24"),
                        content,
                    ]
                ),
                padding=15,
            ),
            color=color,
            elevation=10,
            width=400 if page.width < 600 else 800,
        )

    # Section description
    description_card = create_card(
        "Description",
        ft.Text(
            "Notre application est conçue pour le pointage des étudiants avec une interface intuitive et des fonctionnalités puissantes.",
            color=FWG,
            size=16
        )
    )

    # Section fonctionnalités
    features_content = ft.Column(
        controls=[
            ft.ListTile(
                leading=ft.Icon(ft.Icons.CHECK_CIRCLE, color=PINK),
                title=ft.Text("Pointage des étudiants", color=FWG),
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.CHECK_CIRCLE, color=PINK),
                title=ft.Text("Gestion de la liste de présence", color=FWG),
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.CHECK_CIRCLE, color=PINK),
                title=ft.Text("Statistiques et rapports", color=FWG),
            ),
        ],
        spacing=5,
    )

    features_card = create_card(
        "Fonctionnalités principales",
        features_content
    )

    # Section équipe
    def create_team_member(name, role, icon=ft.Icons.PERSON):
        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(icon, size=40, color=PINK),
                ft.Text(name, size=16, weight=ft.FontWeight.BOLD, color=FWG),
                ft.Text(role, size=14, color=FWG),
            ],
            spacing=5,
        )

    team_content = ft.ResponsiveRow(
        controls=[
            create_team_member("DAO KARIM", "Développeur principal", ft.Icons.CODE),
            create_team_member("Gneto Schiphra Grace", "Designer UX/UI", ft.Icons.DESIGN_SERVICES),
            create_team_member("Diomande Hamed Meloua", "Chef de Projet", ft.Icons.PERSON),
            create_team_member("Kadjo Allouan Moise Bienvenue", "Analyste", ft.Icons.ANALYTICS),
        ],
        spacing=20,
        run_spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    team_card = create_card(
        "Notre équipe",
        team_content
    )

    # Section contact
    contact_content = ft.Column(
        controls=[
            ft.Text("Pour toute question ou commentaire :", color=FWG),
            ft.Text("projetpointage@gmail.com", 
                   color=PINK,
                   weight=ft.FontWeight.BOLD,
                   size=16),
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.EMAIL,
                        icon_color=PINK,
                        tooltip="Envoyer un email"
                    ),
                    ft.IconButton(
                        icon=ft.Icons.PHONE,
                        icon_color=PINK,
                        tooltip="Nous appeler"
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            )
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    contact_card = create_card(
        "Contactez-nous",
        contact_content
    )

    # Contenu principal
    main_content = ft.Column(
        controls=[
            header,
            ft.Divider(height=20, color="transparent"),
            description_card,
            ft.Divider(height=20, color="transparent"),
            features_card,
            ft.Divider(height=20, color="transparent"),
            team_card,
            ft.Divider(height=20, color="transparent"),
            contact_card,
        ],
        spacing=20,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return [main_content]