# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

from biosim.animals import Herbivore
from biosim.animals import Carnivore
import random




class Landscape:
    default_f_max = {'f_max': None}

    @classmethod
    def set_f_max(cls, params):
        """
        Sets new f_max parameter.
        """

        for key in params:
            if key != 'f_max':
                raise KeyError('Invalid parameter name: ' + key)
        cls.default_f_max = params

    def __init__(self, ini_herbs=[], ini_carns=[]):
        self.herb_pop = [Herbivore(ini_herbs[animal]) for animal in range(len(ini_herbs))]
        self.carn_pop = [Carnivore(ini_carns[animal]) for animal in range(len(ini_carns))]
        self.herb_immigrants = []
        self.carn_immigrants = []

    @staticmethod
    def set_animal_parameters(species, params):
        animals = {'Herbivore': Herbivore, 'Carnivore': Carnivore}
        animals[species].set_params(params)

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

    def aging_landscape(self):
        """
        Adds a year for all animals in the population for every time its called.
        """
        for herb in self.herb_pop: # Vi zipper, null carn -> Null vekttap TAKKET VÆRE AMIR ∑
            herb.aging_animal()
            herb.fitness_animal()

        for carn in self.carn_pop:  # Vi zipper, null carn -> Null vekttap TAKKET VÆRE AMIR ∑
            carn.aging_animal()
            carn.fitness_animal()

    def weightloss_landscape(self):
        """

        """
        for herb in self.herb_pop: # Vi zipper, null carn -> Null vekttap TAKKET VÆRE AMIR ∑
            herb.weightloss_animal()
            herb.fitness_animal()

        for carn in self.carn_pop:  # Vi zipper, null carn -> Null vekttap TAKKET VÆRE AMIR ∑
            carn.weightloss_animal()
            carn.fitness_animal()

    def fitness_landscape(self):
        """
        Calculates the fitness for every animal in the population.
        """
        for herb, carn in zip(self.herb_pop, self.carn_pop):
            herb.fitness_animal()
            carn.fitness_animal()

    def birth_landscape(self):
        """
        Adds new animals to the population.
        """

        def herb_newborns(pop):
            return [Herbivore({'species': 'Herbivore',
                               'age': 0,
                               'weight': parent.babyweight}) for parent in pop if parent.birth_animal(self.get_num_herb())]

        def carn_newborns(pop):
            return [Carnivore({'species': 'Herbivore',
                               'age': 0,
                               'weight': parent.babyweight}) for parent in pop if parent.birth_animal(self.get_num_carn())]

        self.herb_pop.extend(herb_newborns(self.herb_pop))
        self.carn_pop.extend(carn_newborns(self.carn_pop))

    def eating_landscape(self):
        """
        Feeds herbivores and carnivores in a cell.
        """

        fodder = self.default_f_max['f_max']
        random.shuffle(self.herb_pop)

        for herb in self.herb_pop:
            if fodder == 0:
                break
            if herb.weight > 0:
                if fodder >= herb.default_params["F"]:
                    herb.eating_animal(herb.default_params["F"])
                    fodder -= herb.default_params["F"]
                elif fodder < herb.default_params["F"] and fodder != 0:
                    herb.eating_animal(fodder)
                    fodder = 0
                herb.fitness_animal()

        def sort_pop(pop, reverse=False):
            for j in reversed(range(len(pop))):
                for k in range(j):
                    if pop[k + 1].fit < pop[k].fit and reverse is False:
                        pop[k], pop[k + 1] = pop[k + 1], pop[k]
                    elif pop[k + 1].fit > pop[k].fit and reverse is True:
                        pop[k], pop[k + 1] = pop[k + 1], pop[k]
            return pop

        self.herb_pop = sort_pop(self.herb_pop)
        self.carn_pop = sort_pop(self.carn_pop, reverse=True)

        for carn in self.carn_pop:
            carn_fodder = 0
            dead_herb = []
            for herb in self.herb_pop:
                if carn.kill(herb.fit) and carn_fodder + herb.weight <= carn.default_params["F"]:
                    carn.eating_animal(herb.weight)
                    dead_herb.append(herb)
                    carn_fodder += herb.weight
                    carn.fitness_animal()
                #elif carn_fodder + herb.weight > carn.default_params["F"]:
                   # break
            self.herb_pop = [herbo for herbo in self.herb_pop if herbo not in dead_herb]

    def death_landscape(self):
        """
        Updates the populations with the animals that survive.

        """

        def survivors(pop):
            return [animal for animal in pop if not animal.death_animal()]

        self.herb_pop = survivors(self.herb_pop)
        self.carn_pop = survivors(self.carn_pop)

    def move_landscape(self):
        """
        Decides if the landscape is water.

        Returns
        -------
        Bool
                True if landscape is not water.
        """
        return not isinstance(self, Water)

    def add_immigrants_landscape(self):
        """
        adds immigrants to the two populations
        """
        self.herb_pop.extend(self.herb_immigrants)
        self.carn_pop.extend(self.carn_immigrants)
        self.herb_immigrants = []
        self.carn_immigrants = []

    def add_animals_landscape(self, new_herbs=None, new_carns=None):
        """
        Adds new animals to the two populations.
        """
        if new_herbs is None:
            new_herbs = []
        elif new_carns is None:
            new_carns = []
        self.herb_pop.extend([Herbivore(new_herbs[animal]) for animal in range(len(new_herbs))])
        self.carn_pop.extend([Carnivore(new_carns[animal]) for animal in range(len(new_carns))])


class Lowland(Landscape):
    default_f_max = {'f_max': 800}

    def __init__(self, ini_herbs=[], ini_carns=[]):
        super().__init__(ini_herbs, ini_carns)


class Highland(Landscape):
    default_f_max = {'f_max': 300}

    def __init__(self, ini_herbs=[], ini_carns=[]):
        super().__init__(ini_herbs, ini_carns)


class Desert(Landscape):
    default_f_max = {'f_max': 0}

    def __init__(self, ini_herbs=[], ini_carns=[]):
        super().__init__(ini_herbs, ini_carns)


class Water(Landscape):
    default_f_max = {'f_max': 0}

    def __init__(self, ini_herbs=[], ini_carns=[]):
        super().__init__(ini_herbs, ini_carns)
