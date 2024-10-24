from flask import Flask, request, jsonify, render_template
from src.get_indicators import  extract_indicators, get_indicators
from src.organize_data import clear_dataset
from ML.random_forest import random_forest, predict_random_forest
from ML.XGBoost import train_xgboost, predict_xgboost
from ML.SVM import train_svm_rbf, predict_svm_rbf
import csv
import os
import pandas as pd

def extract_data_from_csv():
    filepath = "data/collect_data/data_all.csv"

    # extrait les données de la souris pour chaque essai, extrait les indicateurs utiles et les mets dans un dataframe
    dataset = get_indicators(filepath=filepath) 
    
    dataset = clear_dataset(dataset=dataset)
    
    # Sauvegarder le dataset pour le machine learning
    dataset.to_csv('data\extract_indicators\mouse_indicators_dataset.csv', index=False)

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
    return render_template('predict_CAPTCHAT.html')

@app.route('/collect', methods=['POST'])
def collect_data():
    data = request.get_json()
    session_id = data.get('session_id', None)
    if session_id is None:
        # Si aucun session_id n'est fourni, on en génère un
        import uuid
    mouse_movements = data.get('mouseMovements', [])
    click_coordinates = data.get('clickCoordinates', [])
    
    # Définit le label ('human' ou 'robot')
    label = 'human'
    
    # Enregistrer les données
    save_data(session_id=session_id, mouse_movements=mouse_movements, click_coordinates=click_coordinates, label=label)
    
    #indicators = extract_indicators(mouse_movements=mouse_movements)
    # Affichage des résultats
    #for key, value in indicators.items():
    #    print(f"{key}: {value}")
        
        
    # Répondre au client
    return jsonify({'status': 'success'}), 200


@app.route('/extract', methods=['GET'])
def extract_data():
    extract_data_from_csv()

    
    return jsonify({'status': 'success'}), 200



@app.route('/train', methods=['GET'])
def train_dataset():
    extract_data_from_csv()
    # Charger le dataset
    filepath = "data\extract_indicators\mouse_indicators_dataset.csv"
    dataset = pd.read_csv(filepath)
    
    # Exécuter le modèle de machine learning pour la classification
    #random_forest(dataset)
    
    #train_xgboost(dataset)
    
    train_svm_rbf(dataset)
    
    
    return jsonify({'status': 'success'}), 200


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    session_id = data.get('session_id', None)
    if session_id is None:
        # Si aucun session_id n'est fourni, on en génère un
        import uuid
        session_id = str(uuid.uuid4())

    mouse_movements = data.get('mouseMovements', [])
    click_coordinates = data.get('clickCoordinates', []) # Non utilisé pour le moment

    # Extraire les indicateurs à partir des mouvements de souris
    indicators = extract_indicators(mouse_movements=mouse_movements, show_figure=False)

    # Vérifier que les indicateurs sont bien extraits
    if indicators is None or len(indicators) == 0:
        return jsonify({'status': 'error', 'message': 'Impossible d\'extraire les indicateurs'}), 400

    # Charger le modèle et faire une prédiction
    #prediction = predict_random_forest(indicators)
    #prediction = predict_xgboost(indicators)
    prediction = predict_svm_rbf(indicators)
    
    # Renvoyer la prédiction au client (robot ou humain)
    return jsonify({'status': 'success', 'prediction': prediction}), 200


if __name__ == '__main__':
    app.run(debug=True)

