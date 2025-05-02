import random

class Fish:
    def __init__(self, x: int, y: int, reproduction_time: int, alive: bool = True):
        """
        Initialise un poisson avec :
        - sa position (x, y)
        - un âge initial de 0
        - un temps de reproduction
        - un état vivant ou mort
        """
        self.x = x                  # Position en X dans la grille
        self.y = y                  # Position en Y dans la grille
        self.age = 0                # Âge du poisson (en tours)
        self.reproduction_time = reproduction_time  # Temps avant reproduction
        self.alive = alive          # Le poisson est vivant

    def die(self, grid):
        """
        Fait mourir le poisson (il disparaît de la grille).
        """
        self.alive = False                    # Marque le poisson comme mort
        grid.grid[self.x][self.y] = None      # Enlève le poisson de la grille

    def step(self):
        """
        Le poisson vieillit d’un tour.
        """
        self.age += 1

    def move(self, grid):
        """
        Déplace le poisson dans une case vide autour de lui (s'il y en a).
        """
        voisins_vides = grid.get_empty_neighbors(self.x, self.y)

        if not voisins_vides:
            return  # Ne bouge pas si aucune case vide

        new_position = random.choice(voisins_vides)  # Choisit une case vide au hasard

        grid.grid[self.x][self.y] = None  # Vide sa case actuelle
        self.x, self.y = new_position  # Met à jour la position
        grid.grid[self.x][self.y] = self   # Place le poisson dans la nouvelle case

    def reproduce(self):
        """
        Reproduit un nouveau poisson si l’âge est suffisant.
        Le poisson parent garde sa position et son âge est remis à zéro.
        """
        self.age = 0  # Réinitialise l’âge du parent
        return Fish(self.x, self.y, self.reproduction_time)  # Le nouveau poisson (à déplacer ailleurs)

    def position(self):
        """
        Retourne la position actuelle du poisson.
        """
        return (self.x, self.y)

    def __str__(self):
        """
        Représentation du poisson quand on affiche la grille.
        """
        return "🐟"
