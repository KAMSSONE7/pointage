from mysql.connector import Error
from datetime import datetime
from db_config import get_db_connection as create_db_connection
import mysql.connector

# Variable globale pour la connexion
_connection = None

def get_db_connection():
    """
    Obtient une connexion à la base de données.
    Utilise une connexion existante si elle est valide, en crée une nouvelle sinon.
    """
    global _connection
    try:
        if _connection is None or not _connection.is_connected():
            _connection = create_db_connection()
        return _connection
    except Error as e:
        print(f"Erreur lors de la connexion à la base de données: {e}")
        return None

def liste_utilisateur(user):
    """
    Cette fonction prend en paramètre le type d'utilisateur 
    puis retourne la liste des éléments de la base depuis la base de données.
    
    Exemple:
    resultat = liste_utilisateur('etudiant')
    retourne la liste des étudiants dans la variable resultat
    """
    try:
        connection = get_db_connection()
        if connection is None:
            return []
            
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {user}")
        liste_utilisateur = list(cursor.fetchall())
        connection.commit()
        return liste_utilisateur

    except Error as e:
        print(f"Erreur lors de la requête à MySQL: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()

def stat_etu(page=None):
    """
    Récupère les statistiques de présence des étudiants.
    Si 'page' est fourni, retourne les stats de l'étudiant actuel (basé sur la session).
    Sinon, retourne les stats globales des étudiants.
    """
    if page:
        # Version pour un étudiant spécifique (basée sur la session)
        etudiant_connecte = page.session.get("user")
        if not etudiant_connecte:
            print("Erreur: Pas d'utilisateur dans la session")
            return None

        try:
            connection = get_db_connection()
            if not connection or not connection.is_connected():
                print("Erreur: Impossible de se connecter à la base de données")
                return None

            cursor = connection.cursor()
            
            # Récupérer l'IP de l'étudiant depuis la session ou le numéro
            ip_etudiant = etudiant_connecte.get('IP')
            num_etudiant = etudiant_connecte.get('numero')
            
            if not ip_etudiant and not num_etudiant:
                print("Erreur: Aucun identifiant d'étudiant trouvé dans la session")
                return None
                
            # Si l'IP n'est pas dans la session, essayer de la récupérer avec le numéro
            if not ip_etudiant and num_etudiant:
                try:
                    cursor.execute("SELECT IP FROM etudiant WHERE Numero = %s OR Numero_carte_etu = %s LIMIT 1", 
                                 (num_etudiant, num_etudiant))
                    result = cursor.fetchone()
                    if result and result[0]:
                        ip_etudiant = result[0]
                        # Mettre à jour la session avec l'IP trouvée
                        etudiant_connecte['IP'] = ip_etudiant
                        page.session.set("user", etudiant_connecte)
                    else:
                        print(f"Erreur: Aucun étudiant trouvé avec le numéro: {num_etudiant}")
                        return None
                except Exception as e:
                    print(f"Erreur lors de la récupération de l'IP de l'étudiant: {e}")
                    return None
            
            # Récupérer les présences du mois dernier
            cursor.execute("""
                SELECT COUNT(*) 
                FROM detail_presence dp
                JOIN liste_presence lp ON dp.Id_liste = lp.Id_liste
                WHERE dp.IP_etudiant = %s 
                AND lp.Date_liste >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
            """, (ip_etudiant,))
            presence_mois = cursor.fetchone()[0]
            
            # Récupérer les présences de la semaine dernière
            cursor.execute("""
                SELECT COUNT(*) 
                FROM detail_presence dp
                JOIN liste_presence lp ON dp.Id_liste = lp.Id_liste
                WHERE dp.IP_etudiant = %s 
                AND lp.Date_liste >= DATE_SUB(CURDATE(), INTERVAL 1 WEEK)
            """, (ip_etudiant,))
            presence_semaine = cursor.fetchone()[0]
            
            # Récupérer le total des présences
            cursor.execute("""
                SELECT COUNT(*) 
                FROM detail_presence 
                WHERE IP_etudiant = %s
            """, (ip_etudiant,))
            total_presences = cursor.fetchone()[0]
            
            # Calculer le taux de présence (basé sur 20 jours de cours par mois)
            taux_presence = (presence_mois / 20 * 100) if presence_mois > 0 else 0
            
            # Récupérer la présence par jour
            cursor.execute("""
                SELECT 
                    DATE(lp.Date_liste) as date, 
                    COUNT(*) as nb_presences
                FROM detail_presence dp
                JOIN liste_presence lp ON dp.Id_liste = lp.Id_liste
                WHERE dp.IP_etudiant = %s
                AND lp.Date_liste >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
                GROUP BY DATE(lp.Date_liste)
                ORDER BY DATE(lp.Date_liste)
            """, (ip_etudiant,))
            
            presence_par_jour = {row[0].strftime('%Y-%m-%d'): row[1] for row in cursor.fetchall()}
            
            return {
                'total': total_presences,
                'presence_mois': presence_mois,
                'presence_semaine': presence_semaine,
                'taux_presence': taux_presence,
                'presence_par_jour': presence_par_jour
            }
        
        except Error as e:
            print(f"Erreur lors de la récupération des statistiques: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
    else:
        # Version pour les statistiques globales
        try:
            connection = get_db_connection()
            if connection is None:
                return []
                
            cursor = connection.cursor()
            cursor.execute("""
                SELECT e.Nom, e.Prenoms, COUNT(p.IP) AS total_presences
                FROM Etudiant e
                JOIN Presence_etu p ON e.IP = p.IP
                GROUP BY e.Nom, e.Prenoms;
            """)
            taux_presence = list(cursor.fetchall())
            
            cursor.execute("SELECT COUNT(*) FROM Presence_ens")
            total_seances = cursor.fetchone()[0]
            
            connection.commit()
            
            list_taux_presence = []
            for i in range(len(taux_presence)):
                res = (taux_presence[i][2] / total_seances) * 100 if total_seances > 0 else 0
                ch = f"{taux_presence[i][0]} {taux_presence[i][1]}"
                list_taux_presence.append((ch, round(res, 2), taux_presence[i][2], total_seances))
            return list_taux_presence

        except Error as e:
            print(f"Erreur lors de la connexion à MySQL: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()

def stat_etu_admin():
    try:
        # Connexion à la base de données
        connection = mysql.connector.connect(
            host='yamanote.proxy.rlwy.net',  # adresse de serveur MySQL
            database='railway',  # base de données utiliser
            user='root',  # nom d'utilisateur MySQL
            port='13208',
            password='oAEycvrWsPdjBfkQnEhqbSLoggHAadRt',  # Remplacez par votre mot de passe MySQL
            charset='utf8'
        )
        
        if not connection.is_connected():
            raise Exception("Impossible de se connecter à la base de données")
            
        cursor = connection.cursor()
        
        # Récupérer les présences des étudiants
        cursor.execute("""
            SELECT e.Nom, e.Prenoms, COUNT(p.IP) AS total_presences
            FROM Etudiant e
            JOIN Presence_etu p ON e.IP = p.IP
            GROUP BY e.Nom, e.Prenoms;   
        """)
        taux_presence = cursor.fetchall()
        
        # Récupérer le nombre total de séances
        cursor.execute("SELECT COUNT(*) FROM Presence_ens")
        total_seances = cursor.fetchone()[0]  
        
    except Error as e:
        print(f"Erreur MySQL: {e}")
        return []
    except Exception as e:
        print(f"Erreur: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection and connection.is_connected():
            connection.close()
            print("Connexion MySQL fermée")

    # Calculer les taux de présence
    list_taux_presence = []
    for i in range(len(taux_presence)):
        res = (taux_presence[i][2] / total_seances) * 100 if total_seances > 0 else 0
        nom_complet = f"{taux_presence[i][0]} {taux_presence[i][1]}"
        list_taux_presence.append((
            nom_complet,
            round(res, 2),
            taux_presence[i][2],
            total_seances
        ))
    
    return list_taux_presence

def stat_ens():
    """
    Récupère les statistiques de présence des enseignants.
    Retourne une liste de tuples (nom_complet, taux_presence, nb_presences, total_seances)
    """
    try:
        connection = get_db_connection()
        if connection is None:
            return []
            
        cursor = connection.cursor()
        
        # Récupérer le nombre de présences par enseignant
        cursor.execute("""
            SELECT e.Id_ens, e.Nom, e.Prenoms, 
                   COUNT(p.Id_pres) AS nb_presences
            FROM Enseignant e
            LEFT JOIN Presence_ens p ON e.Id_ens = p.Id_ens
            GROUP BY e.Id_ens, e.Nom, e.Prenoms;
        """)
        presences = cursor.fetchall()
        
        # Récupérer le nombre total de séances prévues par enseignant
        cursor.execute("""
            SELECT e.Id_ens, e.Nom, e.Prenoms, 
                   COUNT(edt.Id_emp) AS total_seances
            FROM Enseignant e
            JOIN Cours c ON e.Id_cours = c.Id_cours
            JOIN Emploi_du_temps edt ON c.Id_cours = edt.Id_cours
            GROUP BY e.Id_ens, e.Nom, e.Prenoms;
        """)
        total_seances = cursor.fetchall()
        
        # Créer un dictionnaire pour les totaux de séances
        seances_dict = {ens_id: total for ens_id, _, _, total in total_seances}
        
        # Calculer les taux de présence
        list_taux_presence = []
        for ens_id, nom, prenom, nb_pres in presences:
            total_seances_ens = seances_dict.get(ens_id, 0)
            taux_presence = (nb_pres / total_seances_ens * 100) if total_seances_ens > 0 else 0
            nom_complet = f"{nom} {prenom}"
            list_taux_presence.append((nom_complet, round(taux_presence, 2), nb_pres, total_seances_ens))
        
        return list_taux_presence
        
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()

def emploi_du_temps():
    """
    Renvoie l'emploi du temps.
    Returns:
        list: Une liste contenant quatre listes :
            - date_cours (list): Les dates des cours.
            - matiere (list): Les noms des matières.
            - heure_debut (list): Les heures de début des cours.
            - heure_fin (list): Les heures de fin des cours.
    """
    try:
        connection = get_db_connection()
        if connection is None:
            return [[], [], [], []]
            
        cursor = connection.cursor()
        cursor.execute("""
            SELECT Date_cours, Libelle, heure_deb, heure_fin
            FROM emploi_du_temps emp, cours crs
            WHERE crs.Id_cours = emp.Id_cours
            ORDER BY Date_cours;
        """)
        stat_cours = list(cursor.fetchall())
        connection.commit()
        
        date_cours = []
        matiere = []
        heure_debut = []
        heure_fin = []
        for i in range(len(stat_cours)):
            date_cours.append(stat_cours[i][0])
            matiere.append(stat_cours[i][1])
            heure_debut.append(stat_cours[i][2])
            heure_fin.append(stat_cours[i][3])
        
        return [date_cours, matiere, heure_debut, heure_fin]

    except Error as e:
        print(f"Erreur lors de la requête à MySQL: {e}")
        return [[], [], [], []]
    finally:
        if 'cursor' in locals():
            cursor.close()

def emploi_du_temps_prof(id):
    """
    Renvoie l'emploi du temps d'un enseignant à partir de son identifiant.
    Returns:
        list: Une liste contenant cinq listes :
            - date_cours (list): Les dates des cours.
            - matiere (list): Les noms des matières.
            - heure_debut (list): Les heures de début des cours.
            - heure_fin (list): Les heures de fin des cours.
            - nom_prenoms (list): Les noms complets des enseignants.
    """
    try:
        connection = get_db_connection()
        if connection is None:
            return [[], [], [], [], []]
            
        cursor = connection.cursor()
        cursor.execute(f"""
            SELECT 
                e.Nom, e.Prenoms, c.Libelle AS Cours,
                edt.Date_cours, edt.jours, edt.heure_deb,
                edt.heure_fin, s.Libelle AS Salle
            FROM Emploi_du_temps edt
            JOIN Cours c ON edt.Id_cours = c.Id_cours
            JOIN Enseignant e ON c.Id_cours = e.Id_cours
            JOIN Salle s ON edt.Id_salle = s.Id_salle
            WHERE e.Id_ens = '{id}';
        """)
        stat_cours = list(cursor.fetchall())
        connection.commit()
        
        date_cours = []
        matiere = []
        heure_debut = []
        heure_fin = []
        nom_prenoms = []
        for i in range(len(stat_cours)):
            date_cours.append(stat_cours[i][3])
            matiere.append(stat_cours[i][2])
            heure_debut.append(stat_cours[i][5])
            heure_fin.append(stat_cours[i][6])
            nom_prenoms.append(f"{stat_cours[i][0]} {stat_cours[i][1]}")
        
        return [date_cours, matiere, heure_debut, heure_fin, nom_prenoms]

    except Error as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")
        return [[], [], [], [], []]
    finally:
        if 'cursor' in locals():
            cursor.close()

def infos_presence_enseignant():
    """
    Récupère les informations de présence des enseignants.
    Returns:
        list: Une liste contenant cinq listes :
            - id_ens (list): Les identifiants des enseignants.
            - date (list): Les dates de présence.
            - heure_debut (list): Les heures de début.
            - heure_fin (list): Les heures de fin.
            - jours (list): Les jours de présence.
    """
    try:
        connection = get_db_connection()
        if connection is None:
            return [[], [], [], [], []]
            
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM presence_ens;")
        list_presence = list(cursor.fetchall())
        connection.commit()
        
        id_ens = []
        date = []
        heure_debut = []
        heure_fin = []
        jours = []
        for i in range(len(list_presence)):
            id_ens.append(list_presence[i][1])
            date.append(list_presence[i][3])
            heure_debut.append(list_presence[i][4])
            heure_fin.append(list_presence[i][5])
            jours.append(list_presence[i][6] if len(list_presence[i]) > 6 else None)
        
        return [id_ens, date, heure_debut, heure_fin, jours]

    except Error as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")
        return [[], [], [], [], []]
    finally:
        if 'cursor' in locals():
            cursor.close()

def comparer_dates(date1_str, date2_str):
    """
    Compare deux dates et affiche laquelle est antérieure, postérieure ou si elles sont égales.
    Args:
        date1_str (str): La première date sous forme de chaîne de caractères (format: 'YYYY-MM-DD').
        date2_str (str): La deuxième date sous forme de chaîne de caractères (format: 'YYYY-MM-DD').
    Returns:
        str: Un message indiquant le résultat de la comparaison.
    """
    try:
        date1 = datetime.strptime(date1_str, '%Y-%m-%d')
        date2 = datetime.strptime(date2_str, '%Y-%m-%d')
        if date1 < date2:
            return f"La date {date1_str} est antérieure à la date {date2_str}."
        elif date1 > date2:
            return f"La date {date1_str} est postérieure à la date {date2_str}."
        else:
            return f"La date {date1_str} est égale à la date {date2_str}."
    except ValueError as e:
        print(f"Erreur de format de date: {e}")
        return "Format de date invalide. Utilisez 'YYYY-MM-DD'."

def notify_professor(ip_etudiant, id_pres_ens):
    """
    Notifie le professeur de la présence d'un étudiant et met à jour le statut de la liste
    """
    try:
        connection = get_db_connection()
        if not connection or not connection.is_connected():
            return False

        cursor = connection.cursor()
        
        # Récupérer les informations de l'étudiant
        cursor.execute("""
            SELECT e.Nom, e.Prenoms, e.Numero_carte_etu 
            FROM Etudiant e 
            WHERE e.IP = %s
        """, (ip_etudiant,))
        etudiant = cursor.fetchone()
        
        if not etudiant:
            return False
            
        # Récupérer les informations du professeur
        cursor.execute("""
            SELECT Id_ens, Nom, Prenoms 
            FROM Presence_ens 
            JOIN Enseignant ON Presence_ens.Id_ens = Enseignant.Id_ens 
            WHERE Id_pres = %s
        """, (id_pres_ens,))
        professeur = cursor.fetchone()
        
        if not professeur:
            return False
            
        # Insérer la notification dans la table des messages
        cursor.execute("""
            INSERT INTO Messages (Id_ens, Contenu, Date_message, Lu)
            VALUES (%s, %s, NOW(), 0)
        """, (
            professeur[0],
            f"L'étudiant {etudiant[0]} {etudiant[1]} (N°{etudiant[2]}) a marqué sa présence. Veuillez valider la liste."
        ))
        
        connection.commit()
        return True
        
    except Error as e:
        print(f"Erreur lors de la notification: {e}")
        return False
        
    finally:
        if 'cursor' in locals():
            cursor.close()

def validate_list(id_pres_ens, valide):
    """
    Valide ou invalide la liste de présence d'un professeur
    """
    try:
        connection = get_db_connection()
        if not connection or not connection.is_connected():
            return False

        cursor = connection.cursor()
        
        # Mettre à jour le statut de validation
        cursor.execute("""
            UPDATE Presence_ens 
            SET Valide = %s 
            WHERE Id_pres = %s
        """, (valide, id_pres_ens))
        
        connection.commit()
        return True
        
    except Error as e:
        print(f"Erreur lors de la validation: {e}")
        return False
        
    finally:
        if 'cursor' in locals():
            cursor.close()

def infos_utilisateur(user):
    """
    Cette fonction prend en paramètre le type d'utilisateur 
    et retourne la liste des éléments de la base de données.
    
    Exemple:
    resultat = infos_utilisateur('etudiant')
    retourne la liste des étudiants dans la variable resultat
    """
    try:
        connection = get_db_connection()
        if connection is None:
            return []
            
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {user}")
        infos_utilisateur = list(cursor.fetchall())
        connection.commit()
        return infos_utilisateur

    except Error as e:
        print(f"Erreur lors de la requête à MySQL: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()

def emploi_du_temps_complet():
    """
    Renvoie l'emploi du temps complet.
    Returns:
        list: Une liste contenant six listes :
            - date_cours (list): Les dates des cours.
            - jours (list): Les jours des cours.
            - matiere (list): Les noms des matières.
            - salle (list): Les noms des salles.
            - heure_debut (list): Les heures de début des cours.
            - heure_fin (list): Les heures de fin des cours.
    """
    try:
        connection = get_db_connection()
        if connection is None:
            return [[], [], [], [], [], []]
            
        cursor = connection.cursor()
        cursor.execute("""
            SELECT 
                emp.Date_cours,
                emp.jours,
                crs.Libelle AS cours_libelle,
                s.Libelle AS salle_libelle,
                emp.heure_deb,
                emp.heure_fin
            FROM Emploi_du_temps emp
            JOIN Cours crs ON emp.Id_cours = crs.Id_cours
            JOIN Salle s ON emp.Id_salle = s.Id_salle
            ORDER BY emp.Date_cours, emp.heure_deb;
        """)                       
        emploi_du_temps = list(cursor.fetchall())
        connection.commit()
        
        date_cours = []
        jours = []
        matiere = []
        salle = []
        heure_debut = []
        heure_fin = []
        for i in range(len(emploi_du_temps)):
            date_cours.append(emploi_du_temps[i][0])
            jours.append(emploi_du_temps[i][1])
            matiere.append(emploi_du_temps[i][2])
            salle.append(emploi_du_temps[i][3])
            heure_debut.append(emploi_du_temps[i][4])
            heure_fin.append(emploi_du_temps[i][5])
        
        return [date_cours, jours, matiere, salle, heure_debut, heure_fin]        
    
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")
        return [[], [], [], [], [], []]
    finally:
        if 'cursor' in locals():
            cursor.close()

def affiche(name, type_user):
    """
    Affiche les informations d'un utilisateur (enseignant ou étudiant) à partir de son nom.
    Args:
        name (str): Le nom de l'utilisateur.
        type_user (str): Le type d'utilisateur ('ens' ou 'etu').
    Returns:
        list: Une liste contenant les informations de l'utilisateur.
    """
    try:
        list_ens = infos_utilisateur("enseignant")
        list_enseignant = [f"{ens[2]} {ens[3]}" for ens in list_ens]
        list_et = infos_utilisateur("etudiant")
        list_etudiant = [f"{et[3]} {et[4]}" for et in list_et]
        
        if type_user == 'ens':
            index = list_enseignant.index(name)
            return [list_ens[index][5], list_ens[index][4], list_ens[index][6]]  # numero, email, adresse
        else:
            index = list_etudiant.index(name)
            return [list_et[index][5], list_et[index][7], list_et[index][6], list_et[index][8]]  # niveau, numero, email, adresse

    except ValueError as e:
        print(f"Utilisateur {name} non trouvé: {e}")
        return []
    except Error as e:
        print(f"Erreur lors de la requête à MySQL: {e}")
        return []

def infos_user_connect(name, user):
    """
    Récupère les informations d'un utilisateur connecté (enseignant, étudiant ou admin) à partir de son nom.
    Args:
        name (str): Le nom complet de l'utilisateur (Nom Prénoms).
        user (str): Le type d'utilisateur ('ens', 'etu', 'admin').
    Returns:
        list: Une liste contenant les informations de l'utilisateur (nom, prénoms, numéro, email, adresse).
    """
    try:
        infos_enseignant = infos_utilisateur("enseignant")
        nom_prenom_enseignants = [f"{ens[2]} {ens[3]}" for ens in infos_enseignant]
        infos_etudiant = infos_utilisateur("Etudiant")
        nom_prenom_etudiants = [f"{et[3]} {et[4]}" for et in infos_etudiant]
        infos_admin = infos_utilisateur("administration")
        nom_prenom_admins = [f"{admin[1]} {admin[2]}" for admin in infos_admin]
        
        if user == "ens":
            index = nom_prenom_enseignants.index(name)
            return [
                infos_enseignant[index][2],  # nom
                infos_enseignant[index][3],  # prenoms
                infos_enseignant[index][5],  # numero
                infos_enseignant[index][4],  # email
                infos_enseignant[index][6]   # adresse
            ]
        elif user == "etu":
            index = nom_prenom_etudiants.index(name)
            return [
                infos_etudiant[index][3],  # nom
                infos_etudiant[index][4],  # prenoms
                infos_etudiant[index][7],  # numero
                infos_etudiant[index][6],  # email
                infos_etudiant[index][8]   # adresse
            ]
        elif user == "admin":
            index = nom_prenom_admins.index(name)
            return [
                infos_admin[index][1],  # nom
                infos_admin[index][2],  # prenoms
                infos_admin[index][4],  # numero
                infos_admin[index][3],  # email
                infos_admin[index][5]   # adresse
            ]
        else:
            return []

    except ValueError as e:
        print(f"Utilisateur {name} non trouvé: {e}")
        return []
    except Error as e:
        print(f"Erreur lors de la requête à MySQL: {e}")
        return []

def col():
    """
    Retourne une liste de couleurs prédéfinies.
    Returns:
        list: Une liste contenant les codes de couleur.
    """
    return ["#041955", "#FFFFFF", "#3450a1", "#eb06ff", "#2BC2A9"]

def enregistre_etu_present(ip):
    """
    Placeholder pour enregistrer la présence d'un étudiant.
    Args:
        ip (str): Identifiant de l'étudiant.
    """
    pass

def id_salle(id_enseignant):
    """
    Récupère l'identifiant de salle associées à un enseignant.
    """
    try:
        connection = get_db_connection()
        if connection is None:
            return []
            
        cursor = connection.cursor()
        cursor.execute(f"""
                SELECT distinct e.Id_salle
                FROM Emploi_du_temps e
                JOIN Enseignant ens ON ens.Id_cours = e.Id_cours
                JOIN Salle s ON e.Id_salle = s.Id_salle
                WHERE ens.Id_ens = '{id_enseignant}';                                         
                       """)
        id = cursor.fetchall()[0][0]
        connection.commit()
        return id

    except Error as e:
        print(f"Erreur lors de la requête à MySQL: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()