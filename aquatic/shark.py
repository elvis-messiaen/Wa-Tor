import random
from typing import List, Set, Tuple, Any
from aquatic.fish import Fish

class Shark(Fish):
    """Classe représentant un requin dans la simulation Wa-Tor.
    Hérite de la classe Fish."""
    
    compteur_id_requin: int = 0  # Compteur statique pour les identifiants uniques des requins

    def __init__(self, grid: Any, x: int, y: int, shark_energy: int = 15, 
                 shark_reproduction_time: int = 0, alive: bool = True) -> None:
        """Initialise un requin avec ses caractéristiques spécifiques.
        
        Args:
            grid (Any): Référence à la grille de simulation
            x (int): Position x initiale
            y (int): Position y initiale
            shark_energy (int, optional): Énergie initiale du requin. Defaults to 15.
            shark_reproduction_time (int, optional): Temps nécessaire pour la reproduction. Defaults to 0.
            alive (bool, optional): État de vie du requin. Defaults to True.
        """
        super().__init__(grid, x, y, reproduction_time=shark_reproduction_time, alive=alive)
        self.grid: Any = grid
        self.age: int = 0
        self.id: int = Shark.compteur_id_requin
        Shark.compteur_id_requin += 1
        self.shark_energy: int = shark_energy
        self.shark_reproduction_time: int = shark_reproduction_time
    
    def eat(self, fish: Fish) -> None:
        """Fait manger un poisson au requin, augmentant son énergie.
        
        Args:
            fish (Fish): Le poisson à manger
        """
        self.shark_energy += 15
        if fish.alive:
            fish.remove_fish(self.grid)

    def step(self) -> None:
        """Fait vieillir le requin et diminue son énergie."""
        self.age += 1
        self.shark_energy -= 1

    def get_fish_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Retourne les poissons adjacents à la position du requin.
        
        Args:
            x (int): Position x du requin
            y (int): Position y du requin
            
        Returns:
            List[Tuple[int, int]]: Liste des coordonnées des poissons adjacents
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dx, dy in directions:
            nx, ny = self.grid.get_toroidal_coords(x + dx, y + dy)
            cell = self.grid.cells[nx][ny]
            if isinstance(cell, Fish) and not isinstance(cell, Shark):
                neighbors.append((nx, ny))
        return neighbors
    
    def handle_shark(self, x: int, y: int, already_moved: Set[Tuple[int, int]]) -> None:
        """Gère le comportement du requin pendant un tour de simulation.
        
        Args:
            x (int): Position x actuelle
            y (int): Position y actuelle
            already_moved (Set[Tuple[int, int]]): Ensemble des positions déjà déplacées
        """
        fish_neighbors = self.get_fish_neighbors(x, y)
        if fish_neighbors:
            nx, ny = random.choice(fish_neighbors)
            self.eat(self.grid.cells[nx][ny])
            self.grid.move_entity(self, x, y, nx, ny, already_moved)
        else:
            self.shark_energy -= 5
            empty = self.grid.get_empty_neighbors(x, y)
            if empty:
                nx, ny = random.choice(empty)
                self.grid.move_entity(self, x, y, nx, ny, already_moved)
        
        self.step()
        
        if self.shark_energy <= 0:
            self.die()
            self.grid.cells[self.x][self.y] = None
        elif self.age % self.shark_reproduction_time == 0 and self.age != 0:
            self.reproduce_entity(self.grid, x, y)

    def reproduce_entity(self, grid: Any, x: int, y: int) -> None:
        """Crée un nouveau requin dans une case vide adjacente.
        
        Args:
            grid (Any): Grille de simulation
            x (int): Position x du parent
            y (int): Position y du parent
        """
        empty = self.get_empty_neighbors(grid, x, y)
        if empty:
            nx, ny = random.choice(empty)
            baby = Shark(grid, nx, ny, shark_energy=5,
                        shark_reproduction_time=self.shark_reproduction_time)
            grid.cells[nx][ny] = baby
