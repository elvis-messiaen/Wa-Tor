import random
# from random import randint : not used
from aquatic.fish import Fish

class Shark(Fish):

    compteur_id_requin = 0

    def __init__(self, grid, x: int, y: int, shark_energy: int = 15, shark_reproduction_time: int = 0, shark_starvation_time: int = 0) -> None:
        super().__init__(x, y, reproduction_time=0, alive=True)
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
    # Récupère toutes les cases vides autour de la position actuelle du requin
        empty_cells = self.grid.get_empty_neighbors(self.x, self.y)
    
    # Vérifie s'il y a au moins une case vide disponible
        if empty_cells:
            # Choisit aléatoirement une des cases vides autour
            new_x, new_y = random.choice(empty_cells)
        
        # Vide l’ancienne case où se trouvait le requin dans la grille
            self.grid.grid[self.x][self.y] = None
        
        # Met à jour les coordonnées internes du requin
            self.x, self.y = new_x, new_y
        
        # Place le requin dans la nouvelle case de la grille
            self.grid.grid[self.x][self.y] = self


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
        fish_neighbors = self.grid.get_fish_neighbors(self.x, self.y)
        if fish_neighbors:
            target_fish = random.choice(fish_neighbors)
            if target_fish.alive:
                self.eat(target_fish)
                self.x, self.y = target_fish.x, target_fish.y

def __str__(self):
        return "🦈"