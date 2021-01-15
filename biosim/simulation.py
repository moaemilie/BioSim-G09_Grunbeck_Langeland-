# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

from biosim.island import Island
from biosim.landscape import Lowland
from biosim.landscape import Highland
from biosim.landscape import Desert
from biosim.landscape import Water
import random

class BioSim:
    def __init__(self, island_map, ini_pop, seed):
        self.island_map = island_map
        self.coordinates = ini_pop[0]['loc']
        self.pop = ini_pop[0]['pop']
        random.seed(seed)

    @staticmethod
    def set_landscape_parameters(land_type, new_f_max):
        Island.set_landscape_parameters(new_f_max)

    def set_animal_parameters(self, animal_type, new_params):
        Island.set_animal_parameters(animal_type, new_params)

    def simulate(self, num_years, vis_years):

        island = Island(self.island_map)
        island.make_map()
        if self.pop['species'] == 'Herbivore':
            island.add_animals(self.coordinates, num_herb = self.pop, num_carn = [])
        else:
            island.add_animals(self.coordinates, num_herb = [], num_carn = self.pop)


    def add_population(self, new_herbs = [], new_carns = []):
        #add_animals









