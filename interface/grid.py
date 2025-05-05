import random
from aquatic.fish import Fish
from aquatic.shark import Shark

# Variables globales pour la gestion de la grille et de la simulation
_grid_instance = None  # Instance unique de la grille (singleton)
turn_count = 0  # Compteur de tours de simulation
simulation_running = False  # État de la simulation (en cours ou arrêtée)

def get_grid_instance(point_x=None, point_y=None):
    """Retourne l'instance unique de la grille (pattern Singleton).
    Si l'instance n'existe pas et que les dimensions sont fournies, crée une nouvelle instance."""
    global _grid_instance
    if _grid_instance is None and point_x is not None and point_y is not None:
        _grid_instance = Grid(point_x, point_y)
    return _grid_instance

class Grid:
    """Classe représentant la grille de simulation Wa-Tor."""
    
    def __init__(self, point_x: int, point_y: int):
        """Initialise la grille avec les dimensions spécifiées."""
        self.point_x = point_x  # Largeur de la grille
        self.point_y = point_y  # Hauteur de la grille
        self.cells = [[None for _ in range(point_y)] for _ in range(point_x)]  # Grille 2D initialisée avec None
        self.cell_labels = None  # Labels pour l'interface graphique

    def set_cell_labels(self, labels):
        """Définit les labels de la grille pour l'interface graphique."""
        self.cell_labels = labels

    def populate_grid(self):
        """Remplit la grille avec des requins et des poissons selon des proportions définies."""
        total_cells = self.point_x * self.point_y
        num_sharks = int(total_cells * 0.1)  # 10% de requins
        num_fish = int(total_cells * 0.7)    # 70% de poissons
        total_entities = num_sharks + num_fish
        
        # Création et mélange des positions possibles
        all_positions = [(x, y) for x in range(self.point_x) for y in range(self.point_y)]
        random.shuffle(all_positions)
        
        # Placement des requins
        for i in range(num_sharks):
            x, y = all_positions[i]
            shark = Shark(grid=self, x=x, y=y, shark_energy=2, shark_reproduction_time=5)
            self.cells[x][y] = shark
        
        # Placement des poissons
        for i in range(num_sharks, total_entities):
            x, y = all_positions[i]
            fish = Fish(grid=self, x=x, y=y, reproduction_time=5, alive=True)
            self.cells[x][y] = fish

        # Vérification du nombre d'entités placées
        current_fish, current_sharks = self.count_entities()
        print(f"Initialisation : {current_fish} poissons et {current_sharks} requins")

    def empty(self, x, y):
        """Vérifie si une cellule est vide et dans les limites de la grille."""
        return 0 <= x < self.point_x and 0 <= y < self.point_y and self.cells[x][y] is None

    def __str__(self):
        """Retourne une représentation textuelle de la grille avec des emojis."""
        grid_representation = ""
        for row in self.cells:
            row_rep = ""
            for cell in row:
                if cell is None:
                    row_rep += ". "
                elif isinstance(cell, Fish):
                    row_rep += "🐟 "
                elif isinstance(cell, Shark):
                    row_rep += "🦈 "
            grid_representation += row_rep + "\n"
        return grid_representation

    def move_entity(self, entity, x, y, nx, ny, already_moved):
        """Déplace une entité d'une position à une autre sur la grille."""
        self.cells[nx][ny] = self.cells[x][y]
        print(f"Déplacement de {self.cells[x][y]} de ({x}, {y}) à ({nx}, {ny})")
        self.cells[x][y] = None
        entity.x, entity.y = nx, ny
        already_moved.add((nx, ny))

    def count_entities(self):
        """Compte le nombre de poissons et de requins dans la grille."""
        fish_count = sum(isinstance(cell, Fish) and not isinstance(cell, Shark) for row in self.cells for cell in row)
        shark_count = sum(isinstance(cell, Shark) for row in self.cells for cell in row)
        return fish_count, shark_count

    def update_info(self, label):
        """Met à jour les informations affichées dans l'interface."""
        fish_count, shark_count = self.count_entities()
        label.config(text=f"Tour : {turn_count}   🐟 Poissons : {fish_count}   🦈 Requins : {shark_count}")

    def draw_grid_emojis(self):
        """Dessine la grille avec des emojis dans l'interface graphique."""
        for x in range(self.point_x):
            for y in range(self.point_y):
                cell = self.cells[x][y]
                if cell is None:
                    self.cell_labels[x][y].config(text="🌊")
                elif isinstance(cell, Shark):
                    self.cell_labels[x][y].config(text="🦈")
                elif isinstance(cell, Fish) and not isinstance(cell, Shark):
                    self.cell_labels[x][y].config(text="🐟")

    def simulate_step(self, info_label):
        """Exécute un tour de simulation."""
        global turn_count
        already_moved = set()  # Ensemble des entités déjà déplacées dans ce tour
        # Récupération de toutes les entités (poissons et requins)
        entities = [self.cells[x][y] for x in range(self.point_x) for y in range(self.point_y) 
                   if isinstance(self.cells[x][y], Shark) or (isinstance(self.cells[x][y], Fish) and not isinstance(self.cells[x][y], Shark))]
        random.shuffle(entities)  # Mélange pour un ordre aléatoire

        for entity in entities:
            if entity is None:
                continue
            x, y = entity.x, entity.y
            if (x, y) in already_moved:
                continue
            if isinstance(entity, Shark):
                entity.handle_shark(x, y, already_moved)
            elif isinstance(entity, Fish) and not isinstance(entity, Shark):
                entity.handle_fish(self, x, y, already_moved)

        turn_count += 1
        self.draw_grid_emojis()
        self.update_info(info_label)

    def run_simulation(self, root, button, info_label):
        """Lance la simulation en boucle avec un délai de 500ms entre chaque tour."""
        if simulation_running:
            self.simulate_step(info_label)
            root.after(500, self.run_simulation, root, button, info_label)

    def toggle_simulation(self, root, button, info_label):
        """Active ou désactive la simulation."""
        global simulation_running
        simulation_running = not simulation_running
        if simulation_running:
            button.config(text="Pause")
            self.run_simulation(root, button, info_label)
        else:
            button.config(text="Lancer")
        
    def get_empty_neighbors(self, x, y):
        """Retourne les cellules vides adjacentes à une position donnée."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return [(nx, ny) for dx, dy in directions
                if 0 <= (nx := x + dx) < self.point_x and 0 <= (ny := y + dy) < self.point_y
                and self.cells[nx][ny] is None]
