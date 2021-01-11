# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

import random
from biosim.animals import Herbivore
from biosim.cell import Lowland

N = 10
cell = Lowland(10, 10)



for _ in range(10):
    print(cell.get_num_herb(), cell.get_num_carn())
    cell.aging()
    cell.death()
    cell.birth()
    cell.feeding()
    cell.fitness()


