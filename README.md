# Scraping Prix SERP

## Sommaire
- [Description](#description)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Fonctionnement du script](#fonctionnement-du-script)
- [Sortie](#sortie)
- [Contribution](#contribution)
- [Licence](#licence)

## Description
Le projet `scraping-prix-serp` automatise l'extraction de données tarifaires à partir des pages de résultats des moteurs de recherche (SERPs) en utilisant Python. Ce script utilise des recherches basées sur des mots-clés pour recueillir et analyser les métriques de prix depuis diverses plateformes de e-commerce affichées à travers les résultats de moteur de recherche.

## Prérequis
Pour exécuter ce projet, vous devez avoir Python 3.x installé sur votre machine. De plus, les bibliothèques Python suivantes sont requises :
- requests
- pandas
- numpy
- selenium

Ces dépendances peuvent être installées en utilisant le fichier `requirements.txt` fourni en exécutant :
```bash
pip install -r requirements.txt
```

## Description
Le projet `scraping-prix-serp` automatise l'extraction des prix à partir des pages de résultats des moteurs de recherche (SERPs) en utilisant Python. Ce script utilise des recherches basées sur des mots-clés pour recueillir et analyser les métriques de prix depuis diverses plateformes de e-commerce affichées à travers les résultats de moteur de recherche.

## Prérequis
Pour exécuter ce projet, vous devez avoir Python 3.x installé sur votre machine. De plus, les bibliothèques Python suivantes sont requises :
- requests
- pandas
- numpy
- selenium

Ces dépendances peuvent être installées en utilisant le fichier `requirements.txt` fourni en exécutant :
```bash
pip install -r requirements.txt
```

## Installation

Clonez ce dépôt sur votre machine locale en utilisant :

```bash
git clone https://github.com/votre-nom-utilisateur/scraping-prix-serp.git
```

Naviguez dans le répertoire du projet :

```bash
cd scraping-prix-serp
```

Installez les dépendances nécessaires :

```bash
pip install -r requirements.txt
```

## Configuration
Avant de démarrer le script, vous devez configurer le fichier .env à la racine du projet pour stocker de manière sécurisée vos clés API et autres configurations sensibles :

```bash
API_KEY_VOTRE_SERVICE=insérez_votre_clé_api_ici
```

Assurez-vous que ce fichier n'est jamais ajouté à votre dépôt Git en vérifiant qu'il est bien listé dans votre fichier .gitignore.

## Utilisation

Assurez-vous que le fichier keywords.csv est peuplé avec les mots-clés que vous souhaitez rechercher.
Exécutez le script en utilisant :

```bash
python3 main.py
```

Le script traitera chaque mot-clé et sauvegardera les données de prix extraites dans output_progressive.csv.

## Fonctionnement du script

Le script main.py comporte plusieurs étapes clés pour l'extraction des données de prix :

1. Lecture des Mots-Clés : Les mots-clés pour les recherches sont chargés à partir du fichier keywords.csv.
2. Recherche dans les SERPs : Pour chaque mot-clé, le script utilise Selenium pour simuler une recherche dans un navigateur et récupérer les résultats de la première page.
3. Extraction des Prix : Le script navigue à travers les pages de chaque résultat et utilise des sélecteurs CSS pour extraire les informations de prix. **Ce processus d'extraction est flexible grâce à l'utilisation de sélecteurs CSS personnalisables. Ces sélecteurs peuvent être facilement ajoutés ou modifiés dans le script, permettant au projet de s'adapter rapidement à des changements dans les sites web ciblés ou à l'ajout de nouveaux sites. Cette modularité facilite la maintenance et l'extension du script sans nécessiter de réécriture complète, même en cas de modifications substantielles des pages web source**
4. Gestion des Prix : Les prix sont extraits sous différentes formes (par exemple, entiers, décimaux, fourchettes de prix) et sont normalisés en une représentation numérique unique (en euros).
5. Calcul des Médianes : Pour chaque mot-clé, le script calcule la médiane des prix trouvés pour donner une estimation de prix représentative.


## Sortie

Les résultats du script sont stockés dans output_progressive.csv, qui inclura :

- Les prix médians à travers différentes URLs trouvées dans le SERP.
- Des points de données de prix spécifiques extraits des sites.
- Les urls sur lesquelles le scrapping du site n'a pas réussi.
