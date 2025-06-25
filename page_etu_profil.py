import flet as ft
from flet import (
    AlertDialog,
    alignment,
    border,
    BorderSide,
    BoxShadow,
    ButtonStyle,
    CircleAvatar,
    Column,
    Container,
    CrossAxisAlignment,
    CupertinoNavigationBar,
    ElevatedButton,
    FontWeight,
    Icon,
    IconButton,
    LinearGradient,
    MainAxisAlignment,
    NavigationBarDestination,
    Offset,
    padding,
    RoundedRectangleBorder,
    Row,
    ScrollMode,
    SnackBar,
    Stack,
    Text,
    TextAlign,
    TextButton,
    TextStyle,
    View
)

def page_etu_profil(page: ft.Page, etudiant_connecte=None):
    page.adaptive = True
    page.title = "Profil Étudiant"
    
    # Palette de couleurs
    primary_color = "#667eea"  # Bleu-violet moderne
    secondary_color = "#041955"  # Bleu foncé
    other_color = "#2BC2A9"  # Vert menthe
    background_color = "#3450a1"  # Bleu background
    card_color = "#041955"
    card_color2 = "#1C3989"  # Bleu clair pour les cartes
    text_light = "#ffffff"  # Blanc
    shadow_color = "#516ec5"  # Gris clair pour ombres

    # Utiliser les informations de l'étudiant connecté ou les valeurs par défaut
    if etudiant_connecte and isinstance(etudiant_connecte, dict):
        user = etudiant_connecte
    else:
        # Essayer de récupérer depuis la session
        user = page.session.get("user") or {
            "nom": "Doe",
            "prenom": "John",  
            "email": "non.defini@example.com",
            "numero": "Non défini",
            "adresse": "Non définie",
            "profession": "Étudiant",
            "IP": "Non définie"
        }
    
    # Fonction pour créer un gradient
    def create_gradient_container(content, colors_list):
        return Container(
            content=content,
            gradient=LinearGradient(
                begin=alignment.top_left,
                end=alignment.bottom_right,
                colors=colors_list
            ),
            border_radius=15,
            shadow=BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=shadow_color,
                offset=Offset(0, 4)
            )
        )

    # Fonction pour gérer les clics sur la barre de navigation
    def navigation_changed(e):
        try:
            if e.control.selected_index == 0:
                page.go("/page_etu_acc")  # Accueil
            elif e.control.selected_index == 1:
                page.go("/page_marquer_presence")  # Pointage
            elif e.control.selected_index == 2:
                page.go("/page_etu_stats")  # Statistiques
            elif e.control.selected_index == 3: 
                page.go("/page_etu_profil")  # Profil
        except Exception as ex:
            print(f"Navigation error: {ex}")
    
    # Barre de navigation
    navigation_bar = CupertinoNavigationBar(
        bgcolor="white",
        inactive_color="black",
        active_color="blue",
        selected_index=3,  # Profil sélectionné
        on_change=navigation_changed,
        destinations=[
            NavigationBarDestination(
                icon="home_rounded",
                selected_icon="home_rounded",
                label="Accueil"
            ),
            NavigationBarDestination(
                icon="fingerprint",
                selected_icon="fingerprint",
                label="Pointage"
            ),
            NavigationBarDestination(
                icon="show_chart",
                selected_icon="show_chart",
                label="Statistiques"
            ),
            NavigationBarDestination(
                icon="person_2",
                selected_icon="person_2",
                label="Profil"
            ),
        ],
    )

    # Les informations de l'étudiant depuis la session
    infos_etudiant = [
        user["nom"],
        user["prenom"],
        user["numero"],
        user["email"],
        user.get("adresse", "N/A")
    ]
    
    det_infos_etudiant = ["Nom", "Prénoms", "Numéro de téléphone", "Email", "Adresse"]
    icones_infos = ["badge", "person", "phone", "email", "home"]

    # En-tête avec avatar
    header = create_gradient_container(
        Column(
            controls=[
                Container(height=20),
                CircleAvatar(
                    radius=50,
                    bgcolor=card_color,
                    content=Icon("person", size=60, color=primary_color)
                ),
                Container(height=15),
                Text(
                    f"{user['prenom']} {user['nom']}",
                    size=24,
                    weight=FontWeight.BOLD,
                    color=text_light,
                    text_align=TextAlign.CENTER
                ),
                Text(
                    user.get("profession", "Étudiant"),
                    size=16,
                    color=text_light,
                    text_align=TextAlign.CENTER,
                    opacity=0.9
                ),
                Container(height=20),
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER,
        ),
        [primary_color, secondary_color]
    )

    # Conteneur des informations
    info_cards = Column(spacing=15)
    
    for info, label, icon in zip(infos_etudiant, det_infos_etudiant, icones_infos):
        info_content = Row(
            controls=[
                Container(
                    width=50,
                    height=50,
                    bgcolor=f"{other_color}15",  # Fond vert menthe avec transparence
                    border_radius=25,
                    content=Icon(icon, color=other_color, size=24),
                    alignment=alignment.center
                ),
                Container(width=15),
                Column(
                    controls=[
                        Text(label, size=12, color=other_color, weight=FontWeight.W_500),
                        Text(str(info), size=16, color=text_light, weight=FontWeight.BOLD)
                    ],
                    spacing=2,
                    expand=True
                )
            ],
            alignment=MainAxisAlignment.START
        )
        
        info_card = create_gradient_container(
            content=Container(
                content=info_content,
                padding=20
            ),
            colors_list=[card_color2, card_color]
        )
        
        info_cards.controls.append(info_card)



    # Bouton de déconnexion
    action_buttons = Column(
            controls=[
                Container(
                    content=ElevatedButton(
                        "Se déconnecter",
                        icon="LOGOUT",
                        on_click=lambda _:page.go('/page_bienvenue'),
                        style=ButtonStyle(
                            bgcolor=other_color,
                            color=text_light,
                            shape=RoundedRectangleBorder(radius=25),
                            padding=padding.symmetric(horizontal=25, vertical=12)
                        )
                    ),
                    alignment=alignment.center
                )
            ]
        )

    # Bouton de retour
    retour = IconButton(
        icon="arrow_back",
        icon_color=text_light,
        on_click=lambda _: page.go("/page_etu_acc"),
        tooltip="Retour",
        icon_size=30
    )

    # Conteneur principal avec scroll
    main_content = Container(
        bgcolor=background_color,
        expand=True,
        content=Column(
            controls=[
                Container(
                    content=retour,
                    padding=padding.only(left=10, top=10)
                ),
                Container(height=10),
                Container(
                    padding=padding.symmetric(horizontal=20),
                    content=header
                ),
                Container(height=20),
                Container(
                    padding=padding.symmetric(horizontal=20),
                    content=Column(
                        controls=[
                            Text("Informations personnelles", 
                                size=20, 
                                weight=FontWeight.BOLD, 
                                color=other_color),
                            Container(height=10),
                            info_cards,
                            Container(height=20),
                            action_buttons,
                            Container(height=100)  # Espace pour la navigation bar
                        ]
                    )
                )
            ],
            scroll=ScrollMode.AUTO
        )
    )

    # Créer la structure de la page avec la barre de navigation
    page_structure = [
        Stack(
            controls=[
                main_content,
                Container(
                    content=navigation_bar,
                    alignment=alignment.bottom_center,
                    bottom=0,
                    left=0,
                    right=0
                )
            ],
            expand=True
        )
    ]
    
    return page_structure