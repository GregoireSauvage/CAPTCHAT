import pyautogui
import time
import numpy as np
import random

# position des elements
bouton = (40, 160)
coin_haut_gauche = (10, 150)
coin_bas_droit = (1910, 1000)
refresh = (120, 80)

def random_delay(min_delay=0.1, max_delay=0.5):
    """
    Introduit un délai aléatoire entre les actions.
    
    Paramètres:
    - min_delay: délai minimum en secondes.
    - max_delay: délai maximum en secondes.
    """
    time.sleep(random.uniform(min_delay, max_delay))

def random_point(point, variation):
    """
    Randomise les coordonnées d'un point par une variation spécifiée.
    
    Paramètres:
    - point: un tuple ou une liste avec deux éléments (x, y).
    - variation: la quantité par laquelle varier les coordonnées.
    
    Retourne:
    - Une liste avec les nouvelles coordonnées randomisées.
    """
    if not isinstance(point, (list, tuple)) or len(point) != 2:
        raise ValueError("Le point doit être une liste ou un tuple avec deux éléments (x, y).")
    
    return [
        random.uniform(point[0] - variation, point[0] + variation),
        random.uniform(point[1] - variation, point[1] + variation)
    ]

def click_randomly(variation=10, duration=0.2):
    duration = random.uniform(duration/2, duration*2)
    pyautogui.click(duration=duration)

# Fonction pour générer une courbe de Bézier
def bezier_curve(p1, p2, p3, p4, n_points=30):
    t_values = np.linspace(0, 1, n_points)
    bezier_points = []
    for t in t_values:
        x = (1-t)**3 * p1[0] + 3*(1-t)**2 * t * p2[0] + 3*(1-t) * t**2 * p3[0] + t**3 * p4[0]
        y = (1-t)**3 * p1[1] + 3*(1-t)**2 * t * p2[1] + 3*(1-t) * t**2 * p3[1] + t**3 * p4[1]
        bezier_points.append((x, y))
    return bezier_points

import numpy as np

# Fonction pour générer une courbe avec des splines cubiques (Catmull-Rom)
def cubic_spline_curve(start, destination, n_points=30):
    t_values = np.linspace(0, 1, n_points)
    spline_points = []
    for t in t_values:
        t2 = t * t
        t3 = t2 * t

        # Calcul des coefficients pour la spline de Catmull-Rom
        x = 0.5 * ((2 * start[0]) +
                   (-start[0] + destination[0]) * t +
                   (2 * start[0] - 5 * start[0] + 4 * destination[0] - destination[0]) * t2 +
                   (-start[0] + 3 * start[0] - 3 * destination[0] + destination[0]) * t3)

        y = 0.5 * ((2 * start[1]) +
                   (-start[1] + start[1]) * t +
                   (2 * start[1] - 5 * start[1] + 4 * destination[1] - destination[1]) * t2 +
                   (-start[1] + 3 * start[1] - 3 * destination[1] + destination[1]) * t3)

        spline_points.append((x, y))        
    return spline_points


# Fonction pour générer une courbe avec des déplacements aléatoires
def random_curve(key_points, n_points=30):
    t_values = np.linspace(0, 1, n_points)
    points = []
    nb_key_points = len(key_points)
    for t in t_values:
        for i in range(nb_key_points-1):
            p1 = key_points[i]
            p2 = key_points[i+1]
            # Répartir les points le long de la ligne entre les points clés
            x = (1-t) * p1[0] + t * p2[0]
            y = (1-t) * p1[1] + t * p2[1]
            x, y = random_point((x, y), 3)  # Ajouter une variation aléatoire

        points.append((x, y))
        
    return points

# Fonction pour ajouter une variation aléatoire aux points
def random_point(point, variation):
    return (point[0] + random.uniform(-variation, variation), point[1] + random.uniform(-variation, variation))

# Fonction pour générer des durées aléatoires totalisant une durée spécifiée
def generate_random_durations(total_duration, n_points):
    durations = np.random.exponential(scale=total_duration/n_points, size=n_points)
    return durations / durations.sum() * total_duration

