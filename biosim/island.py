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
        """
        Creates a list with al the landskape classes in for a cell in is corresponding position.

        Returns
        -------
        List
                2D list with the landscape classes for every cell.
        """
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
        """

        Calculates the number of columns and rows in the created map.

        Returns
        -------
        int, int
                number of rows, number of columns
        """
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

        def get_neighbors(row, col):
            """

            Finds neighbouring cells.

            Input
            -------
            int, int
                    number of rows and columns

            Returns
            -------
            dic
                    dictionary with the neighbouring cells.
            """
            return {'left': self.island_map[row][col + 1], 'right': self.island_map[row][col - 1], 'up': self.island_map[row+1][col], 'down': self.island_map[row - 1][col]}

        def move_animals(pop, neighbors):
            """
            Moves the animals from a cell.

            Input
            -------
            list, dict
                    list with population, dict with neighboring cells.

            Returns
            -------
            list
                    list with animals that stays in the cell.
            """
            stay = []
            for animal in pop:
                p_move = animal.mu * animal.fit
                chosen_neighbor = neighbors(random.choice(('left', 'right', 'up', 'down'))
                if isinstance(chosen_neighbor, Water) or random.random() < p_move is False:
                    stay.append(animal)
                else:
                    chosen_neighbor.immigrants.extend(animal)
            return stay


        for row in range(self.map_rows):
            for col in range(self.map_columns):
                    neighbors = get_neighbors(row, col)
                    stay_herb = move_animals(self.island_map[row][col].herb_pop, neighbors)
                    stay_carn = move_animals(self.island_map[row][col].carn_pop, neighbors)
                    self.island_map[row][col].herb_pop.extend(stay_herb)
                    self.island_map[row][col].carn_pop.extend(stay_carn)





