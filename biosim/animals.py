# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

import math
import random



class Animals:
    w_birth = None
    sigma_birth = None
    beta = None
    eta = None
    a_half = None
    phi_age = None
    w_half = None
    phi_weight = None
    mu = None
    gamma = None
    zeta = None
    xi = None
    omega = None
    F = None
    DeltaPhiMax = None

    default_params = {'w_birth': w_birth, 'sigma_birth': sigma_birth, 'beta': beta, 'eta': eta, 'a_half': a_half,
                      'phi_age': phi_age, 'w_half': w_half, 'phi_weight': phi_weight, 'mu': mu, 'gamma': gamma,
                      'zeta': zeta, 'xi': xi, 'omega': omega, 'F': F, 'DeltaPhiMax': DeltaPhiMax}

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
        cls.default_params = new_params

    def __init__(self, age, weight):
        self.age = age
        self.weight = weight
        self.fit = self.fitness()

    def fitness(self):
        """
        Calculates the fitness of the animals.

        Returns
        -------
        Float
            with new fitness between 0 and 1
        """
        if self.weight <= 0:
            self.fit = 0
        else:
            self.fit = (1 / (1 + math.exp(self.phi_age * (self.age - self.a_half)))) * (1 / (1 + math.exp((-self.phi_weight) * (self.weight - self.w_half))))
        return self.fit

    def aging(self):
        """
        Adds one year every time its called.

        Returns
        -------
        Int
            with number of years
        """
        self.age += 1
        return self.age

    def weightloss(self):
        """
        Calculates the weight of an animal.

        Returns
        -------
        Int
            with weight for the animal
        """
        self.weight -= self.weight * self.eta
        return self.weight

    def death(self):
        """
        Decides if an animal should die or not.

        Returns
        -------
        Bool
                True if animal dies
        """
        if self.weight <= 0:
            p_death = 1.0
        else:
            p_death = (self.omega*(1-self.fit))
        return random.random() <= p_death

    def eating(self, F_line):
        """
        Animal gains a sertan amount every year by eating.

        Parameters
        ----------
        F_line: int
            with the amount of food consumed by an animal.

        Returns
        -------
        int
            New weight of animal
        """
        self.weight += self.beta * F_line
        return self.weight

    def birth(self, p_birth):
        """
        Desides if a ned animal should be added to the simulation.

        Input
        -------
        int
            with probability of birth

        Returns
        -------
        Bool
                True if animal should be added.
        """
        baby_weight = random.gauss(self.w_birth, self.sigma_birth)
        if self.weight < self.zeta*(self.w_birth + self.sigma_birth) or self.weight < baby_weight:
            p_birth = 0
        chance = random.random() <= p_birth
        if chance == True:
            self.weight -= baby_weight * self.xi
        return chance, baby_weight







class Herbivore(Animals):
    w_birth = 8
    sigma_birth = 1.5
    beta = 0.9
    eta = 0.05
    a_half = 40
    phi_age = 0.6
    w_half = 10
    phi_weight = 0.1
    mu = 0.25
    gamma = 0.2
    zeta = 3.5
    xi = 1.2
    omega = 0.4
    F = 10
    DeltaPhiMax = None

    default_params = {'w_birth': w_birth, 'sigma_birth': sigma_birth, 'beta': beta, 'eta': eta, 'a_half': a_half,
                      'phi_age': phi_age, 'w_half': w_half, 'phi_weight': phi_weight, 'mu': mu, 'gamma': gamma,
                      'zeta': zeta, 'xi': xi, 'omega': omega, 'F': F, 'DeltaPhiMax': DeltaPhiMax}

    def __init__(self, age, weight):
        super().__init__(age, weight)


