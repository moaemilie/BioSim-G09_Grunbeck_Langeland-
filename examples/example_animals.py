# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

import random
from biosim.animals import Herbivore
from biosim.landscape import Lowland

N = 10
cell = Lowland(10, 10)



for _ in range(10):
    print(cell.get_num_herb_landscape(), cell.get_num_carn_landscape())
    cell.aging_landscape()
    cell.death_landscape()
    cell.birth_landscape()
    cell.eating_landscape()
    cell.fitness_landscape()


