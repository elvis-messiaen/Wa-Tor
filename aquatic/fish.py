# Choisir aléatoirement une case vide
#from random import randint
#from interface.grid import grid 

class Fish:
    def __init__(self, x : int , y: int , reproduction_time, alive : bool,):
        """
        Initialise un poisson avec :
        - sa position (x, y)
        - un compteur d'âge (initialisé à 0)
        - un temps de reproduction requis
        """
        self.x = x  # Coordonnée horizontale dans la grille
        self.y = y  # Coordonnée verticale dans la grille
        self.age = 0  # Nombre de chronons écoulés depuis la naissance
        self.reproduction_time = reproduction_time  # Chronons nécessaires avant reproduction
        self.alive = alive
        
    def die(self):
        """
        Marque le poisson comme mort. 
        Vous pouvez définir un drapeau ou le retirer de la grille ailleurs.
        """
        self.alive = False  # Ajoutez un attribut self.alive dans __init__
        grid[self.x][self.y] = None  # On l’enlève de la grille
        
    def step(self):
        """
        - Le poisson vieillit d'un tour(chronon).
        """
        self.age += 1
    

    def reproduce(self):
        """
        Crée un nouveau poisson (reproduction).
        Le parent garde sa position mais son âge est remis à zéro.
        Le nouveau poisson sera placé ailleurs (à définir à l’extérieur).
        """
        self.age = 0  # Réinitialise l'âge du parent après reproduction
        return Fish(self.x, self.y, self.reproduction_time)  # Bébé poisson à même position (à ajuster ensuite)
    
    def move(self, grid):
        """
        Déplace le poisson vers une case vide disponible autour de lui.
        - empty_cells est une liste de positions (x, y)
        - Si aucune case vide, il ne bouge pas
        """
        empty_cells = grid.empty(self.x, self.y)  # Récupère les cases vides autour du poisson
        if empty_cells:
            self.x, self.y = random.choice(empty_cells)  # Choisit une case vide aléatoire parmi celles disponibles
    
    def choose_direction(self):
        direction = randint(0, 1)  # Choisit aléatoirement 0 (horizontal) ou 1 (vertical)
        sign = 2 * randint(0, 1) - 1  # Génère -1 ou +1 (c’est le sens du déplacement)
        if direction == 0:
            return (sign, 0)  # Déplacement horizontal : à gauche ou à droite
        else:
            return (0, sign)  # Déplacement vertical : en haut ou en bas


    def position(self):
        """
        Retourne la position actuelle du poisson (utile pour la grille).
        """
        return (self.x, self.y)
    
    def __str__(self):
        """
        Représentation visuelle du poisson (utilisée lors de l'affichage de la grille).
        """
        return "🐟"
    
    