from flet import (
    Page, Text, Container, Column, DataTable, DataColumn, DataRow, DataCell,
    BoxShadow, Offset, Row, Icon, IconButton, margin, CrossAxisAlignment,
    padding, FontWeight, ScrollMode, MainAxisAlignment, border, TextStyle,
    alignment
)
from datetime import datetime, timedelta
from fonction import stat_etu
import math

def page_etu_stats(page: Page, user_data: dict = None):
    # Couleurs
    PRIMARY_COLOR = '#0D47A1'  # Bleu foncé
    SUCCESS_COLOR = '#66BB6A'  # Vert
    WARNING_COLOR = '#FFCA28'  # Jaune
    CARD_COLOR = '#FFFFFF'     # Blanc
    TEXT_PRIMARY = '#212121'   # Noir 87%
    TEXT_SECONDARY = '#616161' # Gris foncé
    CARD_SHADOW = '#1A000000'  # Noir 12%

    # Stocker les données utilisateur
    current_user = user_data or {}
    
    # Données de présence
    stats_presence = stat_etu(page)
    
    # Si les statistiques ne sont pas disponibles, utiliser des valeurs par défaut
    if stats_presence is None:
        stats_presence = {
            'presence_mois': 0,
            'presence_semaine': 0,
            'taux_presence': 0,
            'presence_par_jour': {}
        }
    
    # Extraire les statistiques
    presence_mois = stats_presence['presence_mois']
    presence_semaine = stats_presence['presence_semaine']
    taux_presence = stats_presence['taux_presence']
    presence_par_jour = stats_presence['presence_par_jour']
    
    # Préparer les données pour le graphique
    dates = [datetime.strptime(d, '%Y-%m-%d').strftime('%d/%m') for d in presence_par_jour.keys()]
    valeurs = list(presence_par_jour.values())

    # Fonction pour créer une carte de statistiques
    def create_stats_card(title, value, icon, color):
        return Container(
            content=Column([
                Row([
                    Icon(icon, size=24, color=color),
                    Text(title, size=16, weight=FontWeight.BOLD, color=TEXT_PRIMARY)
                ], spacing=10),
                Text(f"{value}{' %' if 'Taux' in title else ''}", size=24, weight=FontWeight.BOLD, color=color),
            ], spacing=5),
            bgcolor=CARD_COLOR,
            padding=15,
            border_radius=10,
            shadow=BoxShadow(
                spread_radius=0,
                blur_radius=5,
                color=CARD_SHADOW,
                offset=Offset(0, 2)
            )
        )

    # Fonction pour créer un graphique de présence simplifié
    def create_chart(data, dates, title):
        if not data or not dates:  # Handle empty data
            return Container(
                content=Text("Aucune donnée disponible", size=14, color=TEXT_SECONDARY),
                bgcolor=CARD_COLOR,
                padding=15,
                border_radius=10,
                shadow=BoxShadow(
                    spread_radius=0,
                    blur_radius=5,
                    color=CARD_SHADOW,
                    offset=Offset(0, 2)
                )
            )

        max_value = max(data, default=10)  # Default to 10 if data is empty
        
        # Créer les barres du graphique
        bars = []
        for i, value in enumerate(data):
            if i < len(dates):  # S'assurer qu'on ne dépasse pas la taille du tableau des dates
                bars.append(
                    Container(
                        width=40,
                        height=value * 10,  # Ajuster l'échelle si nécessaire
                        bgcolor=SUCCESS_COLOR,
                        border_radius=5,
                        tooltip=f"{dates[i]}: {value} présence(s)",
                        margin=margin.only(right=10)
                    )
                )

        # Créer les étiquettes de l'axe X
        x_labels = [
            Container(
                width=50,
                content=Text(dates[i] if i < len(dates) else "", size=10, color=TEXT_SECONDARY),
                margin=margin.only(right=10)
            ) 
            for i in range(len(data))
        ]

        # Créer les étiquettes de l'axe Y
        y_ticks = range(0, max_value + 2)  # +2 pour un peu d'espace en haut
        y_labels = [
            Text(str(y), size=10, color=TEXT_SECONDARY)
            for y in y_ticks
        ]

        return Container(
            content=Column([
                Text(title, size=18, weight=FontWeight.BOLD, color=TEXT_PRIMARY),
                # Conteneur pour le graphique et l'axe Y
                Row([
                    # Étiquettes de l'axe Y
                    Column(
                        [Text(" ", size=10)] + y_labels,  # Espace pour l'alignement
                        spacing=20,
                        horizontal_alignment=CrossAxisAlignment.END
                    ),
                    # Graphique à barres
                    Column([
                        # Les barres
                        Container(
                            content=Row(bars, spacing=10),
                            padding=padding.only(bottom=10, top=20)
                        ),
                        # Étiquettes de l'axe X
                        Container(
                            content=Row(x_labels, spacing=0),
                            margin=margin.only(left=20)
                        )
                    ])
                ])
            ]),
            bgcolor=CARD_COLOR,
            padding=15,
            border_radius=10,
            shadow=BoxShadow(
                spread_radius=0,
                blur_radius=5,
                color=CARD_SHADOW,
                offset=Offset(0, 2)
            )
        )


    # Bouton de retour
    retour = IconButton(
        icon="arrow_back",
        icon_color="white",
        on_click=lambda _: page.go("/page_etu_acc")
    )

    # Statistiques de présence avec défilement horizontal sur mobile
    stats_cards = Container(
        content=Row(
            [
                create_stats_card("Présence ce mois", presence_mois, "today", SUCCESS_COLOR),
                create_stats_card("Présence cette semaine", presence_semaine, "weekend", PRIMARY_COLOR),
                create_stats_card("Taux de présence", f"{taux_presence:.1f}%", "percent", WARNING_COLOR),
            ],
            spacing=15,
            scroll=ScrollMode.AUTO,
        ),
        padding=padding.symmetric(vertical=10),
    )

    # Créer un tableau pour les présences par jour avec défilement horizontal sur mobile
    presence_table = Container(
        content=Column([
            Text("Détail des présences par jour", size=18, weight=FontWeight.BOLD, color=TEXT_PRIMARY),
            Container(
                content=DataTable(
                    columns=[
                        DataColumn(Text("Date", weight=FontWeight.BOLD)),
                        DataColumn(Text("Présences", weight=FontWeight.BOLD))
                    ],
                    rows=[
                        DataRow(
                            cells=[
                                DataCell(Text(date, color=TEXT_PRIMARY)),
                                DataCell(Text(str(count), color=SUCCESS_COLOR))
                            ]
                        ) for date, count in presence_par_jour.items()
                    ],
                    border_radius=5,
                    border=border.all(1, "#e0e0e0"),
                    heading_row_color=PRIMARY_COLOR,
                    heading_text_style=TextStyle(color="white"),
                ),
                width=min(600, page.width - 40) if page else 600,  # Largeur maximale de 600px
            )
        ]),
        bgcolor=CARD_COLOR,
        padding=15,
        border_radius=10,
        shadow=BoxShadow(
            spread_radius=0,
            blur_radius=5,
            color=CARD_SHADOW,
            offset=Offset(0, 2)
        )
    )

    # Graphique et tableau de présence avec défilement horizontal sur mobile
    chart_container = Container(
        content=create_chart(valeurs, dates, "Présence par jour du mois"),
        width=min(800, (page.width - 60) if page else 800),  # Largeur maximale de 800px
    )
    
    presence_content = Column([
        # Conteneur avec défilement horizontal pour le graphique
        Container(
            content=Row(
                [chart_container],
                scroll=ScrollMode.AUTO,
                auto_scroll=False,
            ),
            padding=padding.symmetric(vertical=10),
        ),
        Container(height=20),
        presence_table
    ], spacing=15)

    # Structure de la page avec défilement vertical
    return [
        Container(
            content=Column([
                # En-tête avec bouton retour
                Container(
                    content=retour,
                    alignment=alignment.top_left,
                    padding=padding.only(bottom=10)
                ),
                # Contenu avec défilement vertical
                Container(
                    content=Column([
                        stats_cards,
                        presence_content
                    ], spacing=20, scroll=ScrollMode.AUTO),
                    expand=True,
                    padding=padding.symmetric(horizontal=10)
                )
            ], spacing=0, expand=True),
            padding=padding.all(10),
            expand=True
        )
    ]