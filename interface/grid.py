import random

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
        self.grid = [["" for _ in range(point_y)] for _ in range(point_x)]

    def create(self):
        return self.grid
    
    def populate_grid(self):
        from aquatic.shark import Shark
        from aquatic.fish import Fish

        total_cells = self.point_x * self.point_y
        num_sharks = int(total_cells * 0.1)
        num_fish = int(total_cells * 0.7)

        positions = random.sample(range(total_cells), num_sharks + num_fish)

        for i, pos in enumerate(positions):
            row, col = divmod(pos, self.point_y)
            if i < num_sharks:
                self.grid[row][col] = Shark(grid=self, x=row, y=col, shark_energy=15, shark_reproduction_time=3, shark_starvation_time=5)
            else:
                self.grid[row][col] = Fish(x=row, y=col, reproduction_time=5, alive=True)

    def empty(self, x=None, y=None):
        if x is not None and y is not None:
            if 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0]):
                cell = self.grid[x][y]
                return "vide" if cell == "" else cell
            else:
                return "Coordonnées invalides"
        
        result = []
        for row_index, row in enumerate(self.grid):
            for col_index, cell in enumerate(row):
                status = "vide" if cell == "" else cell
                result.append(f"Cell[{row_index}][{col_index}] : {status}")
    
        return "\n".join(result)
