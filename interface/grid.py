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
        self.cells = [["" for _ in range(point_y)] for _ in range(point_x)]
        self.cell_labels = [[None for _ in range(point_y)] for _ in range(point_x)]

    def create(self):
        self.cells = [[None for _ in range(self.point_y)] for _ in range(self.point_x)]
        self.cell_labels = [[None for _ in range(self.point_y)] for _ in range(self.point_x)]

    def populate_grid(self):
        total_cells = self.point_x * self.point_y
        num_sharks = int(total_cells * 0.1)
        num_fish = int(total_cells * 0.7)
        positions = random.sample(range(total_cells), num_sharks + num_fish)
        entities = []

        for i, pos in enumerate(positions):
            row, col = divmod(pos, self.point_y)
            if i < num_sharks:
                shark = Shark(grid=self, x=row, y=col, shark_energy=15, shark_reproduction_time=3, shark_starvation_time=5)
                self.cells[row][col] = shark
                entities.append(shark)
            else:
                fish = Fish(x=row, y=col, reproduction_time=5, alive=True)
                self.cells[row][col] = fish
                entities.append(fish)
        return entities

    def empty(self, x, y):
        if 0 <= x < self.point_x and 0 <= y < self.point_y:
            return self.cells[x][y] == ""
        return False

    def __str__(self):
        grid_representation = ""
        for row in self.cells:
            row_rep = ""
            for cell in row:
                if cell == "":
                    row_rep += ". "
                elif isinstance(cell, Fish):
                    row_rep += "🐟 "
                elif isinstance(cell, Shark):
                    row_rep += "🦈 "
                else:
                    row_rep += "? "
            grid_representation += row_rep + "\n"
        return grid_representation

    def move_entity(self, entity, x, y, nx, ny, already_moved):
        self.cells[nx][ny] = entity
        self.cells[x][y] = None
        entity.x, entity.y = nx, ny
        already_moved.add((nx, ny))

    def reproduce_entity(self, entity, x, y):
        baby = entity.reproduce()
        if baby:
            baby.grid = self
            empty_spots = self.get_empty_neighbors(x, y)
            if empty_spots:
                bx, by = random.choice(empty_spots)
                baby.x, baby.y = bx, by
                self.cells[bx][by] = baby

    def count_entities(self):
        global turn_count
        fish_count = 0
        shark_count = 0
        for row in self.cells:
            for cell in row:
                if isinstance(cell, Shark):
                    shark_count += 1
                elif isinstance(cell, Fish):
                    fish_count += 1
        return fish_count, shark_count

    def update_info(self, label):
        global turn_count
        fish_count, shark_count = self.count_entities()
        label.config(text=f"Tour : {turn_count}   🐟 Poissons : {fish_count}   🦈 Requins : {shark_count}")

    def draw_grid_emojis(self):
        for x in range(self.point_x):
            for y in range(self.point_y):
                entity = self.cells[x][y]
                if isinstance(entity, Shark):
                    emoji = "🦈"
                elif isinstance(entity, Fish):
                    emoji = "🐟"
                else:
                    emoji = "⬜"
                if self.cell_labels[x][y]:  
                    self.cell_labels[x][y].config(text=emoji)

    def simulate_step(self, info_label):
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
        if simulation_running:
            self.simulate_step(info_label)
            root.after(500, self.run_simulation, root, button, info_label)

    def toggle_simulation(self, root, button, info_label):
        global simulation_running
        simulation_running = not simulation_running
        if simulation_running:
            button.config(text="Pause")
            self.run_simulation(root, button, info_label)
        else:
            button.config(text="Lancer")
