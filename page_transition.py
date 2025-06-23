import flet as ft
import flet_lottie as fl
import asyncio

def page_transition(page: ft.Page):
    page.bgcolor = "#223d89"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    async def auto_redirect():
        # Attendre 10 secondes pour laisser le temps à l'animation de se charger
        await asyncio.sleep(10)
        # Rediriger vers la page d'accueil
        page.go("/page_bienvenue")

    # Démarrer la redirection automatique
    page.run_task(auto_redirect)

    lottie = ft.Row(
        [
            fl.Lottie(
                src="https://raw.githubusercontent.com/Elisa734/gif/refs/heads/main/videologo.mp4.lottie.json",
                reverse=False,
                animate=True,
                repeat=True,
                fit=ft.ImageFit.CONTAIN,
                expand=True,
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    container = ft.Container(
        content=lottie,
        bgcolor="#223d89",
        padding=0,
        expand=True,
        alignment=ft.alignment.center,
    )

    # Retourner une liste de contrôles pour Flet
    return [container]

# Fonction principale pour lancer l'application
def main():
    ft.app(
        target=page_transition,
        web_renderer="canvaskit",  # Utiliser CanvasKit pour un meilleur rendu web
        route_url_strategy="path",  # Stratégie d'URL pour la navigation multi-pages
    )

if __name__ == "__main__":
    main()