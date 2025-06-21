from flet import Page, Text, ElevatedButton, Column
import time
import threading

def main(page: Page):
    # Initialisation de la minuterie
    timer_text = Text(value="10", size=30)

    # Conteneur principal
    container = Column(controls=[timer_text])

    # Fonction pour démarrer la minuterie
    def start_timer(e):
        def countdown():
            for i in range(10, -1, -1):  # Compte à rebours de 10 à 0
                timer_text.value = str(i)
                page.update()  # Mettre à jour la page
                time.sleep(1)  # Pause d'une seconde

        # Démarrer le compte à rebours dans un thread séparé
        threading.Thread(target=countdown).start()

    # Bouton pour démarrer la minuterie
    start_button = ElevatedButton(text="Démarrer la minuterie", on_click=start_timer)
    container.controls.append(start_button)  # Ajouter le bouton dans le conteneur

    return container  # Retourner le conteneur
