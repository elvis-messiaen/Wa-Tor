import random
class Fish:
    def __init__(self, x, y, reproduction_time, alive=True):
        self.x = x
        self.y = y
        self.reproduction_time = reproduction_time
        self.alive = alive
        self.age = 0
        
    def die(self):
        """
        Marque le poisson comme mort. 
        (ne modifie pas la grille ici)
        """
        self.alive = False  # Marque le poisson comme mort
        
    def step(self):
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
    
    def move(self, grid):
        """
        Déplace le poisson vers une case vide disponible autour de lui.
        - empty_cells est une liste de positions (x, y)
        - Si aucune case vide, il ne bouge pas
        """
        empty_cells = grid.empty(self.x, self.y)  # Récupère les cases vides autour du poisson
        if empty_cells:
            self.x, self.y = random.choice(empty_cells)  # Choisit une case vide aléatoire parmi celles disponibles
            
    def get_empty_neighbors(grid, x, y): # Move to fish.py
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return [(nx, ny) for dx, dy in directions
            if 0 <= (nx := x + dx) < len(grid) and 0 <= (ny := y + dy) < len(grid[0])
            and grid[nx][ny] is None]
    
    def position(self):
        """
        Retourne la position actuelle du poisson (utile pour la grille).
        """
        return (self.x, self.y)
    
    def __str__(self):
        """
        Représentation visuelle du poisson (utilisée lors de l'affichage de la grille).
        """
        return "🐟"
