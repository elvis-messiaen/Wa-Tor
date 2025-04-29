import random
from aquatic import Fish,Shark
class Grid:
    def __init__(self, point_x: int, point_y: int):
        self.point_x = point_x
        self.point_y = point_y
        self.grid = [["" for _ in range(20)] for _ in range(20)]

    def creat(self):
        return self.grid
    
    def populate_grid(self):
        import random
        total_cells = self.point_x * self.point_y
        num_sharks = int(total_cells * 0.1)
        num_fish = int(total_cells * 0.7)
        positions = random.sample(range(total_cells), num_sharks + num_fish)
        for i, pos in enumerate(positions):
            row, col = divmod(pos, self.point_y)
            if i < num_sharks:
                self.grid[row][col] = Shark()
            else:
                self.grid[row][col] = Fish()

    def empty(self):
        for row_index, row in enumerate(self.grid):
            for col_index, cell in enumerate(row):
                print(f"Cell[{row_index}][{col_index}] : '{cell}'")


grid_instance = Grid(20, 20)
grid_instance.creat()
grid_instance.populate_grid()
grid_instance.empty()
