# Importation des modules nécessaires
# random : pour les choix aléatoires (déplacement, reproduction)
# typing : pour le typage statique des variables
import random
from typing import List, Set, Tuple, Optional, Any

class Fish:
    """Classe représentant un poisson dans la simulation Wa-Tor.
    Cette classe gère le comportement d'un poisson dans l'écosystème."""
    
    # Variable de classe (statique) pour générer des identifiants uniques
    # Chaque poisson aura un ID unique incrémenté à chaque création
    compteur_id_poisson: int = 0

    def __init__(self, grid: Any, x: int, y: int, reproduction_time: int = 5, alive: bool = True) -> None:
        """Initialise un nouveau poisson avec ses caractéristiques de base.
        
        Args:
            grid (Any): Référence à la grille de simulation où le poisson évolue
            x (int): Position x initiale dans la grille
            y (int): Position y initiale dans la grille
            reproduction_time (int, optional): Âge nécessaire pour la reproduction. Defaults to 5.
            alive (bool, optional): État de vie initial du poisson. Defaults to True.
        """
        # Initialisation des attributs de base du poisson
        self.grid: Any = grid  # Référence à la grille de simulation
        self.x: int = x  # Position x dans la grille
        self.y: int = y  # Position y dans la grille
        self.age: int = 0  # Âge initial du poisson
        self.reproduction_time: int = reproduction_time  # Âge nécessaire pour la reproduction
        self.alive: bool = alive  # État de vie du poisson
        self.id: int = Fish.compteur_id_poisson  # Attribution d'un ID unique
        Fish.compteur_id_poisson += 1  # Incrémentation du compteur pour le prochain poisson
        
    def die(self) -> None:
        """Marque le poisson comme mort.
        Cette méthode est appelée quand le poisson meurt (mangé par un requin)."""
        self.alive = False
        
    def remove_fish(self, grid: Any) -> None:
        """Supprime le poisson de la grille de simulation.
        
        Args:
            grid (Any): Grille de simulation où le poisson doit être supprimé
        """
        # Supprime le poisson de la grille en mettant la cellule à None
        grid.cells[self.x][self.y] = None
        self.alive = False 

    def step(self) -> None:
        """Fait vieillir le poisson d'un tour en incrémentant son âge.
        Cette méthode est appelée à chaque tour de simulation."""
        self.age += 1
            
    def get_empty_neighbors(self, grid: Any, x: int, y: int) -> List[Tuple[int, int]]:
        """Trouve les cellules vides adjacentes à la position du poisson.
        
        Args:
            grid (Any): Grille de simulation
            x (int): Position x du poisson
            y (int): Position y du poisson
            
        Returns:
            List[Tuple[int, int]]: Liste des coordonnées des cellules vides adjacentes
        """
        # Directions possibles : haut, bas, gauche, droite
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        # Vérifie chaque direction pour trouver les cases vides
        for dx, dy in directions:
            # Utilise les coordonnées toroïdales (la grille est un tore)
            nx, ny = grid.get_toroidal_coords(x + dx, y + dy)
            if grid.cells[nx][ny] is None:
                neighbors.append((nx, ny))
        return neighbors
    
    def position(self) -> Tuple[int, int]:
        """Retourne la position actuelle du poisson.
        
        Returns:
            Tuple[int, int]: Coordonnées (x, y) du poisson
        """
        return (self.x, self.y)
    
    def handle_fish(self, grid: Any, x: int, y: int, already_moved: Set[Tuple[int, int]]) -> None:
        """Gère le comportement complet du poisson pendant un tour de simulation.
        
        Args:
            grid (Any): Grille de simulation
            x (int): Position x actuelle
            y (int): Position y actuelle
            already_moved (Set[Tuple[int, int]]): Ensemble des positions déjà déplacées
        """
        # Fait vieillir le poisson
        self.step()
        # Cherche les cases vides adjacentes
        empty = self.get_empty_neighbors(grid, x, y)
        # Si une case vide est trouvée, déplace le poisson
        if empty:
            nx, ny = random.choice(empty)
            grid.move_entity(self, x, y, nx, ny, already_moved)

        # Vérifie si le poisson peut se reproduire
        if self.age >= self.reproduction_time:
            self.reproduce_entity(grid, x, y)

    def reproduce_entity(self, grid: Any, x: int, y: int) -> None:
        """Crée un nouveau poisson dans une case vide adjacente.
        
        Args:
            grid (Any): Grille de simulation
            x (int): Position x du parent
            y (int): Position y du parent
        """
        # Cherche les cases vides adjacentes pour la reproduction
        empty = self.get_empty_neighbors(grid, x, y)
        if empty:
            # Choisit une case vide aléatoire
            nx, ny = random.choice(empty)
            # Crée un nouveau poisson
            baby = Fish(grid, nx, ny, reproduction_time=self.reproduction_time)
            # Place le nouveau poisson dans la grille
            grid.cells[nx][ny] = baby
            # Réinitialise l'âge du parent après reproduction
            self.age = 0
