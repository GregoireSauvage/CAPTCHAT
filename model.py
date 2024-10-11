import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import seaborn as sns


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
    roc_auc = roc_auc_score(y_test.map({'humain': 0, 'machine': 1}), y_pred_proba)
    print(f'Score ROC-AUC: {roc_auc:.2f}')
    
    # Courbe ROC
    fpr, tpr, thresholds = roc_curve(y_test.map({'humain': 0, 'machine': 1}), y_pred_proba)
    plt.plot(fpr, tpr, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('Taux de faux positifs')
    plt.ylabel('Taux de vrais positifs')
    plt.title('Courbe ROC')
    plt.legend(loc='lower right')
    plt.show()
    
    return