import flet as ft
from db_config import DB_CONFIG
from flet import *
import mysql.connector
from mysql.connector import Error
from functools import partial
from datetime import datetime, timedelta
import time
from db_config import get_db_connection

# Fonction utilitaire pour convertir timedelta en chaîne HH:MM:SS
def timedelta_to_str(td):
    if td is None:
        return ""
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# Création des tables si elles n'existent pas
def create_table_if_not_exists():
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if not connection or not connection.is_connected():
            print("Impossible de se connecter à la base de données")
            return
            
        cursor = connection.cursor()
        
        # Créer la table presence_etu_archive
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS presence_etu_archive (
            IP VARCHAR(20) NOT NULL,
            Date_presence DATE NOT NULL,
            Heure_debut TIME NOT NULL,
            Heure_fin TIME NOT NULL,
            PRIMARY KEY (IP, Date_presence),
            FOREIGN KEY (IP) REFERENCES Etudiant(IP)
            )
            """)
            
        # Créer la table notification_professeur
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS notification_professeur (
            Id_notification INT PRIMARY KEY AUTO_INCREMENT,
            Id_ens VARCHAR(20) NOT NULL,
            IP_etudiant VARCHAR(20) NOT NULL,
            Nom_etudiant VARCHAR(50) NOT NULL,
            Prenoms_etudiant VARCHAR(50),
            Message TEXT NOT NULL,
            Date_notification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            Lu BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (Id_ens) REFERENCES Enseignant(Id_ens),
            FOREIGN KEY (IP_etudiant) REFERENCES Etudiant(IP)
        )
        """)
        
        # Créer la table liste_presence
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS liste_presence (
            Id_liste INT PRIMARY KEY AUTO_INCREMENT,
            Id_ens VARCHAR(20) NOT NULL,
            Date_liste DATE NOT NULL,
            Heure_creation TIME NOT NULL,
            Nombre_etudiants INT NOT NULL,
            FOREIGN KEY (Id_ens) REFERENCES Enseignant(Id_ens)
        )
        """)
        
        # Créer la table detail_presence
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS detail_presence (
            Id_liste INT NOT NULL,
            IP_etudiant VARCHAR(20) NOT NULL,
            Heure_arrivee TIME NOT NULL,
            PRIMARY KEY (Id_liste, IP_etudiant),
            FOREIGN KEY (Id_liste) REFERENCES liste_presence(Id_liste),
            FOREIGN KEY (IP_etudiant) REFERENCES Etudiant(IP)
        )
        """)
        
        connection.commit()
        print("Toutes les tables ont été créées avec succès")
        
    except Error as e:
        print(f"Erreur lors de la création des tables: {e}")
        if connection and connection.is_connected():
            connection.rollback()
    
    finally:
        if cursor and connection and connection.is_connected():
            cursor.close()
            connection.close()

