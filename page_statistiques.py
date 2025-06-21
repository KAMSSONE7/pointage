import flet as ft
from db_config import DB_CONFIG
import mysql.connector
from mysql.connector import Error
import time
from db_config import get_db_connection

# Définition des couleurs modernes
BG = "#041955"   # Bleu foncé
FWG = "#FFFFFF"  # Blanc
FG = "#3450a1"   # Bleu clair
PINK = "#eb06ff" # Rose
ACCENT = "#2BC2A9"  # Vert menthe
CARD_BG = "#1C3989"  # Bleu card
SHADOW = "#516ec5"   # Ombre

# Fonction pour récupérer les données de l'enseignant connecté
def fetch_teacher_statistics(teacher_id):
    print(f"Récupération des statistiques pour l'enseignant ID: {teacher_id}")
    try:
        connection = get_db_connection()
        if not connection:
            print("Échec de la connexion à la base de données")
            return None
            
        print("Connexion à la base de données établie")
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Vérifier d'abord si l'enseignant existe
            cursor.execute("SELECT Id_ens, Nom, Prenoms FROM Enseignant WHERE Id_ens = %s", (teacher_id,))
            enseignant = cursor.fetchone()
            
            if not enseignant:
                print(f"Aucun enseignant trouvé avec l'ID: {teacher_id}")
                return None
                
            print(f"Enseignant trouvé: {enseignant}")
            
            # Statistiques de l'enseignant connecté
            cursor.execute("""
                SELECT 
                    e.Nom, e.Prenoms, 
                    COUNT(pe.Id_pres) AS nb_presences, 
                    COALESCE(SUM(TIMESTAMPDIFF(MINUTE, pe.Heure_debut, pe.Heure_fin)), 0) AS total_minutes
                FROM 
                    Enseignant e
                LEFT JOIN 
                    Presence_ens pe ON e.Id_ens = pe.Id_ens
                WHERE 
                    e.Id_ens = %s
                GROUP BY 
                    e.Id_ens, e.Nom, e.Prenoms
            """, (teacher_id,))
            teacher_stats = cursor.fetchone()
            print(f"Statistiques de l'enseignant: {teacher_stats}")
            
            # Récupérer les détails des présences pour l'historique
            cursor.execute("""
                SELECT 
                    DATE(pe.Heure_debut) as date_presence,
                    TIME(pe.Heure_debut) as heure_debut,
                    TIME(pe.Heure_fin) as heure_fin,
                    TIMESTAMPDIFF(MINUTE, pe.Heure_debut, pe.Heure_fin) as duree_minutes
                FROM 
                    Presence_ens pe
                WHERE 
                    pe.Id_ens = %s
                ORDER BY 
                    pe.Heure_debut DESC
                LIMIT 10
            """, (teacher_id,))
            presence_history = cursor.fetchall()
            print(f"Historique des présences: {len(presence_history)} entrées trouvées")
            
            result = {
                'teacher_info': teacher_stats,
                'presence_history': presence_history
            }
            
            return result
            
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")
        return None
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion MySQL fermée")

