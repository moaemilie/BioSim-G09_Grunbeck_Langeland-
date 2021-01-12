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
                    raise ValueError('Invalid landscape letter: ' + letter)

        if self.island_map[0][0:-1] or self.island_map[-1][0:-1] or self.island_map[0:-1][0] or self.island_map[0:-1][-1] != 'W':
            return ValueError('Map must be surrounded by water')

        landscapes = {'W': Water(0, 0), 'L': Lowland(0, 0), 'H': Highland(0, 0), 'D': Desert(0, 0)}

        for line in self.island_map:
            for string, num in zip(line, range(len(line))):
                line[num] = landscapes[string]

        self.map_rows = len(self.island_map[0])
        self.map_columns = len(self.island_map)

        return self.island_map


    def add_animals(self, coordinates, num_herb, num_carn):
        if coordinates[0] > self.map_rows or coordinates[1] > self.map_columns:
            return ValueError('Coordinate out of range' + coordinates)


    #def move(self):
