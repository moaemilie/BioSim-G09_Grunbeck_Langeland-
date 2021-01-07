# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

from biosim.animals import Herbivore


class Cell:
    f_max = None

    @classmethod
    def set_f_max(cls, new_f_max):
        cls.f_max = new_f_max

    def __init__(self, num_herb):
        self.num_herb = num_herb
        self.herb_pop = [Herbivore(4, 20) for _ in range(num_herb)]

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

        p_birth = [min(1, Herbivore.gamma * herb.fit * (self.num_herb - 1)) for herb in self.herb_pop]

        def newborns(pop, p):
            return [Herbivore(4, 20) for parent in pop if parent.birth(p)]

        return self.herb_pop.extend(newborns(self.herb_pop, p_birth))


class Lowland(Cell):
    f_max = 800

    def __init__(self, num_herb):
        super().__init__(num_herb)
