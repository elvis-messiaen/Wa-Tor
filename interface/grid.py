import random
import os
import csv
from typing import List, Set, Tuple, Optional, Any
from aquatic.fish import Fish
from aquatic.shark import Shark
from history import SimulationHistory
from datetime import datetime

# Variables globales pour la gestion de la grille et de la simulation
_grid_instance: Optional['Grid'] = None  # Instance unique de la grille (pattern Singleton)
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
    """Classe représentant la grille de simulation Wa-Tor.
    Cette classe gère :
    - La structure de la grille
    - Le placement des entités
    - Les déplacements
    - La simulation
    - L'affichage
    - La sauvegarde de l'historique
    """
    
    def __init__(self, point_x: int, point_y: int) -> None:
        """Initialise la grille avec les dimensions spécifiées.
        
        Args:
            point_x (int): Largeur de la grille
            point_y (int): Hauteur de la grille
        """
        self.point_x: int = point_x  # Largeur de la grille
        self.point_y: int = point_y  # Hauteur de la grille
        # Initialisation de la grille avec des cellules vides (None)
        self.cells: List[List[Optional[Any]]] = [[None for _ in range(point_y)] for _ in range(point_x)]
        self.cell_labels: Optional[List[List[Any]]] = None  # Labels pour l'interface graphique
        self.history: SimulationHistory = SimulationHistory()  # Instance de l'historique

    def set_cell_labels(self, labels: List[List[Any]]) -> None:
        """Définit les labels de la grille pour l'interface graphique.
        
        Args:
            labels (List[List[Any]]): Matrice de labels pour l'interface graphique
        """
        self.cell_labels = labels

    def populate_grid(self, fish_reproduction_time: int = 5, shark_reproduction_time: int = 5,
                     shark_initial_energy: int = 30) -> None:
        """Remplit la grille avec des requins et des poissons selon des proportions définies.
        
        Args:
            fish_reproduction_time (int): Temps nécessaire pour la reproduction des poissons
            shark_reproduction_time (int): Temps nécessaire pour la reproduction des requins
            shark_initial_energy (int): Énergie initiale des requins
        """
        # Calcul du nombre total de cellules et des proportions
        total_cells: int = self.point_x * self.point_y
        num_sharks: int = int(total_cells * 0.1)  # 10% de requins
        num_fish: int = int(total_cells * 0.7)    # 70% de poissons
        total_entities: int = num_sharks + num_fish
        
        # Création et mélange de toutes les positions possibles
        all_positions: List[Tuple[int, int]] = [(x, y) for x in range(self.point_x) for y in range(self.point_y)]
        random.shuffle(all_positions)
        
        # Placement des requins
        for i in range(num_sharks):
            x, y = all_positions[i]
            shark = Shark(grid=self, x=x, y=y, shark_energy=shark_initial_energy, 
                         shark_reproduction_time=shark_reproduction_time)
            self.cells[x][y] = shark
        
        # Placement des poissons
        for i in range(num_sharks, total_entities):
            x, y = all_positions[i]
            fish = Fish(grid=self, x=x, y=y, reproduction_time=fish_reproduction_time, alive=True)
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
                    row_rep += ". "  # Cellule vide
                elif isinstance(cell, Fish):
                    row_rep += "🐟 "  # Poisson
                elif isinstance(cell, Shark):
                    row_rep += "🦈 "  # Requin
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
        # Vérification de la validité des coordonnées de départ
        if not (0 <= x < self.point_x and 0 <= y < self.point_y):
            return
            
        # Convertir les nouvelles coordonnées en coordonnées toroidales
        toroidal_nx, toroidal_ny = self.get_toroidal_coords(nx, ny)
        # Déplacer l'entité
        self.cells[toroidal_nx][toroidal_ny] = self.cells[x][y]
        self.cells[x][y] = None
        # Mettre à jour les coordonnées de l'entité
        entity.x, entity.y = toroidal_nx, toroidal_ny
        # Marquer la nouvelle position comme déjà déplacée
        already_moved.add((toroidal_nx, toroidal_ny))

    def count_entities(self) -> Tuple[int, int]:
        """Compte le nombre de poissons et de requins dans la grille.
        
        Returns:
            Tuple[int, int]: Nombre de poissons et nombre de requins
        """
        # Compte les poissons (en excluant les requins qui héritent de Fish)
        fish_count = sum(isinstance(cell, Fish) and not isinstance(cell, Shark) for row in self.cells for cell in row)
        # Compte les requins
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
        """Dessine la grille avec des emojis colorés dans l'interface graphique."""
        for x in range(self.point_x):
            for y in range(self.point_y):
                cell = self.cells[x][y]
                if cell is None:
                    # Eau (bleu océan)
                    self.cell_labels[x][y].config(text="🌊", fg="#1E90FF", bg="white")
                elif isinstance(cell, Shark):
                    # Requin (rouge-orange)
                    self.cell_labels[x][y].config(text="🦈", fg="#FF4500", bg="white")
                elif isinstance(cell, Fish) and not isinstance(cell, Shark):
                    # Poisson (vert)
                    self.cell_labels[x][y].config(text="🐟", fg="#32CD32", bg="white")

    def simulate_step(self, info_label: Any) -> bool:
        """Exécute un tour de simulation.
        
        Args:
            info_label (Any): Label pour afficher les informations
            
        Returns:
            bool: True si la simulation continue, False si elle est terminée
        """
        global turn_count
        already_moved: Set[Tuple[int, int]] = set()
        
        # Mélanger toutes les entités pour un ordre aléatoire
        entities = [self.cells[x][y] for x in range(self.point_x) for y in range(self.point_y) 
                   if isinstance(self.cells[x][y], Shark) or (isinstance(self.cells[x][y], Fish) and not isinstance(self.cells[x][y], Shark))]
        random.shuffle(entities)

        # Traiter chaque entité
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

        # Mise à jour du compteur de tours et de l'affichage
        turn_count += 1
        self.draw_grid_emojis()
        self.update_info(info_label)
        
        # Sauvegarde de l'historique
        history_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'simulation_history.csv')
        try:
            # Vérifier si le fichier existe déjà
            file_exists = os.path.exists(history_file)
            
            with open(history_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Écrire l'en-tête si le fichier est nouveau
                if not file_exists:
                    writer.writerow(['date', 'chronons', 'fish_count', 'shark_count'])
                # Écrire les données
                fish_count, shark_count = self.count_entities()
                writer.writerow([
                    datetime.now().isoformat(),
                    turn_count,
                    fish_count,
                    shark_count
                ])
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de l'historique : {e}")
        
        # Vérifier si la simulation est terminée (plus de poissons ET plus de requins)
        fish_count, shark_count = self.count_entities()
        if fish_count == 0 and shark_count == 0:
            global simulation_running
            simulation_running = False
            
            # Réinitialiser la grille pour une nouvelle partie
            self.cells = [[None for _ in range(self.point_y)] for _ in range(self.point_x)]
            self.populate_grid()
            self.draw_grid_emojis()
            turn_count = 0  # Réinitialiser le compteur
            return False
        return True

    def run_simulation(self, root: Any, button: Any, info_label: Any) -> None:
        """Lance la simulation en boucle avec un délai de 500ms entre chaque tour.
        
        Args:
            root (Any): Fenêtre principale
            button (Any): Bouton de contrôle
            info_label (Any): Label d'information
        """
        if simulation_running:
            if not self.simulate_step(info_label):
                # Si la simulation est terminée
                button.config(text="Lancer")
                return
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
        button.config(text="Arrêter" if simulation_running else "Lancer")
        if simulation_running:
            self.run_simulation(root, button, info_label)

    def get_toroidal_coords(self, x: int, y: int) -> Tuple[int, int]:
        """Convertit des coordonnées en coordonnées toroidales (grille circulaire).
        
        Args:
            x (int): Coordonnée x
            y (int): Coordonnée y
            
        Returns:
            Tuple[int, int]: Coordonnées toroidales
        """
        # Gestion des coordonnées toroidales (la grille est un tore)
        return x % self.point_x, y % self.point_y

    def get_empty_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Trouve les cellules vides adjacentes à une position donnée.
        
        Args:
            x (int): Coordonnée x
            y (int): Coordonnée y
            
        Returns:
            List[Tuple[int, int]]: Liste des coordonnées des cellules vides adjacentes
        """
        # Directions possibles : haut, bas, gauche, droite
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        # Vérifie chaque direction
        for dx, dy in directions:
            nx, ny = self.get_toroidal_coords(x + dx, y + dy)
            if self.empty(nx, ny):
                neighbors.append((nx, ny))
        return neighbors

    def reset_simulation(self) -> None:
        """Réinitialise la simulation en vidant la grille et en réinitialisant les compteurs."""
        global turn_count, simulation_running
        turn_count = 0
        simulation_running = False
        self.cells = [[None for _ in range(self.point_y)] for _ in range(self.point_x)]
        self.populate_grid()
        self.draw_grid_emojis()
