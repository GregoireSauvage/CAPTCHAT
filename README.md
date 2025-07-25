# CAPTCHAT 🐱

## Description

CAPTCHAT 🐱 est petit projet de ML que j'ai créé dans le but de me familiariser avec les modèles de classification les plus connus (Random Forest, XGBoost, SVM).
L'application web a été sauvagement vibe codée et sert uniquement de support pour le recueil de données, le test en condition "réelle" et comme vitrine pour les résultats des différents modèles.
</br>
Le projet en lui-même est conçue pour collecter et analyser les mouvements de souris des utilisateurs afin de déterminer s'ils sont effectués par un humain ou un robot.

</br></br>Ce projet est très largement inspiré de reCAPTCHA de Google.


## Fonctionnalités

### Exploitation du modèle de classification (prédiction si Humain ou Robot)
- Collecte des mouvements de souris et des clics sur une page web.
- Enregistrement des données dans un fichier CSV pour une analyse ultérieure.
- Extraction d'indicateurs à partir des données collectées.
- Prédit si le mouvement a été réalisé par un humain ou un robot via plusieurs modèles (Random Forest, XGBoost, SVM)

![alt text](illustration1.png)

![alt text](illustration2.png)

### Collecte et entrainement
- Collecte des mouvements de souris et des clics sur une page web.
- Enregistrement des données dans un fichier CSV pour une analyse ultérieure.
- Extraction d'indicateurs à partir des données collectées.
- Entraînement d'un modèle de machine learning pour classer les mouvements en 'humain' ou 'machine'.
- Interface web interactive pour démarrer et arrêter la collecte des données.


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



