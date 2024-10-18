import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

def grid_search(rf_model, X_train, y_train):
    param_grid = {
    'n_estimators': [100, 200, 500],
    'max_depth': [None, 5, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['auto', 'sqrt']
}

    grid_search = GridSearchCV(
        estimator=rf_model,
        param_grid=param_grid,
        cv=5,
        scoring='accuracy',
        n_jobs=-1
    )

    grid_search.fit(X_train, y_train)

    print("Meilleurs paramètres :", grid_search.best_params_)
    
    best_params = grid_search.best_params_
    rf_best_model = RandomForestClassifier(
        **best_params,
        random_state=42,
        n_jobs=-1
    )

    rf_best_model.fit(X_train, y_train)
    
    return rf_best_model # Retourne le modèle avec les meilleurs paramètres


def random_forest(dataset):
    
    ### Prétraitement des données ###
    
    # Diviser les données en caractéristiques et étiquettes
    X = dataset.drop(['label', 'session_id'], axis=1)
    y = dataset['label']

    # Séparer les données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    
    
    
    ### Entraînement du modèle ###
    
    # Créer une instance du modèle
    rf_model = RandomForestClassifier(
        n_estimators=100,  # Nombre d'arbres dans la forêt
        random_state=42,
        n_jobs=-1  # Utiliser tous les cœurs du processeur
    )
    
    # Entraîner le modèle sur l'ensemble d'entraînement
    rf_model.fit(X_train, y_train)
    
    
    
    ### Évaluation du modèle ###
    
    # Faire des prédictions sur l'ensemble de test
    y_pred = rf_model.predict(X_test)
    
    # Évaluer les performances
    print(classification_report(y_test, y_pred))
    
    # Matrice de confusion
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Prédictions')
    plt.ylabel('Vraies valeurs')
    plt.title('Matrice de confusion')
    plt.show()

    # Score ROC-AUC
    y_pred_proba = rf_model.predict_proba(X_test)[:, 1]
    roc_auc = roc_auc_score(y_test.map({'human': 0, 'robot': 1}), y_pred_proba)
    print(f'Score ROC-AUC: {roc_auc:.2f}')
    
    # Courbe ROC
    fpr, tpr, thresholds = roc_curve(y_test.map({'human': 0, 'robot': 1}), y_pred_proba)
    plt.plot(fpr, tpr, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('Taux de faux positifs')
    plt.ylabel('Taux de vrais positifs')
    plt.title('Courbe ROC')
    plt.legend(loc='lower right')
    plt.show()
    
    # Enregistrer les noms des caractéristiques dans le modèle
    rf_model.feature_names_in_ = X_train.columns
    
    # Sauvegarder le modèle
    joblib.dump(rf_model, 'rf_mouse_movement_model.pkl')
    
    return


def test_model(indicators, model_path='models/random_forestV1.pkl'):
    # Charger le modèle
    model = joblib.load(model_path)

    # Créer un DataFrame à partir des indicateurs
    X = pd.DataFrame([indicators])

    # S'assurer que les colonnes correspondent à celles du modèle
    expected_features = model.feature_names_in_
    X = X.reindex(columns=expected_features, fill_value=0)

    # Faire une prédiction
    prediction = model.predict(X)[0]

    return prediction
