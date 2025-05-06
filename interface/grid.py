import random
from typing import List, Set, Tuple, Optional, Any
from aquatic.fish import Fish
from aquatic.shark import Shark

# Variables globales pour la gestion de la grille et de la simulation
_grid_instance: Optional['Grid'] = None  # Instance unique de la grille (singleton)
turn_count: int = 0  # Compteur de tours de simulation
simulation_running: bool = False  # État de la simulation (en cours ou arrêtée)

def get_grid_instance(point_x: Optional[int] = None, point_y: Optional[int] = None) -> Optional['Grid']:
    """Retourne l'instance unique de la grille (pattern Singleton).
    
    Args:
        point_x (Optional[int]): Largeur de la grille si création d'une nouvelle instance
        point_y (Optional[int]): Hauteur de la grille si création d'une nouvelle instance
        
    Returns:
        Optional[Grid]: L'instance unique de la grille, ou None si les dimensions ne sont pas fournies
    """
    global _grid_instance
    if _grid_instance is None and point_x is not None and point_y is not None:
        _grid_instance = Grid(point_x, point_y)
    return _grid_instance

class Grid:
    """Classe représentant la grille de simulation Wa-Tor."""
    
    def __init__(self, point_x: int, point_y: int) -> None:
        """Initialise la grille avec les dimensions spécifiées.
        
        Args:
            point_x (int): Largeur de la grille
            point_y (int): Hauteur de la grille
        """
        self.point_x: int = point_x
        self.point_y: int = point_y
        self.cells: List[List[Optional[Any]]] = [[None for _ in range(point_y)] for _ in range(point_x)]
        self.cell_labels: Optional[List[List[Any]]] = None

    def set_cell_labels(self, labels: List[List[Any]]) -> None:
        """Définit les labels de la grille pour l'interface graphique.
        
        Args:
            labels (List[List[Any]]): Matrice de labels pour l'interface graphique
        """
        self.cell_labels = labels

    def populate_grid(self) -> None:
        """Remplit la grille avec des requins et des poissons selon des proportions définies."""
        total_cells: int = self.point_x * self.point_y
        num_sharks: int = int(total_cells * 0.1)  # 10% de requins
        num_fish: int = int(total_cells * 0.7)    # 70% de poissons
        total_entities: int = num_sharks + num_fish
        
        all_positions: List[Tuple[int, int]] = [(x, y) for x in range(self.point_x) for y in range(self.point_y)]
        random.shuffle(all_positions)
        
        for i in range(num_sharks):
            x, y = all_positions[i]
            shark = Shark(grid=self, x=x, y=y, shark_energy=30, shark_reproduction_time=5)
            self.cells[x][y] = shark
        
        for i in range(num_sharks, total_entities):
            x, y = all_positions[i]
            fish = Fish(grid=self, x=x, y=y, reproduction_time=5, alive=True)
            self.cells[x][y] = fish

    def empty(self, x: int, y: int) -> bool:
        """Vérifie si une cellule est vide et dans les limites de la grille.
        
        Args:
            x (int): Coordonnée x de la cellule
            y (int): Coordonnée y de la cellule
            
        Returns:
            bool: True si la cellule est vide et dans les limites, False sinon
        """
        return 0 <= x < self.point_x and 0 <= y < self.point_y and self.cells[x][y] is None

    def __str__(self) -> str:
        """Retourne une représentation textuelle de la grille avec des emojis.
        
        Returns:
            str: Représentation textuelle de la grille
        """
        grid_representation = ""
        for row in self.cells:
            row_rep = ""
            for cell in row:
                if cell is None:
                    row_rep += ". "
                elif isinstance(cell, Fish):
                    row_rep += "🐟 "
                elif isinstance(cell, Shark):
                    row_rep += "🦈 "
            grid_representation += row_rep + "\n"
        return grid_representation

    def move_entity(self, entity: Any, x: int, y: int, nx: int, ny: int, already_moved: Set[Tuple[int, int]]) -> None:
        """Déplace une entité d'une position à une autre sur la grille.
        
        Args:
            entity (Any): L'entité à déplacer
            x (int): Coordonnée x actuelle
            y (int): Coordonnée y actuelle
            nx (int): Nouvelle coordonnée x
            ny (int): Nouvelle coordonnée y
            already_moved (Set[Tuple[int, int]]): Ensemble des positions déjà déplacées
        """
        self.cells[nx][ny] = self.cells[x][y]
        self.cells[x][y] = None
        entity.x, entity.y = nx, ny
        already_moved.add((nx, ny))

    def count_entities(self) -> Tuple[int, int]:
        """Compte le nombre de poissons et de requins dans la grille.
        
        Returns:
            Tuple[int, int]: Nombre de poissons et nombre de requins
        """
        fish_count = sum(isinstance(cell, Fish) and not isinstance(cell, Shark) for row in self.cells for cell in row)
        shark_count = sum(isinstance(cell, Shark) for row in self.cells for cell in row)
        return fish_count, shark_count

    def update_info(self, label: Any) -> None:
        """Met à jour les informations affichées dans l'interface.
        
        Args:
            label (Any): Label à mettre à jour
        """
        fish_count, shark_count = self.count_entities()
        label.config(text=f"Tour : {turn_count}   🐟 Poissons : {fish_count}   🦈 Requins : {shark_count}")

    def draw_grid_emojis(self) -> None:
        """Dessine la grille avec des emojis dans l'interface graphique."""
        for x in range(self.point_x):
            for y in range(self.point_y):
                cell = self.cells[x][y]
                if cell is None:
                    self.cell_labels[x][y].config(text="🌊")
                elif isinstance(cell, Shark):
                    self.cell_labels[x][y].config(text="🦈")
                elif isinstance(cell, Fish) and not isinstance(cell, Shark):
                    self.cell_labels[x][y].config(text="🐟")

    def simulate_step(self, info_label: Any) -> None:
        """Exécute un tour de simulation.
        
        Args:
            info_label (Any): Label pour afficher les informations
        """
        global turn_count
        already_moved: Set[Tuple[int, int]] = set()
        entities = [self.cells[x][y] for x in range(self.point_x) for y in range(self.point_y) 
                   if isinstance(self.cells[x][y], Shark) or (isinstance(self.cells[x][y], Fish) and not isinstance(self.cells[x][y], Shark))]
        random.shuffle(entities)

        for entity in entities:
            if entity is None:
                continue
            x, y = entity.x, entity.y
            if (x, y) in already_moved:
                continue
            if isinstance(entity, Shark):
                entity.handle_shark(x, y, already_moved)
            elif isinstance(entity, Fish) and not isinstance(entity, Shark):
                entity.handle_fish(self, x, y, already_moved)

        turn_count += 1
        self.draw_grid_emojis()
        self.update_info(info_label)

    def run_simulation(self, root: Any, button: Any, info_label: Any) -> None:
        """Lance la simulation en boucle avec un délai de 500ms entre chaque tour.
        
        Args:
            root (Any): Fenêtre principale
            button (Any): Bouton de contrôle
            info_label (Any): Label d'information
        """
        if simulation_running:
            self.simulate_step(info_label)
            root.after(500, self.run_simulation, root, button, info_label)

    def toggle_simulation(self, root: Any, button: Any, info_label: Any) -> None:
        """Active ou désactive la simulation.
        
        Args:
            root (Any): Fenêtre principale
            button (Any): Bouton de contrôle
            info_label (Any): Label d'information
        """
        global simulation_running
        simulation_running = not simulation_running
        if simulation_running:
            button.config(text="Pause")
            self.run_simulation(root, button, info_label)
        else:
            button.config(text="Lancer")
        
    def get_empty_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Retourne les cellules vides adjacentes à une position donnée.
        
        Args:
            x (int): Coordonnée x de la position
            y (int): Coordonnée y de la position
            
        Returns:
            List[Tuple[int, int]]: Liste des coordonnées des cellules vides adjacentes
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return [(nx, ny) for dx, dy in directions
                if 0 <= (nx := x + dx) < self.point_x and 0 <= (ny := y + dy) < self.point_y
                and self.cells[nx][ny] is None]
