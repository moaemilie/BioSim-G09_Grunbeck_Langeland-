# -*- encoding: utf-8 -*-
"""
This file contains the simulation class
"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

from biosim.island import Island
from biosim.graphics import Graphics
import random
import subprocess
import matplotlib.pyplot as plt


class BioSim:
    """
    The base class of the simulation
    """
    def __init__(self, island_map, ini_pop, seed=123456,
                 ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_base=None, img_fmt='png', movie_fmt='mp4'):
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
        self.tot_years = 0
        self.hist_specs = hist_specs
        self.img_base = img_base
        if self.img_base is None:
            raise RuntimeError("No filename defined.")
        self.movie_fmt = movie_fmt
        self.img_fmt = img_fmt
        self.island_map = island_map
        self.sim_island = Island(self.island_map)
        self.sim_island.make_map()
        if ini_pop != []:
            if ini_pop[0]['pop'][0]['species'] == 'Herbivore':
                self.sim_island.add_animals_island(ini_pop[0]['loc'], ini_pop[0]['pop'], None)
            else:
                self.sim_island.add_animals_island(ini_pop[0]['loc'], None, ini_pop[0]['pop'])
        self.sim_graphics = Graphics(ymax_animals, cmax_animals, hist_specs, self.sim_island, self.img_base, self.img_fmt)

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

    def simulate(self, num_years=100, vis_years=1, img_years=None):

        if img_years is None:
            img_years = vis_years

        self.tot_years += num_years

        self.sim_graphics.setup(self.tot_years)
        self.sim_graphics.map_plot(self.island_map)

        def simulate_year():
            self.sim_island.feeding_island()
            self.sim_island.birth_island()
            self.sim_island.move_island()
            self.sim_island.add_immigrants_island()
            self.sim_island.aging_island()
            self.sim_island.weightloss_island()
            self.sim_island.death_island()
            self.sim_year += 1

        def age_list():
            """
            Creates two lists, one for herbivore and one for carnivore with the age of every animal.
            Returns
            -------
            age_list_herb: list
                containing the age of every carnivore on the map.
            age_list_carn: list
                containing the age of every carnivore on the map.
            """
            age_list_herb = []
            age_list_carn = []

            for row in range(self.sim_island.map_rows):
                for col in range(self.sim_island.map_columns):
                    for herb in self.sim_island.island_map[row][col].herb_pop:
                        age_list_herb.append(herb.age)
                    for carn in self.sim_island.island_map[row][col].carn_pop:
                        age_list_carn.append([carn.age])
            return [age_list_herb, age_list_carn]

        def weight_list():
            """
            Creates two lists, one for herbivore and one for carnivore with the weight of every animal.
            Returns
            -------
            weight_list_herb: list
                containing the weight of every carnivore on the map.
            weight_list_carn: list
                containing the weight of every carnivore on the map.
            """
            weight_list_herb = []
            weight_list_carn = []

            for row in range(self.sim_island.map_rows):
                for col in range(self.sim_island.map_columns):
                    for herb in self.sim_island.island_map[row][col].herb_pop:
                        weight_list_herb.append(herb.weight)
                    for carn in self.sim_island.island_map[row][col].carn_pop:
                        weight_list_carn.append([carn.weight])
            return [weight_list_herb, weight_list_carn]

        def fitness_list():
            """
            Creates two lists, one for herbivore and one for carnivore with the fitness of every animal.
            Returns
            -------
            fitness_list_herb: list
                containing the fitness of every carnivore on the map.
            fitness_list_carn: list
                containing the fitness of every carnivore on the map.
            """
            fitness_list_herb = []
            fitness_list_carn = []

            for row in range(self.sim_island.map_rows):
                for col in range(self.sim_island.map_columns):
                    for herb in self.sim_island.island_map[row][col].herb_pop:
                        fitness_list_herb.append(herb.fitness_animal())
                    for carn in self.sim_island.island_map[row][col].carn_pop:
                        fitness_list_carn.append([carn.fitness_animal()])
            return [fitness_list_herb, fitness_list_carn]

        counter = 0
        for year in range(num_years):
            simulate_year()
            self.sim_graphics.line_plot(self.sim_year, self.sim_island.get_num_herb_island(), self.sim_island.get_num_carn_island())
            counter += 1
            if counter % vis_years == 0:
                self.sim_graphics.counter(self.sim_year)
                self.sim_graphics.hist_plot(age_list(), weight_list(), fitness_list())
                self.sim_graphics.dist_plot()
            if counter % img_years == 0:
                self.sim_graphics.save_graphics()

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
        return self.sim_island.get_num_carn_island() + self.sim_island.get_num_herb_island()

    @property
    def num_animals_per_species(self):
        """
        Total number of animals on island per species
        """
        return {'Herbivore': self.sim_island.get_num_herb_island(), 'Carnivore': self.sim_island.get_num_carn_island()}

    def make_movie(self):
        """
        Create MPEG4 movie from visualization images saved.

        Returns
        -------

        """

        if self.movie_fmt == 'mp4':
            try:
                subprocess.check_call(['ffmpeg',
                                       '-i', '{}_%05d.png'.format(self.img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self.img_base, 'mp4')])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif self.movie_fmt == 'gif':
            try:
                subprocess.check_call(['magick',
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self.img_base),
                                       '{}.{}'.format(self.img_base, self.movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + self.movie_fmt)

