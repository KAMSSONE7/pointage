from page_profil import page_profil
from page_bienvenue import page_bienvenue
from flet import *
from page_admin import *

def main(page: Page):
    # Configuration des couleurs
    BG = '#041955'
    fond = '#3450a1'
    bulle = '#2BC2A9'
    page.bgcolor = BG
    
    # Configuration de la gestion des routes
    def on_route_change(e):
        page.views.clear()
        
        if page.route == "/page_admins":
            page.views.append(View(route="/page_admins", controls=page_b(page), bgcolor=fond))
        elif page.route == "/page_admin":
            page.views.append(View(route="/page_admin", controls=page_admin(page, "Yao Ama"), bgcolor=fond))
        elif page.route == "/page_bienvenue":
            page.views.append(View(route="/page_bienvenue", controls=page_bienvenue(page), bgcolor=BG))
        elif page.route == "/page_connexion":  # Ajout de la route pour la page_connexion
            from page_connexion import page_connexion
            page.views.append(View(route="/page_connexion", controls=page_connexion(page), bgcolor=fond))
        
        page.update()

    # Gestion de la vue de la fenêtre
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = on_route_change
    page.on_view_pop = view_pop
    page.go("/page_admin")  # Page de démarrage

app(target=main)