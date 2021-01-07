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
        if self.weight <= 0:
            self.fit = 0
        else:
            self.fit = (1 / (1 + math.exp(self.phi_age * (self.age - self.a_half)))) * (1 / (1 + math.exp((-self.phi_weight) * (self.weight - self.w_half))))
        return self.fit

    def aging(self):
        self.age += 1

    def weightloss(self):
        self.weight -= self.weight * self.eta
        return self.weight

    def death(self):
        if self.weight <= 0:
            p_death = 1.0
        else:
            p_death = (self.omega*(1-self.fit))
        return random.random() <= p_death

    def eating(self, F_line):
        self.weight += self.beta * F_line
        return self.weight

    #def birth(self):
        #Animals()


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


