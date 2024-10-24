En Machine Learning, le terme noyau (ou kernel en anglais) fait référence à une technique mathématique utilisée pour résoudre des problèmes non linéaires en appliquant des transformations sur les données. Le kernel trick permet de travailler avec des données qui ne sont pas linéairement séparables en projetant ces données dans un espace de dimension supérieure, où elles deviennent séparables par un hyperplan linéaire.

Les noyaux sont particulièrement associés aux algorithmes basés sur des produits scalaires, comme les Support Vector Machines (SVM) ou les réseaux de neurones à noyau, bien qu'ils soient également utilisés dans d'autres algorithmes.
1. Contexte : Pourquoi les noyaux sont-ils utiles ?

De nombreux algorithmes de classification ou de régression, comme les SVM ou la régression linéaire, fonctionnent bien lorsque les données sont linéairement séparables, c'est-à-dire qu'un simple hyperplan (ou ligne droite en 2D) peut séparer les classes. Cependant, dans de nombreux cas pratiques, les données ne sont pas linéairement séparables dans l'espace original des features.

Voici un exemple simplifié :

    Imagine deux classes de données qui forment deux cercles concentriques : les points à l'intérieur du cercle sont de la classe AA, et ceux à l'extérieur sont de la classe BB. Un SVM linéaire ne peut pas trouver une ligne droite qui sépare ces deux classes dans l'espace d'origine.

C'est là qu'intervient le concept de noyau : il permet de projeter ces données dans un espace de dimension supérieure, où elles deviennent linéairement séparables.
2. Qu'est-ce qu'un noyau en Machine Learning ?

Un noyau est une fonction mathématique qui calcule un produit scalaire dans un espace de dimension supérieure, sans avoir besoin de calculer explicitement les coordonnées de ce nouvel espace. Autrement dit, un noyau permet de transformer les données d'origine dans un espace de dimension supérieure (appelé espace de features ou espace de Hilbert reproduit) où les relations complexes entre les données peuvent devenir linéaires.
a) Fonction de noyau : définition mathématique

Un noyau est une fonction qui prend deux vecteurs xx et x′x′ dans l'espace d'origine et retourne un produit scalaire dans un espace de dimension supérieure (sans calculer explicitement les coordonnées dans cet espace supérieur).

Formellement, un noyau KK est défini comme :
K(x,x′)=ϕ(x)T⋅ϕ(x′)
K(x,x′)=ϕ(x)T⋅ϕ(x′)

Où :

    xx et x′x′ sont des vecteurs dans l'espace d'origine.
    ϕ(x)ϕ(x) et ϕ(x′)ϕ(x′) sont les projections de ces vecteurs dans l'espace projeté de dimension supérieure (souvent inconnu explicitement).
    Le noyau K(x,x′)K(x,x′) calcule directement le produit scalaire entre ϕ(x)ϕ(x) et ϕ(x′)ϕ(x′) sans avoir besoin de connaître explicitement ϕϕ.

b) Le Trick du Noyau (Kernel Trick)

Le kernel trick est une technique puissante qui permet de calculer le produit scalaire dans cet espace projeté de dimension supérieure, sans avoir besoin de calculer explicitement les projections ϕ(x)ϕ(x) et ϕ(x′)ϕ(x′). Cela permet de traiter des problèmes non linéaires avec des méthodes qui utilisent des produits scalaires (comme les SVM), mais de manière efficace et sans le coût de calcul excessif d'une projection explicite.
3. Exemples de fonctions noyaux couramment utilisées

Il existe plusieurs types de noyaux que tu peux utiliser en fonction des propriétés de tes données. Voici les plus couramment utilisés :
a) Noyau linéaire

Le noyau linéaire est le plus simple. Il ne projette pas les données dans un espace de dimension supérieure, car les données sont déjà séparables linéairement dans l'espace d'origine.

    Formule :
    K(x,x′)=xTx′
    K(x,x′)=xTx′
    Quand l'utiliser : Lorsque les données sont linéairement séparables dans l'espace des features d'origine. C'est rapide et simple, et il est adapté lorsque les relations entre les classes peuvent être modélisées par une simple ligne (ou un hyperplan dans des dimensions plus élevées).

b) Noyau polynomial

Le noyau polynomial projette les données dans un espace de dimension plus élevée où les relations entre les classes sont modélisées par des interactions polynomiales. C'est utile si tu penses que les relations entre les features peuvent être modélisées par des interactions non linéaires.

    Formule :
    K(x,x′)=(xTx′+c)d
    K(x,x′)=(xTx′+c)d

    Où dd est le degré du polynôme, et cc est un terme de biais.

    Quand l'utiliser : Ce noyau est utilisé lorsque les classes ne sont pas linéairement séparables mais peuvent l'être via une transformation polynomiale (comme des courbes ou des surfaces dans des dimensions plus élevées). Par exemple, pour capturer des interactions entre les features qui ne sont pas simplement additives mais multiplicatives.

