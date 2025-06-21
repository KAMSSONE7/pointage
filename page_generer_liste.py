import flet as ft
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error
from fonction import *
from db_config import get_db_connection

def page_generer_liste(page: ft.Page, utilisateur_connecte):

    user= page.session.get('user')
    if user and "nom" in user and "prenom" in user:
        name = str(user["nom"]) + " " + str(user["prenom"])
    else:
        name = "Kone Awa"
    list_ens = infos_utilisateur("enseignant")
    list_id = infos_utilisateur("enseignant")
    list_enseignant = [f"{ens[2]} {ens[3]}" for ens in list_ens]     
       
    def infos_id(name):
        index = list_enseignant.index(name)
        id_ens = list_id[index][0]  # Assuming the first element is the ID
        return id_ens
                 
            
    def button_clicked(e):
        # Extract user data
        user_id =  infos_id(name)
        profession = 'Enseignant'  # Assuming the user is an Enseignant

        # Validate user ID
        if not user_id:
            t.value = "❌ Erreur : ID utilisateur manquant"
            t.color = '#eb06ff'
            t.weight = ft.FontWeight.BOLD
            page.update()
            return

        # Validate input fields
        if not heure_debut_dropdown.value:
            t.value = "❌ Veuillez sélectionner une heure de début"
            t.color = '#eb06ff'
            t.weight = ft.FontWeight.BOLD
            page.update()
            return

        if not heure_fin_field.value:
            t.value = "❌ Veuillez entrer une heure de fin"
            t.color = '#eb06ff'
            t.weight = ft.FontWeight.BOLD
            page.update()
            return

        if not date_field.value:
            t.value = "❌ Veuillez entrer une date"
            t.color = '#eb06ff'
            t.weight = ft.FontWeight.BOLD
            page.update()
            return

        # Validate date format
        try:
            date_presence = datetime.strptime(date_field.value, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            t.value = "❌ Format de date incorrect ! Utilisez jj/mm/aaaa"
            t.color = '#eb06ff'
            t.weight = ft.FontWeight.BOLD
            page.update()
            return

        # Validate time format and logic
        try:
            heure_debut = datetime.strptime(heure_debut_dropdown.value, "%H:%M:%S").time()
            heure_fin = datetime.strptime(heure_fin_field.value, "%H:%M:%S").time()
            if heure_debut >= heure_fin:
                t.value = "❌ L'heure de fin doit être après l'heure de début"
                t.color = '#eb06ff'
                t.weight = ft.FontWeight.BOLD
                page.update()
                return
        except ValueError:
            t.value = "❌ Format d'heure incorrect ! Utilisez hh:mm:ss"
            t.color = '#eb06ff'
            t.weight = ft.FontWeight.BOLD
            page.update()
            return

        # Database connection
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            if not connection or not connection.is_connected():
                raise Exception("Impossible de se connecter à la base de données")

            cursor = connection.cursor()

            # Verify teacher exists
            cursor.execute("SELECT Id_ens, Nom, Prenoms FROM Enseignant WHERE Id_ens = %s", (user_id,))
            utilisateur = cursor.fetchone()
            if not utilisateur:
                cursor.execute("SELECT COUNT(*) FROM Enseignant")
                count = cursor.fetchone()[0]
                print(f"Nombre d'enseignants dans la base: {count}")
                raise Exception("Utilisateur non trouvé dans la base de données")

            # Check for existing presence record
            cursor.execute("SELECT COUNT(*) FROM Presence_ens WHERE Id_ens = %s AND Date_presence = %s", 
                          (user_id, date_presence))
            if cursor.fetchone()[0] > 0:
                raise Exception("Une liste de présence existe déjà pour cette date")

            # Insert presence record (use a valid Id_Salle from Salle table)
            cursor.execute(
                "INSERT INTO Presence_ens (Id_ens, Id_Salle, Date_presence, Heure_debut, Heure_fin) "
                "VALUES (%s, %s, %s, %s, %s)",
                (user_id, id_salle(user_id), date_presence, heure_debut_dropdown.value, heure_fin_field.value)
            )
            connection.commit()

            # Fetch students (use correct column IP instead of Id_etu)
            cursor.execute("SELECT IP, Nom, Prenoms FROM Etudiant")
            etudiants = cursor.fetchall()

            # Create student table
            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("ID")),
                    ft.DataColumn(ft.Text("Nom")),
                    ft.DataColumn(ft.Text("Prénom"))
                ],
                rows=[
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(etudiant[0]))),
                        ft.DataCell(ft.Text(etudiant[1])),
                        ft.DataCell(ft.Text(etudiant[2]))
                    ]) for etudiant in etudiants
                ]
            )

            # Display success message and table
            t.value = "✅ Liste de présence générée avec succès !"
            t.color = '#2BC2A9'
            t.weight = ft.FontWeight.BOLD
            page.add(table)
            page.update()

            # Hide input fields
            heure_debut_dropdown.visible = False
            heure_fin_field.visible = False
            date_field.visible = False
            b.visible = False

            # Show snackbar and redirect
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Redirection vers la page d'accueil...", color="white"),
                bgcolor="#2BC2A9"
            )
            page.snack_bar.open = True
            page.update()

            import time
            time.sleep(2)
            page.go('/page_accueil')

        except Error as e:
            print(f"Erreur MySQL: {e}")
            t.value = f"❌ Erreur : {str(e)}"
            t.color = '#eb06ff'
            t.weight = ft.FontWeight.BOLD
            page.update()
        except Exception as e:
            print(f"Erreur générale: {e}")
            t.value = f"❌ Erreur : {str(e)}"
            t.color = '#eb06ff'
            t.weight = ft.FontWeight.BOLD
            page.update()
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
                print("Connexion MySQL fermée")

    # Initialize text object for errors
    t = ft.Text()

    # Define dropdown options for start time
    lts = datetime.now().time()
    heure_options = []
    for i in range(12):
        new_time = (datetime.combine(datetime.now().date(), lts) + timedelta(hours=i)).time()
        r = str(new_time)
        if 6 < int(r[0:2]) <= 18:
            heure_options.append(r[0:8])

    heure_debut_dropdown = ft.Dropdown(
        label="HEURE DE DÉBUT",
        options=[ft.dropdown.Option(key=opt, text=opt) for opt in heure_options],
        label_style=ft.TextStyle(color='WHITE'),
        bgcolor='#2BC2A9',
        border_color='#2BC2A9',
        border_radius=25,
        width=300
    )

    heure_fin_field = ft.TextField(
        label="HEURE DE FIN (hh:mm:ss)",
        label_style=ft.TextStyle(color='WHITE'),
        color='WHITE',
        bgcolor='#2BC2A9',
        border_color='#2BC2A9',
        border_radius=25,
        width=300
    )

    def validate_date(e):
        date_str = date_field.value
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            date_field.error_text = None
        except ValueError:
            date_field.error_text = "Format incorrect ! Utilisez jj/mm/aaaa"
        page.update()

    date_field = ft.TextField(
        label="DATE (jj/mm/aaaa)",
        label_style=ft.TextStyle(color='WHITE'),
        color='WHITE',
        bgcolor='#2BC2A9',
        border_color='#2BC2A9',
        border_radius=25,
        width=300,
        on_change=validate_date
    )

    def validate_time(e):
        heure_debut = heure_debut_dropdown.value
        heure_fin = heure_fin_field.value
        if heure_debut and heure_fin:
            try:
                debut = datetime.strptime(heure_debut, "%H:%M:%S").time()
                fin = datetime.strptime(heure_fin, "%H:%M:%S").time()
                if debut >= fin:
                    t.value = "❌ L'heure de fin doit être après l'heure de début."
                    t.color = '#eb06ff'
                    t.weight = ft.FontWeight.BOLD
                else:
                    t.value = ""
            except ValueError:
                t.value = "❌ Format d'heure incorrect !"
                t.color = '#eb06ff'
                t.weight = ft.FontWeight.BOLD
        page.update()

    heure_debut_dropdown.on_change = validate_time
    heure_fin_field.on_change = validate_time

    b = ft.ElevatedButton(
        text="GÉNÉRER LA LISTE",
        on_click=button_clicked,
        style=ft.ButtonStyle(
            bgcolor="#2BC2A9",
            color="WHITE",
            shape=ft.RoundedRectangleBorder(radius=25),
            padding=ft.padding.all(15)
        )
    )

    return [
        ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color="WHITE", on_click=lambda _: page.go('/page_accueil')),
        ft.Text(value="GENERER LA LISTE DE PRESENCE", color="WHITE", weight=ft.FontWeight.BOLD, size=18),
        ft.Container(content=heure_debut_dropdown, alignment=ft.alignment.center),
        ft.Container(content=heure_fin_field, alignment=ft.alignment.center),
        ft.Container(content=date_field, alignment=ft.alignment.center),
        ft.Container(content=b, alignment=ft.alignment.center),
        t,
    ]