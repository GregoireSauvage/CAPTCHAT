# geckodriver_path = '/usr/local/bin/geckodriver'  # Sur macOS/Linux
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.interaction import POINTER_MOUSE
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
from simulate_robot_pagui import simulate_click_pyautogui

def simulate_nice_click_selenium(driver, mouse, button_x, button_y, screen_width, screen_height):

    print(f"Position du bouton: ({button_x}, {button_y})")
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

    
    # Réinitialiser actions pour les mouvements suivants
    actions = ActionChains(driver)

    # Nombre d'étapes
    steps = random.randint(5, 7)
    print(f"Nombre d'étapes : {steps}")

    # Calculer les positions intermédiaires
    x_positions = [start_x + (button_x - start_x) * (i + 1) / steps for i in range(steps)]
    y_positions = [start_y + (button_y - start_y) * (i + 1) / steps for i in range(steps)]

    prev_x = start_x
    prev_y = start_y

    for x, y in zip(x_positions, y_positions):
        offset_x = x - prev_x
        offset_y = y - prev_y
        #print(f"Déplace vers ({x}, {y}), depuis ({prev_x}, {prev_y}), offset ({offset_x}, {offset_y})")
        actions.move_by_offset(int(offset_x), int(offset_y))
        # Optionnellement, ajouter une petite pause pour simuler un mouvement naturel
        actions.pause(0.001)
        prev_x = x
        prev_y = y
    actions.perform()
    
    
    # Cliquer sur le bouton
    actions = ActionBuilder(driver, mouse)
    actions.pointer_action.click()
    actions.perform()
    
    return True



def simulate_click_selenium(driver, mouse, button_x, button_y, screen_width, screen_height):
    
    
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
    steps = random.randint(5, 7) # (à ajuster si nécessaire)
    print(f"Nombre d'étapes : {steps}")
    # Calculer les positions intermédiaires
    x_positions = [start_x + (button_x - start_x) * (i + 1) / steps for i in range(steps)]
    y_positions = [start_y + (button_y - start_y) * (i + 1) / steps for i in range(steps)]

    # Déplacer la souris en ligne droite vers le bouton
    for x, y in zip(x_positions, y_positions):
        actions.pointer_action.move_to_location(int(x), int(y))
        actions.perform()

    # Cliquer sur le bouton
    actions.pointer_action.click()
    actions.perform()
    
    return True


def simulate_all_clicks(nb_clicks, driver, mouse, button_x, button_y, screen_width, screen_height):
    nb_clicks = int(nb_clicks/4)
    # Simuler n clicks sur le bouton
    for i in range(nb_clicks):
        print("Click: ", i+1)
        simulate_click_selenium(driver, mouse, button_x, button_y, screen_width, screen_height)
        time.sleep(2)  # Attendre un court instant entre les clics (à ajuster si nécessaire)
        driver.refresh()
    # Simuler i clicks sur le bouton
    for i in range(nb_clicks):
        print("Click nice: ", i+1)
        simulate_nice_click_selenium(driver, mouse, button_x, button_y, screen_width, screen_height)
        time.sleep(2)  # Attendre un court instant entre les clics (à ajuster si nécessaire)
        driver.refresh()
    for i in range(nb_clicks*2):
        print("Click PyAutoGui: ", i+1)
        simulate_click_pyautogui(button_x, button_y, screen_width, screen_height)
        time.sleep(2)
        driver.refresh()
    


def main():
    # Chemin vers GeckoDriver
    geckodriver_path = 'C:\\Drivers\\Gecko\\geckodriver.exe'  # Sur Windows

    # Créer un objet Service avec le chemin vers GeckoDriver
    service = Service(executable_path=geckodriver_path)
    
    # Initialiser le driver Firefox
    driver = webdriver.Firefox(service=service)
    driver.fullscreen_window()
    # Ouvrir la page web
    driver.get('http://localhost:5000/')  # Remplacez par l'URL appropriée si différent

    # Attendre que la page se charge
    time.sleep(2)

    # Trouver le bouton sur la page
    button = driver.find_element(By.ID, 'stopButton')

    # Obtenir la position du bouton
    button_location = button.location
    button_size = button.size
   
    # Calculer le point central du bouton
    button_x = button_location['x'] + button_size['width'] / 2
    button_y = button_location['y'] + button_size['height'] / 2
   
    # Taille de l'écran
    screen_width = driver.execute_script("return window.screen.width")
    screen_height = driver.execute_script("return window.screen.height")

    # Créer un dispositif de saisie pour la souris
    mouse = PointerInput(POINTER_MOUSE, "mouse")

    # Simuler n clicks sur le bouton
    simulate_all_clicks(12, driver, mouse, button_x, button_y, int(screen_width), int(screen_height))
   
    # Attendre que les données soient envoyées
    time.sleep(2)

    # Fermer le navigateur
    driver.quit()


# main
if __name__ == "__main__":
    main()