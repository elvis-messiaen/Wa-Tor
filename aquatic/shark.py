import random
from aquatic.fish import Fish

class Shark(Fish):
    """Classe représentant un requin dans la simulation Wa-Tor.
    Hérite de la classe Fish."""
    
    compteur_id_requin = 0  # Compteur statique pour les identifiants uniques des requins

    def __init__(self, grid, x, y, shark_energy=15, shark_reproduction_time=0, alive=True):
        """Initialise un requin avec ses caractéristiques spécifiques."""
        super().__init__(grid, x, y, reproduction_time=shark_reproduction_time, alive=alive)
        self.grid = grid  # Référence à la grille
        self.age = 0  # Âge du requin
        self.id = Shark.compteur_id_requin  # Identifiant unique
        Shark.compteur_id_requin += 1  # Incrémentation du compteur
        self.shark_energy = shark_energy  # Énergie du requin
        self.shark_reproduction_time = shark_reproduction_time  # Temps nécessaire pour la reproduction
    
    def eat(self, fish: Fish) -> None:
        """Fait manger un poisson au requin, augmentant son énergie."""
        self.shark_energy += 2  # Gain d'énergie
        fish.die()  # Le poisson meurt
        fish.remove_fish(self.grid)  # Suppression du poisson de la grille

    def step(self) -> None:
        """Fait vieillir le requin et diminue son énergie."""
        self.age += 1
        self.shark_energy -= 1  # Perte d'énergie à chaque tour

    def get_fish_neighbors(self, x, y):
        """Retourne les poissons adjacents à la position du requin."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Haut, bas, gauche, droite
        return [(nx, ny) for dx, dy in directions
                if 0 <= (nx := x + dx) < self.grid.point_x and 0 <= (ny := y + dy) < self.grid.point_y
                and isinstance(self.grid.cells[nx][ny], Fish) and not isinstance(self.grid.cells[nx][ny], Shark)]
    
    def handle_shark(self, x, y, already_moved):
        """Gère le comportement du requin pendant un tour de simulation."""
        # Recherche de poissons à manger
        fish_neighbors = self.get_fish_neighbors(x, y)
        if fish_neighbors:
            # Manger un poisson et se déplacer vers sa position
            nx, ny = random.choice(fish_neighbors)
            self.eat(self.grid.cells[nx][ny])
            self.grid.move_entity(self, x, y, nx, ny, already_moved)
        else:
            # Si pas de poisson, perdre de l'énergie et chercher une case vide
            self.shark_energy -= 500
            empty = self.grid.get_empty_neighbors(x, y)
            if empty:
                nx, ny = random.choice(empty)
                self.grid.move_entity(self, x, y, nx, ny, already_moved)
        
        # Vieillissement
        self.step()
        
        # Vérification de la mort ou de la reproduction
        if self.shark_energy <= 0:
            self.die()
            self.grid.cells[self.x][self.y] = None
        elif self.age % self.shark_reproduction_time == 0 and self.age != 0:
            self.reproduce_entity(self.grid, x, y)

    def reproduce_entity(self, grid, x, y):
        """Crée un nouveau requin dans une case vide adjacente."""
        empty = self.get_empty_neighbors(grid, x, y)
        if empty:
            nx, ny = random.choice(empty)
            baby = Shark(grid, nx, ny, shark_energy=15,
                        shark_reproduction_time=self.shark_reproduction_time)
            grid.cells[nx][ny] = baby
            print(f"Reproduction: {baby} créé à ({nx}, {ny})")
