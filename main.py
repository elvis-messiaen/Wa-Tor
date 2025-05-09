# Importation des modules nécessaires
import tkinter as tk 
import random  
from typing import List, Any  # Typage statique
from interface.grid import Grid  # Classe de gestion de la grille
from aquatic.fish import Fish 
from aquatic.shark import Shark  
from interface.history_display import display_simulation_history  # Affichage de l'historique

# Configuration de la grille
width: int = 20  # Largeur de la grille en nombre de cellules
height: int = 20  # Hauteur de la grille en nombre de cellules

# Configuration de la fenêtre
WINDOW_WIDTH = 800  # Largeur de la fenêtre en pixels
WINDOW_HEIGHT = 600  # Hauteur de la fenêtre en pixels
MARGIN = 10  # Marge autour des éléments en pixels
CONTROL_HEIGHT = 50  # Hauteur du panneau de contrôle en pixels

# Configuration des entités
FISH_REPRODUCTION_TIME = 3  # Nombre de tours avant reproduction d'un poisson
SHARK_REPRODUCTION_TIME = 5  # Nombre de tours avant reproduction d'un requin
SHARK_INITIAL_ENERGY = 30  # Énergie initiale des requins
SHARK_ENERGY_FROM_FISH = 15  # Énergie gagnée par un requin en mangeant un poisson

def calculate_cell_size(grid_width: int, grid_height: int) -> int:
    """Calcule la taille optimale des cellules en fonction de la taille de la grille.
    
    Args:
        grid_width (int): Largeur de la grille en nombre de cellules
        grid_height (int): Hauteur de la grille en nombre de cellules
        
    Returns:
        int: Taille optimale des cellules en pixels
    """
    # Calcul de l'espace disponible en tenant compte des marges et des scrollbars
    available_width = WINDOW_WIDTH - 2 * MARGIN - 20  # 20 pour la scrollbar
    available_height = WINDOW_HEIGHT - CONTROL_HEIGHT - 2 * MARGIN - 20  # 20 pour la scrollbar
    
    # Calcul de la taille des cellules en fonction de l'espace disponible
    cell_width = available_width // grid_width
    cell_height = available_height // grid_height
    
    # Retourne la plus petite des deux dimensions, avec un minimum de 4 pixels
    return max(4, min(cell_width, cell_height))

# Initialisation de la grille avec les paramètres définis
grid_instance: Grid = Grid(width, height)
grid_instance.populate_grid(
    fish_reproduction_time=FISH_REPRODUCTION_TIME,
    shark_reproduction_time=SHARK_REPRODUCTION_TIME,
    shark_initial_energy=SHARK_INITIAL_ENERGY
)
cell_labels: List[List[Any]] = []  # Liste des labels pour l'affichage des cellules

def create_control_panel(root: tk.Tk, main_frame: tk.Frame) -> tuple[tk.Label, tk.Button, tk.Button, tk.Button]:
    """Crée le panneau de contrôle avec les informations et les boutons.
    
    Args:
        root (tk.Tk): Fenêtre principale
        main_frame (tk.Frame): Cadre principal
        
    Returns:
        tuple: Contient les widgets créés (label d'info, boutons)
    """
    # Création du cadre de contrôle
    control_frame = tk.Frame(main_frame, bg='white')
    control_frame.pack(side=tk.TOP, fill=tk.X, padx=MARGIN, pady=MARGIN)

    # Label pour afficher les informations (nombre de poissons, requins, etc.)
    info_label = tk.Label(control_frame, text="", font=("Arial", 12))
    info_label.pack(side=tk.LEFT, padx=5)

    # Cadre pour les boutons
    button_frame = tk.Frame(control_frame, bg='white')
    button_frame.pack(side=tk.RIGHT, padx=5)

    # Bouton pour avancer d'un tour
    step_button = tk.Button(button_frame, text="Tour suivant", 
                          command=lambda: grid_instance.simulate_step(info_label))
    step_button.pack(side=tk.LEFT, padx=5)

    # Bouton pour lancer/arrêter la simulation
    toggle_button = tk.Button(button_frame, text="Lancer")
    toggle_button.config(command=lambda: grid_instance.toggle_simulation(root, toggle_button, info_label))
    toggle_button.pack(side=tk.LEFT, padx=5)

    # Bouton pour afficher l'historique
    history_button = tk.Button(button_frame, text="Historique",
                             command=display_simulation_history)
    history_button.pack(side=tk.LEFT, padx=5)

    return info_label, step_button, toggle_button, history_button

