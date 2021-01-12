# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

class Island():

    def __init__(self, island_map):
        self.island_map = island_map

    def make_map(self):
        self.island_map = self.island_map.split('\n')
        self.island_map = [string.strip() for string in self.island_map]

        for string in self.island_map:
            for letter in string:
                if letter != 'W' or 'H' or 'L' or'D':
                    raise KeyError ('Invalid landskape letter: ' + letter)

        return self.island_map

    #def migration(self):