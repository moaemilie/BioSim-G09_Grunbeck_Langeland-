# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

from biosim.landscape import Landscape
from biosim.landscape import Lowland
from biosim.landscape import Highland
from biosim.landscape import Desert
from biosim.landscape import Water
from biosim.animals import Herbivore
from biosim.animals import Carnivore
import random


class Island:

    def __init__(self, island_map):
        self.island_map = island_map
        self.map_rows = None
        self.map_columns = None

    @staticmethod
    def set_landscape_parameters(land_type, new_f_max):
        landscapes = {'L': Lowland, 'H': Highland}
        landscapes[land_type].set_f_max(new_f_max)

    @staticmethod
    def set_animal_parameters(animal_type, new_params):
        Landscape.set_animal_parameters(animal_type, new_params)

    def make_map(self):
        """
        Creates a list with al the landskape classes in for a cell in is corresponding position.

        Returns
        -------
        List
                2D list with the landscape classes for every cell.
        """
        self.island_map = [list(line) for line in self.island_map.split('\n')]

        for string in self.island_map:
            for letter in string:
                if letter not in ('W', 'H', 'L', 'D'):
                    raise NameError('Invalid landscape letter: ' + letter)

        for string in self.island_map[0][:] + self.island_map[-1][:] + self.island_map[:][0] + self.island_map[:][-1]:
            if string != 'W':
                raise ValueError('Map must be surrounded by water')

        landscapes = {'W': Water, 'L': Lowland, 'H': Highland, 'D': Desert}

        self.island_map = [[landscapes[string]([], []) for string in line] for line in self.island_map]

        self.map_rows = len(self.island_map)
        self.map_columns = len(self.island_map[0])

        return self.island_map

    def add_animals(self, coordinates, new_herbs=None, new_carns=None):
        if new_herbs is None:
            new_herbs = []
        elif new_carns is None:
            new_carns = []
        x_coord = coordinates[0] - 1
        y_coord = coordinates[1] - 1
        if 0 >= y_coord >= self.map_rows or 0 >= x_coord >= self.map_columns:
            raise IndexError(f'Coordinate out of range {coordinates}')

        if isinstance(self.island_map[x_coord][y_coord], Water):
            raise ValueError(f'Can not place animals in water {coordinates}')

        origin_cell = self.island_map[x_coord][y_coord]
        origin_cell.add_animals(new_herbs, new_carns)

    def get_num_herb(self):
        return sum([sum([self.island_map[row][col].get_num_herb() for col in range(self.map_columns)])
                    for row in range(self.map_rows)])

    def get_num_carn(self):
        return sum([sum([self.island_map[row][col].get_num_carn() for col in range(self.map_columns)])
                    for row in range(self.map_rows)])

    def aging(self):
        for row in range(self.map_rows):
            for col in range(self.map_columns):
                self.island_map[row][col].aging()
        return self.island_map

    def weightloss(self):
        for row in range(self.map_rows):
            for col in range(self.map_columns):
                self.island_map[row][col].weightloss()
        return self.island_map

    def fitness(self):
        for row in range(self.map_rows):
            for col in range(self.map_columns):
                self.island_map[row][col].fitness()
        return self.island_map

    def birth(self):
        for row in range(self.map_rows):
            for col in range(self.map_columns):
                self.island_map[row][col].birth()
        return self.island_map

    def feeding(self):
        for row in range(self.map_rows):
            for col in range(self.map_columns):
                self.island_map[row][col].feeding()
        return self.island_map

    def death(self):
        for row in range(self.map_rows):
            for col in range(self.map_columns):
                self.island_map[row][col].death()
        return self.island_map

    def move(self):
        """

        Moves the animals

        Returns
        -------
        dic
                dictionary with the neighbouring cells.
        """

        def get_neighbors(coord_1, coord_2):
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

            # edges_rows = [(pos, self.map_rows - 1) for pos in range(self.map_rows)] + [(pos, 0) for pos in range(self.map_rows)]
            # edges_columns = [(0, pos) for pos in range(self.map_columns)] + [(self.map_columns-1, pos) for pos in range(self.map_columns)]
            # edges = edges_rows + edges_columns

            # if (coord_1, coord_2) not in edges:
            return {'left': self.island_map[coord_1][coord_2 + 1], 'right': self.island_map[coord_1][coord_2 - 1],
                    'up': self.island_map[coord_1 + 1][coord_2], 'down': self.island_map[coord_1 - 1][coord_2]}

        def move_animals(coord_1, coord_2, pop):
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
            neighbors = get_neighbors(coord_1, coord_2)
            stay = []
            for animal in pop:
                p_move = animal.default_params['mu'] * animal.fit
                chosen_neighbor = neighbors[random.choice(('left', 'right', 'up', 'down'))]
                if isinstance(chosen_neighbor, Water) or random.random() > p_move:
                    stay.append(animal)
                elif isinstance(animal, Herbivore):
                    chosen_neighbor.herb_immigrants.append(animal)
                elif isinstance(animal, Carnivore):
                    chosen_neighbor.carn_immigrants.append(animal)
            return stay

        for row in range(1, self.map_rows - 2, 1):
            for col in range(1, self.map_columns - 2, 1):
                self.island_map[row][col].herb_pop = move_animals(row, col, self.island_map[row][col].herb_pop)
                self.island_map[row][col].carn_pop = move_animals(row, col, self.island_map[row][col].carn_pop)
        return self.island_map

    def add_immigrants(self):
        for row in range(self.map_rows):
            for col in range(self.map_columns):
                self.island_map[row][col].add_immigrants()
        return self.island_map
