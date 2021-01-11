# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

from biosim.animals import Herbivore
from biosim.animals import Carnivore
import random

random.seed(123456)


class Landscape:
    default_f_max = {'f_max': None}

    @classmethod
    def set_f_max(cls, new_f_max):
        """
        Sets new f_max parameter for Lowland and Highland.

        Returns
        -------
        dict
            f_max parameter for landscapes
        """

        for key in new_f_max:
            if key != 'f_max':
                raise KeyError('Invalid parameter name: ' + key)
        cls.default_f_max = new_f_max

    def __init__(self, num_herb, num_carn):

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
        Adds a year for all animals in the population for every time its called.

        Returns
        -------
        int
            Number of years
        """
        for herb, carn in zip(self.herb_pop, self.carn_pop):
            herb.aging()
            carn.aging()

    def death(self):
        """

        """

        def survivors(pop):
            return [animal for animal in pop if not animal.death()]

        self.herb_pop = survivors(self.herb_pop)
        self.carn_pop = survivors(self.carn_pop)

    def birth(self):
        """
        Adds new animals to the population.

        Returns
        -------
        list
            Updated populations
        """

        def herb_newborns(pop):
            return [Herbivore(0, parent.babyweight) for parent in pop if parent.birth(self.get_num_herb())]

        def carn_newborns(pop):
            return [Carnivore(0, parent.babyweight) for parent in pop if parent.birth(self.get_num_carn())]

        self.herb_pop.extend(herb_newborns(self.herb_pop))
        self.carn_pop.extend(carn_newborns(self.carn_pop))

    def feeding(self):
        """
        Feeds herbivores and carnivores in a cell.

        Returns
        -------
        list
            Updated populations
        """

        self.set_f_max(self.default_f_max)

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
                        if pop[k + 1].fit < pop[k].fit and reverse is False:
                            pop[k], pop[k + 1] = pop[k + 1], pop[k]
                        elif pop[k + 1].fit < pop[k].fit and reverse is True:
                            pop[k], pop[k + 1] = pop[k + 1], pop[k]
                return pop

        self.herb_pop = sort_pop(self.herb_pop)
        self.carn_pop = sort_pop(self.carn_pop, reverse=True)

        for carn in self.carn_pop:
            for herb in self.herb_pop:
                if carn.kill(herb.fit):
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


class Lowland(Landscape):
    default_f_max = {'f_max': 800}

    def __init__(self, num_herb, num_carn):
        super().__init__(num_herb, num_carn)


class Highland(Landscape):
    default_f_max = {'f_max': 300}

    def __init__(self, num_herb, num_carn):
        super().__init__(num_herb, num_carn)


class Desert(Landscape):

    def __init__(self, num_herb, num_carn):
        super().__init__(num_herb, num_carn)


class Water(Landscape):

    def __init__(self, num_herb, num_carn):
        super().__init__(num_herb, num_carn)