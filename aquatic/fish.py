import random

class Fish:
    """Classe représentant un poisson dans la simulation Wa-Tor."""
    
    def __init__(self, grid, x, y, reproduction_time, alive=True):
        """Initialise un poisson avec ses caractéristiques."""
        self.grid = grid  # Référence à la grille
        self.x = x  # Position x dans la grille
        self.y = y  # Position y dans la grille
        self.reproduction_time = reproduction_time  # Temps nécessaire pour la reproduction
        self.alive = alive  # État du poisson (vivant ou mort)
        self.age = 0  # Âge du poisson
        
    def die(self):
        """Marque le poisson comme mort."""
        self.alive = False
        
    def remove_fish(self, grid):
        """Supprime le poisson de la grille."""
        grid.cells[self.x][self.y] = None
        
    def step(self):
        """Fait vieillir le poisson d'un tour."""
        self.age += 1
            
    def get_empty_neighbors(self, grid, x, y):
        """Retourne les cellules vides adjacentes à la position du poisson."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Haut, bas, gauche, droite
        return [(nx, ny) for dx, dy in directions
                if 0 <= (nx := x + dx) < grid.point_x and 0 <= (ny := y + dy) < grid.point_y
                and grid.cells[nx][ny] is None]
    
    def position(self):
        """Retourne la position actuelle du poisson."""
        return (self.x, self.y)
    
    def handle_fish(self, grid, x, y, already_moved):
        """Gère le comportement du poisson pendant un tour de simulation."""
        self.step()  # Vieillissement
        empty = self.get_empty_neighbors(grid, x, y)
        if empty:
            # Déplacement vers une case vide aléatoire
            nx, ny = random.choice(empty)
            grid.move_entity(self, x, y, nx, ny, already_moved)

        # Reproduction si l'âge est suffisant
        if self.age >= self.reproduction_time:
            self.reproduce_entity(grid, x, y)

    def reproduce_entity(self, grid, x, y):
        """Crée un nouveau poisson dans une case vide adjacente."""
        empty = self.get_empty_neighbors(grid, x, y)
        if empty:
            nx, ny = random.choice(empty)
            grid.cells[nx][ny] = Fish(grid, nx, ny, self.reproduction_time)
            print(f"Reproduction: {grid.cells[nx][ny]} créé à ({nx}, {ny})")
            self.age = 0  # Réinitialisation de l'âge après reproduction
