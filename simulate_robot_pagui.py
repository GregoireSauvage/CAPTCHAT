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

# Fonction pour ajouter une variation aléatoire aux points
def random_point(point, variation):
    return (point[0] + random.uniform(-variation, variation), point[1] + random.uniform(-variation, variation))

# Fonction pour générer des durées aléatoires totalisant une durée spécifiée
def generate_random_durations(total_duration, n_points):
    durations = np.random.exponential(scale=total_duration/n_points, size=n_points)
    return durations / durations.sum() * total_duration

# Fonction pour déplacer la souris de manière réaliste en utilisant une courbe de Bézier
def move_mouse_realistically(destination, duration=0.5):
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

    # Générer des intervalles de temps aléatoires
    intervals = generate_random_durations(duration, n_points)

    # Déplacer la souris selon les points de la courbe de Bézier
    for point, interval in zip(points, intervals):
        pyautogui.moveTo(point[0], point[1])
        time.sleep(interval/2)


def main():
    taille_ecran = coin_bas_droit[0] - coin_haut_gauche[0], coin_bas_droit[1] - coin_haut_gauche[1]
    
    n = 1
    for i in range(n):
        
        # refresh la page
        pyautogui.moveTo(refresh[0], refresh[1])
        click_randomly(duration=0.2)
        
        # Déplacer la souris vers son point de l'écran
        depart = (taille_ecran[0]/2, taille_ecran[1]/2)
        depart = random_point(depart, 250)
        print(f"[{i+1}/{n}: Point de départ : {depart}")
        pyautogui.moveTo(depart[0], depart[1])

        # Déplacer la souris de manière réaliste vers le bouton
        move_mouse_realistically(bouton, duration=0.2)
        
        # Cliquer sur le bouton
        click_randomly(duration=0.2)
        time.sleep(2)
        
    
    

if __name__ == "__main__":
    main()