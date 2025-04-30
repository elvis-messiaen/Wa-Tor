import random
from random import randint
from aquatic.fish import Fish

class Shark(Fish):

    compteur_id_requin = 0

    def __init__(self, shark_energy: int = 15, shark_reproduction_time: int = 0, shark_starvation_time: int = 0) -> None:
        """
        Initialise une instance de requin avec des attributs spécifiques.

        Args:
            shark_energy (int): Le niveau d'énergie initial du requin. Par défaut, 15.
            shark_reproduction_time (int): Le temps nécessaire pour que le requin se reproduise. Par défaut, 0.
            shark_starvation_time (int): Le temps que le requin peut survivre sans nourriture. Par défaut, 0.
        
        Returns:
            None
        """
        super().__init__(0, 0, reproduction_time=0, alive=True)
        self.id = Shark.compteur_id_requin
        Shark.compteur_id_requin += 1
        self.shark_energy = shark_energy
        self.shark_reproduction_time = shark_reproduction_time
        self.shark_starvation_time = shark_starvation_time

    def eat(self, fish: Fish) -> None:
        """
        Permet au requin de manger un poisson, augmentant ainsi son énergie et provoquant la mort du poisson.

        Args:
            fish (Fish): L'instance du poisson que le requin va manger.
        """
        self.shark_energy += 5
        fish.die()

    def __str__(self) -> str:
        """
        Retourne une représentation sous forme de chaîne de caractères de l'objet Shark.

        Cette méthode fournit des informations sur l'identifiant du requin, son niveau d'énergie,
        son temps de reproduction et son temps de famine.

        Retourne :
            str: Une chaîne de caractères formatée contenant les détails du requin.
        """
        return f"Shark {self.id} - Energy: {self.shark_energy}, Reproduction Time: {self.shark_reproduction_time}, Starvation Time: {self.shark_starvation_time}"
    
    def move(self, grid) -> None:
        """
        Le requin bouge vers une case vide s'il ne mange pas.
        """
        empty_cells = grid.get_empty_neighbors(self.x, self.y)
        if empty_cells:
            self.x, self.y = random.choice(empty_cells)

    def step(self) -> None:
        """
        Vieillit et perd de l'énergie.
        """
        self.age += 1
        self.shark_energy -= 1

    def is_starving(self) -> bool:
        """
        Check if the shark is starving.

        Returns:
            bool: True if the shark's energy level is less than or equal to 0, indicating it is starving; False otherwise.
        """
        return self.shark_energy <= 0

    def reproduce(self) -> 'Shark':
        """
        Reproduction du requin, similaire au poisson.

        Returns:
            Shark: Une nouvelle instance de requin.
        """
        self.age = 0
        return Shark(shark_energy=15, shark_reproduction_time=self.shark_reproduction_time, shark_starvation_time=self.shark_starvation_time)
    
    def hunting(self, grid) -> None:
        """
        Cherche un poisson autour du requin pour le manger.
        """
        fish_neighbors = grid.get_fish_neighbors(self.x, self.y)
        if fish_neighbors:
            target_fish = random.choice(fish_neighbors)
            self.eat(target_fish)
            self.x, self.y = target_fish.x, target_fish.y
