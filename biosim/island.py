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

    def make_map(self):
        self.island_map = self.island_map.split('\n')
        self.island_map = [list(line) for line in self.island_map]

        for string in self.island_map:
            for letter in string:
                if letter != 'W' or 'H' or 'L' or'D':
                    raise KeyError('Invalid landscape letter: ' + letter)

        landscapes = {'W': Water(0, 0), 'L': Lowland(0, 0), 'H': Highland(0, 0), 'D': Desert(0, 0)}

        for line in self.island_map:
            for string, num in zip(line, range(len(line))):
                line[num] = landscapes[string]

        return self.island_map

    #def move(self):