def create_grid_display(main_frame: tk.Frame) -> tuple[tk.Canvas, tk.Frame]:
    """Crée l'affichage de la grille avec scrollbars et ajuste la taille correctement.
    
    Args:
        main_frame (tk.Frame): Cadre principal
        
    Returns:
        tuple: Canvas et cadre de la grille
    """
    # Création du conteneur de la grille
    grid_container = tk.Frame(main_frame, bg='white')
    grid_container.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=MARGIN, pady=MARGIN)

    # Création du canvas avec scrollbars
    canvas = tk.Canvas(grid_container, bg='white', width=WINDOW_WIDTH, height=WINDOW_HEIGHT - CONTROL_HEIGHT)
    scrollbar_y = tk.Scrollbar(grid_container, orient="vertical", command=canvas.yview)
    scrollbar_x = tk.Scrollbar(grid_container, orient="horizontal", command=canvas.xview)
    
    # Configuration des scrollbars
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    
    # Placement des scrollbars et du canvas
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    # Création du cadre de la grille avec une taille fixe
    grid_frame = tk.Frame(canvas, bg='white', width=WINDOW_WIDTH - 2 * MARGIN, height=WINDOW_HEIGHT - CONTROL_HEIGHT - 2 * MARGIN)
    canvas.create_window((0, 0), window=grid_frame, anchor="nw")

    return canvas, grid_frame

def create_cells(grid_frame: tk.Frame) -> List[List[Any]]:
    """Crée les cellules de la grille avec une taille ajustée.
    
    Args:
        grid_frame (tk.Frame): Cadre de la grille
        
    Returns:
        List[List[Any]]: Matrice des labels des cellules
    """
    # Calcul de la taille des cellules et de la police
    cell_size = calculate_cell_size(width, height)
    font_size = max(4, cell_size // 2)  # Taille de police proportionnelle à la taille de la cellule
    labels = []

    # Création des cellules
    for x in range(width):
        row = []
        for y in range(height):
            # Création d'un label pour chaque cellule
            lbl = tk.Label(grid_frame, text="", font=("Arial", font_size),
                          width=2, height=1, relief="solid", borderwidth=1, bg='white')
            lbl.grid(row=y, column=x, padx=0, pady=0)
            row.append(lbl)
        labels.append(row)

    return labels

def main() -> None:
    """Fonction principale qui initialise et lance l'interface graphique."""
    global cell_labels

    # Création de la fenêtre principale
    root = tk.Tk()
    root.title("Simulation Wa-Tor (Emoji Edition)")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.resizable(False, False)  # Fenêtre non redimensionnable
    root.configure(bg='white')

    # Création du cadre principal
    main_frame = tk.Frame(root, bg='white')
    main_frame.pack(expand=True, fill=tk.BOTH)

    # Création du panneau de contrôle
    info_label, _, _, _ = create_control_panel(root, main_frame)

    # Création de l'affichage de la grille
    canvas, grid_frame = create_grid_display(main_frame)

    # Création des cellules
    cell_labels = create_cells(grid_frame)

    # Ajustement de la taille du canvas et du cadre de la grille
    grid_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

    # Association des cellules à la grille et initialisation de l'affichage
    grid_instance.set_cell_labels(cell_labels)
    grid_instance.draw_grid_emojis()
    grid_instance.update_info(info_label)

    # Lancement de la boucle principale de l'interface
    root.mainloop()

if __name__ == "__main__":
    main()
