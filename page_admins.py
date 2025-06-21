import flet as ft
from db_config import DB_CONFIG
from flet import *
from fonction import *
from datetime import datetime


def page_admins(page: Page):
    # Color scheme
    BG = '#041955'
    FOND = '#3450a1'
    BULLE = '#2BC2A9'
    SUCCESS_COLOR = '#2BC2A9'
    TEXT_BLANC = 'white'
    TEXT_NOIR = 'black'
    COULEUR_BACKGROUND = "#C9BFBF"
    primary_color = "#667eea"  # Bleu-violet moderne
    secondary_color = "#041955"  # Bleu foncé
    other_color = "#2BC2A9"  # Vert menthe
    other_color3 = "#2BC2A9"  # Rose vif
    accent_color = "#4facfe"  # Bleu clair
    background_color = "#3450a1"  # Fond bleu
    card_color = "#041955"  # Bleu foncé pour cartes
    card_color2 = "#1C3989"  # Bleu moyen pour gradients
    text_primary = "#f9f9fa"  # Texte clair
    text_secondary = "#f8fafd"  # Texte secondaire
    text_light = "#ffffff"  # Blanc
    shadow_color = "#516ec5"  # Ombre
    page.adaptive = True
    page.bgcolor = BG

    user = page.session.get("user")
    if user and "nom" in user and "prenom" in user:
        name = str(user["nom"]) + " " + str(user["prenom"])
    else:
        name = "Kone Awa"


    # Fonction pour créer un conteneur avec gradient
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

    # Fonction pour créer une carte moderne
    def create_modern_card(content, padding_val=20, margin_val=10):
        return Container(
            content=content,
            padding=padding_val,
            margin=margin_val,
            border_radius=15,
            gradient=LinearGradient(
                begin=alignment.top_left,
                end=alignment.bottom_right,
                colors=[card_color2, card_color]
            ),
            shadow=BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=shadow_color,
                offset=Offset(0, 3)
            )
        )

    # Fonction pour créer un titre de section
    def create_section_title(title, icon=None):
        title_controls = []
        if icon:
            title_controls.append(Icon(icon, color=other_color, size=28))
            title_controls.append(Container(width=10))
        title_controls.append(
            Text(title, size=24, weight=FontWeight.BOLD, color=text_light)
        )
        
        return Container(
            content=Row(
                controls=title_controls,
                alignment=MainAxisAlignment.START,
            ),
            margin=ft.margin.only(bottom=20, top=10)
        )

    # En-tête du profil
    header = create_gradient_container(
        Column(
            controls=[
                Container(height=20),
                CircleAvatar(
                    radius=50,
                    bgcolor=card_color,
                    content=Icon(Icons.PERSON, size=60, color=primary_color)
                ),
                Container(height=15),
                Text(
                    name,
                    size=24,
                    weight=FontWeight.BOLD,
                    color=text_light,
                    text_align=TextAlign.CENTER
                ),
                Text(
                    "Administrateur",
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

    list_ad = infos_utilisateur("administration")
    list_administration = [f"{admin[1]} {admin[2]}" for admin in list_ad]

    # Fetch admin info
    def infos(name):
        index = list_administration.index(name)
        return [
            list_ad[index][1],  # nom
            list_ad[index][2],  # prenoms
            list_ad[index][4],  # numero
            list_ad[index][3],  # email
            list_ad[index][5]   # adresse
        ]
        
    # Admin info display
    infos_admin = infos(name)
    det_infos_admin = ["Nom", "Prénoms", "Numéro de téléphone", "Email", "Adresse"]
    
    # Conteneur des informations
    info_cards = Column(spacing=15)
    icones_infos = [Icons.BADGE, Icons.PERSON, Icons.PHONE, Icons.EMAIL, Icons.HOME]

    for info, label, icon in zip(infos_admin, det_infos_admin, icones_infos):
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
                        Text(str(info), size=16, color=text_primary, weight=FontWeight.BOLD)
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
    # Bouton retour
    retour = Container(
        content=IconButton(
            icon=Icons.ARROW_BACK_IOS,
            icon_color=text_primary,
            on_click=lambda _: page.go('/page_accueil_admin'),
            style=ButtonStyle(
                shape=CircleBorder(),
                bgcolor=card_color,
                shadow_color=shadow_color
            )
        ),
        padding=padding.only(left=10, top=10)
    )
    
    # Conteneur principal
    main_content = Container(
        bgcolor=background_color,
        expand=True,
        content=Column(
            controls=[
                retour,
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
                            Container(height=100)  # Espace pour la navigation
                        ]
                    )
                )
            ],
            scroll=ScrollMode.AUTO
        )
    )    
    
    # Generate list container (modernisé)
    def gener_cont_list(items, chemin):
        conteneur = Column(height=400, scroll='auto', spacing=10)
        
        for i in items:
            card_content = Container(
                content=Row(
                    controls=[
                        Icon(Icons.PERSON if chemin == "ens" else Icons.SCHOOL,color=text_light, size=20),
                        Container(width=10),
                        Text(i, color=text_light, size=16, weight=FontWeight.W_500),
                        Icon(Icons.ARROW_FORWARD_IOS, color=text_light, size=16)
                    ],
                    alignment=MainAxisAlignment.START,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                    
                ),
                padding=15,
                border_radius=12,
                gradient=LinearGradient(
                    begin=alignment.center_left,
                    end=alignment.center_right,
                    colors=[BULLE, accent_color]
                ),
                shadow=BoxShadow(
                    spread_radius=0,
                    blur_radius=4,
                    color=shadow_color,
                    offset=Offset(0, 2)
                ),
                on_click=lambda e, name=i: page.go(f"/{chemin}/{name}")
            )
            conteneur.controls.append(card_content)
            
        return conteneur

    conteneur_profil = Column(height=400, scroll='auto',
           controls=[
              Container(
                content=Row(controls=[Icon(Icons.PERSON, color=TEXT_NOIR, size=50)]),
                padding=15,
                alignment=alignment.center
            )
        ])

    for i, j in zip(infos_admin, det_infos_admin):
        conteneur_profil.controls.extend([
            Text(f"{j} :", color=TEXT_NOIR, size=16),
            Container(
                adaptive=True,
                border_radius=10,
                bgcolor=BULLE,
                height=50,
                padding=padding.symmetric(horizontal=15),
                content=Row(controls=[Text(i, color=TEXT_BLANC, size=16)])
            )
        ])


    is_mobile = page.width < 600
    button_rech_width = 300 if not is_mobile else 170
    button_rech_enter = 50 if not is_mobile else 40
    image_width = 200 if not is_mobile else 150




    # UI Controls (modernisés)
    champ_recherche = TextField(
        label="Rechercher",
        border_radius=12,
        border_color=other_color,
        focused_border_color=primary_color,
        text_style=TextStyle(color=text_light),
        label_style=TextStyle(color=text_secondary),
        bgcolor=card_color,
        prefix_icon=Icons.SEARCH,
        width=button_rech_width
    )
    
    bouton_recherche = ElevatedButton(
        " ",
        icon=Icons.SEARCH,
        style=ButtonStyle(
            bgcolor=other_color,
            color=text_light,
            shape=RoundedRectangleBorder(radius=40),
            padding=padding.symmetric(horizontal=20, vertical=12)
        ),
        on_click=lambda e: rechercher_enseignant()
    )
    
    list_ens = infos_utilisateur("enseignant")        
    list_enseignant = []
    for i in range(len(list_ens)):
        ch = str(list_ens[i][2]) + ' ' + str(list_ens[i][3])
        list_enseignant.append(ch)
    
    list_et = infos_utilisateur("etudiant")        
    list_etudiant = []
    for i in range(len(list_et)):
        ch = str(list_et[i][3]) + ' ' + str(list_et[i][4])
        list_etudiant.append(ch)
            
    cont_ens = gener_cont_list(list_enseignant, "ens")
    cont_etu = gener_cont_list(list_etudiant, "etu")

    list_statistique = stat_ens() 
    element_stat = []     
    for i in range(len(list_statistique)):
        element_stat.append(list_statistique[i][0])
        
    # Search function
    def rechercher_enseignant():
        recherche = champ_recherche.value.lower().strip()
        resultats = [ens for ens in list_enseignant if recherche in ens.lower()]
        cont_ens.controls.clear()
        if resultats:
            cont_ens.controls.extend(gener_cont_list(resultats, "ens").controls)
        else:
            no_result_card = Container(
                content=Column(
                    controls=[
                        Icon(Icons.SEARCH_OFF, size=48, color=text_secondary),
                        Container(height=10),
                        Text("Aucun résultat trouvé", color=text_secondary, size=16, weight=FontWeight.W_500),
                        Text("Essayez avec d'autres mots-clés", color=text_secondary, size=12)
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=5
                ),
                padding=30,
                alignment=alignment.center
            )
            cont_ens.controls.append(no_result_card)
        page.update()

    # Navigation bar with four elements
    def create_navigation_bar(selected_index=0):
        return CupertinoNavigationBar(
            bgcolor=Colors.WHITE,
            inactive_color=Colors.BLACK,
            active_color=Colors.BLUE,
            on_change=lambda e: page.go({
                0: "/page_accueil_admin",
                1: "/page_list_enseignant",
                2: "/page_list_etudiant",
                3: "/page_profil_admin"
            }.get(e.control.selected_index, "/page_list_enseignant")),
            destinations=[
                NavigationBarDestination(
                    icon=Icon(Icons.HOME_ROUNDED, color="black"),
                    selected_icon=Icon(Icons.HOME_ROUNDED, color="BLUE"),
                    label="Accueil"
                ),
                NavigationBarDestination(
                    icon=Icon(Icons.VIEW_LIST, color="black"),
                    selected_icon=Icon(Icons.VIEW_LIST, color="BLUE"),
                    label="Enseignants"
                ),
                NavigationBarDestination(
                    icon=Icon(Icons.VIEW_LIST, color="black"),
                    selected_icon=Icon(Icons.VIEW_LIST, color="BLUE"),
                    label="Etudiants"
                ),
                NavigationBarDestination(
                    icon=Icon(Icons.PERSON_2, color="black"),
                    selected_icon=Icon(Icons.PERSON_2, color="BLUE"),
                    label="Profil"
                ),
            ],
            selected_index=selected_index
        )

    # Fonction pour générer une liste d'étudiants (modernisée)
    def gener_cont_matiere(name):
        index = list_enseignant.index(name)
        id = list_ens[index][0]        
        conteneur = Column(scroll='auto', spacing=8)
        date_cours,matiere,heure_debut_cours,heure_fin_cours,NA = emploi_du_temps_prof(id)
        
        list_id,date,heure_debut,heure_fin,NA= infos_presence_enseignant() 
        heure_actuelle = datetime.now().time()
        date_actuelle = datetime.now().date()
        
        stat_cours = ("En cours", "Effectué", "Non effectué", "À venir")
        status_colors = [accent_color, "#4CAF50", "#F44336", other_color]
        
        for i, j, k, l in zip(date_cours, matiere, heure_debut_cours, heure_fin_cours):
            # Déterminer le statut et la couleur
            if id in list_id and str(date[list_id.index(id)])[:10] == str(i) and str(heure_debut)[:2] == str(heure_debut_cours)[:2] and str(heure_fin)[:2] > str(heure_actuelle)[:2]:
                status_text = stat_cours[0]
                status_color = status_colors[0]
            elif id in list_id and str(date[list_id.index(id)])[:10] == str(i) and str(heure_debut)[:2] == str(heure_debut_cours)[:2]:
                status_text = stat_cours[1]
                status_color = status_colors[1]
            elif id not in list_id and str(i) > str(date_actuelle):
                status_text = stat_cours[3]
                status_color = status_colors[3]
            elif id in list_id and str(i) > str(date_actuelle):
                status_text = stat_cours[3]
                status_color = status_colors[3]
            else:
                status_text = stat_cours[2]
                status_color = status_colors[2]
            
            # Créer la carte du cours
            course_card = Container(
                content=Row(
                    controls=[
                        Container(
                            content=Column(
                                controls=[
                                    Icon(Icons.CALENDAR_TODAY, color=text_light, size=16),
                                    Text(str(i), size=12, color=text_light, weight=FontWeight.W_500)
                                ],
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                spacing=5
                            ),
                            padding=8,
                            border_radius=8,
                            bgcolor=f"{primary_color}50",
                            expand=True,
                        ),
                        Container(
                            content=Column(
                                controls=[
                                    Icon(Icons.BOOK, color=text_light, size=16),
                                    Text(str(j), size=12, color=text_light, weight=FontWeight.W_500)
                                ],
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                spacing=5
                            ),
                            padding=8,
                            border_radius=8,
                            bgcolor=f"{secondary_color}80",
                            expand=True,
                        ),
                        Container(
                            content=Column(
                                controls=[
                                    Icon(Icons.ACCESS_TIME, color=text_light, size=16),
                                    Text(f"{k} - {l}", size=12, color=text_light, weight=FontWeight.W_500)
                                ],
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                spacing=5
                            ),
                            padding=8,
                            border_radius=8,
                            bgcolor=f"{accent_color}60",
                            expand=True,
                        ),
                        Container(
                            content=Column(
                                controls=[
                                    Icon(Icons.CHECK_CIRCLE if "effectué" in status_text.lower() or "cours" in status_text.lower() 
                                         else Icons.SCHEDULE if "venir" in status_text.lower() 
                                         else Icons.CANCEL,
                                         color=text_light, size=16),
                                    Text(status_text, size=12, color=text_light, weight=FontWeight.W_500)
                                ],
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                spacing=5
                            ),
                            padding=8,
                            border_radius=8,
                            bgcolor=status_color,
                            expand=True,
                        ),
                    ],
                    spacing=8,
                ),
                padding=12,
                border_radius=12,
                gradient=LinearGradient(
                    begin=alignment.top_left,
                    end=alignment.bottom_right,
                    colors=[card_color2, card_color]
                ),
                shadow=BoxShadow(
                    spread_radius=1,
                    blur_radius=4,
                    color=shadow_color,
                    offset=Offset(0, 2)
                ),
                margin=margin.symmetric(vertical=4)
            )
            conteneur.controls.append(course_card)
                
        return conteneur 


    # Fonction pour generer l'emploi du temps
    def gener_emploi_du_temps():
        conteneur_emploi_tmp = Column(height=400, scroll='auto')     
        date_cours,jours,matiere,salle,heure_deb,heure_fin=emploi_du_temps_complet()
        for i, j, k, l, m, n in zip(date_cours, jours, matiere, salle, heure_deb, heure_fin):
            card_content = Container(
                content=Row(
                    controls=[
                        Container(
                            content=Column(
                                controls=[
                                    Icon(Icons.CALENDAR_TODAY, color=text_light, size=16),
                                    Text(str(i), size=12, color=text_light, weight=FontWeight.W_500)
                                ],
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                spacing=5
                            ),
                            padding=8,
                            border_radius=8,
                            bgcolor=f"{primary_color}50",
                            expand=True,
                        ),
                        Container(
                            content=Column(
                                controls=[
                                    Icon(Icons.EVENT, color=text_light, size=16),
                                    Text(str(j), size=12, color=text_light, weight=FontWeight.W_500)
                                ],
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                spacing=5
                            ),
                            padding=8,
                            border_radius=8,
                            bgcolor=f"{secondary_color}80",
                            expand=True,
                        ),
                        Container(
                            content=Column(
                                controls=[
                                    Icon(Icons.BOOK, color=text_light, size=16),
                                    Text(str(k), size=12, color=text_light, weight=FontWeight.W_500)
                                ],
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                spacing=5
                            ),
                            padding=8,
                            border_radius=8,
                            bgcolor=f"{accent_color}60",
                            expand=True,
                        ),
                        Container(
                            content=Column(
                                controls=[
                                    Icon(Icons.LOCATION_ON, color=text_light, size=16),
                                    Text(str(l), size=12, color=text_light, weight=FontWeight.W_500)
                                ],
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                spacing=5
                            ),
                            padding=8,
                            border_radius=8,
                            bgcolor=f"{other_color}50",
                            expand=True,
                        ),
                        Container(
                            content=Column(
                                controls=[
                                    Icon(Icons.ACCESS_TIME, color=text_light, size=16),
                                    Text(f"{m} - {n}", size=12, color=text_light, weight=FontWeight.W_500)
                                ],
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                spacing=5
                            ),
                            padding=8,
                            border_radius=8,
                            bgcolor=f"{other_color3}60",
                            expand=True,
                        ),
                    ],
                    spacing=8,
                ),
                padding=12,
                border_radius=12,
                gradient=LinearGradient(
                    begin=alignment.top_left,
                    end=alignment.bottom_right,
                    colors=[card_color2, card_color]
                ),
                shadow=BoxShadow(
                    spread_radius=1,
                    blur_radius=4,
                    color=shadow_color,
                    offset=Offset(0, 2)
                ),
                margin=margin.symmetric(vertical=4)
            )
                    
            conteneur_emploi_tmp.controls.append(card_content)
        return conteneur_emploi_tmp
        
    # User detail view (modernisée)
    def vue_utilisateur(name, chemin):
        infos = infos_user_connect(name, chemin)
        
        # Récupérer les statistiques de l'étudiant
        stats = None
        if chemin == 'etu':  # Si c'est un étudiant
            list_stat= stat_etu_admin()
            element_st=[]     
            for i in range(len(list_stat)):
                element_st.append(list_stat[i][0])          
            if name in element_st:
                index=element_st.index(name)
                stats = list_stat[index]
        
        # Carte d'informations utilisateur modernisée
        user_info_card = create_modern_card(
            Column(
                controls=[
                    # En-tête avec avatar
                    Row(
                        controls=[
                            CircleAvatar(
                                radius=30,
                                bgcolor=primary_color,
                                content=Icon(
                                    Icons.PERSON if chemin == 'ens' else Icons.SCHOOL,
                                    size=30,
                                    color=text_light
                                )
                            ),
                            Container(width=15),
                            Column(
                                controls=[
                                    Text(name, size=20, weight=FontWeight.BOLD, color=text_light),
                                    Text(
                                        'Professeur' if chemin == 'ens' else 'Étudiant',
                                        size=16,
                                        color=other_color,
                                        weight=FontWeight.W_500
                                    )
                                ],
                                spacing=2
                            )
                        ],
                        alignment=MainAxisAlignment.START,
                        vertical_alignment=CrossAxisAlignment.CENTER
                    ),
                    Divider(color=f"{text_secondary}30", height=20),
                    
                    # Informations détaillées
                    *[
                        Container(
                            content=Row(
                                controls=[
                                    Icon(icon, color=other_color, size=20),
                                    Container(width=12),
                                    Column(
                                        controls=[
                                            Text(label, size=12, color=text_secondary, weight=FontWeight.W_400),
                                            Text(str(value), size=16, color=text_light, weight=FontWeight.W_500)
                                        ],
                                        spacing=2
                                    )
                                ],
                                alignment=MainAxisAlignment.START
                            ),
                            padding=padding.symmetric(vertical=8)
                        )
                        for (label, value, icon) in [
                            ("Téléphone", infos[2], Icons.PHONE),
                            ("Email", infos[3], Icons.EMAIL),
                            ("Adresse", infos[4], Icons.HOME),
                            ("Statistiques", f"{stats[2]} présence(s) sur {stats[3]} ({stats[1]}%)" if stats else "Aucune présence", Icons.BOOK),
                        ]
                    ],
                ],
                spacing=8
            )
        )
        
        # Section emploi du temps
        schedule_section = Container(
            content=Column(
                controls=[
                    create_section_title("Emploi du temps", Icons.SCHEDULE),
                    
                    # En-tête du tableau
                    Container(
                        content=Row(
                            controls=[
                                Container(
                                    content=Text("Date", size=14, color=text_light, weight=FontWeight.BOLD),
                                    padding=8,
                                    alignment=alignment.center,
                                    expand=True
                                ),
                                Container(
                                    content=Text("Matière", size=14, color=text_light, weight=FontWeight.BOLD),
                                    padding=8,
                                    alignment=alignment.center,
                                    expand=True
                                ),
                                Container(
                                    content=Text("Horaire", size=14, color=text_light, weight=FontWeight.BOLD),
                                    padding=8,
                                    alignment=alignment.center,
                                    expand=True
                                ),
                                Container(
                                    content=Text("Statut", size=14, color=text_light, weight=FontWeight.BOLD),
                                    padding=8,
                                    alignment=alignment.center,
                                    expand=True
                                ),
                            ],
                            spacing=8
                        ),
                        padding=12,
                        border_radius=BorderRadius(12, 12, 0, 0),
                        gradient=LinearGradient(
                            begin=alignment.center_left,
                            end=alignment.center_right,
                            colors=[primary_color, secondary_color]
                        )
                    ),
                    
                    # Contenu de l'emploi du temps
                    Container(
                        content=gener_cont_matiere(name),
                        padding=padding.symmetric(horizontal=12, vertical=8),
                        border_radius=BorderRadius(0, 0, 12, 12),
                        bgcolor=COULEUR_BACKGROUND
                    )
                ],
                spacing=0
            ),
            margin=margin.symmetric(horizontal=10, vertical=10)
        )if chemin == "ens" else Container(
            content=Column(
                controls=[
                    create_section_title("Emploi du temps", Icons.SCHEDULE),
                    
                    # En-tête du tableau
                    Container(
                        content=Row(
                            controls=[
                                Container(
                                    content=Text("Date", size=14, color=text_light, weight=FontWeight.BOLD),
                                    padding=8,
                                    alignment=alignment.center,
                                    expand=True
                                ),
                                Container(
                                    content=Text("Jours", size=14, color=text_light, weight=FontWeight.BOLD),
                                    padding=8,
                                    alignment=alignment.center,
                                    expand=True
                                ),
                                Container(
                                    content=Text("Matière", size=14, color=text_light, weight=FontWeight.BOLD),
                                    padding=8,
                                    alignment=alignment.center,
                                    expand=True
                                ),
                                Container(
                                    content=Text("Salle", size=14, color=text_light, weight=FontWeight.BOLD),
                                    padding=8,
                                    alignment=alignment.center,
                                    expand=True
                                ),
                                Container(
                                    content=Text("Horaire", size=14, color=text_light, weight=FontWeight.BOLD),
                                    padding=8,
                                    alignment=alignment.center,
                                    expand=True
                                ),
                            ],
                            spacing=8
                        ),
                        padding=12,
                        border_radius=BorderRadius(12, 12, 0, 0),
                        gradient=LinearGradient(
                            begin=alignment.center_left,
                            end=alignment.center_right,
                            colors=[primary_color, secondary_color]
                        )
                    ),
                    
                    # Contenu de l'emploi du temps
                    Container(
                        content=gener_emploi_du_temps(),
                        padding=padding.symmetric(horizontal=12, vertical=8),
                        border_radius=BorderRadius(0, 0, 12, 12),
                        bgcolor=COULEUR_BACKGROUND
                    )
                ],
                spacing=0
            ),
            margin=margin.symmetric(horizontal=10, vertical=10)
        )
 
 
        
        return View(
            route=f"/{chemin.lower()}/{name}",
            bgcolor=background_color,
            controls=[
                Container(
                    content=Column(
                        controls=[
                            # Bouton retour stylisé
                            Container(
                                content=Row(
                                    controls=[
                                        IconButton(
                                            icon=Icons.ARROW_BACK_IOS,
                                            icon_color=text_light,
                                            on_click=lambda e: page.go("/page_list_enseignant" if chemin == "ens" else "/page_list_etudiant"),
                                            style=ButtonStyle(
                                                shape=CircleBorder(),
                                                bgcolor=card_color,
                                                shadow_color=shadow_color
                                            )
                                        ),
                                        Container(width=10),
                                        Text(
                                            f"Détails {'Enseignant' if chemin == 'ens' else 'Étudiant'}",
                                            size=20,
                                            weight=FontWeight.BOLD,
                                            color=text_light
                                        )
                                    ],
                                    alignment=MainAxisAlignment.START
                                ),
                                padding=padding.symmetric(horizontal=20, vertical=10)
                            ),
                            
                            Container(height=10),
                            
                            # Carte d'informations
                            Container(
                                content=user_info_card,
                                padding=padding.symmetric(horizontal=20)
                            ),
                            
                            Container(height=10),
                            
                            # Section emploi du temps
                            schedule_section,
                            
                            Container(height=100)  # Espace pour la navigation
                        ]
                    ),
                    expand=True
                )
            ],
            navigation_bar=create_navigation_bar(1 if chemin == 'ens' else 2),
            scroll=ScrollMode.AUTO
        )

    # Route change handler (avec vues stylisées)
    def route_change(route):
        page.views.clear()
        global welcome_card
        if page.route == "/page_accueil_admin":
            # Page d'accueil modernisée
            welcome_card = create_modern_card(
                Column(
                    controls=[
                        Container(
                            content=Icon(Icons.HOME, size=80, color=primary_color),
                            alignment=alignment.center,
                            padding=padding.only(bottom=20)
                        ),
                        Text(
                            "Bienvenue sur votre tableau de bord",
                            size=24,
                            weight=FontWeight.BOLD,
                            color=text_light,
                            text_align=TextAlign.CENTER
                        ),
                        Container(height=10),
                        Text(
                            f"Bonjour {name}",
                            size=18,
                            color=text_secondary,
                            text_align=TextAlign.CENTER
                        ),
                        Container(height=20),
                        Row(
                            controls=[
                                Container(
                                    content=Column(
                                        controls=[
                                            Icon(Icons.PEOPLE, size=40, color=other_color),
                                            Container(height=8),
                                            Text("Enseignants", size=16, color=text_light, weight=FontWeight.BOLD),
                                            Text(f"{len(list_enseignant)}", size=24, color=other_color, weight=FontWeight.BOLD)
                                        ],
                                        horizontal_alignment=CrossAxisAlignment.CENTER
                                    ),
                                    padding=20,
                                    border_radius=12,
                                    gradient=LinearGradient(
                                        begin=alignment.top_center,
                                        end=alignment.bottom_center,
                                        colors=[f"{card_color}80", card_color]
                                    ),
                                    expand=True
                                ),
                                Container(width=15),
                                Container(
                                    content=Column(
                                        controls=[
                                            Icon(Icons.SCHOOL, size=40, color=accent_color),
                                            Container(height=8),
                                            Text("Étudiants", size=16, color=text_light, weight=FontWeight.BOLD),
                                            Text(f"{len(list_etudiant)}", size=24, color=accent_color, weight=FontWeight.BOLD)
                                        ],
                                        horizontal_alignment=CrossAxisAlignment.CENTER
                                    ),
                                    padding=20,
                                    border_radius=12,
                                    gradient=LinearGradient(
                                        begin=alignment.top_center,
                                        end=alignment.bottom_center,
                                        colors=[f"{card_color}80", card_color]
                                    ),
                                    expand=True
                                )
                            ]
                        )
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER
                ),
                padding_val=30
            )
            
            page.views.append(
                View(
                    route="/page_accueil_admin",
                    bgcolor=background_color,
                    controls=[
                        Container(
                            content=Column(
                                controls=[
                                    Container(height=20),
                                    Container(
                                        content=welcome_card,
                                        padding=padding.symmetric(horizontal=20)
                                    ),
                                    Container(height=100)
                                ],
                                alignment=MainAxisAlignment.START
                            ),
                            expand=True
                        )
                    ],
                    navigation_bar=create_navigation_bar(0),
                    scroll=ScrollMode.AUTO
                )
            )        
        elif page.route == "/page_list_enseignant":
            # Page enseignants modernisée
            search_section = create_modern_card(
                Row(
                    controls=[champ_recherche, bouton_recherche],
                    alignment=MainAxisAlignment.CENTER,
                    spacing=15
                ),
                padding_val=20
            )
            
            page.views.append(
                View(
                    route="/page_list_enseignant",
                    bgcolor=background_color,
                    controls=[
                        Container(
                            content=Column(
                                controls=[
                                    Container(height=20),
                                    create_section_title("Liste des Enseignants", Icons.PEOPLE),
                                    Container(
                                        content=search_section,
                                        padding=padding.symmetric(horizontal=20)
                                    ),
                                    Container(height=10),
                                    Container(
                                        content=cont_ens,
                                        padding=padding.symmetric(horizontal=20)
                                    ),
                                    Container(height=100)
                                ],
                                alignment=MainAxisAlignment.START
                            ),
                            expand=True
                        )
                    ],
                    navigation_bar=create_navigation_bar(1),
                    scroll=ScrollMode.AUTO
                )
            )
        elif page.route == "/page_list_etudiant":
            # Page étudiants modernisée
            search_section = create_modern_card(
                Row(
                    controls=[champ_recherche, bouton_recherche],
                    alignment=MainAxisAlignment.CENTER,
                    spacing=15
                ),
                padding_val=20
            )
            
            page.views.append(
                View(
                    route="/page_list_etudiant",
                    bgcolor=background_color,
                    controls=[
                        Container(
                            content=Column(
                                controls=[
                                    Container(height=20),
                                    create_section_title("Liste des Étudiants", Icons.SCHOOL),
                                    Container(
                                        content=search_section,
                                        padding=padding.symmetric(horizontal=20)
                                    ),
                                    Container(height=10),
                                    Container(
                                        content=cont_etu,
                                        padding=padding.symmetric(horizontal=20)
                                    ),
                                    Container(height=100)
                                ],
                                alignment=MainAxisAlignment.START
                            ),
                            expand=True
                        )
                    ],
                    navigation_bar=create_navigation_bar(2),
                    scroll=ScrollMode.AUTO
                )
            )
        elif page.route == "/page_profil_admin":
            # Page profil (déjà stylisée)
            page.views.append(
                View(
                    route="/page_profil_admin",
                    bgcolor=background_color,
                    controls=[
                        Stack(
                            controls=[
                                main_content,
                                Container(
                                    alignment=alignment.bottom_center,
                                    bottom=0,
                                    left=0,
                                    right=0
                                )
                            ],
                            expand=True
                        )
                    ],
                    navigation_bar=create_navigation_bar(3),
                    scroll=ScrollMode.AUTO
                )
            )
      
        elif page.route.startswith('/ens/'):
            ens_name = page.route.split('/')[-1]
            page.views.append(vue_utilisateur(ens_name, 'ens'))
        elif page.route.startswith('/etu/'):
            etu_name = page.route.split('/')[-1]
            page.views.append(vue_utilisateur(etu_name, 'etu'))
        page.update()

    page.on_route_change = route_change
    page.update()

    # Main structure
    return [
        Column(
            controls=[
                Container(
                    content=Column(
                        controls=[
                            Container(height=20),
                            Container(
                                content=create_modern_card(
                                    Column(
                                        controls=[
                                            Container(
                                                content=Icon(Icons.HOME, size=80, color=primary_color),
                                                alignment=alignment.center,
                                                padding=padding.only(bottom=20)
                                            ),
                                            Text(
                                                "Bienvenue sur votre tableau de bord",
                                                size=24,
                                                weight=FontWeight.BOLD,
                                                color=text_light,
                                                text_align=TextAlign.CENTER
                                            ),
                                            Container(height=10),
                                            Text(
                                                f"Bonjour {name}",
                                                size=18,
                                                color=text_secondary,
                                                text_align=TextAlign.CENTER
                                            ),
                                            Container(height=20),
                                            Row(
                                                controls=[
                                                    Container(
                                                        content=Column(
                                                            controls=[
                                                                Icon(Icons.PEOPLE, size=40, color=other_color),
                                                                Container(height=8),
                                                                Text("Enseignants", size=16, color=text_light, weight=FontWeight.BOLD),
                                                                Text(f"{len(list_enseignant)}", size=24, color=other_color, weight=FontWeight.BOLD)
                                                            ],
                                                            horizontal_alignment=CrossAxisAlignment.CENTER
                                                        ),
                                                        padding=20,
                                                        border_radius=12,
                                                        gradient=LinearGradient(
                                                            begin=alignment.top_center,
                                                            end=alignment.bottom_center,
                                                            colors=[f"{card_color}80", card_color]
                                                        ),
                                                        expand=True
                                                    ),
                                                    Container(width=15),
                                                    Container(
                                                        content=Column(
                                                            controls=[
                                                                Icon(Icons.SCHOOL, size=40, color=accent_color),
                                                                Container(height=8),
                                                                Text("Étudiants", size=16, color=text_light, weight=FontWeight.BOLD),
                                                                Text(f"{len(list_etudiant)}", size=24, color=accent_color, weight=FontWeight.BOLD)
                                                            ],
                                                            horizontal_alignment=CrossAxisAlignment.CENTER
                                                        ),
                                                        padding=20,
                                                        border_radius=12,
                                                        gradient=LinearGradient(
                                                            begin=alignment.top_center,
                                                            end=alignment.bottom_center,
                                                            colors=[f"{card_color}80", card_color]
                                                        ),
                                                        expand=True
                                                    )
                                                ]
                                            )
                                        ],
                                        horizontal_alignment=CrossAxisAlignment.CENTER
                                    ),
                                    padding_val=30
                                ),
                                padding=padding.symmetric(horizontal=20)
                            ),
                            Container(height=100)
                        ],
                        alignment=MainAxisAlignment.START
                    ),
                )
            ],
            expand=True
        ),
        create_navigation_bar(0)  # page d'accueil
    ]