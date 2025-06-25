from flet import *
import time

class ProfilPage:
    def __init__(self, page: Page):
        self.page = page
        self.page.adaptive = True
        self.page.title = "Profil Enseignant"
        
        # Palette de couleurs
        self.primary_color = "#667eea"  # Bleu-violet moderne
        self.secondary_color = "#041955"  # Rose doux
        self.other_color = "#2BC2A9"  # Vert menthe
        self.other_color2 = "#010102"  # Gris clair
        self.accent_color = "#4facfe"  # Bleu clair
        self.background_color = "#3450a1"  # Gris très clair
        self.card_color = "#041955"
        self.card_color2 = "#1C3989"  # Gris clair pour les cartes
        self.text_primary = "#f9f9fa"  # Gris foncé
        self.text_secondary = "#f8fafd"  # Gris moyen
        self.text_light = "#ffffff"  # Blanc
        self.shadow_color = "#516ec5"  # Gris clair pour ombres

        # Récupérer les informations de l'utilisateur
        self.user = page.session.get("user") or {
            "nom": "Inconnu",
            "prenom": "Inconnu",
            "email": "inconnu@example.com",
            "numero": "0000000000",
            "adresse": "N/A",
            "profession": "Enseignant"
        }

        # Initialiser les composants
        self.initialize_components()

    def initialize_components(self):
        # Fonction pour créer un gradient
        def create_gradient_container(content, colors_list):
            return Container(
                content=content,
                gradient=LinearGradient(
                    begin=alignment.top_left,
                    end=alignment.bottom_right,
                    colors=colors_list
                ),
                border_radius=15,
                shadow=BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=self.shadow_color,
                    offset=Offset(0, 4)
                )
            )

        # Navigation
        def navigation_changed(e):
            self.page.splash = ProgressBar(visible=True)
            self.page.update()
            
            if e.control.selected_index == 0:
                self.page.go("/page_accueil")
            elif e.control.selected_index == 1:
                self.page.go("/page_emploi_temps")
            elif e.control.selected_index == 2:
                self.page.go("/page_statistiques")
            elif e.control.selected_index == 3:
                self.page.go("/page_profil")

        # Barre de navigation
        self.navigation_bar = CupertinoNavigationBar(
            bgcolor=self.text_secondary,
            inactive_color=self.other_color2,
            active_color=self.primary_color,
            on_change=navigation_changed,
            border=Border(top=BorderSide(1, self.shadow_color)),
            destinations=[
                NavigationBarDestination(
                    icon=Icon(Icons.HOME_ROUNDED, color=self.text_secondary),
                    selected_icon=Icon(Icons.HOME_ROUNDED, color=self.primary_color),
                    label="Accueil"
                ),
                NavigationBarDestination(
                    icon=Icon(Icons.CALENDAR_TODAY, color=self.other_color2),
                    selected_icon=Icon(Icons.CALENDAR_TODAY, color=self.other_color2),
                    label="Emploi du temps"
                ),
                NavigationBarDestination(
                    icon=Icon(Icons.SHOW_CHART, color=self.other_color2),
                    selected_icon=Icon(Icons.SHOW_CHART, color=self.other_color2),
                    label="Statistiques"
                ),
                NavigationBarDestination(
                    icon=Icon(Icons.PERSON_2, color=self.other_color2),
                    selected_icon=Icon(Icons.PERSON_2, color=self.other_color2),
                    label="Profil"
                ),
            ],
        )

        # Informations de l'utilisateur
        self.infos_admin = [
            self.user["nom"],
            self.user["prenom"],
            self.user["numero"],
            self.user["email"],
            self.user["adresse"]
        ]
        
        self.det_infos_admin = ["Nom", "Prénoms", "Numéro de téléphone", "Email", "Adresse"]
        self.icones_infos = [Icons.BADGE, Icons.PERSON, Icons.PHONE, Icons.EMAIL, Icons.HOME]

        # En-tête avec avatar
        self.header = create_gradient_container(
            Column(
                controls=[
                    Container(height=20),
                    CircleAvatar(
                        radius=50,
                        bgcolor=self.card_color,
                        content=Icon(Icons.PERSON, size=60, color=self.primary_color)
                    ),
                    Container(height=15),
                    Text(
                        f"{self.user['prenom']} {self.user['nom']}",
                        size=24,
                        weight=FontWeight.BOLD,
                        color=self.text_light,
                        text_align=TextAlign.CENTER
                    ),
                    Text(
                        self.user.get("profession", "Enseignant"),
                        size=16,
                        color=self.text_light,
                        text_align=TextAlign.CENTER,
                        opacity=0.9
                    ),
                    Container(height=20),
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
            ),
            [self.primary_color, self.secondary_color]
        )

        # Cartes d'information
        self.info_cards = Column(spacing=15)
        
        for info, label, icon in zip(self.infos_admin, self.det_infos_admin, self.icones_infos):
            info_content = Row(
                controls=[
                    Container(
                        width=50,
                        height=50,
                        bgcolor=f"{self.other_color}15",
                        border_radius=25,
                        content=Icon(icon, color=self.other_color, size=24),
                        alignment=alignment.center
                    ),
                    Container(width=15),
                    Column(
                        controls=[
                            Text(label, size=12, color=self.other_color, weight=FontWeight.W_500),
                            Text(str(info), size=16, color=self.text_primary, weight=FontWeight.BOLD)
                        ],
                        spacing=2,
                        expand=True
                    )
                ],
                alignment=MainAxisAlignment.START
            )
            
            info_card = create_gradient_container(
                content=Container(
                    content=info_content,
                    padding=20
                ),
                colors_list=[self.card_color2, self.card_color]
            )
            
            self.info_cards.controls.append(info_card)

        # Boutons d'action
        self.action_buttons = Column(
            controls=[
                Container(
                    content=ElevatedButton(
                        "Se déconnecter",
                        icon=Icons.LOGOUT,
                        on_click=lambda _: self.page.go('/page_bienvenue'),
                        style=ButtonStyle(
                            bgcolor=self.other_color,
                            color=self.text_light,
                            shape=RoundedRectangleBorder(radius=25),
                            padding=padding.symmetric(horizontal=25, vertical=12)
                        )
                    ),
                    alignment=alignment.center
                )
            ]
        )

        # Bouton retour
        self.retour = Container(
            content=IconButton(
                icon=Icons.ARROW_BACK_IOS,
                icon_color=self.text_primary,
                on_click=lambda _: self.page.go('/page_accueil'),
                style=ButtonStyle(
                    shape=CircleBorder(),
                    bgcolor=self.card_color,
                    shadow_color=self.shadow_color
                )
            ),
            padding=padding.only(left=10, top=10)
        )

        # Structure principale
        self.main_content = Container(
            bgcolor=self.background_color,
            expand=True,
            content=Column(
                controls=[
                    self.retour,
                    Container(height=10),
                    Container(
                        padding=padding.symmetric(horizontal=20),
                        content=self.header
                    ),
                    Container(height=20),
                    Container(
                        padding=padding.symmetric(horizontal=20),
                        content=Column(
                            controls=[
                                Text("Informations personnelles", 
                                    size=20, 
                                    weight=FontWeight.BOLD, 
                                    color=self.other_color),
                                Container(height=10),
                                self.info_cards,
                                Container(height=20),
                                self.action_buttons,
                                Container(height=100)
                            ]
                        )
                    )
                ],
                scroll=ScrollMode.AUTO
            )
        )

    # Déconnexion - Version améliorée
    def confirmer_deconnexion(self, e):
        # Fermer la boîte de dialogue
        self.page.dialog.open = False
        self.page.update()
        # Supprimer les données de la session
        self.page.session.clear()
        # Redirection vers la page de connexion
        self.page.go('/page_bienvenue')

    def annuler_deconnexion(self, e):
        # Fermer la boîte de dialogue
        self.page.dialog.open = False
        self.page.update()

    def __init__(self, page: Page):
        self.page = page
        self.page.adaptive = True
        self.page.title = "Profil Enseignant"
        self.dialog = None  # Ajout de la variable d'instance pour la boîte de dialogue
        
        # Palette de couleurs
        self.primary_color = "#667eea"  # Bleu-violet moderne
        self.secondary_color = "#041955"  # Rose doux
        self.other_color = "#2BC2A9"  # Vert menthe
        self.other_color2 = "#010102"  # Gris clair
        self.accent_color = "#4facfe"  # Bleu clair
        self.background_color = "#3450a1"  # Gris très clair
        self.card_color = "#041955"
        self.card_color2 = "#1C3989"  # Gris clair pour les cartes
        self.text_primary = "#f9f9fa"  # Gris foncé
        self.text_secondary = "#f8fafd"  # Gris moyen
        self.text_light = "#ffffff"  # Blanc
        self.shadow_color = "#516ec5"  # Gris clair pour ombres

        # Récupérer les informations de l'utilisateur
        self.user = page.session.get("user") or {
            "nom": "Inconnu",
            "prenom": "Inconnu",
            "email": "inconnu@example.com",
            "numero": "0000000000",
            "adresse": "N/A",
            "profession": "Enseignant"
        }

        # Initialiser les composants
        self.initialize_components()

    def __init__(self, page: Page):
        self.page = page
        self.page.adaptive = True
        self.page.title = "Profil Enseignant"
        
        # Palette de couleurs
        self.primary_color = "#667eea"  # Bleu-violet moderne
        self.secondary_color = "#041955"  # Rose doux
        self.other_color = "#2BC2A9"  # Vert menthe
        self.other_color2 = "#010102"  # Gris clair
        self.accent_color = "#4facfe"  # Bleu clair
        self.background_color = "#3450a1"  # Gris très clair
        self.card_color = "#041955"
        self.card_color2 = "#1C3989"  # Gris clair pour les cartes
        self.text_primary = "#f9f9fa"  # Gris foncé
        self.text_secondary = "#f8fafd"  # Gris moyen
        self.text_light = "#ffffff"  # Blanc
        self.shadow_color = "#516ec5"  # Gris clair pour ombres

        # Récupérer les informations de l'utilisateur
        self.user = page.session.get("user") or {
            "nom": "Inconnu",
            "prenom": "Inconnu",
            "email": "inconnu@example.com",
            "numero": "0000000000",
            "adresse": "N/A",
            "profession": "Enseignant"
        }

        # Initialiser les composants
        self.initialize_components()

        # Créer la boîte de dialogue de déconnexion
        self.dlg_deconnexion = AlertDialog(
            modal=True,
            title=Text("Déconnexion", color=self.text_primary),
            content=Text("Voulez-vous vraiment vous déconnecter ?", color=self.text_secondary),
            actions=[
                TextButton(
                    "Oui",
                    on_click=self.deconnecter,
                    style=ButtonStyle(color=self.other_color)
                ),
                TextButton(
                    "Non",
                    on_click=lambda e: self.dlg_deconnexion.close(),
                    style=ButtonStyle(color=self.text_secondary)
                )
            ],
            actions_alignment=MainAxisAlignment.END,
            on_dismiss=lambda e: print("Fenêtre de déconnexion fermée"),
            bgcolor=self.card_color
        )

    def deconnecter(self, e=None):
        """Gestion de la déconnexion"""
        try:
            # Effacer toutes les données de session
            self.page.session.clear()
            
            # Afficher un message de confirmation
            self.page.snack_bar = SnackBar(
                content=Text("Déconnexion réussie", color="white"),
                bgcolor=self.other_color  # Utilisation de notre couleur verte
            )
            self.page.snack_bar.open = True
            self.page.update()
            
            # Petit délai pour voir le message
            time.sleep(0.5)
            
            # Fermer la boîte de dialogue
            self.dlg_deconnexion.open = False
            self.page.update()
            
            # Redirection vers la page de connexion
            self.page.go("/page_bienvenue")
            
        except Exception as e:
            print(f"Erreur lors de la déconnexion: {e}")
            # Afficher un message d'erreur
            self.page.snack_bar = SnackBar(
                content=Text("Erreur lors de la déconnexion", color="white"),
                bgcolor="red"
            )
            self.page.snack_bar.open = True
            self.page.update()
            
            # Fermer la boîte de dialogue
            self.dlg_deconnexion.open = False
            self.page.update()

    def ouvrir_dialogue_deconnexion(self, e):
        """Ouvre la boîte de dialogue de déconnexion"""
        self.page.dialog = self.dlg_deconnexion
        self.dlg_deconnexion.open = True
        self.page.update()

    def get_page(self):
        # Structure finale
        return Stack(
            controls=[
                self.main_content,
                Container(
                    content=self.navigation_bar,
                    alignment=alignment.bottom_center,
                    bottom=0,
                    left=0,
                    right=0
                )
            ],
            expand=True
        )

def page_profil(page: Page, name=None):
    profil = ProfilPage(page)
    return [profil.get_page()]