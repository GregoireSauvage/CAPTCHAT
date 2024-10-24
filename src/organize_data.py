import pandas as pd
from sklearn.preprocessing import StandardScaler
import pandas as pd

def preprocess_indicators(indicators):
    """
    Prétraite les indicateurs en les standardisant.

    Paramètres:
    -----------
    indicators : pd.DataFrame
        DataFrame contenant les indicateurs à standardiser.

    Retourne:
    ---------
    indicators_scaled : pd.DataFrame
        DataFrame des indicateurs standardisés.
    scaler : StandardScaler
        Objet StandardScaler ajusté sur les données fournies.
    """
    # Créer une instance de StandardScaler
    scaler = StandardScaler()

    # Ajuster le scaler sur les données et les transformer
    indicators_scaled_array = scaler.fit_transform(indicators)

    # Convertir le tableau numpy résultant en DataFrame
    indicators_scaled = pd.DataFrame(indicators_scaled_array, columns=indicators.columns, index=indicators.index)

    return indicators_scaled, scaler



def clear_dataset(dataset):
    
    print(dataset.isnull().sum())
    # Suppression des lignes avec des valeurs manquantes
    dataset.dropna(inplace=True)
    
    # Arrondir à 4 décimales
    dataset = dataset.round(3)
    
        
    return dataset