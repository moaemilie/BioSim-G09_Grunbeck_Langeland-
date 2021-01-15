# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

import math
import random

random.seed(123456)


class Animals:
    default_params = {'w_birth': None, 'sigma_birth': None, 'beta': None, 'eta': None, 'a_half': None,
                      'phi_age': None, 'w_half': None, 'phi_weight': None, 'mu': None, 'gamma': None,
                      'zeta': None, 'xi': None, 'omega': None, 'F': None, 'DeltaPhiMax': None}

    @classmethod
    def set_params(cls, new_params):
        """
        Sets new parametres.

        Parameters
        ----------
        new_params: dict
            New parametres

        Returns
        -------
        dict
            Dictionary with new class parameters.
    """
        for key in new_params:
            if key not in ('w_birth', 'sigma_birth', 'beta', 'eta', 'a_half',
                           'phi_age', 'w_half', 'phi_weight', 'mu', 'gamma',
                           'zeta', 'xi', 'omega', 'F', 'DeltaPhiMax'):
                raise KeyError('Invalid parameter name: ' + key)
            else:
                cls.default_params[key] = new_params[key]

    def __init__(self, animal_info):
        self.age = animal_info['age']
        self.weight = animal_info['weight']
        self.fit = self.fitness()
        self.babyweight = None
        self.fodder = None



    def aging(self):
        """
        Adds one year every time its called.

        Returns
        -------
        Int
            with number of years
        """
        self.age += 1



    def weightloss(self):
        """
        Calculates the weight of an animal.

        Returns
        -------
        Int
            with weight for the animal
        """
        if self.weight <= 0:
            self.death()
        else:
            self.weight -= self.weight * self.default_params["eta"]



    def fitness(self):
        """
        Calculates the fitness of an animal.

        Returns
        -------
        Float
            with new fitness between 0 and 1
        """
        if self.weight <= 0:
            self.fit = 0
        else:
            self.fit = (1 / (
                        1 + math.exp(self.default_params["phi_age"] * (self.age - self.default_params["a_half"]))) *
                        (1 / (1 + math.exp((-self.default_params["phi_weight"]) *
                                           (self.weight - self.default_params["w_half"])))))
        return self.fit


    def birth(self, n):
        """
        Decides if a new animal should be added to the simulation.

        Input
        -------
        int
                with probability of birth

        Returns
        -------
        Bool
                True if animal should be added.
        """
        baby_weight = random.gauss(self.default_params["w_birth"], self.default_params["sigma_birth"])

        p_birth = min(1, self.default_params["gamma"] * self.fit * (n - 1))

        if self.weight < self.default_params["zeta"] * (
                self.default_params["w_birth"] + self.default_params["sigma_birth"]) or self.weight < baby_weight:
            p_birth = 0
        chance = random.random() <= p_birth
        if chance:
            self.weight -= baby_weight * self.default_params["xi"]
            self.babyweight = baby_weight
        return chance


    def eating(self, fodder):
        """
        Animal gains a certain amount every year by eating.

        Parameters
        ----------
        fodder: int
                with the amount of food consumed by an animal.

        Returns
        -------
        int
            New weight of animal
        """
        self.weight += self.default_params["beta"] * fodder


    def death(self):
        """
        Decides if an animal should die or not.

        Returns
        -------
        Bool
                True if animal dies
        """
        if self.weight <= 0 or self.age < 0:
            p_death = 1
        else:
            p_death = (self.default_params["omega"] * (1 - self.fit))
        return random.random() <= p_death


class Herbivore(Animals):
    default_params = {'w_birth': 8, 'sigma_birth': 1.5, 'beta': 0.9, 'eta': 0.05, 'a_half': 40,
                      'phi_age': 0.6, 'w_half': 10, 'phi_weight': 0.1, 'mu': 0.25, 'gamma': 0.2,
                      'zeta': 3.5, 'xi': 1.2, 'omega': 0.4, 'F': 10, 'DeltaPhiMax': None}

    def __init__(self, animal_info):
        super().__init__(animal_info)


class Carnivore(Animals):
    default_params = {'w_birth': 6, 'sigma_birth': 1, 'beta': 0.75, 'eta': 0.125, 'a_half': 40,
                      'phi_age': 0.3, 'w_half': 4, 'phi_weight': 0.4, 'mu': 0.4, 'gamma': 0.8,
                      'zeta': 3.5, 'xi': 1.1, 'omega': 0.8, 'F': 50, 'DeltaPhiMax': 10}

    def __init__(self, animal_info):
        super().__init__(animal_info)

    def kill(self, fit_herb):
        """
        Tests if the carnivore can kill a herbivore.

        Input
        -------
        int
                fitness of a herbivore

        Returns
        -------
        Bool
                True if carnivore can kill.
        """
        if fit_herb >= self.fit or self.weight <= 0:
            p_kill = 0
        elif 0 < self.fit - fit_herb < self.default_params["DeltaPhiMax"]:
            p_kill = (self.fit - fit_herb) / (self.default_params["DeltaPhiMax"])
        else:
            p_kill = 1
        return random.random() <= p_kill
