import random
from random import randint
from aquatic.fish import Fish

class Shark(Fish):

    compteur_id_requin = 0

    def __init__(self, shark_energy: int = 15, shark_reproduction_time: int = 0, shark_starvation_time: int = 0) -> None:
        super().__init__(0, 0, reproduction_time=0, alive=True)
        self.id = Shark.compteur_id_requin
        Shark.compteur_id_requin += 1
        self.shark_energy = shark_energy
        self.shark_reproduction_time = shark_reproduction_time
        self.shark_starvation_time = shark_starvation_time

    def eat(self, fish: Fish) -> None:
        self.shark_energy += 5
        fish.die()

    def __str__(self) -> str:
        return f"Shark {self.id} - Energy: {self.shark_energy}, Reproduction Time: {self.shark_reproduction_time}, Starvation Time: {self.shark_starvation_time}"

    def move(self, grid) -> None:
        """Déplacement vers une case vide."""
        empty_cells = grid.get_empty_neighbors(self.x, self.y)
        if empty_cells:
            self.x, self.y = random.choice(empty_cells)

    def step(self) -> None:
        self.age += 1
        self.shark_energy -= 1

    def is_starving(self) -> bool:
        return self.shark_energy <= 0

    def reproduce(self):
        self.age = 0
        return Shark(
            shark_energy=15,
            shark_reproduction_time=self.shark_reproduction_time,
            shark_starvation_time=self.shark_starvation_time
        )

    def hunting(self, grid) -> None:
        """Cherche un poisson autour du requin pour le manger."""
        fish_neighbors = grid.get_fish_neighbors(self.x, self.y)
        if fish_neighbors:
            target_fish = random.choice(fish_neighbors)
            self.eat(target_fish)
            self.x, self.y = target_fish.x, target_fish.y
