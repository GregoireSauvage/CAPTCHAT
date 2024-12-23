# CAPTCHAT 🐱

## Description

CAPTCHAT 🐱 est une application web conçue pour collecter et analyser les mouvements de souris des utilisateurs afin de déterminer s'ils sont effectués par un humain ou un robot. Le projet utilise un serveur Flask pour le backend en Python et une page web en HTML et JavaScript pour le frontend. Les données collectées sont utilisées pour extraire des indicateurs pertinents, puis son exploités par des modèles de ML (Random Forest, XGBoost, SVM) constituer un dataset ou faire une prédiction.
</br></br>Ce projet est très largement inspiré de reCAPTCHA de Google.


## Fonctionnalités

### Collecte et entrainement
- Collecte des mouvements de souris et des clics sur une page web.
- Enregistrement des données dans un fichier CSV pour une analyse ultérieure.
- Extraction d'indicateurs à partir des données collectées.
- Entraînement d'un modèle de machine learning pour classer les mouvements en 'humain' ou 'machine'.
- Interface web interactive pour démarrer et arrêter la collecte des données.

### Exploitation du modèle de classification (prédiction si Humain ou Robot)
- Collecte des mouvements de souris et des clics sur une page web.
- Enregistrement des données dans un fichier CSV pour une analyse ultérieure.
- Extraction d'indicateurs à partir des données collectées.
- Prédit si le mouvement a été réalisé par un humain ou un robot via plusieurs modèles (Random Forest, XGBoost, SVM)


## Prérequis

- Python 3.10
- Navigateur Firefox
- GeckoDriver

## Bibliothèques Python requises

- Flask
- pandas
- numpy
- scikit-learn
- seaborn
- matplotlib
- scipy
- selenium
- pyautogui
- joblib
- pydotplus
- IPython
- xgboost
- graphviz

### Installation classique
1. Cloner le dépôt ou télécharger les fichiers du projet

```bash
git clone https://github.com/GregoireSauvage/CAPTCHAT.git
cd CAPTCHAT
```

2. Créer un environnement virtuel (recommandé)

```bash
python -m venv venv
```

3. Activer l'environnement virtuel

    Sur Windows:

    ```bash
    venv\Scripts\activate
    ```

    Sur macOS/Linux:

    ```bash
    source venv/bin/activate
    ```

4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### Installation avec Docker
1. Cloner le dépôt ou télécharger les fichiers du projet

```bash
git clone https://github.com/GregoireSauvage/CAPTCHAT.git
cd CAPTCHAT
```

2. Build l'image docker

```bash
docker build -t captchat .
```

3. Run l'image docker
```bash
docker run captchat
```

## Utilisation
1. Démarrer le serveur Flask

Assurez-vous d'être dans le répertoire du projet et exécutez:

```bash
python app.py
```

Le serveur devrait démarrer sur http://localhost:5000/.

</br> Vous pouvez tester les modèles vous même ou avec un script pour simuler un robot (des scripts sont disponibles dans le répertoire /src/simulate_robot)

2. Collecte des données

- Ouvrez un navigateur web et accédez à http://localhost:5000/. La page affichera un bouton Vérifier.
- Déplacez la souris sur la page et cliquez sur le bouton "Vérifier" pour arrêter l'enregistrement et envoyer les données au serveur.
- Les données de mouvements de souris et de clics seront enregistrées dans mouse_data.csv.

3. Extraction des indicateurs

Pour extraire les indicateurs à partir des données collectées:
- Accédez à http://localhost:5000/extract.
- Cette route exécutera la fonction get_indicators() qui extrait les indicateurs et les enregistre dans mouse_indicators_dataset.csv.

4. Entraîner le modèle

Pour entraîner le modèle de machine learning:
- Accédez à http://localhost:5000/train.
- Cette route exécutera la fonction random_forest() qui entraîne le modèle et affiche les résultats.

5. Interpréter les résultats
- Les résultats de l'entraînement, y compris les métriques de performance et l'importance des caractéristiques, seront affichés dans la console.
- Le modèle entraîné peut être sauvegardé pour une utilisation ultérieure.



