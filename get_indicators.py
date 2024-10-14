import math
import numpy as np
from scipy.stats import entropy
import matplotlib.pyplot as plt
import pandas as pd

def entropy_movements(mouse_movements, show_figure=False):

    # Extraire les coordonnées x et y
    x = np.array([point['x'] for point in mouse_movements])
    y = np.array([point['y'] for point in mouse_movements])

    # Calculer les différences entre les positions successives
    delta_x = np.diff(x)
    delta_y = np.diff(y)

    # Calculer les angles en radians
    angles = np.arctan2(delta_y, delta_x)

    # Calculer les changements d'angle
    delta_angles = np.diff(angles)

    # Normaliser les changements d'angle pour les amener entre -π et π
    delta_angles = (delta_angles + np.pi) % (2 * np.pi) - np.pi

    # Calculer la variance des changements d'angle
    variance_delta_angles = np.var(delta_angles)
    #print(f"Variance des changements d'angle : {variance_delta_angles}")

    # Créer un histogramme des changements d'angle
    hist, bin_edges = np.histogram(delta_angles, bins=30, density=True)
    hist += 1e-12  # Pour éviter log(0)

    # Calculer l'entropie de Shannon
    angle_entropy = entropy(hist, base=np.e)
    #print(f"Entropie des changements d'angle : {angle_entropy}")

    if show_figure:
        # Visualisation de la distribution des changements d'angle
        #plt.figure(figsize=(8, 4))
        #plt.hist(delta_angles, bins=30, density=True, alpha=0.7, color='blue')
        #plt.title("Distribution des changements d'angle")
        #plt.xlabel("Changement d'angle (radians)")
        #plt.ylabel("Densité")
        #plt.show()

        # Visualisation de la trajectoire de la souris
        plt.figure(figsize=(8, 6))
        plt.plot(x, y, marker='o', linestyle='-', color='green')
        plt.title("Trajectoire de la souris")
        plt.xlabel("Position X")
        plt.ylabel("Position Y")
        plt.gca().invert_yaxis()
        plt.show()
        
    return variance_delta_angles, angle_entropy



def extract_indicators(mouse_movements, show_figure=False):
    """
    Extrait les indicateurs liés à l'accélération et à la trajectoire à partir des mouvements de souris.

    Paramètre:
        mouse_movements (list): Liste de dictionnaires avec les clés 'x', 'y' et 'time'.

    Retourne:
        dict: Dictionnaire contenant les indicateurs calculés.
    """

    # Extraire les coordonnées x, y et les temps
    x = np.array([point['x'] for point in mouse_movements])
    y = np.array([point['y'] for point in mouse_movements])
    time = np.array([point['time'] for point in mouse_movements]) / 1000.0  # Convertir le temps en secondes

    # Calculer les différences entre les positions successives
    delta_x = np.diff(x)
    delta_y = np.diff(y)
    delta_time = np.diff(time)

    # Éviter la division par zéro
    delta_time[delta_time == 0] = 1e-6

    # Calculer les distances entre les points successifs
    distances = np.sqrt(delta_x**2 + delta_y**2)

    # Calculer les vitesses
    speeds = distances / delta_time

    # Calculer les accélérations
    delta_speeds = np.diff(speeds)
    delta_time_acc = delta_time[1:]  # Les temps correspondants pour les accélérations
    accelerations = delta_speeds / delta_time_acc

    # Indicateurs liés à l'accélération
    acceleration_mean = np.mean(accelerations)
    acceleration_min = np.min(accelerations)
    acceleration_max = np.max(accelerations)
    acceleration_std = np.std(accelerations)

    # Indicateurs liés à la trajectoire
    # Distance totale parcourue
    total_distance = np.sum(distances)

    # Distance en ligne droite entre le premier et le dernier point
    straight_line_distance = np.sqrt((x[-1] - x[0])**2 + (y[-1] - y[0])**2)

    # Ratio de linéarité
    linearity_ratio = straight_line_distance / total_distance if total_distance != 0 else 0

    # Nombre de changements de direction significatifs
    # Calculer les angles de direction
    angles = np.arctan2(delta_y, delta_x)
    delta_angles = np.diff(angles)
    # Normaliser les changements d'angle entre -π et π
    delta_angles = (delta_angles + np.pi) % (2 * np.pi) - np.pi

    # Seuil pour un changement de direction significatif (par exemple, 30 degrés)
    threshold = np.deg2rad(30)
    significant_direction_changes = np.sum(np.abs(delta_angles) > threshold)

    # Calcul de l'écart-type de la vitesse
    speed_std = np.std(speeds)

    # Calcul du coefficient de variation de la vitesse (écart-type / moyenne)
    speed_mean = np.mean(speeds)
    speed_cv = speed_std / speed_mean if speed_mean != 0 else 0

    # Votre mesure de l'écart de vitesse
    speed_max = np.max(speeds)
    speed_min = np.min(speeds)
    speed_range_ratio = (speed_max - speed_min) / speed_max if speed_max != 0 else 0

    ## calcule de l'entropie dans les mouvements de la souris (ligne droite ou mouvements complexes)
    variance_angles, entropie_angles = entropy_movements(mouse_movements=mouse_movements, show_figure=show_figure)
    
    indicateurs = {
        # Indicateurs de vitesse
        'vitesse_moyenne': speed_mean,
        'vitesse_min': speed_min,
        'vitesse_max': speed_max,
        'vitesse_ecart_type': speed_std,
        'vitesse_coefficient_variation': speed_cv,
        'vitesse_range_ratio': speed_range_ratio,

        # Indicateurs d'accélération
        'acceleration_moyenne': acceleration_mean,
        'acceleration_min': acceleration_min,
        'acceleration_max': acceleration_max,
        'acceleration_ecart_type': acceleration_std,

        # Indicateurs de trajectoire
        'distance_totale': total_distance,
        'distance_ligne_droite': straight_line_distance,
        'ratio_linearite': linearity_ratio,
        'nombre_changements_direction': significant_direction_changes,
        
        # indicateurs d'angles dans les changements de trajectoire
        'variance_angles': variance_angles,
        'entropie_angles' : entropie_angles
    }

    return indicateurs



def get_indicators(filepath: str):
    # Charger les données
    data = pd.read_csv(filepath)
    #print(data)
    # Regrouper les données par session_id
    sessions = data.groupby('session_id')

    # Liste pour stocker les indicateurs de chaque session
    indicators_list = []

    for session_id, session_data in sessions:
        # Séparer les mouvements et les clics
        mouse_movements = session_data[session_data['event_type'] == 'move']
        click_coordinates = session_data[session_data['event_type'] == 'click']
        label = session_data['label'].iloc[0]  # Récupérer le label de la session
        
        # Convertir les données en format approprié
        movements_list = mouse_movements[['x', 'y', 'time']].to_dict('records')
        clicks_list = click_coordinates[['x', 'y', 'time']].to_dict('records')
        
        # Extraire les indicateurs (utilisez vos fonctions existantes)
        indicators = extract_indicators(mouse_movements=movements_list)
        indicators['label'] = label
        indicators['session_id'] = session_id  # Inclure le session_id si nécessaire
        
        # Ajouter les indicateurs à la liste
        indicators_list.append(indicators)

    # Créer un DataFrame avec les indicateurs
    dataset = pd.DataFrame(indicators_list)

    
    return dataset
