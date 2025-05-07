import tkinter as tk
from tkinter import ttk
import random
import sys
from pathlib import Path

# Ajouter le répertoire parent au chemin Python de manière standard
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from interface.grid import Grid
from aquatic.fish import Fish
from aquatic.shark import Shark

class ToroidalVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualisation Toroidale - Poissons et Requins")
        
        # Créer une grille de test 5x5
        self.grid = Grid(5, 5)
        self.cell_size = 80
        self.padding = 20
        
        # Créer le canvas principal
        self.canvas = tk.Canvas(
            root,
            width=self.grid.point_x * self.cell_size + 2 * self.padding,
            height=self.grid.point_y * self.cell_size + 2 * self.padding,
            bg='white'
        )
        self.canvas.pack(padx=10, pady=10)
        
        # Créer les contrôles
        self.control_frame = ttk.Frame(root)
        self.control_frame.pack(pady=10)
        
        # Bouton pour tester le déplacement
        self.test_button = ttk.Button(
            self.control_frame,
            text="Tester Déplacement",
            command=self.test_movement
        )
        self.test_button.pack(side=tk.LEFT, padx=5)
        
        # Bouton pour effacer
        self.clear_button = ttk.Button(
            self.control_frame,
            text="Effacer",
            command=self.clear_canvas
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Label pour afficher les informations
        self.info_label = ttk.Label(root, text="")
        self.info_label.pack(pady=5)
        
        # Initialiser la grille avec quelques entités
        self.initialize_grid()
        
    def initialize_grid(self):
        """Initialise la grille avec quelques poissons et requins"""
        # Placer un poisson au centre
        self.fish = Fish(self.grid, 2, 2, reproduction_time=5, alive=True)
        self.grid.cells[2][2] = self.fish
        
        # Placer un requin dans un coin
        self.shark = Shark(self.grid, 0, 0, shark_energy=30, shark_reproduction_time=5)
        self.grid.cells[0][0] = self.shark
        
        # Dessiner la grille
        self.draw_grid()
    
    def draw_grid(self):
        """Dessine la grille avec les entités"""
        self.canvas.delete("all")
        
        # Dessiner les cellules
        for x in range(self.grid.point_x):
            for y in range(self.grid.point_y):
                # Calculer les coordonnées du rectangle
                x1 = x * self.cell_size + self.padding
                y1 = y * self.cell_size + self.padding
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Dessiner le rectangle
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    outline='gray',
                    width=2
                )
                
                # Dessiner l'entité si présente
                cell = self.grid.cells[x][y]
                if isinstance(cell, Fish):
                    self.canvas.create_text(
                        x1 + self.cell_size/2,
                        y1 + self.cell_size/2,
                        text="🐟",
                        font=('Arial', 20)
                    )
                elif isinstance(cell, Shark):
                    self.canvas.create_text(
                        x1 + self.cell_size/2,
                        y1 + self.cell_size/2,
                        text="🦈",
                        font=('Arial', 20)
                    )
    
    def move_entity(self, entity, new_x, new_y, description):
        """Déplace une entité et met à jour l'affichage"""
        old_x, old_y = entity.x, entity.y
        print(f"\n=== Déplacement {description} ===")
        print(f"Position initiale: ({old_x}, {old_y})")
        print(f"Position demandée: ({new_x}, {new_y})")
        
        self.grid.cells[old_x][old_y] = None
        
        # Calculer les coordonnées toroidales
        toroidal_x, toroidal_y = self.grid.get_toroidal_coords(new_x, new_y)
        print(f"Position toroidale calculée: ({toroidal_x}, {toroidal_y})")
        
        # Vérifier si le déplacement est correct
        expected_x = new_x
        expected_y = new_y
        if new_x >= self.grid.point_x:
            expected_x = 0
        elif new_x < 0:
            expected_x = 0
        if new_y >= self.grid.point_y:
            expected_y = 0
        elif new_y < 0:
            expected_y = 0
            
        if toroidal_x != expected_x or toroidal_y != expected_y:
            print(f"ERREUR: Position attendue ({expected_x}, {expected_y})")
        
        entity.x, entity.y = toroidal_x, toroidal_y
        self.grid.cells[toroidal_x][toroidal_y] = entity
        
        # Mettre à jour l'affichage
        self.draw_grid()
        self.info_label.config(
            text=f"{description}: ({old_x},{old_y}) → ({new_x},{new_y}) → ({toroidal_x},{toroidal_y})"
        )
        print(f"Position finale: ({entity.x}, {entity.y})")
        print("=== Fin du déplacement ===\n")
        
        self.root.update()
        self.root.after(1000)
    
    def test_movement(self):
        """Teste le déplacement des entités sur la grille toroidale"""
        print("\n=== DÉBUT DES TESTS DE DÉPLACEMENT ===")
        
        # Test du poisson : déplacement horizontal
        print("\n--- Test du poisson : déplacement horizontal ---")
        # Position initiale : centre (2,2)
        self.move_entity(self.fish, 2, 2, "Poisson position initiale")
        # Déplacement vers la droite
        self.move_entity(self.fish, 3, 2, "Poisson vers droite")
        # Déplacement vers la droite (dépassement)
        self.move_entity(self.fish, 5, 2, "Poisson vers droite (dépassement)")
        # Déplacement vers la gauche
        self.move_entity(self.fish, 4, 2, "Poisson vers gauche")
        # Déplacement vers la gauche (dépassement)
        self.move_entity(self.fish, -1, 2, "Poisson vers gauche (dépassement)")
        
        # Test du poisson : déplacement vertical
        print("\n--- Test du poisson : déplacement vertical ---")
        # Retour au centre
        self.move_entity(self.fish, 2, 2, "Poisson retour centre")
        # Déplacement vers le bas
        self.move_entity(self.fish, 2, 3, "Poisson vers bas")
        # Déplacement vers le bas (dépassement)
        self.move_entity(self.fish, 2, 5, "Poisson vers bas (dépassement)")
        # Déplacement vers le haut
        self.move_entity(self.fish, 2, 4, "Poisson vers haut")
        # Déplacement vers le haut (dépassement)
        self.move_entity(self.fish, 2, -1, "Poisson vers haut (dépassement)")
        
        # Test du requin : déplacement horizontal
        print("\n--- Test du requin : déplacement horizontal ---")
        # Position initiale : coin (0,0)
        self.move_entity(self.shark, 0, 0, "Requin position initiale")
        # Déplacement vers la droite
        self.move_entity(self.shark, 1, 0, "Requin vers droite")
        # Déplacement vers la droite (dépassement)
        self.move_entity(self.shark, 5, 0, "Requin vers droite (dépassement)")
        # Déplacement vers la gauche
        self.move_entity(self.shark, 4, 0, "Requin vers gauche")
        # Déplacement vers la gauche (dépassement)
        self.move_entity(self.shark, -1, 0, "Requin vers gauche (dépassement)")
        
        print("\n=== FIN DES TESTS DE DÉPLACEMENT ===\n")
    
    def clear_canvas(self):
        """Efface le canvas et réinitialise la grille"""
        self.grid.cells = [[None for _ in range(self.grid.point_y)] for _ in range(self.grid.point_x)]
        self.initialize_grid()
        self.info_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToroidalVisualizer(root)
    root.mainloop() 