# Fonction pour déplacer la souris de manière réaliste en utilisant une courbe de Bézier
def move_mouse_bezier(destination, duration=0.5, perturbations=True):
    start_x, start_y = pyautogui.position()
    start_x, start_y = random_point((start_x, start_y), 5) # Ajouter une variation aléatoire aux points de départ
    end_x, end_y = destination
    end_x, end_y = random_point((end_x, end_y), 5) # Ajouter une variation aléatoire aux points de destination

    distance = ((end_x - start_x)**2 + (end_y - start_y)**2)**0.5   # distance entre le point de départ et le point d'arrivée
    n_points = 5 + int(distance / 35)  # ajuster le nombre de points en fonction de la distance
    n_points = int(n_points*2/3)
    print(f"nb de points: {n_points}")
    distance_x = abs(end_x - start_x)
    distance_y = abs(end_y - start_y)
    
    # Définir les points de contrôle
    control1 = start_x + random.uniform(-distance_x, distance_x), start_y + random.uniform(-distance_y, distance_y)
    control2 = end_x + random.uniform(-distance_x, distance_x), end_y + random.uniform(-distance_y, distance_y)
    control1 = random_point(control1, 5) # Ajouter une variation aléatoire aux points de contrôle
    control2 = random_point(control2, 5) # Ajouter une variation aléatoire aux points de contrôle

    # Générer les points le long de la courbe de Bézier
    points = bezier_curve((start_x, start_y), control1, control2, (end_x, end_y), n_points)

    # Ajouter des perturbations aléatoires pour simuler les changements brusques de direction
    if perturbations:
        points = perturbation(points)
    
    # vérifie que les points ont des coordonnées valides (positives)
    for i, (x, y) in enumerate(points):
        if x <= 0 or y <= 0:
            points[i] = (max(1, x), max(1, y))
            
    # Générer des intervalles de temps aléatoires
    intervals = generate_random_durations(duration, n_points)

    # Sélectionner des points d'hésitation
    total_points = len(points)
    num_pauses = random.randint(2, 5)
    pause_indices = sorted(random.sample(range(1, total_points - 1), num_pauses))
    pause_durations = {index: random.uniform(0.1, 0.5) for index in pause_indices}
    
    # Déplacer la souris selon les points avec hésitations
    for index, (point, interval) in enumerate(zip(points, intervals)):
        pyautogui.moveTo(point[0], point[1])

        # Vérifier si c'est un point d'hésitation
        if index in pause_indices and perturbations:
            pause_duration = pause_durations[index]
            time.sleep(pause_duration)

        time.sleep(interval / 2)
        

# Fonction pour déplacer la souris de manière réaliste en utilisant une courbe avec des splines cubiques
def move_mouse_cubic_spline(destination, duration=0.5, perturbations=True):
    start_x, start_y = pyautogui.position()
    start_x, start_y = random_point((start_x, start_y), 5) # Ajouter une variation aléatoire aux points de départ
    end_x, end_y = destination
    end_x, end_y = random_point((end_x, end_y), 5) # Ajouter une variation aléatoire aux points de destination

    distance = ((end_x - start_x)**2 + (end_y - start_y)**2)**0.5   # distance entre le point de départ et le point d'arrivée
    n_points = 5 + int(distance / 35)  # ajuster le nombre de points en fonction de la distance
    print(f"nb de points: {n_points}")
    distance_x = abs(end_x - start_x)
    distance_y = abs(end_y - start_y)
    
    # Définir les points de contrôle
    control1 = start_x + random.uniform(-distance_x, distance_x), start_y + random.uniform(-distance_y, distance_y)
    control2 = end_x + random.uniform(-distance_x, distance_x), end_y + random.uniform(-distance_y, distance_y)
    control1 = random_point(control1, 5) # Ajouter une variation aléatoire aux points de contrôle
    control2 = random_point(control2, 5) # Ajouter une variation aléatoire aux points de contrôle

    # Générer les points le long de la courbe cubique spline
    points = cubic_spline_curve((start_x, start_y), (end_x, end_y), n_points)
    
    if perturbations:
        # Ajouter des perturbations aléatoires pour simuler les changements brusques de direction
        points = perturbation(points)
        
    # vérifie que les points ont des coordonnées valides (positives)
    for i, (x, y) in enumerate(points):
        if x <= 0 or y <= 0:
            points[i] = (max(1, x), max(1, y))
    
    # Générer des intervalles de temps aléatoires
    intervals = generate_random_durations(duration, n_points)

    # Sélectionner des points d'hésitation
    total_points = len(points)
    num_pauses = random.randint(2, 5)
    pause_indices = sorted(random.sample(range(1, total_points - 1), num_pauses))
    pause_durations = {index: random.uniform(0.1, 0.5) for index in pause_indices}
    
    # Déplacer la souris selon les points avec hésitations
    for index, (point, interval) in enumerate(zip(points, intervals)):
        pyautogui.moveTo(point[0], point[1])

        # Vérifier si c'est un point d'hésitation
        if perturbations and index in pause_indices:
            pause_duration = pause_durations[index]
            time.sleep(pause_duration)

        time.sleep(interval / 2)


