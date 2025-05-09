import random
from typing import List, Set, Tuple, Any, Optional
from aquatic.fish import Fish

class Shark(Fish):
    """Classe représentant un requin dans la simulation Wa-Tor.
    Hérite de la classe Fish et ajoute des comportements spécifiques aux requins :
    - Gestion de l'énergie
    - Prédation des poissons
    - Reproduction avec coût énergétique
    """
    
    # Variable de classe (statique) pour générer des identifiants uniques
    # Chaque requin aura un ID unique incrémenté à chaque création
    compteur_id_requin: int = 0

    def __init__(self, grid: Any, x: int, y: int, shark_energy: int = 15, 
                 shark_reproduction_time: int = 0, alive: bool = True) -> None:
        """Initialise un nouveau requin avec ses caractéristiques spécifiques.
        
        Args:
            grid (Any): Référence à la grille de simulation où le requin évolue
            x (int): Position x initiale dans la grille
            y (int): Position y initiale dans la grille
            shark_energy (int, optional): Énergie initiale du requin. Defaults to 15.
            shark_reproduction_time (int, optional): Temps nécessaire pour la reproduction. Defaults to 0.
            alive (bool, optional): État de vie initial du requin. Defaults to True.
        """
        # Appel du constructeur de la classe parente (Fish)
        super().__init__(grid, x, y, reproduction_time=shark_reproduction_time, alive=alive)
        # Initialisation des attributs spécifiques au requin
        self.grid: Any = grid  # Référence à la grille de simulation
        self.age: int = 0  # Âge initial du requin
        self.id: int = Shark.compteur_id_requin  # Attribution d'un ID unique
        Shark.compteur_id_requin += 1  # Incrémentation du compteur pour le prochain requin
        self.shark_energy: int = shark_energy  # Énergie initiale du requin
        self.shark_reproduction_time: int = shark_reproduction_time  # Temps nécessaire pour la reproduction
        self.energy_from_fish: int = 15  # Énergie gagnée en mangeant un poisson
    
    def eat(self, fish: Fish) -> None:
        """Fait manger un poisson au requin, augmentant son énergie.
        
        Args:
            fish (Fish): Le poisson à manger
        """
        # Augmente l'énergie du requin en mangeant le poisson
        self.shark_energy += self.energy_from_fish
        # Supprime le poisson mangé de la grille s'il est encore vivant
        if fish.alive:
            fish.remove_fish(self.grid)

    def step(self) -> None:
        """Fait vieillir le requin et diminue son énergie.
        Cette méthode est appelée à chaque tour de simulation.
        Le requin perd de l'énergie même s'il ne se déplace pas."""
        self.age += 1  # Incrémente l'âge
        self.shark_energy -= 1  # Diminue l'énergie (coût de la vie)

    def get_fish_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Trouve les poissons adjacents à la position du requin.
        
        Args:
            x (int): Position x du requin
            y (int): Position y du requin
            
        Returns:
            List[Tuple[int, int]]: Liste des coordonnées des poissons adjacents
        """
        # Directions possibles : haut, bas, gauche, droite
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        # Vérifie chaque direction pour trouver les poissons
        for dx, dy in directions:
            # Utilise les coordonnées toroïdales (la grille est un tore)
            nx, ny = self.grid.get_toroidal_coords(x + dx, y + dy)
            cell = self.grid.cells[nx][ny]
            # Vérifie si la cellule contient un poisson (mais pas un requin)
            if isinstance(cell, Fish) and not isinstance(cell, Shark):
                neighbors.append((nx, ny))
        return neighbors
    
    def handle_shark(self, x: int, y: int, already_moved: Set[Tuple[int, int]]) -> None:
        """Gère le comportement complet du requin pendant un tour de simulation.
        
        Args:
            x (int): Position x actuelle
            y (int): Position y actuelle
            already_moved (Set[Tuple[int, int]]): Ensemble des positions déjà déplacées
        """
        # Cherche les poissons adjacents
        fish_neighbors = self.get_fish_neighbors(x, y)
        if fish_neighbors:
            # Si des poissons sont trouvés, en mange un au hasard
            nx, ny = random.choice(fish_neighbors)
            self.eat(self.grid.cells[nx][ny])
            self.grid.move_entity(self, x, y, nx, ny, already_moved)
        else:
            # Si pas de poisson, perd plus d'énergie et cherche une case vide
            self.shark_energy -= 5  # Pénalité énergétique pour ne pas avoir mangé
            empty = self.grid.get_empty_neighbors(x, y)
            if empty:
                nx, ny = random.choice(empty)
                self.grid.move_entity(self, x, y, nx, ny, already_moved)
        
        # Fait vieillir le requin et diminue son énergie
        self.step()
        
        # Vérifie si le requin meurt de faim
        if self.shark_energy <= 0:
            self.die()
            self.grid.cells[self.x][self.y] = None
        # Vérifie si le requin peut se reproduire
        elif self.age % self.shark_reproduction_time == 0 and self.age != 0:
            self.reproduce_entity(self.grid, x, y)

    def reproduce_entity(self, grid: Any, x: int, y: int) -> None:
        """Crée un nouveau requin dans une case vide adjacente.
        
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
            # Crée un nouveau requin avec une énergie initiale de 5
            # L'énergie est faible car le parent a déjà dépensé de l'énergie pour la reproduction
            baby = Shark(grid, nx, ny, shark_energy=5,
                        shark_reproduction_time=self.shark_reproduction_time)
            # Place le nouveau requin dans la grille
            grid.cells[nx][ny] = baby
