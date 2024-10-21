import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

def train_xgboost(dataset, optimization=False):

    ### Prétraitement des données ###
    # Diviser les données en caractéristiques et étiquettes
    X = dataset.drop(['label', 'session_id'], axis=1)
    y = dataset['label']

    # Encodage des étiquettes si nécessaire
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Séparer les données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, stratify=y_encoded, random_state=42
    )

    ### Entraînement du modèle XGBoost ###
    # Création de l'instance du modèle
    xgb_model = XGBClassifier(
        objective='binary:logistic',
        eval_metric='auc',
        use_label_encoder=False,
        random_state=42
    )

    if optimization:
        # Définition de la grille de paramètres pour la recherche en grille
        param_grid = {
            'n_estimators': [100, 200, 500],
            'max_depth': [3, 5, 7],
            'learning_rate': [0.01, 0.1, 0.2],
            'subsample': [0.7, 0.8, 0.9],
            'colsample_bytree': [0.7, 0.8, 0.9]
        }

        grid_search = GridSearchCV(
            estimator=xgb_model,
            param_grid=param_grid,
            cv=5,
            scoring='roc_auc',
            n_jobs=-1,
            verbose=1
        )

        grid_search.fit(X_train, y_train)

        print("Meilleurs paramètres :", grid_search.best_params_)

        xgb_model = grid_search.best_estimator_
    else:
        # Entraîner le modèle sur l'ensemble d'entraînement
        xgb_model.fit(X_train, y_train)

    ### Évaluation du modèle ###
    # Faire des prédictions sur l'ensemble de test
    y_pred = xgb_model.predict(X_test)
    y_pred_proba = xgb_model.predict_proba(X_test)[:, 1]

    # Rapport de classification
    print(classification_report(y_test, y_pred, target_names=le.classes_))

    # Matrice de confusion
    cm = confusion_matrix(y_test, y_pred)
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
    print(f'Score ROC-AUC: {roc_auc:.2f}')

    # Courbe ROC
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    plt.plot(fpr, tpr, label=f'Courbe ROC (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('Taux de faux positifs')
    plt.ylabel('Taux de vrais positifs')
    plt.title('Courbe ROC')
    plt.legend(loc='lower right')
    plt.show()

    # Importance des caractéristiques
    feature_importances = pd.Series(xgb_model.feature_importances_, index=X_train.columns)
    feature_importances.sort_values(ascending=False, inplace=True)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=feature_importances, y=feature_importances.index)
    plt.title('Importance des caractéristiques')
    plt.xlabel('Importance')
    plt.ylabel('Caractéristiques')
    plt.show()

    ### Sauvegarde du modèle ###
    # Enregistrer le modèle
    joblib.dump(xgb_model, 'models/XGBoost_V1/xgboost_model.pkl')

    # Sauvegarder l'encodeur de labels
    joblib.dump(le, 'models/XGBoost_V1/label_encoder.pkl')

    print('Le modèle XGBoost a été entraîné et sauvegardé avec succès.')

    return xgb_model  # Retourne le modèle entraîné


def test_xgboost(indicators, model_path='models/XGBoost_V1/xgboost_model.pkl', encoder_path='models/XGBoost_V1/label_encoder.pkl'):

    # Charger le modèle
    model = joblib.load(model_path)

    # Charger l'encodeur de labels
    le = joblib.load(encoder_path)

    # Créer un DataFrame à partir des indicateurs
    X = pd.DataFrame([indicators])

    # S'assurer que les colonnes correspondent à celles du modèle
    expected_features = model.feature_names_in_
    X = X.reindex(columns=expected_features, fill_value=0)

    # Faire une prédiction
    y_pred = model.predict(X)

    # Décoder le label prédit
    prediction_label = le.inverse_transform(y_pred)[0]

    return prediction_label
