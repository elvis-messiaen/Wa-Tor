import tkinter as tk
import random
from interface.grid import Grid
from aquatic.fish import Fish
from aquatic.shark import Shark

width, height = 20, 20
grid_instance = Grid(width, height)
grid_instance.create()
cell_labels = []

def initialize_entities():
    """Initialise la grille en utilisant la méthode populate_grid()."""
    return grid_instance.populate_grid()

def main(): # Move to grid.py
    initialize_entities()
    global cell_labels

    root = tk.Tk()
    root.title("Simulation Wa-Tor (Emoji Edition)")

    grid_frame = tk.Frame(root)
    grid_frame.pack()

    for x in range(width):
        row = []
        for y in range(height):
            lbl = tk.Label(grid_frame, text="⬜", font=("Arial", 16), width=2, height=1)
            lbl.grid(row=y, column=x)
            row.append(lbl)
        cell_labels.append(row)

    info_label = tk.Label(root, text="", font=("Arial", 12))
    info_label.pack(pady=5)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)

    step_button = tk.Button(button_frame, text="Tour suivant", command=lambda: grid_instance.simulate_step(info_label)
)
    step_button.pack(side=tk.LEFT, padx=5)

    toggle_button = tk.Button(button_frame, text="Lancer")
    toggle_button.config(command=lambda: grid_instance.toggle_simulation(root, toggle_button, info_label))
    toggle_button.pack(side=tk.LEFT, padx=5)

    grid_instance.draw_grid_emojis()
    grid_instance.update_info(info_label)

    root.mainloop()

if __name__ == "__main__": # Entry point of the program
    main() 
