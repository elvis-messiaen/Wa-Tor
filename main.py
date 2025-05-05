# Importation des modules nécessaires
import tkinter as tk
import random
from interface.grid import Grid
from aquatic.fish import Fish
from aquatic.shark import Shark

# Dimensions de la grille
width, height = 20, 20

# Création de l'instance de la grille
grid_instance = Grid(width, height)
grid_instance.populate_grid()  # Remplissage initial de la grille
cell_labels = []  # Liste pour stocker les labels de l'interface graphique

def main():
    """Fonction principale qui initialise et lance l'interface graphique."""
    grid_instance.populate_grid()  # Remplissage de la grille
    global cell_labels

    # Création de la fenêtre principale
    root = tk.Tk()
    root.title("Simulation Wa-Tor (Emoji Edition)")

    # Création du cadre pour la grille
    grid_frame = tk.Frame(root)
    grid_frame.pack()

    # Création des labels pour chaque cellule de la grille
    for x in range(width):
        row = []
        for y in range(height):
            lbl = tk.Label(grid_frame, text="⬜", font=("Arial", 16), width=2, height=1)
            lbl.grid(row=y, column=x)
            row.append(lbl)
        cell_labels.append(row)

    # Association des labels à la grille
    grid_instance.set_cell_labels(cell_labels)

    # Création du label pour les informations
    info_label = tk.Label(root, text="", font=("Arial", 12))
    info_label.pack(pady=5)

    # Création du cadre pour les boutons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)

    # Bouton pour avancer d'un tour
    step_button = tk.Button(button_frame, text="Tour suivant", command=lambda: grid_instance.simulate_step(info_label))
    step_button.pack(side=tk.LEFT, padx=5)

    # Bouton pour lancer/arrêter la simulation
    toggle_button = tk.Button(button_frame, text="Lancer")
    toggle_button.config(command=lambda: grid_instance.toggle_simulation(root, toggle_button, info_label))
    toggle_button.pack(side=tk.LEFT, padx=5)

    # Mise à jour initiale de l'affichage
    grid_instance.draw_grid_emojis()
    grid_instance.update_info(info_label)

    # Lancement de la boucle principale
    root.mainloop()

if __name__ == "__main__":
    main() 
