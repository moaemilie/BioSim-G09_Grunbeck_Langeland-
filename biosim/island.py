# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

from biosim.landscape import Lowland
from biosim.landscape import Highland
from biosim.landscape import Desert
from biosim.landscape import Water

class Island():

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

        new1_list = []
        new2_list = []
        for line in self.island_map:
            for string in line:
                new1_list.append(landscapes[string])
            new2_list.append(new1_list)
        self.island_map = new2_list
        return self.island_map


    def find_num_row_col(self):
        self.map_rows = len(self.island_map)
        self.map_columns = len(self.island_map[0])
        return self.map_rows, self.map_columns


    def add_animals(self, coordinates, num_herb, num_carn):
        x_coor = coordinates[0]
        y_coor = coordinates[1]
        if y_coor > self.map_rows or x_coor > self.map_columns:
            return ValueError('Coordinate out of range' + coordinates)

        origin = self.island_map[x_coor - 1][y_coor - 1]
        origin.num_herb = num_herb
        origin.num_carn = num_carn

    #def move(self):
