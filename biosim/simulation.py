# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

from biosim.island import Island

class BioSim():
    def __init__(self, island_map, ini_pop):
        self.island_map = island_map
        self.coordinates = ini_pop[0]['loc']
        self.pop = ini_pop[0]['pop']


    def simulate(self, num_years, vis_years):

        island = Island(self.island_map)
        island.make_map()
        if self.pop['species'] == 'Herbivore':
            island.add_animals(self.coordinates, self.pop, num_carn = [])
        else:
            island.add_animals(self.coordinates, num_herb = [], self.pop)



    def add_population(self, dict):