# Fonction pour déplacer la souris avec des changements de direction aléatoires
def move_mouse_randomly(destination, duration=0.5, perturbations=True):
    start_x, start_y = pyautogui.position()
    start_x, start_y = random_point((start_x, start_y), 5) # Ajouter une variation aléatoire aux points de départ

    end_x, end_y = destination
    end_x, end_y = random_point((end_x, end_y), 5) # Ajouter une variation aléatoire aux points de destination

    distance = ((end_x - start_x)**2 + (end_y - start_y)**2)**0.5   # distance entre le point de départ et le point d'arrivée
    n_points = 5 + int(distance / 35)  # ajuster le nombre de points en fonction de la distance
    n_points = int(n_points*2/3)
    print(f"nb de points: {n_points}")

    nb_key_points = random.randint(2, 5)  # Nombre de points clés pour la trajectoire (changements de direction)
    key_points = [(start_x, start_y)]
    for i in range(nb_key_points): # Générer les points clés aléatoires entre le point de départ et le point d'arrivée
        prev_x, prev_y = key_points[i]  # Extraire les coordonnées x et y du point précédent
        x = random.uniform(prev_x, end_x)# + random.uniform(50, distance/5)
        y = random.uniform(prev_y, end_y) #+ random.uniform(50, distance/5)
        x, y = random_point((x, y), 5)
        key_points.append((x, y))
    key_points.append((end_x, end_y))
    # Générer les points le long de la courbe de Bézier
    points = random_curve(key_points, n_points)

    if perturbations:
        # Ajouter des perturbations aléatoires pour simuler les changements brusques de direction
        points = perturbation(points)
    
    # vérifie que les points ont des coordonnées valides (positives)
    for i, (x, y) in enumerate(points):
        if x <= 0 or y <= 0:
            points[i] = (max(1, x), max(1, y))
    
    # Générer des intervalles de temps aléatoires
    intervals = generate_random_durations(duration, n_points)

    # Sélectionner des points d'hésitation
    total_points = len(points)
    num_pauses = random.randint(2, 5)
    pause_indices = sorted(random.sample(range(1, total_points - 1), num_pauses))
    pause_durations = {index: random.uniform(0.1, 0.5) for index in pause_indices}
    
    # Déplacer la souris selon les points avec hésitations
    for index, (point, interval) in enumerate(zip(points, intervals)):
        pyautogui.moveTo(point[0], point[1])

        # Vérifier si c'est un point d'hésitation
        if perturbations and index in pause_indices:
            pause_duration = pause_durations[index]
            time.sleep(pause_duration)

        time.sleep(interval / 2)


