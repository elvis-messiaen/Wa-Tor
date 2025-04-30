from interface.grid import Grid

grid_instance = Grid(20, 20)
grid_instance.create()
grid_instance.populate_grid()

cell_status = grid_instance.empty(5, 10)
print(f"Le contenu de la case [5][10] est : {cell_status}")
