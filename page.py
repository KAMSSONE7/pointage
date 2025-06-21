import flet as ft
from page_connexion import *
from page_inscription import *
from page_recup_mot_passe import *
from page_renit_mot_passe import *
from page_bienvenue import *
from page_transition import *
from page_etu_acc import *
from page_etu_emploi import *
from page_etu_notif import *
from page_etu_profil import *
from page_etu_propos import *
from page_etu_stats import *
from page_accueil import *
from page_emploi_temps import *
from page_statistiques import *
from page_profil import *
from page_a_propos import *
from page_notif import *
from page_generer_liste import *
from page_liste_de_presence import *
from page_marquer_presence import *
from page_liste_etudiants import *
from page_admins import *
from database import create_table_if_not_exists
from page_boite_de_reception import page_boite_de_reception
col='#3450A1'

def page(page: ft.Page):
    # Créer les tables nécessaires au démarrage
    create_table_if_not_exists()
    
    page.bgcolor='blue'
    
    # Configuration de la gestion des routes
    def on_route_change(e):
        page.views.clear()
        if page.route == "/page_connexion":
            page.views.append(ft.View(route="/page_connexion", controls=page_connexion(page),bgcolor=col))
        elif page.route == "/page_inscription":
            page.views.append(ft.View(route="/page_inscription", controls=page_inscription(page),bgcolor=col))
        elif page.route=="/page_recup_mot_passe":
            page.views.append(ft.View(route="/page_recup_mot_passe",controls=page_recup_mot_passe(page),bgcolor=col))
        elif page.route=="/page_renit_mot_passe":
            page.views.append(ft.View(route="/page_renit_mot_passe",controls=page_renit_mot_passe(page),bgcolor=col))
        elif page.route=="/page_bienvenue":
            page.views.append(ft.View(route="/page_bienvenue",controls=page_bienvenue(page),bgcolor=col))
        elif page.route=="/page_transition":
            page.views.append(ft.View(route="/page_transition",controls=page_transition(page),bgcolor=col))
        elif page.route == "/page_admins":
            page.views.append(ft.View(route="/page_admins",controls=page_admins(page),bgcolor=col))
        elif page.route == "/page_liste_de_presence":
            enseignant_connecte = page.session.get('user')
            if enseignant_connecte and enseignant_connecte.get('profession') == 'Enseignant':
                page_liste_de_presence(page, enseignant_connecte)
            else:
                page.go("/page_accueil")
        elif page.route =="/page_bienvenue":
            page.views.append(ft.View(route="/page_bienvenue",controls=page_bienvenue(page),bgcolor=col)) 
        elif page.route == "/page_etu_acc":
            # Récupérer les données de l'étudiant connecté
            etudiant_connecte = page.session.get("user")
            if etudiant_connecte:
                # Créer un bouton pour marquer la présence
                btn_presence = ft.ElevatedButton(
                    "Marquer ma présence",
                    on_click=lambda _: page.go('/page_marquer_presence')
                )
                
                # Récupérer les contrôles existants de la page étudiant
                etu_controls = page_etu_acc(page)
                
                # Créer une nouvelle liste de contrôles avec le bouton en premier
                new_controls = [btn_presence] + etu_controls
                
                # Afficher la page avec les nouveaux contrôles
                page.views.append(ft.View(
                    route="/page_etu_acc",
                    controls=new_controls,
                    bgcolor=col
                ))
            else:
                page.go('/pageetu')  # Rediriger vers la connexion étudiant
        elif page.route =="/page_boite_de_reception":
            # Récupérer les données de l'enseignant connecté
            enseignant_connecte = page.session.get("user")
            if enseignant_connecte:
                # Ajouter l'ID de l'enseignant aux données
                enseignant_connecte['id'] = enseignant_connecte.get('id') or 'ENS009'
                print(f"Données de l'enseignant avec ID ajouté: {enseignant_connecte}")
                page.views.append(ft.View(route="/page_boite_de_reception",controls=page_boite_de_reception(page, enseignant_connecte),bgcolor=col))
            else:
                page.go('/pageetu')  # Rediriger vers la connexion étudiant
        elif page.route =="/page_marquer_presence":
            # Récupérer les données de l'étudiant connecté
            etudiant_connecte = page.session.get("user")
            if etudiant_connecte:
                page.views.append(ft.View(route="/page_marquer_presence",controls=page_marquer_presence(page, etudiant_connecte),bgcolor=col))
            else:
                page.go('/page_etu_acc')  # Rediriger vers la connexion étudiant
        elif page.route == "/page_etu_notif":
            page.views.append(ft.View(route="/page_etu_notif",controls=page_etu_notif(page),bgcolor=col))
        elif page.route == "/page_etu_profil":
            page.views.append(ft.View(route="/page_etu_profil",controls=page_etu_profil(page),bgcolor=col))
        elif page.route == "/page_etu_propos":
            page.views.append(ft.View(route="/page_etu_propos",controls=page_etu_propos(page),bgcolor=col))
        elif page.route == "/page_etu_stats":
            page.views.append(ft.View(route="/page_etu_stats",controls=page_etu_stats(page),bgcolor=col))
        elif page.route =="/page_accueil":
            page.views.append(ft.View(route="/page_accueil",controls=page_accueil(page),bgcolor=col))
        elif page.route =="/page_emploi_temps":
            page.views.append(ft.View(route="/page_emploi_temps",controls=page_emploi_temps(page),bgcolor=col))
        elif page.route =="/page_statistiques":
            page.views.append(ft.View(route="/page_statistiques",controls=page_statistiques(page),bgcolor=col))
        elif page.route =="/page_profil":
            page.views.append(ft.View(route="/page_profil",controls=page_profil(page),bgcolor=col))
        elif page.route =="/page_a_propos":
            page.views.append(ft.View(route="/page_a_propos",controls=page_a_propos(page),bgcolor=col))
        elif page.route =="/page_notif":
            page.views.append(ft.View(route="/page_notif",controls=page_notif(page),bgcolor=col))
        elif page.route =="/page_generer_liste":
            # On sait que l'utilisateur est connecté, on récupère directement ses données
            # Récupérer les données de la session
            session_data = page.session.get("user")
            
            # Afficher les données pour le débogage
            print(f"Données de la session: {session_data}")
            print(f"Clés de la session: {session_data.keys() if session_data else 'Aucune donnée'}")
            
            # Utiliser directement les données de la session
            utilisateur_connecte = {
                'id': 'ENS001',  # On sait que c'est l'ID de l'enseignant
                'profession': session_data.get('profession'),
                'adresse': session_data.get('adresse'),
                'IP': session_data.get('IP')
            }
            
            # Afficher les données finales
            print(f"Données utilisateur finales: {utilisateur_connecte}")
            
            # Vérifier que toutes les données nécessaires existent
            if utilisateur_connecte.get('id') and utilisateur_connecte.get('profession') and utilisateur_connecte.get('adresse') and utilisateur_connecte.get('IP'):
                page.views.append(ft.View(route="/page_generer_liste",controls=page_generer_liste(page, utilisateur_connecte),bgcolor=col))
            else:
                t = ft.Text("❌ Données utilisateur incomplètes", color='#eb06ff', weight=ft.FontWeight.BOLD)
                page.views.append(ft.View(route="/page_generer_liste",controls=[t],bgcolor=col))
            
            # Rediriger vers la page de connexion si nécessaire
            if not session_data:
                page.go('/page_bienvenue')
        elif page.route == "/page_liste_de_presence":
            # Récupérer l'utilisateur connecté depuis la session
            enseignant_connecte = page.session.get("user")
            page.views.append(ft.View(route="/page_liste_de_presence",controls=page_boite_de_reception(page, enseignant_connecte),bgcolor=col))
        elif page.route == "/page_marquer_presence":
            # Récupérer l'étudiant connecté depuis la session
            etudiant_connecte = page.session.get("user")
            if etudiant_connecte:
                page.views.append(ft.View(route="/page_marquer_presence", controls=page_marquer_presence(page, etudiant_connecte), bgcolor='#3450A1'))
            else:
                page.go('/page_etu_acc')
        elif page.route == "/page_liste_etudiants":
            page.views.append(ft.View("/page_liste_etudiants", page_liste_etudiants(page),bgcolor=col))
        page.update()


    # Configuration initiale
    page.on_route_change = on_route_change
    
    # Redirection vers la page de connexion si l'utilisateur n'est pas connecté
    def check_auth(e):
        if not page.session.get("user") and page.route != "/page_bienvenue":
            page.go("/page_bienvenue")

    page.on_route_change = on_route_change
    page.on_view_pop = check_auth
    page.on_view_push = check_auth
    
    # Redirection initiale vers la page de connexion
    page.go("/page_transition")

ft.app(target=page)