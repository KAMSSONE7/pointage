import flet as ft
from db_config import DB_CONFIG
import mysql.connector
from mysql.connector import Error
from db_config import get_db_connection

# Définition des couleurs
BG = "#041955"   # Bleu foncé
FWG = "#FFFFFF"  # Blanc
FG = "#3450a1"   # Bleu clair
PINK = "#eb06ff" # Rose

# Fonction pour récupérer les statistiques d'un enseignant spécifique
def fetch_teacher_statistics(teacher_id):
    try:
        connection = get_db_connection()
        if not connection or not connection.is_connected():
            print("Échec de la connexion à la base de données")
            return None
            
        print("Connexion à la base de données établie")
        cursor = connection.cursor(dictionary=True)
        
        # Statistiques de l'enseignant
        cursor.execute("""
            SELECT 
                e.Nom, 
                e.Prenoms, 
                COUNT(pe.Id_pres) AS nb_presences, 
                COALESCE(SUM(TIMESTAMPDIFF(MINUTE, pe.Heure_debut, pe.Heure_fin)), 0) AS total_minutes
            FROM 
                Enseignant e
            LEFT JOIN 
                Presence_ens pe ON e.Id_ens = pe.Id_ens
            WHERE 
                e.Id_ens = %s
            GROUP BY 
                e.Id_ens, e.Nom, e.Prenoms
        """, (teacher_id,))
            
        stats = cursor.fetchone()
        
        # Historique des présences
        cursor.execute("""
            SELECT 
                DATE(pe.Heure_debut) as date_presence,
                TIME(pe.Heure_debut) as heure_debut,
                TIME(pe.Heure_fin) as heure_fin,
                TIMESTAMPDIFF(MINUTE, pe.Heure_debut, pe.Heure_fin) as duree_minutes
            FROM 
                Presence_ens pe
            WHERE 
                pe.Id_ens = %s
            ORDER BY 
                pe.Heure_debut DESC
            LIMIT 10
        """, (teacher_id,))
        
        history = cursor.fetchall()
        
        return {
            'teacher_info': stats,
            'presence_history': history
        }

    except Error as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")
        return None

    finally:
        if 'connection' in locals() and connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion MySQL fermée")

# statistique en courbe
class State:
    toggle = True

s = State()

def page_stat1(page: ft.Page, teacher_id=None):
    # Si teacher_id n'est pas fourni, essayer de le récupérer depuis la session
    if teacher_id is None:
        try:
            user_data = page.session.get("user")
            if user_data and isinstance(user_data, dict) and 'id' in user_data:
                teacher_id = user_data['id']
                print(f"ID enseignant récupéré depuis la session: {teacher_id}")
            else:
                teacher_id = 'ENS004'  # Valeur par défaut pour les tests
                print(f"Aucun ID enseignant trouvé, utilisation de la valeur par défaut: {teacher_id}")
        except Exception as e:
            print(f"Erreur lors de la récupération de l'ID enseignant: {e}")
            teacher_id = 'ENS004'  # Valeur par défaut en cas d'erreur

    title = ft.Text(" STATISTIQUES ", size=30, color="WHITE", weight=ft.FontWeight.BOLD)

    # Récupération des données
    stats_data = fetch_teacher_statistics(teacher_id)
    if not stats_data or not stats_data.get('teacher_info'):
        print("Aucune donnée trouvée pour l'enseignant")
        return ft.Text("Aucune donnée disponible pour cet enseignant", color="red")
    
    # Extraction des données
    stats = stats_data['teacher_info']
    history = stats_data.get('presence_history', [])

    # Préparer les données pour le graphique
    if stats and 'nb_presences' in stats and 'total_minutes' in stats:
        # Créer des points de données pour le graphique
        data_points = [
            ft.LineChartDataPoint(0, 0),  # Point de départ à 0
            ft.LineChartDataPoint(1, stats['nb_presences']),  # Nombre de présences
            ft.LineChartDataPoint(2, stats['total_minutes'] / 60)  # Heures totales
        ]
        
        # 1. Statistiques en courbe
        data_1 = [
            ft.LineChartData(
                data_points=data_points,
                stroke_width=8,
                color=ft.Colors.LIGHT_GREEN,
                curved=True,
                stroke_cap_round=True,
            )
        ]
    else:
        # Données par défaut si pas de stats
        data_points = [ft.LineChartDataPoint(0, 0)]
        data_1 = [
            ft.LineChartData(
                data_points=data_points,
                stroke_width=8,
                color=ft.Colors.LIGHT_GREEN,
                curved=True,
                stroke_cap_round=True,
            )
        ]

    chart_1 = ft.LineChart(
        data_series=data_1,
        border=ft.Border(
            bottom=ft.BorderSide(4, ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE))
        ),
        left_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=1,
                    label=ft.Text("1H", size=14, weight=ft.FontWeight.BOLD),
                ),
                ft.ChartAxisLabel(
                    value=2,
                    label=ft.Text("2H", size=14, weight=ft.FontWeight.BOLD),
                ),
                ft.ChartAxisLabel(
                    value=3,
                    label=ft.Text("3H", size=14, weight=ft.FontWeight.BOLD),
                ),
            ],
            labels_size=40,
        ),
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=2,
                    label=ft.Container(
                        ft.Text(
                            "SEP",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                ),
                ft.ChartAxisLabel(
                    value=7,
                    label=ft.Container(
                        ft.Text(
                            "OCT",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                ),
            ],
            labels_size=32,
        ),
        tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY),
        min_y=0,
        max_y=4,
        min_x=0,
        max_x=14,
        expand=True,
    )

    def toggle_data(e):
        if s.toggle:
            chart_1.data_series = data_1[:2]
            chart_1.data_series[2].point = True
            chart_1.max_y = 6
            chart_1.interactive = False
        else:
            chart_1.data_series = data_1
            chart_1.max_y = 4
            chart_1.interactive = True
        s.toggle = not s.toggle
        chart_1.update()

    # Retourner une liste contenant les contrôles de la page des statistiques
    return [
        ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color="WHITE", on_click=lambda _: page.go('/page_statistiques')),
        title,ft.IconButton(ft.Icons.REFRESH, on_click=toggle_data),
        chart_1,
    ]