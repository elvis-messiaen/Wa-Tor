# Importation des modules nécessaires
import tkinter as tk
import random
from typing import List, Any
from interface.grid import Grid
from aquatic.fish import Fish
from aquatic.shark import Shark
from interface.history_display import display_simulation_history

# Configuration de la grille
width: int = 20
height: int = 20

# Configuration de la fenêtre
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
MARGIN = 10
CONTROL_HEIGHT = 50

# Configuration des entités
FISH_REPRODUCTION_TIME = 3
SHARK_REPRODUCTION_TIME = 5
SHARK_INITIAL_ENERGY = 30
SHARK_ENERGY_FROM_FISH = 15

def calculate_cell_size(grid_width: int, grid_height: int) -> int:
    """Calcule la taille optimale des cellules en fonction de la taille de la grille.
    
    Args:
        grid_width (int): Largeur de la grille
        grid_height (int): Hauteur de la grille
        
    Returns:
        int: Taille optimale des cellules en pixels
    """
    available_width = WINDOW_WIDTH - 2 * MARGIN - 20  # 20 pour la scrollbar
    available_height = WINDOW_HEIGHT - CONTROL_HEIGHT - 2 * MARGIN - 20  # 20 pour la scrollbar
    
    cell_width = available_width // grid_width
    cell_height = available_height // grid_height
    
    return max(4, min(cell_width, cell_height))  # Minimum 4 pixels pour la visibilité

# Initialisation de la grille
grid_instance: Grid = Grid(width, height)
grid_instance.populate_grid(
    fish_reproduction_time=FISH_REPRODUCTION_TIME,
    shark_reproduction_time=SHARK_REPRODUCTION_TIME,
    shark_initial_energy=SHARK_INITIAL_ENERGY
)
cell_labels: List[List[Any]] = []

def create_control_panel(root: tk.Tk, main_frame: tk.Frame) -> tuple[tk.Label, tk.Button, tk.Button, tk.Button]:
    """Crée le panneau de contrôle avec les informations et les boutons.
    
    Args:
        root (tk.Tk): Fenêtre principale
        main_frame (tk.Frame): Cadre principal
        
    Returns:
        tuple: Label d'information et boutons de contrôle
    """
    control_frame = tk.Frame(main_frame, bg='white')
    control_frame.pack(side=tk.TOP, fill=tk.X, padx=MARGIN, pady=MARGIN)

    info_label = tk.Label(control_frame, text="", font=("Arial", 12), bg='white')
    info_label.pack(side=tk.LEFT, padx=5)

    button_frame = tk.Frame(control_frame, bg='white')
    button_frame.pack(side=tk.RIGHT, padx=5)

    step_button = tk.Button(button_frame, text="Tour suivant", 
                          command=lambda: grid_instance.simulate_step(info_label))
    step_button.pack(side=tk.LEFT, padx=5)

    toggle_button = tk.Button(button_frame, text="Lancer")
    toggle_button.config(command=lambda: grid_instance.toggle_simulation(root, toggle_button, info_label))
    toggle_button.pack(side=tk.LEFT, padx=5)

    history_button = tk.Button(button_frame, text="Historique",
                             command=display_simulation_history)
    history_button.pack(side=tk.LEFT, padx=5)

    return info_label, step_button, toggle_button, history_button

def create_grid_display(main_frame: tk.Frame) -> tuple[tk.Canvas, tk.Frame]:
    """Crée l'affichage de la grille avec scrollbars.
    
    Args:
        main_frame (tk.Frame): Cadre principal
        
    Returns:
        tuple: Canvas et cadre de la grille
    """
    grid_container = tk.Frame(main_frame, bg='white')
    grid_container.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=MARGIN, pady=MARGIN)

    canvas = tk.Canvas(grid_container, bg='white')
    scrollbar_y = tk.Scrollbar(grid_container, orient="vertical", command=canvas.yview)
    scrollbar_x = tk.Scrollbar(grid_container, orient="horizontal", command=canvas.xview)
    
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    grid_frame = tk.Frame(canvas, bg='white')
    canvas.create_window((0, 0), window=grid_frame, anchor="nw")

    return canvas, grid_frame

def create_cells(grid_frame: tk.Frame) -> List[List[Any]]:
    """Crée les cellules de la grille.
    
    Args:
        grid_frame (tk.Frame): Cadre de la grille
        
    Returns:
        List[List[Any]]: Matrice des labels des cellules
    """
    cell_size = calculate_cell_size(width, height)
    font_size = max(4, cell_size // 2)
    labels = []

    for x in range(width):
        row = []
        for y in range(height):
            lbl = tk.Label(grid_frame, text="", 
                          font=("Arial", font_size),
                          width=2, height=1,
                          relief="solid", borderwidth=1,
                          bg='white')
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
    root.resizable(False, False)
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

    # Configuration finale
    grid_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    grid_instance.set_cell_labels(cell_labels)
    grid_instance.draw_grid_emojis()
    grid_instance.update_info(info_label)

    # Lancement de la boucle principale
    root.mainloop()

if __name__ == "__main__":
    main() 