# Fonction pour déplacer la souris avec des changements de direction aléatoires
def move_mouse_linear(destination, duration=0.5, perturbations=True):
    start_x, start_y = pyautogui.position()
    start_x, start_y = random_point((start_x, start_y), 5) # Ajouter une variation aléatoire aux points de départ

    end_x, end_y = destination
    end_x, end_y = random_point((end_x, end_y), 5) # Ajouter une variation aléatoire aux points de destination

    distance = ((end_x - start_x)**2 + (end_y - start_y)**2)**0.5   # distance entre le point de départ et le point d'arrivée
    n_points = 5 + int(distance / 35)  # ajuster le nombre de points en fonction de la distance
    n_points = int(n_points*2/3)
    print(f"nb de points: {n_points}")

    nb_key_points = random.randint(2, 5)  # Nombre de points clés pour la trajectoire (changements de direction)
    key_points = [(start_x, start_y)]
    for i in range(nb_key_points): # Générer les points clés aléatoires entre le point de départ et le point d'arrivée
        prev_x, prev_y = key_points[i]  # Extraire les coordonnées x et y du point précédent
        x = random.uniform(prev_x, end_x) + random.uniform(50, distance/5)
        y = random.uniform(prev_y, end_y) + random.uniform(50, distance/5)
        x, y = random_point((x, y), 5)
        key_points.append((x, y))
    key_points.append((end_x, end_y))
    # Générer les points le long de la courbe de Bézier
    points = random_curve(key_points, n_points)
    
    if perturbations:
        # Ajouter des perturbations aléatoires pour simuler les changements brusques de direction
        points = perturbation(points)
    
    # vérifie que les points ont des coordonnées valides (positives)
    for i, (x, y) in enumerate(points):
        if x <= 0 or y <= 0:
            points[i] = (max(1, x), max(1, y))
    
    # Générer des intervalles de temps aléatoires
    intervals = generate_random_durations(duration, n_points)

    # Sélectionner des points d'hésitation
    total_points = len(points)
    num_pauses = random.randint(2, 5)
    pause_indices = sorted(random.sample(range(1, total_points - 1), num_pauses))
    pause_durations = {index: random.uniform(0.1, 0.5) for index in pause_indices}
    
    # Déplacer la souris selon les points avec hésitations
    for index, (point, interval) in enumerate(zip(points, intervals)):
        pyautogui.moveTo(point[0], point[1])

        # Vérifier si c'est un point d'hésitation
        if perturbations and index in pause_indices:
            pause_duration = pause_durations[index]
            time.sleep(pause_duration)

        time.sleep(interval / 2)



def simulate_bezier_click_pyautogui(button_x, button_y, screen_width, screen_height, perturbations=True):
    try:
        depart = (500, 500)

        button = (button_x, button_y)
        # Déplacer la souris vers son point de l'écran
        depart = (random.uniform(0, screen_width), random.uniform(0, screen_height))
        
        
        print(f"Point de départ : {depart}")
        pyautogui.moveTo(depart[0], depart[1])
        print(f"Point d'arrivée : {button}")
        # Déplacer la souris de manière réaliste vers le bouton
        move_mouse_bezier(button, duration=0.2, perturbations=perturbations)
        
        # Cliquer sur le bouton
        click_randomly(duration=0.2)
    except Exception as e:
        print(f"Erreur: {e}")
    return

def simulate_cubic_spline_click_pyautogui(button_x, button_y, screen_width, screen_height, perturbations=True):
    try:
        depart = (500, 500)

        button = (button_x, button_y)
        # Déplacer la souris vers son point de l'écran
        depart = (random.uniform(0, screen_width), random.uniform(0, screen_height))
        
        
        print(f"Point de départ : {depart}")
        pyautogui.moveTo(depart[0], depart[1])
        print(f"Point d'arrivée : {button}")
        # Déplacer la souris de manière réaliste vers le bouton
        move_mouse_cubic_spline(button, duration=0.2, perturbations=perturbations)
        
        # Cliquer sur le bouton
        click_randomly(duration=0.2)
    except Exception as e:
        print(f"Erreur: {e}")
    return


def simulate_random_click_pyautogui(button_x, button_y, screen_width, screen_height, perturbations=True):
    try:
        depart = (500, 500)

        button = (button_x, button_y)
            # Déplacer la souris vers son point de l'écran
        depart = (random.uniform(0, screen_width), random.uniform(0, screen_height))
        
        
        print(f"Point de départ : {depart}")
        pyautogui.moveTo(depart[0], depart[1])
        print(f"Point d'arrivée : {button}")
        # Déplacer la souris de manière réaliste vers le bouton
        move_mouse_randomly(button, duration=0.2, perturbations=perturbations)
        
        # Cliquer sur le bouton
        click_randomly(duration=0.2)
    except Exception as e:
        print(f"Erreur: {e}")
        
    return


