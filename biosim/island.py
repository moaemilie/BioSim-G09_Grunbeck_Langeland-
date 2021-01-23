# -*- encoding: utf-8 -*-
"""
This file contains the class Island
"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

from biosim.landscape import Landscape, Lowland, Highland, Desert, Water
from biosim.animals import Herbivore, Carnivore
import random


class Island:
    """
    The base class of the Island.
    """
    def __init__(self, island_map):
        """
        Parameters
        ----------
        island_map : string
            with the information of the landscape combination that creates the map.
        """
        self.island_map = island_map
        self.map_rows = None
        self.map_columns = None

    @staticmethod
    def set_animal_parameters(species, params):
        Landscape.set_animal_parameters(species, params)

    @staticmethod
    def set_landscape_parameters(landscape, params):
        landscapes = {'L': Lowland, 'H': Highland}
        landscapes[landscape].set_f_max(params)

    def make_map(self):
        """
        Creates a list with al the landskape classes in for a cell in is corresponding position.

        Returns
        -------
        List
                2D list with the landscape classes for every cell.
        """
        self.island_map = [list(line) for line in self.island_map.split('\n')]

        first_line = len(self.island_map[0])
        for string in self.island_map:
            if len(string) != first_line:
                raise ValueError('Map rows must be of same length.')
            for letter in string:
                if letter not in ('W', 'H', 'L', 'D'):
                    raise ValueError('Invalid landscape letter: ' + letter)

        for string in self.island_map[0][:] + self.island_map[-1][:] + self.island_map[:][0] + self.island_map[:][-1]:
            if string != 'W':
                raise ValueError('Map must be surrounded by water.')

        landscapes = {'W': Water, 'L': Lowland, 'H': Highland, 'D': Desert}

        self.island_map = [[landscapes[string]([], []) for string in line] for line in self.island_map]

        self.map_rows = len(self.island_map)
        self.map_columns = len(self.island_map[0])

    def add_animals_island(self, coordinates, new_herbs=None, new_carns=None):
        """

        Parameters
        ----------
        coordinates: tuple
            the coordinates that the new animals wil be placed on.
        new_herbs: list / None
            containing a dictionary with age and weight of the new herbivores.
        new_carns: list / None
            containing a dictionary with age and weight of the new carnivores.

        Raises
        -------
        ValueError, ValueError
        """
        if new_herbs is None:
            new_herbs = []
        elif new_carns is None:
            new_carns = []
        r_coord = coordinates[0] - 1
        c_coord = coordinates[1] - 1
        if r_coord >= self.map_rows or 0 > r_coord or c_coord >= self.map_columns or 0 > c_coord:
            raise ValueError(f'Coordinate out of range {coordinates}')

        elif isinstance(self.island_map[r_coord][c_coord], Water):
            raise ValueError(f'Can not place animals in water {coordinates}')

        origin_cell = self.island_map[r_coord][c_coord]
        origin_cell.add_animals_landscape(new_herbs, new_carns)

    def get_num_herb_island(self):
        """
        Finds the total number herbivores on the map
        Returns
        -------
        int:
            number of herbs
        """
        return sum([sum([self.island_map[row][col].get_num_herb_landscape() for col in range(self.map_columns)])
                    for row in range(self.map_rows)])

    def get_num_carn_island(self):
        """
        Finds the total number carnivores on the map
        Returns
        -------
        int:
            number of carnivores
        """
        return sum([sum([self.island_map[row][col].get_num_carn_landscape() for col in range(self.map_columns)])
                    for row in range(self.map_rows)])

    def aging_island(self):
        """
        Ages every animal on the map with one year.
        """
        for row in range(self.map_rows):
            for col in range(self.map_columns):
                self.island_map[row][col].aging_landscape()

    def weightloss_island(self):
        """
        Make every animal on the map loose weight.
        """
        for row in range(self.map_rows):
            for col in range(self.map_columns):
                self.island_map[row][col].weightloss_landscape()

    def fitness_island(self):
        """
        Calculates the fitness of every animal on the map.
        """
        for row in range(self.map_rows):
            for col in range(self.map_columns):
                self.island_map[row][col].fitness_landscape()

    def birth_island(self):
        """
        Find out which animal on the map wil give weight and adds the newborn to the population.
        """
        for row in range(self.map_rows):
            for col in range(self.map_columns):
                self.island_map[row][col].birth_landscape()

    def feeding_island(self):
        """
        Makes every animal on the map eat.
        """
        for row in range(self.map_rows):
            for col in range(self.map_columns):
                self.island_map[row][col].eating_landscape()

    def death_island(self):
        """
        Finds the animals that dies and take them away from the population.
        """
        for row in range(self.map_rows):
            for col in range(self.map_columns):
                self.island_map[row][col].death_landscape()

    def move_island(self):
        """
        Moves the animals

        Returns
        -------
        dic
                dictionary with the neighbouring cells.
        """

        def choose_neighbor(coord_1, coord_2):
            """
            Finds neighbouring cells.

            Input
            -------
            coord_1: int
                    x_positon of the placement of the animal
            coord_2: int
                 y_positon of the placement of the animal

            Returns
            -------
            landscape instance
                Where the animal is going to move.

            """
            neighbors = {'left': self.island_map[coord_1][coord_2 + 1], 'right': self.island_map[coord_1][coord_2 - 1],
                         'up': self.island_map[coord_1 + 1][coord_2], 'down': self.island_map[coord_1 - 1][coord_2]}

            return neighbors[random.choice(('left', 'right', 'up', 'down'))]

        def move_one_animal(coord_1, coord_2, pop):
            """
            Moves the animals from a cell.

            Input
            -------
            coord_1: int
                    x_positon of the placement of the animal
            coord_2: int
                 y_positon of the placement of the animal
            pop: List
                containing a dictionary with animals weight and age.

            Returns
            -------
            list
                    list with animals that stays in the cell.
            """
            chosen = choose_neighbor(coord_1, coord_2)
            stay = []
            for animal in pop:

                if chosen.move_landscape() is False or animal.move_animal() is False:
                    stay.append(animal)
                elif isinstance(animal, Herbivore):
                    chosen.herb_immigrants.append(animal)
                elif isinstance(animal, Carnivore):
                    chosen.carn_immigrants.append(animal)
            return stay

        for row in range(1, self.map_rows - 2, 1):
            for col in range(1, self.map_columns - 2, 1):
                self.island_map[row][col].herb_pop = move_one_animal(row, col, self.island_map[row][col].herb_pop)
                self.island_map[row][col].carn_pop = move_one_animal(row, col, self.island_map[row][col].carn_pop)

    def add_immigrants_island(self):
        """
        Adds the animals that have chosen to move to the populations in the different cells.
        """
        for row in range(self.map_rows):
            for col in range(self.map_columns):
                self.island_map[row][col].add_immigrants_landscape()
