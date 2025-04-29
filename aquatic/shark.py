from aquatic.fish import Fish

class Shark(Fish):

    compteur_id_requin = 0

    def __init__(self, shark_energy: int = 15, shark_reproduction_time: int = 0, shark_starvation_time: int = 0):
        super().__init__()
        self.id = Shark.compteur_id_requin
        Shark.compteur_id_requin += 1
        self.shark_energy = shark_energy
        self.shark_reproduction_time = shark_reproduction_time
        self.shark_starvation_time = shark_starvation_time

    def eat(self, fish: Fish):
        self.shark_energy += 5
        fish.die()

    def __str__(self):
        return f"Shark {self.id} - Energy: {self.shark_energy}, Reproduction Time: {self.shark_reproduction_time}, Starvation Time: {self.shark_starvation_time}"