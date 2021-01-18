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
    def __init__(self, island_map, ini_pop, seed,
                 ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_base=None, img_fmt='png'):
        """
        Parameters
        ----------
        island_map : string
            with the information of the landscape combination that creates the map.
        ini_pop: list
            with dictionaries that contains the initial coordinates, age, weight and number of animals that begins on the island.
        seed: int
            contains the seed for the whole project.
        ymax_animals: int
            IDK
        cmax_animals: IDK
            IDK
        hist_specs: dict
            IDK
        img_fmt: string
            which format the images should be saved as.
        """
        random.seed(seed)
        self.sim_year = 0
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.hist_specs = hist_specs
        self.img_base = img_base
        self.img_fmt = img_fmt
        self.sim_island = Island(island_map)
        self.sim_island.make_map()
        if ini_pop != []:
            if ini_pop[0]['pop'][0]['species'] == 'Herbivore':
                self.sim_island.add_animals_island(ini_pop[0]['loc'], ini_pop[0]['pop'], None)
            else:
                self.sim_island.add_animals_island(ini_pop[0]['loc'], None, ini_pop[0]['pop'])

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.
        """
        self.sim_island.set_animal_parameters(species, params)

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.
        """
        self.sim_island.set_landscape_parameters(landscape, params)

    def simulate(self, num_years, vis_years=1, img_years=None):
        def simulate_year():
            self.sim_island.feeding_island()
            self.sim_island.birth_island()
            self.sim_island.move_island()
            self.sim_island.add_immigrants_island()
            self.sim_island.aging_island()
            self.sim_island.weightloss_island()
            self.sim_island.death_island()
            self.sim_year += 1
            print(self.sim_island.get_num_herb(), self.sim_island.get_num_carn())

        for year in range(num_years):
            simulate_year()

    def add_population(self, population):
        if population[0]['pop'][0]['species'] == 'Herbivore':
            self.sim_island.add_animals_island(population[0]['loc'], population[0]['pop'], None)
        else:
            self.sim_island.add_animals_island(population[0]['loc'], None, population[0]['pop'])

    @property
    def year(self):
        """
        Last year simulated.
        """
        return self.sim_year

    @property
    def num_animals(self):
        """
        Total number of animals on island.
        """
        return self.sim_island.get_num_carn() + self.sim_island.get_num_herb()

    @property
    def num_animals_per_species(self):
        """
        Total number of animals on island per species
        """
        return {'Herbivore': self.sim_island.get_num_herb(), 'Carnivore': self.sim_island.get_num_carn()}
