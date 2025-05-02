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

    def populate_grid(self):
        """Remplit la grille avec des poissons et des requins."""
        total_cells = self.point_x * self.point_y
        num_sharks = int(total_cells * 0.1)
        num_fish = int(total_cells * 0.7)   

        positions = random.sample(range(total_cells), num_sharks + num_fish)
        entities = []  # Liste pour stocker les entités     

        for i, pos in enumerate(positions):
            row, col = divmod(pos, self.point_y)
            if i < num_sharks:
                shark = Shark(grid=self, x=row, y=col, shark_energy=15, shark_reproduction_time=3, shark_starvation_time=5)
                self.cells[row][col] = shark  # Remplacement de self.grid par self.cells
                entities.append(shark)
            else:
                fish = Fish(x=row, y=col, reproduction_time=5, alive=True)
                self.cells[row][col] = fish  # Remplacement de self.grid par self.cells
                entities.append(fish)   

        return entities  # Retourne la liste des entités

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
    

