import flet as ft
import mysql.connector
from mysql.connector import Error
from db_config import get_db_connection

BG = "#041955"


def page_liste_de_presence(page: ft.Page, enseignant_connecte=None):
    try:
        # Vérifier que l'utilisateur est connecté
        if not enseignant_connecte:
            page.go("/page_accueil")
            return

        # Connexion à la base de données
        connection = get_db_connection()
        if not connection:
            print("Impossible de se connecter à la base de données")
            return
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Récupérer les listes de présence de l'enseignant
            cursor.execute(
                """
                SELECT lp.Id_liste, lp.Date_liste, lp.Heure_creation, lp.Nombre_etudiants
                FROM liste_presence lp
                WHERE lp.Id_ens = %s
                ORDER BY lp.Date_liste DESC, lp.Heure_creation DESC
                """,
                (enseignant_connecte.get('id'),)
            )
            listes_presence = list(cursor.fetchall())
            
            # Pour chaque liste, récupérer les détails
            listes_detaillees = []
            for liste in listes_presence:
                id_liste, date_liste, heure_creation, nombre_etudiants = liste
                cursor.execute(
                    """
                    SELECT dp.IP_etudiant, dp.Heure_arrivee, e.Nom, e.Prenoms
                    FROM detail_presence dp
                    JOIN etudiant e ON dp.IP_etudiant = e.IP
                    WHERE dp.Id_liste = %s
                    ORDER BY dp.Heure_arrivee
                    """,
                    (id_liste,)
                )
                details = list(cursor.fetchall())
                listes_detaillees.append({
                    'id': id_liste,
                    'date': date_liste,
                    'heure': heure_creation,
                    'nombre': nombre_etudiants,
                    'details': details
                })
            
            connection.commit()
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")
        listes_detaillees = []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion MySQL fermée")
    
    # Créer les contrôles pour afficher les listes
    listes_controls = []
    
    for liste in listes_detaillees:
        # Créer un conteneur pour chaque liste
        liste_container = ft.Container(
            content=ft.Column([
                # Titre de la liste
                ft.Text(
                    f"Liste du {liste['date']} à {liste['heure']}",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="WHITE"
                ),
                # Nombre d'étudiants
                ft.Text(
                    f"Nombre d'étudiants présents: {liste['nombre']}",
                    size=16,
                    color="WHITE"
                ),
                # Liste des étudiants présents
                ft.Column([
                    ft.Text(
                        f"{detail[2]} {detail[3]} - {detail[1]}",
                        size=14,
                        color="WHITE"
                    )
                    for detail in liste['details']
                ])
            ]),
            padding=10,
            margin=10,
            bgcolor=BG,
            border_radius=10
        )
        listes_controls.append(liste_container)
    
    # Ajouter la barre de navigation
    page.appbar = ft.AppBar(
        title=ft.Text("Liste des présences", color="WHITE"),
        bgcolor=ft.Colors.BLUE_900,
        leading=ft.IconButton(
            ft.Icons.ARROW_BACK,
            tooltip="Retour",
            on_click=lambda _: page.go("/page_accueil")
        ),
        actions=[
            ft.IconButton(
                ft.Icons.HOME,
                tooltip="Accueil",
                on_click=lambda _: page.go("/page_accueil")
            )
        ]
    )
    
    # Créer un bouton retour en haut de la page
    retour_button = ft.ElevatedButton(
        "Retour",
        icon=ft.Icons.ARROW_BACK,
        bgcolor=ft.Colors.BLUE_900,
        color="WHITE",
        on_click=lambda _: page.go("/page_accueil")
    )
    
    # Créer la vue avec les listes
    if not listes_detaillees:
        # Si aucune liste n'existe, afficher un message
        page.views.append(
            ft.View(
                "/page_liste_de_presence",
                [
                    retour_button,
                    ft.Text(
                        "Aucune liste de présence n'a été générée pour l'instant.",
                        size=16,
                        color="WHITE",
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Text(
                        "Pour créer une nouvelle liste de présence, utilisez le bouton 'Générer liste' dans la barre de navigation.",
                        size=14,
                        color="WHITE"
                    )
                ],
                bgcolor=BG
            )
        )
    else:
        page.views.append(
            ft.View(
                "/page_liste_de_presence",
                [
                    retour_button,
                    # Liste des présences
                    ft.Column(
                        listes_controls,
                        spacing=10,
                        alignment=ft.MainAxisAlignment.START
                    )
                ],
                bgcolor=BG
            )
        )
    
    # Afficher la page
    page.update()