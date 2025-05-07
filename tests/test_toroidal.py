import unittest
from interface.grid import Grid
from aquatic.fish import Fish
from aquatic.shark import Shark

class TestToroidalGrid(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(5, 5)

    def test_fish_moves_left_toroidal(self):
        fish = Fish(self.grid, 0, 2)
        self.grid.cells[0][2] = fish
        if (self.grid.cells[4][2] is None):  # Vérifie si la case de destination est vide
            fish.move_left()
        self.assertEqual((fish.x, fish.y), (4, 2) if self.grid.cells[4][2] is None else (0, 2))

    def test_fish_moves_right_toroidal(self):
        fish = Fish(self.grid, 4, 2)
        self.grid.cells[4][2] = fish
        if (self.grid.cells[0][2] is None):
            fish.move_right()
        self.assertEqual((fish.x, fish.y), (0, 2) if self.grid.cells[0][2] is None else (4, 2))

    def test_fish_moves_up_toroidal(self):
        fish = Fish(self.grid, 2, 0)
        self.grid.cells[2][0] = fish
        if (self.grid.cells[2][4] is None):
            fish.move_up()
        self.assertEqual((fish.x, fish.y), (2, 4) if self.grid.cells[2][4] is None else (2, 0))

    def test_fish_moves_down_toroidal(self):
        fish = Fish(self.grid, 2, 4)
        self.grid.cells[2][4] = fish
        if (self.grid.cells[2][0] is None):
            fish.move_down()
        self.assertEqual((fish.x, fish.y), (2, 0) if self.grid.cells[2][0] is None else (2, 4))

    def test_shark_moves_left_toroidal(self):
        shark = Shark(self.grid, 0, 2)
        self.grid.cells[0][2] = shark
        fish_target = self.grid.cells[4][2]  # Vérifie s'il peut manger un poisson
        if isinstance(fish_target, Fish):
            shark.eat(fish_target)
        shark.move_left()
        self.assertEqual((shark.x, shark.y), (4, 2))

    def test_shark_moves_right_toroidal(self):
        shark = Shark(self.grid, 4, 2)
        self.grid.cells[4][2] = shark
        fish_target = self.grid.cells[0][2]
        if isinstance(fish_target, Fish):
            shark.eat(fish_target)
        shark.move_right()
        self.assertEqual((shark.x, shark.y), (0, 2))

    def test_shark_moves_up_toroidal(self):
        shark = Shark(self.grid, 2, 0)
        self.grid.cells[2][0] = shark
        fish_target = self.grid.cells[2][4]
        if isinstance(fish_target, Fish):
            shark.eat(fish_target)
        shark.move_up()
        self.assertEqual((shark.x, shark.y), (2, 4))

    def test_shark_moves_down_toroidal(self):
        shark = Shark(self.grid, 2, 4)
        self.grid.cells[2][4] = shark
        fish_target = self.grid.cells[2][0]
        if isinstance(fish_target, Fish):
            shark.eat(fish_target)
        shark.move_down()
        self.assertEqual((shark.x, shark.y), (2, 0))

if __name__ == '__main__':
    unittest.main()
