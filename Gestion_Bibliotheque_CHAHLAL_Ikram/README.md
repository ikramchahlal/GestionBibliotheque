# Système de Gestion de Bibliothèque en Python

**Auteur** : Ikram Chahlal  
**Filière** : Génie Informatique  
**Année Universitaire** : 2024/2025  
 ENSAO – École Nationale des Sciences Appliquées d’Oujda


## Description du Projet
Ce projet est une application complète de gestion de bibliothèque développée en Python. Elle intègre :
- Un backend POO pour la logique métier
- Une interface en ligne de commande (CLI) et une interface graphique (Tkinter)
- La gestion des exceptions personnalisées
- La persistance des données dans des fichiers (JSON/CSV)
- La génération de rapports statistiques avec Matplotlib

## Fonctionnalités
1. **Gestion des Livres et Membres** :
   - Ajout, suppression et liste des livres
   - Inscription des membres et gestion des emprunts/retours

2. **Interfaces** :
   - Interface en ligne de commande (CLI) avec menu interactif
   - Interface graphique (Tkinter) avec onglets pour une navigation facile

3. **Gestion des Erreurs** :
   - Exceptions personnalisées (`LivreIndisponibleError`, `QuotaEmpruntDepasseError`, etc)
   - Messages d'erreur clairs pour l'utilisateur

4. **Statistiques** :
   - Diagramme circulaire : Répartition des livres par genre
   - Histogramme : Top 10 des auteurs les plus populaires
   - Courbe temporelle : Activité des emprunts sur 30 jours

5. **Persistance des Données** :
   - Sauvegarde automatique dans des fichiers (`livres.txt`, `membres.txt`, `historique.csv`)
   - Chargement des données au démarrage de l'application

## Structure du Projet
Gestion_Bibliotheque_Ikram_Chahlal/
├── data/
│ ├── livres.txt # Données des livres
│ ├── membres.txt # Données des membres
│ └── historique.csv # Historique des emprunts
├── src/
│ ├── main.py # Programme principal
│ ├── bibliotheque.py # Classes POO (Livre, Membre, Bibliotheque)
│ ├── exceptions.py # Exceptions personnalisées
│ ├── visualisations.py # Génération des graphiques
│ └── gui.py # Interface graphique (Tkinter)
├── docs/
│ ├── Ikram_CHAHLAL Rapport de projet.pdf # Rapport détaillé du projet
│ 
├── assets/
│ ├── stats_genres.png # Graphique des genres
│ └── stats_auteurs.png # Graphique des auteurs
  └── stats_activite.png #pour les 30 derniers jours
  └── presentation.mp4 #video demonstratid
├── requirements.txt # Dépendances Python
└── README.md # 



## Installation
1. **Prérequis** :
   - Python 3.8 ou supérieur
   - Bibliothèques requises : `tkinter`, `matplotlib`

2. **Configuration** :
   - Clonez le dépôt GitHub :
     ```bash
     git clone https://github.com/ikramchahlal/GestionBibliotheque
     ```
   - Installez les dépendances :
     ```bash
     pip install -r requirements.txt
     ```

3. **Exécution** :
   - **Mode CLI** :
     ```bash
     python src/main.py
     ```
     Choisissez l'option 1 pour l'interface en ligne de commande.
   - **Mode Graphique** :
     ```bash
     python src/main.py
     ```
     Choisissez l'option 2 pour l'interface graphique.

## Exemples d'Utilisation
1. **Ajouter un Livre** :
   - Dans le menu CLI, sélectionnez l'option 1 et suivez les instructions.
   - Dans l'interface graphique, allez dans l'onglet "Livres" et remplissez le formulaire.

2. **Emprunter un Livre** :
   - Fournissez l'ISBN du livre et l'ID du membre.
   - Le système vérifie la disponibilité et les quotas.

3. **Générer des Statistiques** :
   - Dans le menu CLI, sélectionnez l'option 7.
   - Dans l'interface graphique, allez dans l'onglet "Statistiques" et cliquez sur "Afficher Statistiques".

## Documentation Supplémentaire
- **Rapport PDF** : Consultez `docs/Ikram_CHAHLAL Rapport de projet.pdf` pour :
  - Le diagramme de classes UML
  - Les explications des algorithmes clés
  - Les difficultés rencontrées et solutions
- **Vidéo de Présentation** : Regardez `docs/presentation.mp4` pour une démonstration des fonctionnalités.

