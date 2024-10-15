from flask import Flask, request, jsonify, render_template
import csv
import os

def save_data(session_id, mouse_movements, click_coordinates, label):
    
    
    # Nom du fichier CSV
    filename = f'data.csv'
    
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
    return render_template('train_CAPTCHAT.html')

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
        
    # Répondre au client
    return jsonify({'status': 'success'}), 200




if __name__ == '__main__':
    app.run(debug=True)

