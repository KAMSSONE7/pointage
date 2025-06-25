import flet as ft
import mysql.connector
from mysql.connector import Error
from db_config import get_db_connection

BG = '#041955'
BULLE = '#2BC2A9'
TEXT_WHITE = 'white'
TEXT_BLACK = 'black'

def page_liste_etudiants(page: ft.Page):
    page.bgcolor = BG
    page.adaptive = True

    # Vérifier si l'utilisateur est un enseignant
    user = page.session.get("user") or {"profession": "Inconnu"}
    if user["profession"] != "Enseignant":
        return [ft.Text("Accès réservé aux enseignants", color="red", size=20)]

    # Récupérer les étudiants
    def get_students():
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            if not connection or not connection.is_connected():
                print("Erreur: Impossible de se connecter à la base de données")
                return []
                
            cursor = connection.cursor()
            cursor.execute("""
                SELECT IP, Nom, Prenoms, Niveau, Numero, Email, Adresse 
                FROM Etudiant
            """)
            students = cursor.fetchall()
            return students
        except Error as e:
            print(f"Erreur lors de la récupération des étudiants: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    # Récupérer les statistiques de présence d'un étudiant
    def get_student_stats(student_ip):
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            if not connection or not connection.is_connected():
                print("Erreur: Impossible de se connecter à la base de données")
                return [student_ip, 0, 0, 0]
                
            cursor = connection.cursor()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM Presence_etu 
                WHERE IP = %s
            """, (student_ip,))
            attended = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM Emploi_du_temps")
            total = cursor.fetchone()[0]
            percentage = (attended / total * 100) if total > 0 else 0
            return [student_ip, round(percentage, 2), attended, total]
        except Error as e:
            print(f"Erreur lors de la récupération des statistiques: {e}")
            return [student_ip, 0, 0, 0]
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    students = get_students()
    student_names = [f"{s[1]} {s[2]}" for s in students]

    def affiche(name):
        index = student_names.index(name)
        return [students[index][3], students[index][4], students[index][5], students[index][6], students[index][0]]

    # Vue détaillée d'un étudiant
    def vue_etudiant(name):
        infos = affiche(name)
        stats = get_student_stats(infos[4])
        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(f"Nom & Prénoms : {name}", size=20, weight="bold", color=TEXT_WHITE),
                            ft.Text(f"Profession : Étudiant", size=16, color=TEXT_WHITE),
                            ft.Text(f"Niveau d'étude : {infos[0]}", size=16, color=TEXT_WHITE),
                            ft.Text(f"Numéro de téléphone : {infos[1]}", size=16, color=TEXT_WHITE),
                            ft.Text(f"Email : {infos[2]}", size=16, color=TEXT_WHITE),
                            ft.Text(f"Adresse : {infos[3]}", size=16, color=TEXT_WHITE),
                            ft.Text(
                                f"Statistiques : {stats[2]} présence(s) sur {stats[3]} soit {stats[1]} % de présence",
                                size=16, color=TEXT_WHITE
                            ) if stats[2] > 0 else ft.Text("Statistiques : Aucune présence", size=16, color=TEXT_WHITE),
                        ],
                        spacing=10,
                    ),
                    padding=20,
                    border_radius=10,
                    bgcolor=BULLE,
                    margin=10,
                ),
                ft.ElevatedButton("Retour", on_click=lambda _: page.go('/page_liste_etudiants')),
            ]
        )

    # Gestion des routes
    def changement_route(event):
        route = event.route
        if route.startswith('/etu/'):
            student_name = route.split('/')[-1]
            page.views.append(ft.View(route, [vue_etudiant(student_name)]))
        else:
            page.views.append(ft.View(route="/page_liste_etudiants", controls=page_liste_etudiants(page)))
        page.update()

    # Générer la liste des étudiants
    def gener_cont_list(lst, chemin):
        conteneur = ft.Column(height=400, scroll='auto')
        for i in lst:
            conteneur.controls.append(
                ft.Container(
                    adaptive=True,
                    border_radius=10,
                    bgcolor=BULLE,
                    height=50,
                    width=1500,
                    padding=15,
                    content=ft.Row(controls=[ft.Text(i, color=TEXT_WHITE)], scroll='auto'),
                    on_click=lambda e, name=i: page.go(f"/{chemin}/{name}")
                )
            )
        return conteneur

    # Rechercher un étudiant
    def rechercher_etudiant(e):
        recherche = champ_recherche.value.lower()
        resultats = [student for student in student_names if recherche in student.lower()]
        cont_etu.controls.clear()
        if resultats:
            cont_etu.controls.extend(gener_cont_list(resultats, "etu").controls)
        else:
            cont_etu.controls.append(ft.Text("Aucun étudiant trouvé", color="red", size=15))
        page.update()

    champ_recherche = ft.TextField(
        label="Rechercher un étudiant",
        width=300,
        bgcolor='white',
        color=TEXT_BLACK
    )
    bouton_recherche = ft.ElevatedButton("Rechercher", on_click=rechercher_etudiant)

    cont_etu = gener_cont_list(student_names, "etu")

    # Barre de navigation
    navigation_bar = ft.CupertinoNavigationBar(
        bgcolor=ft.Colors.WHITE,
        inactive_color=ft.Colors.BLACK,
        active_color=ft.Colors.BLUE,
        on_change=lambda e: (
            page.go("/page_accueil") if e.control.selected_index == 0 else
            page.go("/page_emploi_temps") if e.control.selected_index == 1 else
            page.go("/page_statistiques") if e.control.selected_index == 2 else
            page.go("/page_profil") if e.control.selected_index == 3 else
            page.go("/page_liste_etudiants") if e.control.selected_index == 4 else None
        ),
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
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.Icons.LIST, color="black"),
                selected_icon=ft.Icon(ft.Icons.LIST, color="BLUE"),
                label="Étudiants"
            ),
        ],
    )

    tout = ft.Column(
        controls=[
            ft.Row(
                controls=[champ_recherche, bouton_recherche],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            cont_etu,
            navigation_bar,
        ],
        expand=True,
    )

    page.on_route_change = changement_route
    return [tout]