import random
from typing import List, Set, Tuple, Optional, Any

class Fish:
    """Classe représentant un poisson dans la simulation Wa-Tor."""
    
    def __init__(self, grid: Any, x: int, y: int, reproduction_time: int, alive: bool = True) -> None:
        """Initialise un poisson avec ses caractéristiques.
        
        Args:
            grid (Any): Référence à la grille de simulation
            x (int): Position x initiale
            y (int): Position y initiale
            reproduction_time (int): Temps nécessaire pour la reproduction
            alive (bool, optional): État de vie du poisson. Defaults to True.
        """
        self.grid: Any = grid
        self.x: int = x
        self.y: int = y
        self.reproduction_time: int = reproduction_time
        self.alive: bool = alive
        self.age: int = 0
        
    def die(self) -> None:
        """Marque le poisson comme mort."""
        self.alive = False
        
    def remove_fish(self, grid: Any) -> None:
        """Supprime le poisson de la grille.
        
        Args:
            grid (Any): Grille de simulation
        """
        grid.cells[self.x][self.y] = None
        
    def step(self) -> None:
        """Fait vieillir le poisson d'un tour."""
        self.age += 1
            
    def get_empty_neighbors(self, grid: Any, x: int, y: int) -> List[Tuple[int, int]]:
        """Retourne les cellules vides adjacentes à la position du poisson.
        
        Args:
            grid (Any): Grille de simulation
            x (int): Position x du poisson
            y (int): Position y du poisson
            
        Returns:
            List[Tuple[int, int]]: Liste des coordonnées des cellules vides adjacentes
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return [(nx, ny) for dx, dy in directions
                if 0 <= (nx := x + dx) < grid.point_x and 0 <= (ny := y + dy) < grid.point_y
                and grid.cells[nx][ny] is None]
    
    def position(self) -> Tuple[int, int]:
        """Retourne la position actuelle du poisson.
        
        Returns:
            Tuple[int, int]: Coordonnées (x, y) du poisson
        """
        return (self.x, self.y)
    
    def handle_fish(self, grid: Any, x: int, y: int, already_moved: Set[Tuple[int, int]]) -> None:
        """Gère le comportement du poisson pendant un tour de simulation.
        
        Args:
            grid (Any): Grille de simulation
            x (int): Position x actuelle
            y (int): Position y actuelle
            already_moved (Set[Tuple[int, int]]): Ensemble des positions déjà déplacées
        """
        self.step()
        empty = self.get_empty_neighbors(grid, x, y)
        if empty:
            nx, ny = random.choice(empty)
            grid.move_entity(self, x, y, nx, ny, already_moved)

        if self.age >= self.reproduction_time:
            self.reproduce_entity(grid, x, y)

    def reproduce_entity(self, grid: Any, x: int, y: int) -> None:
        """Crée un nouveau poisson dans une case vide adjacente.
        
        Args:
            grid (Any): Grille de simulation
            x (int): Position x du parent
            y (int): Position y du parent
        """
        empty = self.get_empty_neighbors(grid, x, y)
        if empty:
            nx, ny = random.choice(empty)
            grid.cells[nx][ny] = Fish(grid, nx, ny, self.reproduction_time)
            self.age = 0
