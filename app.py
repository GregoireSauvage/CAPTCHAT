from flask import Flask, request, jsonify, render_template
from get_indicators import  extract_indicators, get_indicators
from organize_data import clear_dataset
from model import random_forest
import csv
import os
import pandas as pd

def save_data(session_id, mouse_movements, click_coordinates, label):
    # Nom du fichier CSV
    filename = 'mouse_data.csv'
    
    # Vérifier si le fichier existe
    file_exists = os.path.isfile(filename)
    
    # Ouvrir le fichier en mode ajout (append)
    with open(filename, mode='a', newline='') as csvfile:
        fieldnames = ['session_id', 'x', 'y', 'time', 'event_type', 'label']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Écrire l'en-tête si le fichier n'existe pas
        if not file_exists:
            writer.writeheader()
        
        # Enregistrer les mouvements de souris
        for movement in mouse_movements:
            writer.writerow({
                'session_id': session_id,
                'x': movement['x'],
                'y': movement['y'],
                'time': movement['time'],
                'event_type': 'move',
                'label': label
            })
        
        # Enregistrer les clics de souris
        for click in click_coordinates:
            writer.writerow({
                'x': click['x'],
                'y': click['y'],
                'time': click['time'],
                'event_type': 'click',
                'label': label
            })




app = Flask(__name__)

@app.route('/')
def index():
    return render_template('CAPTCHAT.html')

@app.route('/collect', methods=['POST'])
def collect_data():
    data = request.get_json()
    session_id = data.get('session_id', None)
    if session_id is None:
        # Si aucun session_id n'est fourni, on en génère un
        import uuid
    mouse_movements = data.get('mouseMovements', [])
    click_coordinates = data.get('clickCoordinates', [])
    
    # Définit le label ('humain' ou 'robot')
    label = 'robot'
    
    # Enregistrer les données
    save_data(session_id=session_id, mouse_movements=mouse_movements, click_coordinates=click_coordinates, label=label)
    
    #indicators = extract_indicators(mouse_movements=mouse_movements)
    # Affichage des résultats
    #for key, value in indicators.items():
    #    print(f"{key}: {value}")
        
        
    # Répondre au client
    return jsonify({'status': 'success'}), 200


@app.route('/extract', methods=['GET'])
def extract_data_from_csv():
    filepath = "mouse_data.csv"
    # extrait les données de la souris pour chaque essai, extrait les indicateurs utiles et les mets dans un dataframe
    dataset = get_indicators(filepath=filepath) 
    
    dataset = clear_dataset(dataset=dataset)
    
    # Sauvegarder le dataset pour le machine learning
    dataset.to_csv('mouse_indicators_dataset.csv', index=False)
    
    return jsonify({'status': 'success'}), 200


@app.route('/train', methods=['GET'])
def train_dataset():
    # Charger le dataset
    filepath = "mouse_indicators_dataset.csv"
    dataset = pd.read_csv(filepath)
    
    # Exécuter le modèle de machine learning pour la classification
    random_forest(dataset)
    
    
    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(debug=True)