c) Noyau RBF (Radial Basis Function) ou noyau gaussien

Le noyau RBF est l'un des noyaux les plus puissants et les plus utilisés. Il projette les données dans un espace de dimension infinie et est capable de modéliser des séparations très complexes. Il est basé sur la distance entre deux points, et il mesure à quel point les points sont proches l'un de l'autre.

    Formule :
    K(x,x′)=exp⁡(−γ∣∣x−x′∣∣2)
    K(x,x′)=exp(−γ∣∣x−x′∣∣2)

    Où γγ est un hyperparamètre qui contrôle l'importance de chaque point. Un petit γγ signifie que chaque point a une influence large, tandis qu'un γγ élevé limite l'influence à des points très proches.

    Quand l'utiliser : Le noyau RBF est idéal lorsque les données sont très non linéaires et que les relations entre les features sont complexes. Ce noyau est capable de capturer des séparations fines et flexibles entre les classes.

d) Noyaux personnalisés

Si les noyaux standards ne fonctionnent pas bien pour ton problème spécifique, tu peux aussi concevoir un noyau personnalisé qui correspond mieux à la structure de tes données. Tant que la fonction de noyau respecte certaines propriétés (comme la symétrie et la positivité définie), elle peut être utilisée avec des algorithmes comme SVM.
4. Exemple d'utilisation du noyau avec les SVM

Prenons un exemple pour illustrer l'utilisation des noyaux dans les SVM :

Supposons que tu as deux classes de données qui ne sont pas linéairement séparables dans l'espace des features d'origine. Par exemple, des points qui forment des cercles concentriques. Si tu appliques un SVM linéaire, il ne pourra pas trouver de frontière simple pour séparer les classes.

Cependant, si tu utilises un noyau RBF, les données seront projetées dans un espace de dimension supérieure, et dans cet espace, elles peuvent devenir séparables par un hyperplan.

Le kernel trick te permet de calculer les produits scalaires dans cet espace supérieur sans avoir à connaître explicitement les coordonnées dans cet espace, ce qui rend le calcul très efficace.
5. Quand utiliser un noyau en Machine Learning ?

L'utilisation d'un noyau est recommandée dans les cas suivants :

    Non-linéarité : Si les relations entre les features et les classes ne peuvent pas être capturées par un modèle linéaire, un noyau (comme le RBF ou le polynomial) peut projeter les données dans un espace où les relations deviennent linéaires.
    Interactions complexes entre les features : Par exemple, si tu penses que les features interagissent entre elles de manière multiplicative, un noyau polynomial pourrait mieux capturer ces interactions.
    Classification ou régression avec peu d'exemples : Les noyaux comme le RBF peuvent être très efficaces avec de petites quantités de données, car ils peuvent capturer des structures complexes avec peu d'exemples.

6. Avantages et inconvénients des noyaux
Avantages :

    Flexibilité : Les noyaux permettent de résoudre des problèmes non linéaires complexes en projetant les données dans un espace de dimension supérieure.
    Pas de projection explicite nécessaire : Le kernel trick permet de travailler efficacement dans des espaces de dimension élevée sans avoir besoin de calculer les coordonnées dans cet espace.
    Puissance du noyau RBF : Le noyau RBF, en particulier, est capable de gérer des séparations complexes et est très polyvalent.

Inconvénients :

    Coût computationnel : L'utilisation de noyaux (notamment le noyau RBF) peut augmenter le temps de calcul, surtout sur de grands ensembles de données.
    Choix du noyau : Le choix du bon noyau et des bons hyperparamètres (comme γγ pour le noyau RBF) peut être difficile. Un mauvais choix peut conduire à un surapprentissage ou à une sous-apprentissage.
    Complexité du modèle : Certains noyaux, comme le noyau polynomial de haut degré, peuvent rendre le modèle très complexe et difficile à interpréter.

7. Résumé

    Un noyau est une fonction qui permet de projeter des données dans un espace de dimension supérieure afin de résoudre des problèmes non linéaires de manière efficace.
    Le kernel trick permet de travailler dans cet espace sans calculer explicitement les coordonnées des données dans cet espace projeté.
    Il existe plusieurs noyaux couramment utilisés, comme le noyau linéaire, le noyau polynomial, et le noyau RBF, chacun ayant ses avantages en fonction des propriétés des données.
    Les noyaux sont particulièrement utiles dans les algorithmes comme les SVM pour résoudre des problèmes complexes de classification et de régression.