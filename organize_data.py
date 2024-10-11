import pandas as pd
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt

def clear_dataset(dataset):
    
    print(dataset.isnull().sum())
    # Suppression des lignes avec des valeurs manquantes
    dataset.dropna(inplace=True)
    
    # Arrondir à 4 décimales
    dataset = dataset.round(3)
    
        
    return dataset