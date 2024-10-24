import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from src import organize_data

def grid_search(svm_model, param_grid, cv=5, scoring='roc_auc'):
    """
    Effectue une recherche sur grille pour trouver les meilleurs hyperparamètres pour un modèle SVM avec noyau RBF.

    Paramètres:
    -----------
    svm_model : SVC
        Modèle SVM avec noyau RBF.
    X_train : np.ndarray
        Données d'entraînement.
    y_train : np.ndarray
        Étiquettes d'entraînement.
    param_grid : dict
        Grille de paramètres à tester.
    cv : int
        Nombre de folds pour la validation croisée.
    scoring : str
        Métrique à optimiser.

    Retourne:
    ---------
    best_model : SVC
        Meilleur modèle SVM avec noyau RBF.
    best_params : dict
        Meilleurs hyperparamètres trouvés.
    """
    
    # Configuration de la validation croisée
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    # Initialisation de GridSearchCV
    grid = GridSearchCV(
        estimator=svm_model,
        param_grid=param_grid,
        scoring=scoring,
        cv=cv,
        n_jobs=-1,
        verbose=2
    )

    # Renvoie le meilleur modèle et les meilleurs paramètres
    return grid 


def train_svm_rbf(data, folder="models/SVM_RBF"):
    """
    Charge les données, entraîne un modèle SVM avec noyau RBF en utilisant GridSearchCV pour l'optimisation des hyperparamètres,
    évalue le modèle et sauvegarde le modèle entraîné ainsi que le scaler et l'encodeur de labels.

    Paramètres:
    -----------
    data_path : str
        Chemin vers le fichier CSV contenant les données.
    model_output_path : str
        Chemin où le modèle entraîné sera sauvegardé.
    scaler_output_path : str
        Chemin où le StandardScaler sera sauvegardé.
    encoder_output_path : str
        Chemin où le LabelEncoder sera sauvegardé.
    """
    
    # Chemins de sauvegarde
    model_output_path=f'{folder}/svm_rbf_model.pkl'
    scaler_output_path=f'{folder}/scaler.pkl'
    encoder_output_path=f'{folder}/label_encoder.pkl'
    
    ### 1. Chargement des données ###
    # Séparer les caractéristiques et les étiquettes
    X = data.drop(['label', 'session_id'], axis=1)
    y = data['label']

    # Encodage des étiquettes
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Sauvegarder l'encodeur de labels
    joblib.dump(le, encoder_output_path)

    ### 2. Prétraitement des données ###
    # Standardisation des caractéristiques
    X_scaled, scaler = organize_data.preprocess_indicators(X)

    # Sauvegarder le scaler
    joblib.dump(scaler, scaler_output_path)

    ### 3. Division des données en ensembles d'entraînement et de test ###
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, test_size=0.2, stratify=y_encoded, random_state=42
    )

    ### 4. Entraînement du modèle SVM avec noyau RBF ###
    # Définition du modèle SVM
    svm_model = SVC(kernel='rbf', probability=True, random_state=42)

    # Définition de la grille de paramètres pour GridSearchCV
    param_grid = {
        'C': [0.1, 1, 10, 100, 1000],
        'gamma': [1, 0.1, 0.01, 0.001],
        'kernel': ['rbf']
    }

    # Initialisation de GridSearchCV
    grid = grid_search(svm_model, param_grid, cv=5, scoring='roc_auc')

    # Entraînement du modèle avec recherche des meilleurs hyperparamètres
    grid.fit(X_train, y_train)

    # Meilleurs paramètres
    print("Meilleurs paramètres :", grid.best_params_)

    # Meilleur modèle entraîné
    best_svm_model = grid.best_estimator_

    ### 5. Évaluation du modèle ###
    # Prédictions sur l'ensemble de test
    y_pred = best_svm_model.predict(X_test)
    y_pred_proba = best_svm_model.predict_proba(X_test)[:, 1]

    # Rapport de classification
    print("\nRapport de classification :")
    print(classification_report(y_test, y_pred, target_names=le.classes_))

    # Matrice de confusion
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 4))
    sns.heatmap(
        cm, annot=True, fmt='d', cmap='Blues',
        xticklabels=le.classes_, yticklabels=le.classes_
    )
    plt.xlabel('Prédictions')
    plt.ylabel('Vraies valeurs')
    plt.title('Matrice de confusion')
    plt.show()

    # Score ROC-AUC
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    print(f"\nScore ROC-AUC : {roc_auc:.2f}")

    # Courbe ROC
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    plt.figure()
    plt.plot(fpr, tpr, label=f'Courbe ROC (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('Taux de faux positifs')
    plt.ylabel('Taux de vrais positifs')
    plt.title('Courbe ROC')
    plt.legend(loc='lower right')
    plt.show()

    ### 6. Sauvegarde du modèle ###
    joblib.dump(best_svm_model, model_output_path)
    print(f"\nLe modèle SVM a été entraîné et sauvegardé avec succès dans '{model_output_path}'.")




def predict_svm_rbf(indicators, folder="models/SVM_RBF"):
    """
    Utilise le modèle SVM entraîné pour prédire le label d'un nouvel ensemble d'indicateurs.

    Paramètres:
    -----------
    indicators : dict
        Dictionnaire contenant les indicateurs pour lesquels faire la prédiction.
    folder : str
        Dossier où sont sauvegardés le modèle, le scaler et l'encodeur de labels.

    Retourne:
    ---------
    prediction_label : str
        Le label prédit ('human' ou 'robot', par exemple).
    """
    # Chemins vers les fichiers sauvegardés
    model_path = f'{folder}/svm_rbf_model.pkl'
    scaler_path = f'{folder}/scaler.pkl'
    encoder_path = f'{folder}/label_encoder.pkl'

    # Charger le modèle, le scaler et l'encodeur de labels
    svm_model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    le = joblib.load(encoder_path)

    # Convertir les indicateurs en DataFrame
    X_new = pd.DataFrame([indicators])

    # Vérifier que les colonnes correspondent à celles du modèle
    expected_features = svm_model.feature_names_in_
    missing_features = set(expected_features) - set(X_new.columns)
    if missing_features:
        raise ValueError(f"Les indicateurs suivants sont manquants : {missing_features}")

    # Réorganiser les colonnes dans le même ordre que lors de l'entraînement
    X_new = X_new[expected_features]

    # Standardiser les nouvelles données avec le scaler ajusté
    X_new_scaled = scaler.transform(X_new)

    # Faire une prédiction
    y_pred = svm_model.predict(X_new_scaled)

    # Décoder le label prédit
    prediction_label = le.inverse_transform(y_pred)[0]

    return prediction_label