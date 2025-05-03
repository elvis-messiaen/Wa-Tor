import random
from aquatic.fish import Fish
from aquatic.shark import Shark

_grid_instance = None
turn_count = 0
simulation_running = False

def get_grid_instance(point_x=None, point_y=None):
    global _grid_instance
    if _grid_instance is None and point_x is not None and point_y is not None:
        _grid_instance = Grid(point_x, point_y)
    return _grid_instance

class Grid:
    def __init__(self, point_x: int, point_y: int):
        self.point_x = point_x
        self.point_y = point_y
        self.cells = [[None for _ in range(point_y)] for _ in range(point_x)]
        self.cell_labels = None  # Initialisé à None, sera défini plus tard

    def create(self):
        """Initialise les cellules."""
        self.cells = [[None for _ in range(self.point_y)] for _ in range(self.point_x)]

    def set_cell_labels(self, labels):
        """Définit les labels de la grille."""
        self.cell_labels = labels

    def populate_grid(self):
        """Remplit la grille avec 10% de requins et 70% de poissons."""
        total_cells = self.point_x * self.point_y
        num_sharks = int(total_cells * 0.1)
        num_fish = int(total_cells * 0.7)
        positions = random.sample(range(total_cells), num_sharks + num_fish)

        for i, pos in enumerate(positions):
            row, col = divmod(pos, self.point_y)
            if i < num_sharks:
                shark = Shark(grid=self, x=row, y=col, shark_energy=15, shark_reproduction_time=3, shark_starvation_time=5)
                self.cells[row][col] = shark
            else:
                fish = Fish(x=row, y=col, reproduction_time=5, alive=True)
                self.cells[row][col] = fish

    def empty(self, x, y):
        """Vérifie si une cellule est vide."""
        return 0 <= x < self.point_x and 0 <= y < self.point_y and self.cells[x][y] is None

    def __str__(self):
        """Retourne une représentation textuelle de la grille."""
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
        """Déplace une entité sur la grille."""
        self.cells[nx][ny] = entity
        self.cells[x][y] = None
        entity.x, entity.y = nx, ny
        already_moved.add((nx, ny))

    def reproduce_entity(self, entity, x, y):
        """Permet la reproduction d'une entité sur une case vide."""
        baby = entity.reproduce()
        if baby:
            empty_spots = self.get_empty_neighbors(x, y)
            if empty_spots:
                bx, by = random.choice(empty_spots)
                baby.x, baby.y = bx, by
                self.cells[bx][by] = baby

    def count_entities(self):
        """Compte le nombre de requins et de poissons."""
        fish_count = sum(isinstance(cell, Fish) for row in self.cells for cell in row)
        shark_count = sum(isinstance(cell, Shark) for row in self.cells for cell in row)
        return fish_count, shark_count

    def update_info(self, label):
        """Met à jour les informations affichées."""
        fish_count, shark_count = self.count_entities()
        label.config(text=f"Tour : {turn_count}   🐟 Poissons : {fish_count}   🦈 Requins : {shark_count}")

    def draw_grid_emojis(self):
        """Met à jour l'affichage des entités."""
        for x in range(self.point_x):
            for y in range(self.point_y):
                entity = self.cells[x][y]
                emoji = "⬜"
                if isinstance(entity, Shark):
                    emoji = "🦈"
                elif isinstance(entity, Fish):
                    emoji = "🐟"

                if self.cell_labels[x][y]:  
                    self.cell_labels[x][y].config(text=emoji)  # Mise à jour affichage

    def simulate_step(self, info_label):
        """Exécute un tour de simulation."""
        global turn_count
        already_moved = set()
        entities = [self.cells[x][y] for x in range(self.point_x) for y in range(self.point_y) if isinstance(self.cells[x][y], (Shark, Fish))]
        random.shuffle(entities)

        for entity in entities:
            x, y = entity.x, entity.y
            if (x, y) in already_moved:
                continue
            if isinstance(entity, Shark):
                entity.handle_shark(x, y, already_moved)
            elif isinstance(entity, Fish):
                entity.handle_fish(self, x, y, already_moved)

        turn_count += 1
        self.draw_grid_emojis()
        self.update_info(info_label)

    def run_simulation(self, root, button, info_label):
        """Lance la simulation en boucle."""
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
        """Retourne les cellules vides adjacentes."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return [(nx, ny) for dx, dy in directions
                if 0 <= (nx := x + dx) < self.point_x and 0 <= (ny := y + dy) < self.point_y
                and self.cells[nx][ny] is None]
