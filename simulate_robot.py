# geckodriver_path = '/usr/local/bin/geckodriver'  # Sur macOS/Linux
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.interaction import POINTER_MOUSE
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.action_builder import ActionBuilder
import time
import random


def simulate_click(driver, mouse, button_location, button_size, screen_width, screen_height):
    
    # Calculer le point central du bouton
    button_x = button_location['x'] + button_size['width'] / 2
    button_y = button_location['y'] + button_size['height'] / 2
    
    # Point de départ du mouvement (par exemple, coin supérieur gauche)
    start_x = screen_width/2
    start_y = screen_height/2

    # Randomise le point de départ
    start_x += random.randint(-screen_width/4, screen_width/4)
    start_y += random.randint(-screen_height/4, screen_height/4)

    print(f"Point de départ : ({start_x}, {start_y})")
    
    # Créer un constructeur d'actions
    actions = ActionBuilder(driver, mouse)

    # Déplacer la souris au point de départ
    actions.pointer_action.move_to_location(int(start_x), int(start_y))
    actions.perform()

    # Nombre d'étapes pour le mouvement
    steps = random.randint(15, 40) # (à ajuster si nécessaire)
    print(f"Nombre d'étapes : {steps}")
    # Calculer les positions intermédiaires
    x_positions = [start_x + (button_x - start_x) * (i + 1) / steps for i in range(steps)]
    y_positions = [start_y + (button_y - start_y) * (i + 1) / steps for i in range(steps)]

    # Déplacer la souris en ligne droite vers le bouton
    for x, y in zip(x_positions, y_positions):
        actions.pointer_action.move_to_location(int(x), int(y))
        actions.perform()
        time.sleep(0.02)  # Attendre un court instant pour simuler un mouvement naturel (à ajuster si nécessaire)

    # Cliquer sur le bouton
    actions.pointer_action.click()
    actions.perform()
    
    return True

def main():
    # Chemin vers GeckoDriver
    geckodriver_path = 'C:\\Drivers\\Gecko\\geckodriver.exe'  # Sur Windows

    # Créer un objet Service avec le chemin vers GeckoDriver
    service = Service(executable_path=geckodriver_path)

    # Initialiser le driver Firefox
    driver = webdriver.Firefox(service=service)

    # Ouvrir la page web
    driver.get('http://localhost:5000/')  # Remplacez par l'URL appropriée si différent

    # Attendre que la page se charge
    time.sleep(2)

    # Trouver le bouton sur la page
    button = driver.find_element(By.ID, 'stopButton')

    # Obtenir la position du bouton
    button_location = button.location
    button_size = button.size

    # Taille de l'écran
    screen_width = driver.execute_script("return window.screen.width")
    screen_height = driver.execute_script("return window.screen.height")

    # Créer un dispositif de saisie pour la souris
    mouse = PointerInput(POINTER_MOUSE, "mouse")

    # Simuler i clicks sur le bouton
    nb_clicks = 40 
    for i in range(nb_clicks):
        print("Click: ", i+1)
        simulate_click(driver, mouse, button_location, button_size, screen_width, screen_height)
        time.sleep(0.5)  # Attendre un court instant entre les clics (à ajuster si nécessaire)

    # Attendre que les données soient envoyées
    time.sleep(2)

    # Fermer le navigateur
    driver.quit()



# main
if __name__ == "__main__":
    main()