import tkinter as tk  # Tkinter permet de créer une interface graphique
import random         # Pour effectuer des choix aléatoires 
from aquatic.fish import Fish  
from aquatic.shark import Shark  
from interface.grid import get_grid_instance  # Fonction pour obtenir l’instance unique de la grille

# Définition des dimensions de la grille et taille d’une cellule (en pixels)
GRID_WIDTH = 20   # Nombre de colonnes dans la grille
GRID_HEIGHT = 20  # Nombre de lignes dans la grille
CELL_SIZE = 30    # Taille d’un carré (cellule) sur l’écran (30 pixels par côté)


# On récupère ou crée l’instance unique de la grille (singleton)
grid = get_grid_instance(GRID_WIDTH, GRID_HEIGHT)  # Initialise la grille avec largeur et hauteur
grid.create()           # Crée une grille vide sous forme de liste 2D
grid.populate_grid()    # Remplit la grille avec des poissons et requins aléatoirement


# Création de la fenêtre principale avec Tkinter
root = tk.Tk()           # Initialise une nouvelle fenêtre graphique
root.title("Simulation Wa-Tor")  # Définit le nom de la fenêtre

# Création du canevas où l’on dessinera les entités (grille visuelle)
canvas = tk.Canvas(
    root,  # La fenêtre parente
    width=GRID_WIDTH * CELL_SIZE,      # Largeur du canevas = largeur grille * taille cellule
    height=GRID_HEIGHT * CELL_SIZE     # Hauteur du canevas = hauteur grille * taille cellule
)
canvas.pack()  # Affiche le canevas dans la fenêtre


# Label pour afficher le nombre de poissons et de requins en temps réel
info_label = tk.Label(root, text="Poissons: 0 | Requins: 0")  # Crée le label
info_label.pack()  # L'affiche dans la fenêtre


# Variable pour indiquer si la simulation est en cours ou en pause
running = True  # Si True, la simulation tourne ; si False, elle est en pause

def toggle_simulation():
    """Inverse l'état de la simulation : pause <-> en cours"""
    global running     # On dit que la variable globale running est utilisée ici
    running = not running  # Si running vaut True, devient False et inversement


# Bouton permettant de mettre en pause ou de reprendre la simulation
pause_button = tk.Button(
    root,  # Fenêtre parente
    text="Pause / Reprendre",  # Texte du bouton
    command=toggle_simulation  # Fonction appelée quand on clique
)
pause_button.pack()  # Affiche le bouton dans la fenêtre


def update_stats():
    """Compte le nombre de poissons et requins et met à jour l’affichage du label"""
    num_fish = 0    # Compteur de poissons
    num_sharks = 0  # Compteur de requins
    for row in grid.grid:           # Pour chaque ligne de la grille
        for cell in row:            # Pour chaque cellule de la ligne
            if isinstance(cell, Fish):   # Si c’est un poisson
                num_fish += 1
            elif isinstance(cell, Shark):  # Si c’est un requin
                num_sharks += 1
    # Met à jour le texte du label avec les nouveaux nombres
    info_label.config(text=f"Poissons: {num_fish} | Requins: {num_sharks}")


def draw_grid():
    """Dessine toutes les cellules de la grille sur le canevas"""
    canvas.delete("all")  # Supprime tous les anciens dessins

    for i in range(GRID_WIDTH):         # Parcours des lignes
        for j in range(GRID_HEIGHT):    # Parcours des colonnes
            # Coordonnées pixelisées de la cellule (rectangle)
            x1 = i * CELL_SIZE
            y1 = j * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            # Récupère l’entité présente dans la cellule
            entity = grid.grid[i][j]

            # Choix de la couleur selon le type d’entité
            if isinstance(entity, Fish):
                color = "blue"   # Poisson = bleu
            elif isinstance(entity, Shark):
                color = "red"    # Requin = rouge
            else:
                color = "white"  # Cellule vide

            # Dessine le rectangle de la cellule
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")


def simulation_step():
    """Exécute un tour complet de simulation (déplacement, reproduction, mort)"""
    if not running:
        # Si simulation en pause, ne rien faire pour l’instant
        root.after(200, simulation_step)
        return

    for i in range(GRID_WIDTH):          # Parcours de chaque cellule
        for j in range(GRID_HEIGHT):
            entity = grid.grid[i][j]
            if isinstance(entity, Shark):
                entity.step()        # Le requin vieillit et perd de l'énergie
                entity.hunting()     # Il cherche un poisson à manger
                if entity.is_starving():  # Vérifie s’il meurt de faim
                    entity.die()
                    grid.grid[i][j] = None
                elif entity.reproduce():  # Reproduction
                    new_shark = entity.reproduce()
                    grid.grid[i][j] = new_shark
            elif isinstance(entity, Fish):
                entity.step()  # Le poisson vieillit
                if entity.age >= entity.reproduction_time:
                    new_fish = entity.reproduce()
                    grid.grid[i][j] = new_fish
                entity.move(grid)  # Le poisson se déplace

    update_stats()  # Met à jour les compteurs affichés
    draw_grid()     # Redessine la grille
    root.after(500, simulation_step)  # Recommence dans 500 ms

# Lancement initial : on affiche la grille et on lance la simulation
draw_grid()
update_stats()
simulation_step()


# Démarre la boucle principale Tkinter (la fenêtre reste ouverte)
root.mainloop()