def simulate_linear_click_pyautogui(button_x, button_y, screen_width, screen_height, perturbations=True):
    try:
        depart = (500, 500)
        button = (button_x, button_y)
            # Déplacer la souris vers son point de l'écran
        depart = (random.uniform(0, screen_width), random.uniform(0, screen_height))
        
        
        print(f"Point de départ : {depart}")
        pyautogui.moveTo(depart[0], depart[1])
        print(f"Point d'arrivée : {button}")
        # Déplacer la souris de manière réaliste vers le bouton
        move_mouse_linear(button, duration=0.2, perturbations=perturbations)
        
        # Cliquer sur le bouton
        click_randomly(duration=0.2)
    except Exception as e:
        print(f"Erreur: {e}")
        
    return


def perturbation(points):
    # **Ajouter des perturbations aléatoires pour simuler les changements brusques de direction**
    total_points = len(points)
    num_perturbations = random.randint(3, 7)  # Nombre de perturbations à ajouter
    perturbation_indices = random.sample(range(1, total_points - 1), num_perturbations)

    # Ajouter les perturbations aux points sélectionnés
    for index in perturbation_indices:
        x, y = points[index]
        x += random.uniform(-20, 20)  # Déviation en x
        y += random.uniform(-20, 20)  # Déviation en y
        points[index] = (x, y)
        
    return points
    
    
def main():
    taille_ecran = coin_bas_droit[0] - coin_haut_gauche[0], coin_bas_droit[1] - coin_haut_gauche[1]
    
    
    n = int(150/6)
    # for i in range(n):
    #     # Simule un déplacement linéaire vers le bouton
    #     pyautogui.moveTo(refresh[0], refresh[1])
    #     click_randomly(duration=0.2)
    #     simulate_linear_click_pyautogui(bouton[0], bouton[1], taille_ecran[0], taille_ecran[1], perturbations=False)
    #     time.sleep(1)
    # for i in range(n):
    #     # Simule un déplacement linéaire vers le bouton avec des perturbations
    #     pyautogui.moveTo(refresh[0], refresh[1])
    #     click_randomly(duration=0.2)
    #     simulate_linear_click_pyautogui(bouton[0], bouton[1], taille_ecran[0], taille_ecran[1], perturbations=True)
    #     time.sleep(1)
    # for i in range(n):
    #     # Simule un déplacement random vers le boutons
    #     pyautogui.moveTo(refresh[0], refresh[1])
    #     click_randomly(duration=0.2)
    #     simulate_random_click_pyautogui(bouton[0], bouton[1], taille_ecran[0], taille_ecran[1], perturbations=False)
    #     time.sleep(1)
    # for i in range(n):
    #     # Simule un déplacement random vers le bouton avec des perturbations
    #     pyautogui.moveTo(refresh[0], refresh[1])
    #     click_randomly(duration=0.2)
    #     simulate_random_click_pyautogui(bouton[0], bouton[1], taille_ecran[0], taille_ecran[1], perturbations=True)
    #     time.sleep(1)

    # for i in range(n):
    #     # Simule un déplacement en suivant une courb de bézier vers le bouton
    #     pyautogui.moveTo(refresh[0], refresh[1])
    #     click_randomly(duration=0.2)
    #     simulate_bezier_click_pyautogui(bouton[0], bouton[1], taille_ecran[0], taille_ecran[1], perturbations=False)
    #     time.sleep(1)
    # for i in range(n):
    #     # Simule un déplacement en suivant une courb de bézier vers le bouton avec des perturbations
    #     pyautogui.moveTo(refresh[0], refresh[1])
    #     click_randomly(duration=0.2)
    #     simulate_bezier_click_pyautogui(bouton[0], bouton[1], taille_ecran[0], taille_ecran[1], perturbations=True)
    #     time.sleep(1)
        
        
    pyautogui.moveTo(refresh[0], refresh[1])
    click_randomly(duration=0.2)
    #simulate_bezier_click_pyautogui(bouton[0], bouton[1], taille_ecran[0], taille_ecran[1], perturbations=False)
    #simulate_random_click_pyautogui(bouton[0], bouton[1], taille_ecran[0], taille_ecran[1], perturbations=False)
    simulate_linear_click_pyautogui(bouton[0], bouton[1], taille_ecran[0], taille_ecran[1], perturbations=True)   

if __name__ == "__main__":
    main()