# Fonction pour calculer les statistiques de l'enseignant
def calculate_teacher_stats(teacher_data):
    print(f"Calcul des statistiques pour les données: {teacher_data}")
    
    # Valeurs par défaut
    default_stats = {
        'nom_complet': 'Aucun utilisateur',
        'nb_presences': 0,
        'total_heures': 0,
        'moyenne_heures_par_jour': 0,
        'derniere_presence': 'Aucune',
        'historique_presences': []
    }
    
    # Vérifier si les données sont valides
    if not teacher_data or not isinstance(teacher_data, dict):
        print("Aucune donnée d'enseignant fournie")
        return default_stats
        
    if not teacher_data.get('teacher_info'):
        print("Aucune information d'enseignant trouvée dans les données")
        return default_stats
    
    # Extraire les informations de base
    try:
        nom, prenoms, nb_presences, total_minutes = teacher_data['teacher_info']
        nom_complet = f"{prenoms} {nom}" if nom and prenoms else "Inconnu"
        
        # Calculer les statistiques
        total_heures = round(total_minutes / 60, 1) if total_minutes and nb_presences > 0 else 0
        moyenne_heures = round(total_heures / max(1, nb_presences), 1) if nb_presences > 0 else 0
        
        # Récupérer l'historique des présences
        historique = teacher_data.get('presence_history', [])
        derniere_presence = historique[0][0].strftime('%d/%m/%Y') if historique and historique[0] and historique[0][0] else 'Aucune'
        
        return {
            'nom_complet': nom_complet,
            'nb_presences': nb_presences,
            'total_heures': total_heures,
            'moyenne_heures_par_jour': moyenne_heures,
            'derniere_presence': derniere_presence,
            'historique_presences': historique
        }
        
    except (ValueError, IndexError, AttributeError, KeyError) as e:
        print(f"Erreur lors du calcul des statistiques: {e}")
        return default_stats

class State:
    toggle = True
    
s = State()

