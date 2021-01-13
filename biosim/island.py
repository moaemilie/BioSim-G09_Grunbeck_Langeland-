# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

from biosim.landscape import Lowland
from biosim.landscape import Highland
from biosim.landscape import Desert
from biosim.landscape import Water
import random


class Island:

    def __init__(self, island_map):
        self.island_map = island_map
        self.map_rows = None
        self.map_columns = None

    def make_map(self):
        self.island_map = self.island_map.split('\n')
        self.island_map = [list(line) for line in self.island_map]

        for string in self.island_map:
            for letter in string:
                if letter not in ('W', 'H', 'L', 'D'):
                    raise NameError('Invalid landscape letter: ' + letter)

        for string in self.island_map[0][:] + self.island_map[-1][:] + self.island_map[:][0] + self.island_map[:][-1]:
            if string != 'W':
                raise ValueError('Map must be surrounded by water')

        landscapes = {'W': Water(0, 0), 'L': Lowland(0, 0), 'H': Highland(0, 0), 'D': Desert(0, 0)}

        self.island_map = [[landscapes[string] for string in line] for line in self.island_map]

        return self.island_map

    def find_num_row_col(self):
        self.map_rows = len(self.island_map)
        self.map_columns = len(self.island_map[0])
        return self.map_rows, self.map_columns

    def add_animals(self, coordinates, num_herb, num_carn):
        x_coor = coordinates[0]
        y_coor = coordinates[1]
        if y_coor >= self.map_rows or x_coor >= self.map_columns:
            raise ValueError(f'Coordinate out of range {coordinates}')

        if isinstance(self.island_map[x_coor - 1][y_coor - 1], Water):
            raise ValueError(f'Can not place animals in water {coordinates}')

        origin = self.island_map[x_coor - 1][y_coor - 1]
        origin.num_herb = num_herb
        origin.num_carn = num_carn

    def move(self):

        def check_move_animal(row, col, pop):
            for animal in pop:
                p_move = animal.mu * animal.fit
                if check_which_cell(row, col) is False or random.random() < p_move is False:
                    stay = [animal]
                else:
                    go = [animal]
                    coord = [new_coord]



        def check_which_cell(row, col):
            directions = {'left': (row, col+1),'right': (row, col-1), 'up': (row+1, col), 'down': (row-1, col)}
            choice = random.choice(('left','right', 'up', 'down'))
            new_coord = directions(choice)
            if isinstance(self.island_map[new_coord[0]][new_coord[1]], Water):
                return False
            else:
                return new_coord


        def move_to_new_cell(row, col, pop):
            if check_move_animal(pop):
                new_coord = check_which_cell(row, col)
                if isinstance(self.island_map[new_coord[0]][new_coord[1]], Water):

                else:



        for row in range(self.map_rows):
            for col in range(self.map_columns):
                if check_move_animal(self.island_map[row][col]):