def page_boite_de_reception(page: ft.Page, enseignant_connecte=None):
    create_table_if_not_exists()
    
    # Récupération de l'ID de l'enseignant
    enseignant_id = None
    if enseignant_connecte:
        print(f"Données de l'enseignant connecté: {enseignant_connecte}")
        if isinstance(enseignant_connecte, dict):
            enseignant_id = enseignant_connecte.get('id')
            print(f"ID de l'enseignant récupéré: {enseignant_id}")
        else:
            enseignant_id = enseignant_connecte
            print(f"ID de l'enseignant récupéré (non-dict): {enseignant_id}")
    
    if not enseignant_id:
        print("Erreur: ID de l'enseignant non trouvé")
        return []
    
    liste_notifications = []
    liste_presences_actuelles = []
    liste_etu = []
    liste_presence_historique = []
    
    def charger_donnees():
        nonlocal liste_notifications, liste_presences_actuelles, liste_etu, liste_presence_historique
        
        connection = None
        cursor = None
        
        try:
            from db_config import get_db_connection
            connection = get_db_connection()
            if not connection or not connection.is_connected():
                raise Exception("Impossible de se connecter à la base de données")
            
            if connection.is_connected():
                cursor = connection.cursor()
                
                if enseignant_id:
                    cursor.execute(
                        """
                        SELECT Id_notification, IP_etudiant, Nom_etudiant, Prenoms_etudiant, 
                               Message, Date_notification, Lu 
                        FROM notification_professeur 
                        WHERE Id_ens = %s 
                        ORDER BY Date_notification DESC
                        """,
                        (enseignant_id,)
                    )
                    liste_notifications = list(cursor.fetchall())
                
                cursor.execute("""
                    SELECT pe.IP, pe.Date_presence, pe.Heure_debut, pe.Heure_fin, 
                           e.Nom, e.Prenoms
                    FROM presence_etu pe
                    JOIN Etudiant e ON pe.IP = e.IP
                    WHERE DATE(pe.Date_presence) = CURDATE()
                    ORDER BY pe.Date_presence DESC
                """)
                liste_presences_actuelles = list(cursor.fetchall())
                
                cursor.execute("SELECT IP, Numero, Adresse, Nom, Prenoms FROM Etudiant")
                liste_etu = list(cursor.fetchall())
                
                if enseignant_id:
                    cursor.execute(
                        """
                        SELECT lp.Id_liste, lp.Date_liste, lp.Heure_creation, lp.Nombre_etudiants
                        FROM liste_presence lp
                        WHERE lp.Id_ens = %s
                        ORDER BY lp.Date_liste DESC, lp.Heure_creation DESC
                        """,
                        (enseignant_id,)
                    )
                    liste_presence_historique = list(cursor.fetchall())
                
                connection.commit()

        except Error as e:
            print(f"Erreur lors de la connexion à MySQL: {e}")
        
        finally:
            if cursor and connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    charger_donnees()
    
    def get_info_etudiant(ip):
        for etu in liste_etu:
            if etu[0] == ip:
                nom = etu[3] or ""
                prenoms = etu[4] or ""
                return f"{nom} {prenoms}".strip()
        return "Étudiant inconnu"
    
    def get_liste_details(id_liste):
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            if connection and connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(
                    """
                    SELECT dp.IP_etudiant, e.Nom, e.Prenoms, dp.Heure_arrivee
                    FROM detail_presence dp
                    JOIN Etudiant e ON dp.IP_etudiant = e.IP
                    WHERE dp.Id_liste = %s
                    ORDER BY dp.Heure_arrivee
                    """,
                    (id_liste,)
                )
                return cursor.fetchall()
                
        except Error as e:
            print(f"Erreur lors de la récupération des détails: {e}")
            return []
        finally:
            if cursor and connection and connection.is_connected():
                cursor.close()
                connection.close()
                
        return []
    
    def afficher_details_liste(e, id_liste):
        details = get_liste_details(id_liste)
        
        if not details:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Aucun détail trouvé pour cette liste")))
            return
        
        detail_controls = [
            ft.Text("Détails de la liste de présence", size=20, weight=ft.FontWeight.BOLD, color="WHITE"),
            ft.Divider(color="WHITE"),
        ]
        
        for detail in details:
            ip_etu, nom, prenoms, heure_arrivee = detail
            detail_controls.append(
                ft.Card(
                    content=ft.ListTile(
                        title=ft.Text(f"{nom} {prenoms or ''}", weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"IP: {ip_etu} | Arrivée: {timedelta_to_str(heure_arrivee) if heure_arrivee else 'N/A'}")
                    ),
                    margin=ft.margin.all(5)
                )
            )
        
        detail_controls.append(
            ft.ElevatedButton("Retour", on_click=lambda _: page.go('/page_boite_de_reception'))
        )
        
        detail_view = ft.View(
            route=f"/details/{id_liste}",
            controls=detail_controls,
            bgcolor="#1a1a1a",
            scroll=ft.ScrollMode.AUTO
        )
        
        page.views.append(detail_view)
        page.update()
    
    def enregistrer_liste_presence(e):
        if not liste_presences_actuelles:
            success_message.value = "Aucune présence à enregistrer !"
            success_message.color = "RED"
            page.update()
            return
        
        if not enseignant_id:
            success_message.value = "Enseignant non identifié !"
            success_message.color = "RED"
            page.update()
            return
            
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            
            if connection.is_connected():
                cursor = connection.cursor()
                
                cursor.execute(
                    """
                    INSERT INTO liste_presence (Id_ens, Date_liste, Heure_creation, Nombre_etudiants)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (enseignant_id, datetime.now().date(), datetime.now().time(), len(liste_presences_actuelles))
                )
                
                # Récupérer l'ID de la liste créée
                id_liste = cursor.lastrowid
                if id_liste is None:
                    cursor.execute("SELECT LAST_INSERT_ID()")
                    id_liste = cursor.fetchone()[0]
                
                # Enregistrer les détails de présence
                for presence in liste_presences_actuelles:
                    ip_etu = presence[0]
                    heure_debut = presence[2]
                    
                    try:
                        cursor.execute(
                            """
                            INSERT INTO detail_presence (Id_liste, IP_etudiant, Heure_arrivee)
                            VALUES (%s, %s, %s)
                            """,
                            (id_liste, ip_etu, heure_debut)
                        )
                    except Error as e:
                        print(f"Erreur lors de l'insertion dans detail_presence: {e}")
                        connection.rollback()
                        raise
                
                for presence in liste_presences_actuelles:
                    ip_etu, date_presence, heure_debut, heure_fin = presence[:4]
                    
                    cursor.execute(
                        "SELECT COUNT(*) FROM presence_etu_archive WHERE IP = %s AND Date_presence = %s",
                        (ip_etu, date_presence.date())
                    )
                    count = cursor.fetchone()[0]
                    
                    if count == 0:
                        cursor.execute(
                            """
                            INSERT INTO presence_etu_archive (IP, Date_presence, Heure_debut, Heure_fin) 
                            VALUES (%s, %s, %s, %s)
                            """,
                            (ip_etu, date_presence.date(), heure_debut, heure_fin)
                        )
                
                cursor.execute("DELETE FROM presence_etu WHERE DATE(Date_presence) = CURDATE()")
                
                connection.commit()
                
                charger_donnees()
                construire_interface()
                
                success_message.value = f"Liste de présence enregistrée avec succès ! ({len(liste_presences_actuelles)} étudiants)"
                success_message.color = "GREEN"
                page.update()
                
                def clear_message():
                    time.sleep(3)
                    success_message.value = ""
                    page.update()
                
                import threading
                threading.Thread(target=clear_message, daemon=True).start()

        except Error as e:
            print(f"Erreur lors de l'enregistrement : {e}")
            success_message.value = f"Erreur lors de l'enregistrement : {str(e)}"
            success_message.color = "RED"
            page.update()
            
        finally:
            if cursor and connection and connection.is_connected():
                cursor.close()
                connection.close()

    def supprimer_presence(e: ft.ControlEvent, ip_etudiant):
        nom_etudiant = get_info_etudiant(ip_etudiant)
        
        def confirmer_suppression(e):
            dlg_modal.open = False
            page.update()
            effectuer_suppression(ip_etudiant, nom_etudiant)
            
        def annuler_suppression(e):
            dlg_modal.open = False
            page.update()
            
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmation de suppression"),
            content=ft.Text(f"Êtes-vous sûr de vouloir retirer '{nom_etudiant}' de la liste de présence ?"),
            actions=[
                ft.TextButton("Annuler", on_click=annuler_suppression),
                ft.TextButton("Supprimer", on_click=confirmer_suppression),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    def effectuer_suppression(ip_etudiant, nom_etudiant):
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(
                    "DELETE FROM presence_etu WHERE IP = %s AND DATE(Date_presence) = CURDATE()",
                    (ip_etudiant,)
                )
                connection.commit()
                
                charger_donnees()
                construire_interface()
                
                success_message.value = f"'{nom_etudiant}' a été retiré de la liste de présence"
                success_message.color = "ORANGE"
                page.update()
                
                def clear_message():
                    time.sleep(3)
                    success_message.value = ""
                    page.update()
                
                import threading
                threading.Thread(target=clear_message, daemon=True).start()

        except Error as e:
            print(f"Erreur lors de la suppression: {e}")
            success_message.value = f"Erreur lors de la suppression : {str(e)}"
            success_message.color = "RED"
            page.update()

        finally:
            if cursor and connection and connection.is_connected():
                cursor.close()
                connection.close()

    def modifier_heure_presence(e: ft.ControlEvent, ip_etudiant):
        nom_etudiant = get_info_etudiant(ip_etudiant)
        
        heure_actuelle = None
        for presence in liste_presences_actuelles:
            if presence[0] == ip_etudiant:
                heure_actuelle = presence[2]
                break
        
        heure_field = ft.TextField(
            label="Nouvelle heure (HH:MM:SS)",
            value=timedelta_to_str(heure_actuelle) if heure_actuelle else "",
            width=200
        )
        
        def confirmer_modification(e):
            dlg_modal.open = False
            page.update()
            
            try:
                nouvelle_heure_str = heure_field.value
                datetime.strptime(nouvelle_heure_str, "%H:%M:%S")
                effectuer_modification_heure(ip_etudiant, nouvelle_heure_str, nom_etudiant)
                
            except ValueError:
                success_message.value = "Format d'heure invalide ! Utilisez HH:MM:SS"
                success_message.color = "RED"
                page.update()
        
        def annuler_modification(e):
            dlg_modal.open = False
            page.update()
        
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Modifier l'heure d'arrivée de {nom_etudiant}"),
            content=ft.Column([
                ft.Text("Entrez la nouvelle heure d'arrivée :"),
                heure_field,
            ], height=100),
            actions=[
                ft.TextButton("Annuler", on_click=annuler_modification),
                ft.TextButton("Modifier", on_click=confirmer_modification),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    def effectuer_modification_heure(ip_etudiant, nouvelle_heure_str, nom_etudiant):
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(
                    """
                    UPDATE presence_etu 
                    SET Heure_debut = %s 
                    WHERE IP = %s AND DATE(Date_presence) = CURDATE()
                    """,
                    (nouvelle_heure_str, ip_etudiant)
                )
                connection.commit()
                
                charger_donnees()
                construire_interface()
                
                success_message.value = f"Heure d'arrivée de '{nom_etudiant}' modifiée à {nouvelle_heure_str}"
                success_message.color = "BLUE"
                page.update()
                
                def clear_message():
                    time.sleep(3)
                    success_message.value = ""
                    page.update()
                
                import threading
                threading.Thread(target=clear_message, daemon=True).start()

        except Error as e:
            print(f"Erreur lors de la modification: {e}")
            success_message.value = f"Erreur lors de la modification : {str(e)}"
            success_message.color = "RED"
            page.update()

        finally:
            if cursor and connection and connection.is_connected():
                cursor.close()
                connection.close()

    def marquer_notification_lue(e: ft.ControlEvent, id_notification):
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(
                    "UPDATE notification_professeur SET Lu = TRUE WHERE Id_notification = %s",
                    (id_notification,)
                )
                connection.commit()
                
                charger_donnees()
                construire_interface()
                page.update()

        except Error as e:
            print(f"Erreur lors de la mise à jour de la notification: {e}")

        finally:
            if cursor and connection and connection.is_connected():
                cursor.close()
                connection.close()

    panel_notifications = ft.ExpansionPanelList()
    panel_presence = ft.ExpansionPanelList()
    panel_listes = ft.ExpansionPanelList()
    success_message = ft.Text(value="", weight=ft.FontWeight.BOLD, size=16)
    main_content = ft.Column()

    def construire_interface():
        panel_notifications.controls.clear()
        panel_notifications.expand_icon_color = ft.Colors.GREEN_500
        panel_notifications.elevation = 8
        panel_notifications.divider_color = ft.Colors.GREEN

        if enseignant_id and liste_notifications:
            for notification in liste_notifications:
                id_notif, ip_etu, nom_etu, prenoms_etu, message, date_notif, lu = notification
                bg_color = ft.Colors.GREY_200 if lu else ft.Colors.WHITE
                
                exp_notif = ft.ExpansionPanel(
                    bgcolor=bg_color,
                    header=ft.ListTile(
                        title=ft.Text(f"📧 {nom_etu} {prenoms_etu or ''}", 
                                    weight=ft.FontWeight.BOLD if not lu else ft.FontWeight.NORMAL),
                        subtitle=ft.Text(f"Le {date_notif.strftime('%d/%m/%Y à %H:%M')}")
                    ),
                    content=ft.ListTile(
                        title=ft.Text(message),
                        subtitle=ft.Text("Cliquez pour marquer comme lu" if not lu else "Lu"),
                        on_click=partial(marquer_notification_lue, id_notification=id_notif) if not lu else None,
                    ),
                )
                panel_notifications.controls.append(exp_notif)
        elif enseignant_id:
            exp_notif = ft.ExpansionPanel(
                header=ft.ListTile(title=ft.Text("📧 AUCUNE NOTIFICATION")),
                content=ft.ListTile(title=ft.Text("Aucune notification reçue", size=20)),
            )
            panel_notifications.controls.append(exp_notif)

        panel_presence.controls.clear()
        panel_presence.expand_icon_color = ft.Colors.BLUE_500
        panel_presence.elevation = 8
        panel_presence.divider_color = ft.Colors.PURPLE

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
                                    "✏️ Modifier l'heure",
                                    on_click=partial(modifier_heure_presence, ip_etudiant=ip_etu),
                                    color="BLUE"
                                ),
                                ft.ElevatedButton(
                                    "🗑️ Supprimer",
                                    on_click=partial(supprimer_presence, ip_etudiant=ip_etu),
                                    color="RED"
                                ),
                            ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                        ]),
                        padding=10
                    ),
                )
                panel_presence.controls.append(exp)

        panel_listes.controls.clear()
        panel_listes.expand_icon_color = ft.Colors.ORANGE_500
        panel_listes.elevation = 8
        panel_listes.divider_color = ft.Colors.ORANGE

        if enseignant_id and liste_presence_historique:
            for id_liste, date_liste, heure_creation, nb_etudiants in liste_presence_historique:
                exp = ft.ExpansionPanel(
                    bgcolor=ft.Colors.WHITE,
                    header=ft.ListTile(
                        title=ft.Text(f"Liste du {date_liste.strftime('%d/%m/%Y')}", weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"Créée à {timedelta_to_str(heure_creation)} - {nb_etudiants} étudiants")
                    ),
                    content=ft.ListTile(
                        title=ft.Text("Voir les détails"),
                        trailing=ft.IconButton(
                            ft.Icons.VISIBILITY,
                            on_click=partial(afficher_details_liste, id_liste=id_liste)
                        ),
                    ),
                )
                panel_listes.controls.append(exp)
        elif enseignant_id:
            exp = ft.ExpansionPanel(
                header=ft.ListTile(title=ft.Text("AUCUNE LISTE ENREGISTRÉE")),
                content=ft.ListTile(title=ft.Text("Aucune liste de présence enregistrée", size=20)),
            )
            panel_listes.controls.append(exp)

        main_content.controls.clear()
        main_content.controls.extend([
            ft.Divider(height=20, color=ft.Colors.WHITE),
            ft.Text(value="📧 NOTIFICATIONS", color="WHITE", weight=ft.FontWeight.BOLD, size=16) if enseignant_id else ft.Container(),
            panel_notifications if enseignant_id else ft.Container(),
            ft.Divider(height=20, color=ft.Colors.WHITE) if enseignant_id else ft.Container(),
            ft.Text(value="👥 ÉTUDIANTS PRÉSENTS AUJOURD'HUI", color="WHITE", weight=ft.FontWeight.BOLD, size=16),
            panel_presence,
            ft.Divider(height=20, color=ft.Colors.WHITE),
            ft.Text(value="📄 HISTORIQUE DES LISTES", color="WHITE", weight=ft.FontWeight.BOLD, size=16),
            panel_listes,
            ft.Row([
                ft.ElevatedButton(
                    text=f"Enregistrer la liste ({len(liste_presences_actuelles)} étudiants)", 
                    on_click=enregistrer_liste_presence,
                    disabled=len(liste_presences_actuelles) == 0
                ),
                ft.ElevatedButton(
                    text="Actualiser", 
                    on_click=lambda _: (charger_donnees(), construire_interface(), page.update())
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            success_message,
        ])
        
        main_content.scroll = ft.ScrollMode.AUTO
        main_content.expand = True

    construire_interface()

    return [
        ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color="WHITE", on_click=lambda _: page.go('/page_accueil')),
        ft.Text(value="VÉRIFICATION DE LA LISTE DU JOUR", color="WHITE", weight=ft.FontWeight.BOLD, size=18),
        main_content,
    ]