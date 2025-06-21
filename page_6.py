from flet import *

def page_6(page: Page):
    BG = '#041955'
    FG = '#3450a1'
    ICON_COLOR = FG  # Couleur des icônes (bleu)
    FOCUS_COLOR = 'black'  # Couleur pour l'icône active

    # Variable d'état pour contrôler la visibilité du champ de recherche
    search_visible = False

    # Variable pour le nombre de notifications
    notification_count = 3  # Exemple : 3 notifications

    def change(e):
        page.go('/page6')

    def aller(e):
        page.go('/page7')

    def profi(e):
        page.go('/page8')

    def home(e):
        page.go('/page9')

    def parametres(e):
        page.go('/page_connexion0')  # Ajoutez une route pour les paramètres

    def a_propos(e):
        page.go('/page_connexion1')  # Ajoutez une route pour "À propos de"

    # Fonction pour gérer la recherche
    def rechercher(e):
        nonlocal search_visible
        search_visible = not search_visible  # Bascule la visibilité
        search_field.visible = search_visible  # Met à jour la visibilité du champ
        page.update()  # Met à jour la page

    # Champ de saisie pour la recherche
    search_field = TextField(
        label="Rechercher",
        hint_text="Entrez votre recherche ici",
        visible=search_visible,  # Contrôle la visibilité
    )

    # Définition des icônes et textes
    rech = IconButton(
        icon=Icons.SEARCH,
        on_click=rechercher,  # Appelle la fonction rechercher
    )

    # Icône de notification avec badge personnalisé
    noti = Stack(
        controls=[
            Icon(Icons.NOTIFICATIONS_OUTLINED),  # Icône de notification
            Container(
                content=Text(
                    str(notification_count),  # Nombre de notifications
                    size=12,
                    color="white",
                ),
                alignment=alignment.top_right,  # Positionne le badge en haut à droite
                bgcolor="red",  # Couleur de fond du badge
                padding=padding.all(4),  # Espacement interne
                border_radius=50,  # Rend le badge circulaire
            ),
        ],
    )

    # Menu déroulant
    menu_deroulant = PopupMenuButton(
        items=[
            PopupMenuItem(
                content=Text("Accueil"),
                on_click=change,
            ),
            PopupMenuItem(
                content=Text("Profil"),
                on_click=home,
            ),
            PopupMenuItem(
                content=Text("Paramètres"),
                on_click=parametres,
            ),
            PopupMenuItem(
                content=Text("À propos de"),
                on_click=a_propos,
            ),
        ],
        icon=Icons.MENU,  # Icône du menu
    )

    txt1 = Text('Welcome user', size=30)
    txt2 = Text('Boite de réception', size=20)
    txt3 = Text('Deconection',size=10,color='white')
    saut = Container(height=30)
    sauti = Container(height=2)
    saute = Container(height=100)
    retour = Icon(Icons.ARROW_BACK, color='white')


    # Création des blocs de statistiques
    ress = Column(
        controls=[Container(expand=True, height=50, border_radius=30, bgcolor='white') for _ in range(4)]
    )

    # Création de la boîte cliquable
    box = Container(
        content=Row([txt2], alignment=MainAxisAlignment.CENTER),
        width=200,
        height=100,
        bgcolor=BG,
        border_radius=30,
        on_click=aller,
    )
    deco = Container(
        content=Row([txt3], alignment=MainAxisAlignment.CENTER),
        width=70,
        height=30,
        bgcolor='black',
        border_radius=15,
    )

    # Barre de navigation avec texte sous les icônes
    nav_bar = Container(
    content=Row(
        controls=[
            Container(
                content=Column(
                    controls=[
                        Icon(Icons.HOME, color=FOCUS_COLOR if page.route == '/page6' else ICON_COLOR),
                        Text("Accueil", size=12, color=FOCUS_COLOR if page.route == '/page6' else ICON_COLOR),
                    ],
                    spacing=5,  # Espace entre l'icône et le texte
                    horizontal_alignment=CrossAxisAlignment.CENTER,  # Centrer horizontalement
                ),
                on_click=lambda e: page.go('/page6'),  # Redirige vers la page d'accueil
                padding=10,
            ),
            Container(
                content=Column(
                    controls=[
                        Icon(Icons.BAR_CHART, color=FOCUS_COLOR if page.route == '/page8' else ICON_COLOR),
                        Text("Stats", size=12, color=FOCUS_COLOR if page.route == '/page8' else ICON_COLOR),
                    ],
                    spacing=5,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
                on_click=lambda e: page.go('/page8'),  # Redirige vers la page des stats
                padding=10,
            ),
            Container(
                content=Column(
                    controls=[
                        Icon(Icons.PERSON, color=FOCUS_COLOR if page.route == '/page9' else ICON_COLOR),
                        Text("Profil", size=12, color=FOCUS_COLOR if page.route == '/page9' else ICON_COLOR),
                    ],
                    spacing=5,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
                on_click=lambda e: page.go('/page9'),  # Redirige vers la page de profil
                padding=10,
            ),
            Container(
                content=Column(
                    controls=[
                        Icon(Icons.FINGERPRINT, color=FOCUS_COLOR if page.route == '/page7' else ICON_COLOR),
                        Text("Pointage", size=12, color=FOCUS_COLOR if page.route == '/page7' else ICON_COLOR),
                    ],
                    spacing=5,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
                on_click=lambda e: page.go('/page7'),  # Redirige vers la page de pointage
                padding=10,
            ),
        ],
        alignment=MainAxisAlignment.SPACE_AROUND,
    ),
    bgcolor='white',  # Fond de la barre en blanc
    padding=5,
    border_radius=20,
)

    # Structure principale de la page
    tout = Column(
        controls=[
            # Barre du haut avec les icônes
            Row(
                controls=[
                    menu_deroulant,  # Remplacement de `men` par le menu déroulant
                    Row([search_field, rech, noti], spacing=10),  # Ajout du champ de saisie
                ],
                alignment=MainAxisAlignment.SPACE_BETWEEN,
            ),
            txt1,
            sauti,
            box,
            sauti,
            ress,
            sauti,
            deco,
            saute,
            Container(expand=True),  # Espace vide pour pousser state vers le bas
            Container(  # Container pour centrer state en bas
                alignment=alignment.center,
                padding=padding.only(bottom=20)  # Petit espace en bas
            ),
            nav_bar,  # Ajout de la barre de navigation
        ],
        expand=True  # Permet au Column de remplir la hauteur
    )

    return [tout]