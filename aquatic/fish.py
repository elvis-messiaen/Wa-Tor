import random

class Fish:
    def __init__(self, x, y, reproduction_time, alive=True):
        self.x = x
        self.y = y
        self.reproduction_time = reproduction_time
        self.alive = alive
        self.age = 0
        
    def die(self):
        self.alive = False
        
    def step(self):
        self.age += 1
    
    def reproduce(self):
        self.age = 0
        return Fish(self.x, self.y, self.reproduction_time)
    
    def move(self, grid):
        empty_cells = grid.empty(self.x, self.y)
        if empty_cells:
            self.x, self.y = random.choice(empty_cells)
            
    def get_empty_neighbors(self, grid, x, y):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return [(nx, ny) for dx, dy in directions
                if 0 <= (nx := x + dx) < grid.point_x and 0 <= (ny := y + dy) < grid.point_y
                and grid.cells[nx][ny] is None]
    
    def position(self):
        return (self.x, self.y)
    
    def handle_fish(self, grid, x, y, already_moved):
        self.step()
        empty = self.get_empty_neighbors(grid, x, y)
        if empty:
            nx, ny = random.choice(empty)
            self.move_entity(grid, x, y, nx, ny, already_moved)

        if self.age >= self.reproduction_time:
            self.reproduce_entity(grid, x, y)
    
    def move_entity(self, grid, x, y, nx, ny, already_moved):
        """Déplace l'entité sur la grille."""
        grid.cells[nx][ny] = grid.cells[x][y]
        grid.cells[x][y] = None
        already_moved.add((nx, ny))

    def reproduce_entity(self, grid, x, y):
        empty = self.get_empty_neighbors(grid, x, y)
        if empty:
            nx, ny = random.choice(empty)
            grid.cells[nx][ny] = Fish(nx, ny, self.reproduction_time)
