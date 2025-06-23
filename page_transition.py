import flet as ft
import flet_lottie as fl
import asyncio

def page_transition(page: ft.Page):
    page.bgcolor = "#223d89"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    async def auto_redirect():
        # Attendre 5 secondes
        await asyncio.sleep(5)
        # Rediriger vers la page d'accueil
        page.go("/page_bienvenue")
        
    # Démarrer la redirection automatique
    page.run_task(auto_redirect)
            
    lottie = ft.Row([
        fl.Lottie(
        src="https://raw.githubusercontent.com/Elisa734/gif/refs/heads/main/videologo.mp4.lottie.json",
        reverse=False,
        animate=True,
        repeat=True,
        fit=ft.ImageFit.CONTAIN,
        expand=True,
        filter_quality=ft.FilterQuality.NONE,
        background_loading=True,
        
       
    )
    ])

    container = ft.Container(
        content=lottie,
        bgcolor="#223d89",
        padding=0,
        expand=True,
    )
    
    # Return a list containing the container
    return [container]