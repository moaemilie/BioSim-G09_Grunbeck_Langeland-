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
        self.coordinates = ini_pop[0]['loc']
        self.pop = ini_pop[0]['pop']
        random.seed(seed)
        self.sim_island = Island(island_map)
        self.sim_island.make_map()
        if self.pop[0]['species'] == 'Herbivore':
            self.sim_island.add_animals(self.coordinates, self.pop, None)
        else:
            self.sim_island.add_animals(self.coordinates, None, self.pop)


    @staticmethod
    def set_landscape_parameters(land_type, new_f_max):
        Island.set_landscape_parameters(land_type,new_f_max)


    @staticmethod
    def set_animal_parameters(animal_type, new_params):
        Island.set_animal_parameters(animal_type, new_params)


    def simulate(self, num_years):
        def simulate_year():
            self.sim_island.aging()
            self.sim_island.weightloss()
            self.sim_island.fitness()
            self.sim_island.birth()
            self.sim_island.feeding()
            self.sim_island.death()
            self.sim_island.move_island()
            self.sim_island.add_immigrants()
            print(self.sim_island.get_num_herb(), self.sim_island.get_num_carn())
        for year in range(num_years):
            simulate_year()


    def add_population(self, population):
        if population[0]['pop'][0]['species'] == 'Herbivore':
            self.sim_island.add_animals(population[0]['loc'], population[0]['pop'], None)
        else:
            self.sim_island.add_animals(population[0]['loc'], None, population[0]['pop'])



