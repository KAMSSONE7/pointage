import flet as ft
import asyncio

def page_transition(page: ft.Page):
    
    async def auto_redirect():
        # Attendre 5 secondes
        await asyncio.sleep(5)
        # Rediriger vers la page d'accueil
        page.go("/page_bienvenue")
    
    # Démarrer la redirection automatique
    page.run_task(auto_redirect)
    
    # Afficher seulement l'image
    img = ft.Row([ft.Image(src="bienvenue.gif")], alignment=ft.MainAxisAlignment.CENTER)
    
    saut = ft.Row(height=30)
    
    # Retourner seulement l'image et l'espace (sans bouton)
    champ = [img, saut]
    
    return champ