def page_statistiques(page: ft.Page, teacher_id=None):
    # Si teacher_id n'est pas fourni, essayer de le récupérer depuis la session
    if teacher_id is None:
        # Essayer de récupérer l'ID depuis la session si disponible
        if hasattr(page, 'session'):
            user_data = page.session.get('user')
            if user_data and 'id' in user_data:
                teacher_id = user_data['id']
                print(f"ID enseignant récupéré depuis la session: {teacher_id}")
            else:
                # Valeur par défaut si aucune session n'est disponible (pour le débogage)
                teacher_id = 'ENS004'  # À utiliser uniquement pour les tests
                print(f"Aucun ID enseignant trouvé dans la session, utilisation de la valeur par défaut: {teacher_id}")
        else:
            teacher_id = 'ENS004'  # Valeur par défaut si la session n'est pas disponible
            print(f"Session non disponible, utilisation de la valeur par défaut: {teacher_id}")
    
    page.bgcolor = BG
    page.spacing = 0
    page.padding = 0
    
    # Variables pour stocker les données de l'enseignant connecté
    teacher_data = {}
    teacher_stats = {}
    
    print(f"Chargement des statistiques pour l'enseignant: {teacher_id}")
    
    # Animation de chargement
    loading_ring = ft.ProgressRing(
        width=60, 
        height=60, 
        stroke_width=4,
        color=ACCENT,
        visible=False
    )
    
    # Titre animé avec gradient
    title_container = ft.Container(
        content=ft.Text(
            "📊 STATISTIQUES", 
            size=32, 
            color=FWG,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[FG, ACCENT]
        ),
        border_radius=20,
        padding=ft.padding.symmetric(vertical=20, horizontal=30),
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=15,
            color=SHADOW,
            offset=ft.Offset(0, 5)
        ),
        animate=ft.Animation(800, ft.AnimationCurve.BOUNCE_OUT),
        animate_scale=ft.Animation(600, ft.AnimationCurve.EASE_OUT)
    )
    
    # Cartes de statistiques animées avec données dynamiques
    def create_animated_card(title, subtitle, icon, color, delay=0):
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Icon(icon, size=40, color=color),
                    bgcolor=f"{color}20",
                    border_radius=50,
                    width=80,
                    height=80,
                    alignment=ft.alignment.center,
                    animate=ft.Animation(400 + delay, ft.AnimationCurve.ELASTIC_OUT)
                ),
                ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color=FWG),
                ft.Text(subtitle, size=14, color=f"{FWG}80", text_align=ft.TextAlign.CENTER)
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10),
            bgcolor=CARD_BG,
            border_radius=20,
            padding=25,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=12,
                color=SHADOW,
                offset=ft.Offset(0, 4)
            ),
            animate=ft.Animation(600 + delay, ft.AnimationCurve.EASE_OUT),
            animate_scale=ft.Animation(400 + delay, ft.AnimationCurve.BOUNCE_OUT),
            on_hover=lambda e: animate_card_hover(e),
            expand=True
        )
    
    def animate_card_hover(e):
        if e.data == "true":
            e.control.scale = 1.05
            e.control.shadow = ft.BoxShadow(
                spread_radius=3,
                blur_radius=20,
                color=ACCENT,
                offset=ft.Offset(0, 8)
            )
        else:
            e.control.scale = 1.0
            e.control.shadow = ft.BoxShadow(
                spread_radius=1,
                blur_radius=12,
                color=SHADOW,
                offset=ft.Offset(0, 4)
            )
        page.update()
    
    # Boutons animés pour les statistiques
    def create_animated_button(text, route, icon, color, delay=0):
        return ft.Container(
            content=ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(icon, size=24),
                    ft.Text(text, size=16, weight=ft.FontWeight.BOLD)
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10),
                on_click=lambda e: navigate_with_animation(route),
                style=ft.ButtonStyle(
                    bgcolor=color,
                    color=FWG,
                    shape=ft.RoundedRectangleBorder(radius=15),
                    padding=ft.padding.symmetric(vertical=15, horizontal=25),
                    shadow_color=color,
                    elevation=8
                ),
                animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT)
            ),
            animate=ft.Animation(500 + delay, ft.AnimationCurve.EASE_OUT),
            animate_offset=ft.Animation(500 + delay, ft.AnimationCurve.EASE_OUT),
            offset=ft.Offset(0, 1)
        )
    
    def navigate_with_animation(route):
        loading_ring.visible = True
        page.update()
        time.sleep(0.5)
        page.go(route)
    
    # Navigation avec animations
    def navigation_changed(e):
        loading_ring.visible = True
        page.update()
        
        if e.control.selected_index == 0:
            page.go("/page_accueil")
        elif e.control.selected_index == 1:
            page.go("/page_emploi_temps")
        elif e.control.selected_index == 2:
            page.go("/page_statistiques")
        elif e.control.selected_index == 3: 
            page.go("/page_profil")
    
    # Barre de navigation moderne
    navigation_bar = ft.CupertinoNavigationBar(
        bgcolor=FWG,
        inactive_color="#666666",
        active_color=FG,
        on_change=navigation_changed,
        border=ft.Border(top=ft.BorderSide(2, ACCENT)),
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.Icons.HOME_ROUNDED),
                selected_icon=ft.Icon(ft.Icons.HOME_ROUNDED, color=FG),
                label="Accueil"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.Icons.CALENDAR_TODAY),
                selected_icon=ft.Icon(ft.Icons.CALENDAR_TODAY, color=FG),
                label="Emploi du temps"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.Icons.SHOW_CHART),
                selected_icon=ft.Icon(ft.Icons.SHOW_CHART, color=FG),
                label="Statistiques"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.Icons.PERSON_2),
                selected_icon=ft.Icon(ft.Icons.PERSON_2, color=FG),
                label="Profil"
            ),
        ],
    )
    
    # Variables pour les conteneurs de cartes (à mettre à jour dynamiquement)
    stats_cards_container = ft.Row([], spacing=15)
    
    # Fonction pour créer les expansion tiles avec données de l'enseignant
    def create_expansion_tiles():
        if not teacher_data or not teacher_data.get('teacher_info'):
            return [
                ft.Container(
                    content=ft.Text("Aucune donnée disponible pour cet enseignant", color=FWG, size=16),
                    bgcolor=CARD_BG,
                    border_radius=15,
                    padding=20,
                    margin=ft.margin.symmetric(vertical=5)
                )
            ]
        
        tiles = []
        
        # Tile pour les informations générales
        tiles.append(ft.Container(
            content=ft.ExpansionTile(
                title=ft.Text(f"📊 Résumé de {teacher_stats['nom_complet']}", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text(f"Vos statistiques personnelles", opacity=0.8),
                leading=ft.Icon(ft.Icons.PERSON, color=ACCENT, size=30),
                controls=[
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.CHECK_CIRCLE, color="#4CAF50"),
                        title=ft.Text(f"Nombre de présences: {teacher_stats['nb_presences']}", color=FWG),
                        subtitle=ft.Text("Présences enregistrées", color=f"{FWG}80")
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.SCHEDULE, color=ACCENT),
                        title=ft.Text(f"Temps total: {teacher_stats['total_heures']} heures", color=FWG),
                        subtitle=ft.Text("Heures travaillées au total", color=f"{FWG}80")
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.ANALYTICS, color=PINK),
                        title=ft.Text(f"Moyenne: {teacher_stats['moyenne_heures_par_jour']}h/jour", color=FWG),
                        subtitle=ft.Text("Temps moyen par présence", color=f"{FWG}80")
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.CALENDAR_TODAY, color="#FF9800"),
                        title=ft.Text(f"Dernière présence: {teacher_stats['derniere_presence']}", color=FWG),
                        subtitle=ft.Text("Date de dernière connexion", color=f"{FWG}80")
                    )
                ],
            ),
            bgcolor=CARD_BG,
            border_radius=15,
            margin=ft.margin.symmetric(vertical=5),
            animate=ft.Animation(600, ft.AnimationCurve.EASE_OUT)
        ))
        
        # Tile pour l'historique des présences
        if teacher_data.get('presence_history'):
            history_controls = []
            for i, (date_presence, heure_debut, heure_fin, duree_minutes) in enumerate(teacher_data['presence_history'][:5]):
                duree_heures = round(duree_minutes / 60, 1) if duree_minutes else 0
                history_controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.ACCESS_TIME, color=ACCENT),
                        title=ft.Text(f"{date_presence} - {heure_debut} à {heure_fin}", color=FWG),
                        subtitle=ft.Text(f"Durée: {duree_heures}h ({duree_minutes}min)", color=f"{FWG}80")
                    )
                )
            
            tiles.append(ft.Container(
                content=ft.ExpansionTile(
                    title=ft.Text("📅 Historique des présences", weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text("Vos 5 dernières présences", opacity=0.8),
                    leading=ft.Icon(ft.Icons.HISTORY, color="#4CAF50", size=30),
                    controls=history_controls,
                ),
                bgcolor=CARD_BG,
                border_radius=15,
                margin=ft.margin.symmetric(vertical=5),
                animate=ft.Animation(700, ft.AnimationCurve.EASE_OUT)
            ))
        
        return tiles
    
    # Container pour les expansion tiles
    expansion_tiles_container = ft.ListView(
        controls=[],
        expand=True,
        spacing=10
    )
    
    # Bouton retour animé
    back_button = ft.Container(
        content=ft.IconButton(
            icon=ft.Icons.ARROW_BACK_IOS,
            icon_color=FWG,
            icon_size=24,
            on_click=lambda _: page.go('/page_accueil'),
            style=ft.ButtonStyle(
                shape=ft.CircleBorder(),
                bgcolor=CARD_BG,
                shadow_color=SHADOW,
                elevation=5
            ),
            animate_scale=ft.Animation(200, ft.AnimationCurve.BOUNCE_OUT)
        ),
        padding=ft.padding.all(10),
        animate=ft.Animation(400, ft.AnimationCurve.EASE_OUT)
    )
    
    # Mise à jour des statistiques avec animation
    def update_statistics():
        nonlocal teacher_data, teacher_stats
        
        loading_ring.visible = True
        page.update()
        
        # Récupérer les données de l'enseignant connecté
        teacher_data = fetch_teacher_statistics(teacher_id)
        loading_ring.visible = False
        
        if teacher_data and teacher_data['teacher_info']:
            # Calculer les statistiques de l'enseignant
            teacher_stats = calculate_teacher_stats(teacher_data)
            
            # Mettre à jour les cartes de statistiques
            stats_cards_container.controls = [
                create_animated_card(
                    f"{teacher_stats['nb_presences']}", 
                    "Vos présences", 
                    ft.Icons.CHECK_CIRCLE, 
                    "#4CAF50", 
                    100
                ),
                create_animated_card(
                    f"{teacher_stats['total_heures']}h", 
                    "Heures travaillées", 
                    ft.Icons.SCHEDULE, 
                    ACCENT, 
                    200
                ),
                create_animated_card(
                    f"{teacher_stats['moyenne_heures_par_jour']}h", 
                    "Moyenne/jour", 
                    ft.Icons.TRENDING_UP, 
                    PINK, 
                    300
                )
            ]
            
            # Mettre à jour les expansion tiles
            expansion_tiles_container.controls = create_expansion_tiles()
            
            # Animation de mise à jour réussie
            page.open(
                ft.SnackBar(
                    ft.Text(f"✅ Statistiques de {teacher_stats['nom_complet']} mises à jour"),
                    duration=2000,
                    bgcolor="#4CAF50"
                )
            )
        else:
            # En cas d'erreur, afficher des valeurs par défaut
            stats_cards_container.controls = [
                create_animated_card("0", "Présences", ft.Icons.CHECK_CIRCLE, "#4CAF50", 100),
                create_animated_card("0h", "Heures", ft.Icons.SCHEDULE, ACCENT, 200),
                create_animated_card("0h", "Moyenne", ft.Icons.TRENDING_UP, PINK, 300)
            ]
            
            expansion_tiles_container.controls = [
                ft.Container(
                    content=ft.Text("❌ Aucune donnée trouvée pour cet enseignant", color="#F44336", size=16),
                    bgcolor=CARD_BG,
                    border_radius=15,
                    padding=20
                )
            ]
            
            page.open(
                ft.SnackBar(
                    ft.Text("❌ Erreur lors du chargement de vos données"),
                    duration=2000,
                    bgcolor="#F44336"
                )
            )
        
        page.update()
    
    # Animation d'entrée pour les éléments
    def animate_elements():
        title_container.offset = ft.Offset(0, 0)
        stat1_container.offset = ft.Offset(0, 0)
        stat2_container.offset = ft.Offset(0, 0)
        page.update()
    
    # Boutons d'action
    stat1_container = create_animated_button(
        "STATISTIQUE EN COURBE", 
        '/page_stat1', 
        ft.Icons.SHOW_CHART, 
        FG, 
        100
    )
    
    stat2_container = create_animated_button(
        "STATISTIQUE EN DIAGRAMME", 
        '/page_stat2', 
        ft.Icons.PIE_CHART, 
        PINK, 
        200
    )
    
    # Structure principale
    main_content = ft.Container(
        content=ft.Column([
            back_button,
            ft.Container(height=20),
            title_container,
            ft.Container(height=30),
            stats_cards_container,
            ft.Container(height=30),
            ft.Text("Options d'analyse", size=20, color=ACCENT, weight=ft.FontWeight.BOLD),
            ft.Container(height=15),
            stat1_container,
            ft.Container(height=15),
            stat2_container,
            ft.Container(height=30),
            ft.Text("Détails par enseignant", size=20, color=ACCENT, weight=ft.FontWeight.BOLD),
            ft.Container(height=15),
            expansion_tiles_container,
            ft.Container(height=100)  # Espace pour la navigation
        ],
        scroll=ft.ScrollMode.AUTO),
        padding=ft.padding.symmetric(horizontal=20),
        expand=True
    )
    
    # Structure finale avec Stack
    page_structure = ft.Stack([
        main_content,
        ft.Container(
            content=loading_ring,
            alignment=ft.alignment.center,
            top=50
        ),
        ft.Container(
            content=navigation_bar,
            alignment=ft.alignment.bottom_center,
            bottom=0,
            left=0,
            right=0
        )
    ], expand=True)
    
    # Démarrer les animations et charger les données
    page.add(page_structure)
    animate_elements()
    update_statistics()  # Chargement initial des données
    
    return [page_structure]