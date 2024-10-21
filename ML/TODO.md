# TODO

## XGBoost (Extreme Gradient Boosting)
Description

    XGBoost est une implémentation optimisée des arbres de décision en gradient boosting.
    Connu pour sa performance et son efficacité en termes de temps de calcul.

Avantages

    Performance élevée : Souvent meilleur que les Random Forests sur de nombreux jeux de données.
    Gestion des valeurs manquantes : Peut gérer les données manquantes de manière interne.
    Régularisation : Offre des options pour éviter le surapprentissage.

Inconvénients

    Complexité : Plus difficile à paramétrer correctement.
    Temps de formation : Peut être plus lent sur de très grands jeux de données.

Pourquoi c'est une bonne alternative

    XGBoost est efficace pour capturer des relations complexes entre les caractéristiques et la cible. Il est souvent utilisé dans les compétitions de data science pour sa haute performance.

## Support Vector Machines (SVM)
Description

    Les SVM sont des modèles supervisés utilisés pour la classification et la régression.
    Ils cherchent à trouver l'hyperplan qui sépare les classes avec le plus grand écart.

Avantages

    Efficace sur les petits à moyens jeux de données.
    Performant avec des marges claires : Idéal si les classes sont bien séparables.
    Kernels : Possibilité d'utiliser différents noyaux pour capturer des relations non linéaires.

Inconvénients

    Temps de calcul : Peut être lent sur de grands jeux de données.
    Difficile à paramétrer : Le choix du noyau et des paramètres peut être complexe.
    Pas probabiliste : Ne fournit pas directement de probabilités, sauf avec des méthodes comme Platt scaling.

Pourquoi c'est une bonne alternative

    Si vos données ont une séparation claire ou si vous souhaitez essayer des modèles non probabilistes, les SVM peuvent être efficaces.


## MLP
Perceptron Multicouche (MLP)
Description

    Les MLP sont des réseaux de neurones artificiels composés de couches entièrement connectées.
    Capables de modéliser des relations non linéaires complexes.

Avantages

    Flexibilité : Peut capturer des relations non linéaires.
    Performance : Peut surpasser d'autres modèles si bien paramétré.
    Adaptabilité : Convient à une variété de types de données.

Inconvénients

    Temps d'entraînement : Peut nécessiter plus de temps pour s'entraîner.
    Données nécessaires : Peut nécessiter un grand nombre de données pour bien généraliser.
    Paramétrage : Nécessite un réglage fin des hyperparamètres (nombre de couches, neurones, taux d'apprentissage).

Pourquoi c'est une bonne alternative

    Si vous suspectez des relations complexes non capturées par les arbres de décision, un MLP peut être utile.

## Interpolation



## RNN

Réseaux de Neurones Récurrents (RNN)
Description

    Les RNN sont conçus pour traiter des données séquentielles ou temporelles.
    Peut être utile si vos données de mouvement de souris sont séquentielles.

Avantages

    Traitement des séquences : Capable de capturer les dépendances temporelles.
    Modélisation avancée : Peut modéliser des patterns complexes dans les données temporelles.

Inconvénients

    Complexité : Plus difficile à implémenter et à entraîner.
    Données nécessaires : Besoin d'un grand volume de données pour éviter le surapprentissage.

Pourquoi c'est une bonne alternative

    Si vous souhaitez exploiter la nature temporelle de vos données de mouvement de souris, les RNN peuvent être appropriés.
