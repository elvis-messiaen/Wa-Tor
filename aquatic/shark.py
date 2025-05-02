import random
from aquatic.fish import Fish

class Shark(Fish):
    compteur_id_requin = 0

    def __init__(self, grid, x, y, shark_energy=15, shark_reproduction_time=0, shark_starvation_time=0, alive=True):
        super().__init__(x, y, reproduction_time=shark_reproduction_time, alive=alive)
        self.grid = grid
        self.age = 0
        self.id = Shark.compteur_id_requin
        Shark.compteur_id_requin += 1
        self.shark_energy = shark_energy
        self.shark_reproduction_time = shark_reproduction_time
        self.shark_starvation_time = shark_starvation_time

    def eat(self, fish: Fish) -> None:
        if fish.alive:
            self.shark_energy += 5
            fish.die()

    def move(self) -> None:
        empty_cells = self.grid.get_empty_neighbors(self.x, self.y)  # Utilisation de la méthode de la classe Grid
        if empty_cells:
            self.x, self.y = random.choice(empty_cells)

    def step(self) -> None:
        self.age += 1
        self.shark_energy -= 1

    def is_starving(self) -> bool:
        return self.shark_energy <= 0

    def reproduce(self) -> 'Shark':
        if self.age >= self.shark_reproduction_time:
            self.age = 0
            return Shark(self.grid, self.x, self.y, shark_energy=15, shark_reproduction_time=self.shark_reproduction_time, shark_starvation_time=self.shark_starvation_time)

    def hunting(self) -> None:
        fish_neighbors = self.get_fish_neighbors(self.x, self.y)  # Appel de la méthode get_fish_neighbors
        if fish_neighbors:
            target_fish = random.choice(fish_neighbors)
            if target_fish.alive:
                self.eat(target_fish)
                self.x, self.y = target_fish.x, target_fish.y

    def get_fish_neighbors(self, x, y):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return [(nx, ny) for dx, dy in directions
                if 0 <= (nx := x + dx) < self.grid.point_x and 0 <= (ny := y + dy) < self.grid.point_y
                and isinstance(self.grid.cells[nx][ny], Fish)]
    
    def handle_shark(self, x, y, already_moved):
        self.step()  # Effectue une étape pour le requin
        fish_neighbors = self.get_fish_neighbors(x, y)  # Appel correct de get_fish_neighbors
        if fish_neighbors:
            nx, ny = random.choice(fish_neighbors)  # Choix d'un poisson à manger
            self.eat(self.grid.cells[nx][ny])  # Mange le poisson
            self.move_entity(x, y, nx, ny, already_moved)  # Déplace le requin
        else:
            empty = self.get_empty_neighbors(self.grid, x, y)  # Recherche de cellules vides
            if empty:
                nx, ny = random.choice(empty)
                self.move_entity(x, y, nx, ny, already_moved)

        if self.shark_energy <= 0:
            self.grid.cells[self.x][self.y] = None  # Le requin meurt s'il n'a plus d'énergie
        elif self.age >= self.shark_reproduction_time:
            self.reproduce_entity(x, y)  # Reproduction du requin
