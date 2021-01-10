# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

from biosim.animals import Herbivore
import random

random.seed(123456)


class Cell:
    f_max = None

    @classmethod
    def set_f_max(cls, new_f_max):
        cls.f_max = new_f_max

    def __init__(self, num_herb):
        # self.num_herb = self.get_num_herb()
        self.herb_pop = [Herbivore(random.randint(0, 50), random.randint(0, 50)) for _ in range(num_herb)]

    def get_num_herb(self):
        return len(self.herb_pop)

    def aging(self):
        for herb in self.herb_pop:
            herb.aging()

    def death(self):
        def survivors(pop):
            return [herb for herb in pop if not herb.death()]

        self.herb_pop = survivors(self.herb_pop)

    def birth(self):

        def newborns(pop):
            return [Herbivore(0, random.randint(5, 10)) for parent in pop if parent.birth(self.get_num_herb())]

        return self.herb_pop.extend(newborns(self.herb_pop))

    def feeding(self):

        # F = self.f_max
        for herb in self.herb_pop:
            herb.eating(8)

    def fitness(self):
        for herb in self.herb_pop:
            herb.fitness()


class Lowland(Cell):
    f_max = 800

    def __init__(self, num_herb):
        super().__init__(num_herb)


class Highland(Cell):
    f_max = 300

    def __init__(self, num_herb):
        super().__init__(num_herb)


class Desert(Cell):

    def __init__(self, num_herb):
        super().__init__(num_herb)


class Water(Cell):

    def __init__(self, num_herb):
        super().__init__(num_herb)
