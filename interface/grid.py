import random
from aquatic.fish import Fish
from aquatic.shark import Shark

_grid_instance = None

def get_grid_instance(point_x=None, point_y=None):
    global _grid_instance
    if _grid_instance is None and point_x is not None and point_y is not None:
        _grid_instance = Grid(point_x, point_y)
    return _grid_instance

class Grid:
    def __init__(self, point_x: int, point_y: int):
        self.point_x = point_x
        self.point_y = point_y
        self.cells = [["" for _ in range(point_y)] for _ in range(point_x)]  # La grille est initialisée ici

    def create(self):
        """Réinitialiser la grille."""
        self.cells = [[None for _ in range(self.point_y)] for _ in range(self.point_x)]

    def populate_grid(self, entities):
        for x in range(self.point_x):
            for y in range(self.point_y):
                r = random.random()
                
                if r < 0.1:  # 10% de chance de placer un poisson
                    fish = Fish(x, y), reproduction_time=3, alive=True)
                    self.cells[x][y] = fish  # Placement du poisson dans la grille
                    entities.append(fish)
                    print(f"Poisson ajouté à la position ({x}, {y})")  # Log pour les poissons
                    
                elif r < 0.3:  # 20% de chance de placer un requin (augmentation de la probabilité)
                    shark = Shark(x=x, y=y, shark_energy=15, shark_reproduction_time=5, shark_starvation_time=5, grid=self, alive=True)
                    shark.grid = self
                    self.cells[x][y] = shark  # Placement du requin dans la grille
                    entities.append(shark)
                    print(f"Requin ajouté à la position ({x}, {y})")  # Log pour les requins

    def empty(self, x, y):
        """Vérifie si une case (x, y) est vide."""
        if 0 <= x < self.point_x and 0 <= y < self.point_y:
            return self.cells[x][y] == ""  # Retourne True si la case est vide
        return False

    def get_fish_neighbors(self, x, y):
        """Retourne les poissons voisins autour de (x, y)."""
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.point_x and 0 <= ny < self.point_y:
                if isinstance(self.cells[nx][ny], Fish) and not isinstance(self.cells[nx][ny], Shark):
                    neighbors.append(self.cells[nx][ny])
        return neighbors

    def get_empty_neighbors(self, x, y):
        """Retourne les voisins vides autour de (x, y)."""
        empty_cells = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.point_x and 0 <= ny < self.point_y:
                if self.cells[nx][ny] == "":  # Si la case est vide
                    empty_cells.append((nx, ny))
        return empty_cells

    def __str__(self):
        """Représente la grille pour l'affichage."""
        grid_representation = ""
        for row in self.cells:
            row_rep = ""
            for cell in row:
                if cell == "":
                    row_rep += ". "  # Case vide
                elif isinstance(cell, Fish):
                    row_rep += "🐟 "  # Poisson
                elif isinstance(cell, Shark):
                    row_rep += "🦈 "  # Requin
                else:
                    row_rep += "? "  # Si la cellule contient autre chose
            grid_representation += row_rep + "\n"
        return grid_representation
