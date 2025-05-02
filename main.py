import tkinter as tk
import random
from interface.grid import Grid
from aquatic.fish import Fish
from aquatic.shark import Shark

width, height = 20, 20
grid_instance = Grid(width, height)
grid_instance.create()
simulation_running = False
turn_count = 0
cell_labels = []

def initialize_entities():
    """Initialise la grille en utilisant la méthode populate_grid()."""
    return grid_instance.populate_grid()

def count_entities():  # Move to grid.py
    fish_count = 0
    shark_count = 0
    for row in grid_instance.cells:
        for cell in row:
            if isinstance(cell, Shark):
                shark_count += 1
            elif isinstance(cell, Fish):
                fish_count += 1
    return fish_count, shark_count

def update_info(label):  # Move to grid.py
    fish_count, shark_count = count_entities()
    label.config(text=f"Tour : {turn_count}   🐟 Poissons : {fish_count}   🦈 Requins : {shark_count}")

def draw_grid_emojis():  # Move to grid.py
    for x in range(width):
        for y in range(height):
            entity = grid_instance.cells[x][y]
            if isinstance(entity, Shark):
                emoji = "🦈"
            elif isinstance(entity, Fish):
                emoji = "🐟"
            else:
                emoji = "⬜"
            cell_labels[x][y].config(text=emoji)

def simulate_step(info_label):  # Move to grid.py
    global turn_count
    already_moved = set()

    entities = [grid_instance.cells[x][y] for x in range(width) for y in range(height) if isinstance(grid_instance.cells[x][y], (Shark, Fish))]
    random.shuffle(entities)

    for entity in entities:
        x, y = entity.x, entity.y
        if (x, y) in already_moved:
            continue

        if isinstance(entity, Shark):
            handle_shark(entity, x, y, already_moved)
        elif isinstance(entity, Fish):
            handle_fish(entity, x, y, already_moved)

    turn_count += 1
    draw_grid_emojis()
    update_info(info_label)

def handle_shark(entity, x, y, already_moved): # Move to shark.py
    entity.step()
    fish_neighbors = grid_instance.get_fish_neighbors(x, y)
    if fish_neighbors:
        nx, ny = random.choice(fish_neighbors)
        entity.eat(grid_instance.cells[nx][ny])
        move_entity(entity, x, y, nx, ny, already_moved)
    else:
        empty = get_empty_neighbors(grid_instance.cells, x, y)
        if empty:
            nx, ny = random.choice(empty)
            move_entity(entity, x, y, nx, ny, already_moved)

    if entity.shark_energy <= 0:
        grid_instance.cells[entity.x][entity.y] = None
    elif entity.age >= entity.shark_reproduction_time:
        reproduce_entity(entity, x, y)

def handle_fish(entity, x, y, already_moved): # Move to fish.py
    entity.step()
    empty = get_empty_neighbors(grid_instance.cells, x, y)
    if empty:
        nx, ny = random.choice(empty)
        move_entity(entity, x, y, nx, ny, already_moved)

    if entity.age >= entity.reproduction_time:
        reproduce_entity(entity, x, y)

def move_entity(entity, x, y, nx, ny, already_moved): # Move to grid.py
    grid_instance.cells[nx][ny] = entity
    grid_instance.cells[x][y] = None
    entity.x, entity.y = nx, ny
    already_moved.add((nx, ny))

def reproduce_entity(entity, x, y): # Move to grid.py
    baby = entity.reproduce()
    if baby:
        baby.grid = grid_instance
        empty_spots = get_empty_neighbors(grid_instance.cells, x, y)
        if empty_spots:
            bx, by = random.choice(empty_spots)
            baby.x, baby.y = bx, by
            grid_instance.cells[bx][by] = baby

def run_simulation(root, button, info_label): # Move to grid.py
    if simulation_running:
        simulate_step(info_label)
        root.after(500, run_simulation, root, button, info_label)

def toggle_simulation(root, button, info_label): # Move to grid.py
    global simulation_running
    simulation_running = not simulation_running
    if simulation_running:
        button.config(text="Pause")
        run_simulation(root, button, info_label)
    else:
        button.config(text="Lancer")

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

    step_button = tk.Button(button_frame, text="Tour suivant", command=lambda: simulate_step(info_label))
    step_button.pack(side=tk.LEFT, padx=5)

    toggle_button = tk.Button(button_frame, text="Lancer")
    toggle_button.config(command=lambda: toggle_simulation(root, toggle_button, info_label))
    toggle_button.pack(side=tk.LEFT, padx=5)

    draw_grid_emojis()
    update_info(info_label)

    root.mainloop()

if __name__ == "__main__": # Entry point of the program
    main() 
