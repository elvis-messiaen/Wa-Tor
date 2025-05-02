import random
from aquatic.fish import Fish

class Shark(Fish):
    compteur_id_requin = 0

    def __init__(self, x, y, shark_energy = 15, shark_reproduction_time = 5, shark_starvation_time = 7, grid=None, alive=True):
        # Appel du constructeur de la classe parente (Fish)
        super().__init__(x, y, reproduction_time=shark_reproduction_time, alive=alive)
        
        self.shark_energy = shark_energy
        self.shark_reproduction_time = shark_reproduction_time
        self.shark_starvation_time = shark_starvation_time
        self.grid = grid  # Lier l'instance de la grille à cet objet requin
        self.has_moved = False

    def eat(self, fish):
        """
        Mange un poisson, augmentant l'énergie du requin.
        """
        fish.die()  # Supprime le poisson de la grille en appelant die()
        self.shark_energy += 5  # Augmentation de l'énergie du requin après avoir mangé

    def move(self) -> None:
        # Récupère toutes les cases vides autour de la position actuelle du requin
        empty_neighbors = self.grid.get_empty_neighbors(self.x, self.y)
        
        # Vérifie s'il y a au moins une case vide disponible
        if empty_neighbors:
            # Choisit aléatoirement une des cases vides autour
            new_x, new_y = random.choice(empty_neighbors)
            
            # Vide l’ancienne case où se trouvait le requin dans la grille
            self.grid.grid[self.x][self.y] = None
            
            # Met à jour les coordonnées internes du requin
            self.x, self.y = new_x, new_y
            
            # Place le requin dans la nouvelle case de la grille
            self.grid.grid[self.x][self.y] = self

    def step(self):
        """Le requin fait un tour. Il perd de l'énergie et vieillit."""
        self.age += 1
        self.shark_energy -= 1

        # Si le requin est affamé (énergie <= 0), il meurt
        if self.shark_energy <= 0:
            self.die()

    def die(self):
        """Le requin meurt s'il n'a plus d'énergie."""
        self.alive = False
        self.grid.cells[self.x][self.y] = None  # Efface le requin de la grille

    def is_starving(self):
        """Retourne True si le requin est affamé (énergie <= 0)."""
        return self.shark_energy <= 0

    def reproduce(self):
        """Le requin se reproduit et crée un nouveau requin à la même position."""
        return Shark(self.x, self.y, shark_energy=15, shark_reproduction_time=self.shark_reproduction_time, shark_starvation_time=self.shark_starvation_time, grid=self.grid)

    def hunting(self):
        """Le requin chasse les poissons voisins."""
        fish_neighbors = self.get_fish_neighbors()
        if fish_neighbors:
            target_fish = random.choice(fish_neighbors)
            if target_fish.alive:
                self.eat(target_fish)
                self.x, self.y = target_fish.x, target_fish.y

    def get_empty_neighbors(self):
        """Retourne les cases vides autour de la position actuelle du requin."""
        if self.grid is None:
            return []
        return [(nx, ny) for nx, ny in self.grid.get_neighbors(self.x, self.y) if self.grid.cells[nx][ny] == ""]

    def get_fish_neighbors(self):
        """Retourne les poissons voisins du requin."""
        if self.grid is None:
            return []
        return [(nx, ny) for nx, ny in self.grid.get_neighbors(self.x, self.y)
                if isinstance(self.grid.cells[nx][ny], Fish) and not isinstance(self.grid.cells[nx][ny], Shark)]
