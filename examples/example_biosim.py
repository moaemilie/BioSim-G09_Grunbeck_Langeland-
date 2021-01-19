# -*- coding: utf-8 -*-

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'
import textwrap
import matplotlib.pyplot as plt
from biosim.simulation import BioSim

"""
An example to use the BioSim simulation on.
"""


if __name__ == '__main__':

    geogr = """\
               WWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWHWWWWLLLLWWWW
               WWWHHHLLLLWWWWWHHLLWW
               WWWWWHHHHHWWWWWLLLWWW
               WHHHHHLLLLLLLLLLLLWWW
               WHHWWWLLLDDLLLHLLLWWW
               WHHLLLLLDDDLLLHHHHWWW
               WWHHHHLLLHHHHHLWWWWWW
               WHHHLLLLLWWDDLLLHHWWW
               WHHHHLLLLWDDDLLWWWWWW
               WWHHHHLLLLLLLLWWWWWWW
               WWWWHHHLLLLWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWWWW"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [{'loc': (7, 7),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(15)]}]
    ini_carns = [{'loc': (7, 7),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(5)]}]

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs,
                 seed=123456, ymax_animals=20000, img_base='../data/img_',
                 hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                             'age': {'max': 60.0, 'delta': 2},
                             'weight': {'max': 60, 'delta': 2}},
                 )

    sim.set_animal_parameters('Herbivore', {'zeta': 3.2, 'xi': 1.8})
    sim.set_animal_parameters('Carnivore', {'a_half': 70, 'phi_age': 0.5,
                                            'omega': 0.3, 'F': 80,
                                            'DeltaPhiMax': 8.})

    sim.set_landscape_parameters('L', {'f_max': 800})
    sim.set_landscape_parameters('H', {'f_max': 400})

    sim.simulate(num_years=50, vis_years=5, img_years=10)
    sim.add_population(population=ini_carns)
    sim.simulate(num_years=100, vis_years=5, img_years=10)
    sim.make_movie()