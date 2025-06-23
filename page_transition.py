import flet as ft
import asyncio

def page_transition(page: ft.Page):
    page.bgcolor = "#223d89"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    async def auto_redirect():
        # Attendre 10 secondes pour laisser le temps au GIF de se charger
        await asyncio.sleep(10)
        # Rediriger vers la page d'accueil
        page.go("/page_bienvenue")

    # Démarrer la redirection automatique
    page.run_task(auto_redirect)

    # Afficher seulement l'image
    img = ft.Row(
        [ft.Image(src="bienvenue.gif", fit=ft.ImageFit.CONTAIN, expand=True)],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    saut = ft.Row(height=30)

    # Retourner seulement l'image et l'espace (sans bouton)
    champ = [img, saut]

    return champ

# Fonction principale pour lancer l'application
def main():
    ft.app(
        target=page_transition,
        web_renderer="canvaskit",  # Utiliser CanvasKit pour un meilleur rendu web
        route_url_strategy="path",  # Stratégie d'URL pour la navigation multi-pages
        assets_dir="assets",  # Dossier pour les ressources comme le GIF
    )

if __name__ == "__main__":
    main()