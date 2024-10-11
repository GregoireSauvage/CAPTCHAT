import pandas as pd
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt

def clear_dataset(dataset):
    
    # Supposons que 'dataset' est votre DataFrame contenant les indicateurs
    print(dataset.isnull().sum())
    
    # Arrondir à 4 décimales
    dataset = dataset.round(3)
    print(dataset)
        
    return