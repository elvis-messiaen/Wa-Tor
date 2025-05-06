# Simulation Wa-Tor

## Description
Wa-Tor est une simulation écologique qui modélise l'interaction entre les poissons et les requins dans un écosystème marin. Cette implémentation utilise Python avec une interface graphique Tkinter.

## Fonctionnalités
- Simulation d'un écosystème marin avec des poissons et des requins
- Interface graphique interactive avec des emojis
- Contrôle de la simulation (pause/reprise, tour par tour)
- Affichage en temps réel du nombre d'entités

## Règles de la simulation
- Les poissons :
  - Se déplacent aléatoirement dans les cases vides
  - Se reproduisent après un certain nombre de tours
  - Sont mangés par les requins

- Les requins :
  - Chassent les poissons pour se nourrir
  - Perdent de l'énergie à chaque tour
  - Meurent s'ils n'ont plus d'énergie
  - Se reproduisent après un certain nombre de tours

## Installation
1. Clonez le dépôt :
```bash
git clone [https://github.com/elvis-messiaen/Wa-Tor.git]
cd Wa-Tor
```

2. Assurez-vous d'avoir Python 3.13 installé
https://legacy.python.org/about/gettingstarted/

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation
1. Lancez la simulation :

- Windows :
```bash
python main.py
```

- MacOs / Linux:
```bash
python3 main.py
```

2. Contrôles :
- Bouton "Tour suivant" : Avance d'un tour
- Bouton "Lancer/Pause" : Démarre/arrête la simulation en continu

## Structure du projet
```
Wa-Tor/
├── aquatic/
│   ├── fish.py      # Classe des poissons
│   ├── shark.py     # Classe des requins
│   └── __init__.py
├── interface/
│   ├── grid.py      # Gestion de la grille
│   └── __init__.py
├── main.py          # Point d'entrée
└── README.md
```

## Configuration
Les paramètres de la simulation peuvent être ajustés dans le code :
- Taille de la grille (`width`, `height` dans `main.py`)
- Proportions initiales des entités
- Temps de reproduction
- Énergie des requins