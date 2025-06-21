import flet as ft 

def page_bienvenue(page:ft.Page):
    # Nettoyer la session et les vues au chargement de la page de connexion
    try:
        page.session.clear()
        page.views.clear()
        page.update()
    except Exception as e:
        print(f"Erreur lors du nettoyage de la session : {e}")
    
    def COMMENCER(e):
        try:
            # S'assurer que la session est vide avant de démarrer
            page.session.clear()
            # Rediriger vers la page de connexion principale
            page.go("/page_connexion")
        except Exception as e:
            print(f"Erreur lors de la redirection : {e}")
            page.go("/page_connexion")
    # Calculate responsive dimensions based on screen width
    is_mobile = page.width < 600
    text_size = 26 if not is_mobile else 20
    description_size = 18 if not is_mobile else 14
    button_width = 200 if not is_mobile else 150
    button_height = 50 if not is_mobile else 40
    image_width = 200 if not is_mobile else 150
            
    img = ft.Row([ft.Image(src="logo_sans_fond.png",width=image_width,color='white')],alignment=ft.MainAxisAlignment.CENTER)
    
    #texte=ft.Text("MI_POINT",size=40,weight="bold",color='#e0f7fa')
    
        # Responsive welcome text
    text = ft.Row([ft.Text("Bienvenue sur", size=text_size, weight="bold", color="white")],
        alignment=ft.MainAxisAlignment.CENTER
    )
    text2 = ft.Row([ft.Text("MI_P🎯INT", size=text_size, weight="bold", color="white")],
        alignment=ft.MainAxisAlignment.CENTER
    )
    
    description=ft.Row([
        ft.Text(
            "L'application de pointage des etudiants,de verification des enseignants,et de supervision pour l'administration",
                size=description_size,
                color='white',
                text_align=ft.TextAlign.CENTER
                )],
                alignment=ft.MainAxisAlignment.CENTER,
                wrap=True
                )
    
    commencer=ft.Row(
        [
            ft.ElevatedButton(
                'COMMENCER',
                animate_size=50,
                bgcolor='#90EE90',
                width=button_width,
                height=button_height,
                on_click=COMMENCER,
                style=ft.ButtonStyle(color='black')
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )
    # Responsive spacing
    spacing = ft.Container(height=10 if not is_mobile else 20)
    # Use ResponsiveRow for adaptive layout
    content = ft.ResponsiveRow(
        [
            ft.Column(
                [
                    img,
                    text,
                    text2,
                    description,
                    spacing,
                    commencer
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                col={"xs": 12, "sm": 10, "md": 8, "lg": 6}  # Responsive column sizing
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )    
       
    # Add padding to prevent edge sticking
    container = ft.Container(
        content=content,
        padding=ft.padding.symmetric(horizontal=20, vertical=40),
        expand=True,
        bgcolor='#3450a1' # Assuming a dark background for white text visibility
    )
    return [container]