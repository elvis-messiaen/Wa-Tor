# Choisir aléatoirement une case vide
import random
from interface import 
class Fish:
    def __init__(self, x : int , y: int , reproduction_time, Alive : bool,):
        """
        Initialise un poisson avec :
        - sa position (x, y)
        - un compteur d'âge (initialisé à 0)
        - un temps de reproduction requis
        """
        self.x = x  # Coordonnée horizontale dans la grille
        self.y = y  # Coordonnée verticale dans la grille
        self.age = 0  # Nombre de chronons écoulés depuis la naissance
        self.reproduction_time = reproduction_time  # Chronons nécessaires avant reproduction
    
    def Step(self):
        """
        - Le poisson vieillit d'un tour(chronon).
        """
        self.age += 1
    

    def reproduce(self):
        """
        Crée un nouveau poisson (reproduction).
        Le parent garde sa position mais son âge est remis à zéro.
        Le nouveau poisson sera placé ailleurs (à définir à l’extérieur).
        """
        self.age = 0  # Réinitialise l'âge du parent après reproduction
        return Fish(self.x, self.y, self.reproduction_time)  # Bébé poisson à même position (à ajuster ensuite)
    
    def move (self):
        """
        Déplace le poisson vers une case vide disponible autour de lui.
        - empty_cells est une liste de positions (x, y)
        - Si aucune case vide, il ne bouge pas
        """
        if empty:
            new_position = random.choice(empty)
            self.x, self.y = new_position  # Met à jour la position du poisson
    
    def choose_direction(self):
    direction = randint(0, 1)  # Choisit aléatoirement 0 (horizontal) ou 1 (vertical)
    sign = 2 * randint(0, 1) - 1  # Génère -1 ou +1 (c’est le sens du déplacement)
    if direction == 0:
        return (sign, 0)  # Déplacement horizontal : à gauche ou à droite
    else:
        return (0, sign)  # Déplacement vertical : en haut ou en bas


    def Position(self):
        """
        Retourne la position actuelle du poisson (utile pour la grille).
        """
        return (self.x, self.y)
    
    def __str__(self):
        """
        Représentation visuelle du poisson (utilisée lors de l'affichage de la grille).
        """
        return "🐟"
    
    