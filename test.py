# Voici les corrections à apporter à votre fonction supprimer_presence

# PROBLÈME 1: Syntaxe incorrecte avec partial
# Au lieu de :
# on_click=lambda e, ip=ip_etu, date=date_presence: supprimer_presence(e, ip, date)

# Utilisez :
on_click=lambda e, ip=ip_etu, date=date_presence: supprimer_presence(e, ip, date)

# PROBLÈME 2: Définition de la fonction corrigée
def supprimer_presence(e: ft.ControlEvent, ip_etudiant, date_presence=None):
    nom_etudiant = get_info_etudiant(ip_etudiant)
    
    def confirmer_suppression(e):
        dlg_modal.open = False
        page.update()
        effectuer_suppression(ip_etudiant, nom_etudiant, date_presence)
        
    def annuler_suppression(e):
        dlg_modal.open = False
        page.update()
        
    message = f"Êtes-vous sûr de vouloir retirer '{nom_etudiant}' de la liste de présence ?"
    if date_presence:
        message += f" pour le {date_presence.strftime('%d/%m/%Y')}"
        
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmation de suppression"),
        content=ft.Text(message),
        actions=[
            ft.TextButton("Annuler", on_click=annuler_suppression),
            ft.TextButton("Supprimer", on_click=confirmer_suppression),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    page.dialog = dlg_modal
    dlg_modal.open = True
    page.update()

# PROBLÈME 3: Dans la construction des panels, remplacez :
ft.ElevatedButton(
    "🗑️ Supprimer",
    on_click=lambda e, ip=ip_etu, date=date_presence: supprimer_presence(e, ip, date),
    color="RED"
),

# Par :
ft.ElevatedButton(
    "🗑️ Supprimer",
    on_click=lambda e, ip=ip_etu, date=date_presence: supprimer_presence(e, ip, date),
    color="RED"
),

# CORRECTION COMPLÈTE DE LA SECTION DANS construire_interface():
def construire_interface():
    # ... autres codes ...
    
    # Dans la partie panel_presence
    if not liste_presences_actuelles:
        exp = ft.ExpansionPanel(
            header=ft.ListTile(title=ft.Text("AUCUNE PRÉSENCE AUJOURD'HUI !")),
            content=ft.ListTile(title=ft.Text("Aucun étudiant présent pour le moment", size=20)),
        )
        panel_presence.controls.append(exp)
    else:
        for presence in liste_presences_actuelles:
            ip_etu, date_presence, heure_debut, heure_fin, nom, prenoms = presence
            nom_complet = f"{nom} {prenoms or ''}".strip()
            
            exp = ft.ExpansionPanel(
                bgcolor=ft.Colors.WHITE,
                header=ft.ListTile(
                    title=ft.Text(f"{nom_complet}", color="BLACK"),
                    subtitle=ft.Text(f"IP: {ip_etu} | Arrivée: {timedelta_to_str(heure_debut) if heure_debut else 'N/A'}")
                ),
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("ACTIONS DISPONIBLES", weight=ft.FontWeight.BOLD),
                        ft.Row([
                            ft.ElevatedButton(
                                "🗑️ Supprimer",
                                # CORRECTION ICI :
                                on_click=lambda e, ip=ip_etu, date=date_presence: supprimer_presence(e, ip, date),
                                color="RED"
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                    ]),
                    padding=10
                ),
            )
            panel_presence.controls.append(exp)
    
    # ... reste du code ...