# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

from biosim.animals import Herbivore
from biosim.animals import Carnivore
import random

random.seed(123456)


class Cell:
    f_max = None

    @classmethod
    def set_f_max(cls, new_f_max):
        cls.f_max = new_f_max

    def __init__(self, num_herb, num_carn):
        # self.num_herb = self.get_num_herb()
        self.herb_pop = [Herbivore(random.randint(0, 50), random.randint(0, 50)) for _ in range(num_herb)]
        self.carn_pop = [Carnivore(random.randint(0, 50), random.randint(0, 50)) for _ in range(num_carn)]

    def get_num_herb(self):
        """
       Counts how many herbivores its in the population.

       Returns
       -------
       int
           Number of herbivores
        """
        return len(self.herb_pop)

    def get_num_carn(self):
        """
        Counts how many carnivores its in the population.

        Returns
        -------
        int
            Number of carnivores
        """
        return len(self.carn_pop)


    def aging(self):
        """
        Adds a year for al animals in the population for every time its called.

        Returns
        -------
        int
            Number of years
        """
        for herb, carn in zip(self.herb_pop, self.carn_pop):
            herb.aging()
            carn.aging()


    def death(self):
        def survivors(pop):
            return [herb for herb in pop if not herb.death()]

        self.herb_pop = survivors(self.herb_pop)

    def birth(self):

        def newborns(pop):
            return [Herbivore(0, parent.babyweight) for parent in pop if parent.birth(self.get_num_herb())]

        return self.herb_pop.extend(newborns(self.herb_pop))

    def feeding(self):
        """
        Feeds herbivores and carnivores in a cell.

        Returns
        -------
        list
            Updated populations
        """

        self.set_f_max(self.default_f_max['f_max'])

        for herb in self.herb_pop:
            if self.default_f_max['f_max'] >= herb.default_params["F"]:
                herb.eating(herb.default_params["F"])
                self.default_f_max['f_max'] -= herb.default_params["F"]
            elif self.default_f_max['f_max'] < herb.default_params["F"] and self.default_f_max['f_max'] != 0:
                herb.fodder = self.default_f_max['f_max']
                herb.eating(self.default_f_max['f_max'])
            herb.fitness()

            def sort_pop(pop, reverse=False):
                for j in reversed(range(len(pop))):
                    for k in range(j):
                        if self.herb_pop[k + 1].fit < self.herb_pop[k].fit and reverse == False:
                            self.herb_pop[k], self.herb_pop[k + 1] = self.herb_pop[k + 1], self.herb_pop[k]
                        elif self.herb_pop[k + 1].fit < self.herb_pop[k].fit and reverse == True:
                            self.herb_pop[k], self.herb_pop[k + 1] = self.herb_pop[k + 1], self.herb_pop[k]
                return pop

        self.herb_pop = sort_pop(self.herb_pop)
        self.carn_pop = sort_pop(self.carn_pop, reverse=True)

        for carn in self.carn_pop:
            for herb in self.herb_pop:
                if carn.killing() == True:
                    carn.eating(herb.weight)
                    carn.fitness()

    def fitness(self):
        """
         Calculates the fitness for every animal in the population.

         Returns
         -------
         Float
             with new fitness between 0 and 1
         """
        for herb, carn in zip(self.herb_pop, self.carn_pop):
            herb.fitness()
            carn.fitness()


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
