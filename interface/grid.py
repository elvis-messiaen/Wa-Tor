import random
from aquatic.fish import Fish
from aquatic.shark import Shark

class Grid:
    def __init__(self, point_x: int, point_y: int):
        self.point_x = point_x
        self.point_y = point_y
        self.grid = [["" for _ in range(point_y)] for _ in range(point_x)]

    def create(self):
        return self.grid
    
    def populate_grid(self):
        total_cells = self.point_x * self.point_y
        num_sharks = int(total_cells * 0.1)
        num_fish = int(total_cells * 0.7)

        positions = random.sample(range(total_cells), num_sharks + num_fish)

        for i, pos in enumerate(positions):
            row, col = divmod(pos, self.point_y)
            if i < num_sharks:
                self.grid[row][col] = Shark(shark_energy=15, shark_reproduction_time=3, shark_starvation_time=5)
            else:
                self.grid[row][col] = Fish(x=row, y=col, reproduction_time=5, Alive=True)

    def empty(self, pos_x=None, pos_y=None):
        if pos_x is not None and pos_y is not None:
            if 0 <= pos_x < len(self.grid) and 0 <= pos_y < len(self.grid[0]):
                cell = self.grid[pos_x][pos_y]
                return "vide" if cell == "" else cell
            else:
                return "Coordonnées invalides"
        result = []
        for row_index, row in enumerate(self.grid):
            for col_index, cell in enumerate(row):
                status = "vide" if cell == "" else cell
                result.append(f"Cell[{row_index}][{col_index}] : {status}")
    
        return "\n".join(result)
