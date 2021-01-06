# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

import math


class Animals:




    def __init__(self, age, weight, species):
        self.age = age
        self.weight = weight
        self.species = species
        self.count_new_animal()

    def birth(self):
        Animals()



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

    default_params = {'w_birth': w_birth, 'sigme_birth': sigma_birth, 'beta': beta, 'eta': eta, 'a_half': a_half,
                      'phi_age': phi_age, 'w_half': w_half, 'phi_weight': phi_weight, 'mu': mu, 'gamma': gamma,
                      'zeta': zeta, 'xi': xi, 'omega': omega, 'F': F, 'DeltaPhiMax': DeltaPhiMax}

    def __init__(self, age, weight, species):
        super().__init__(age, weight, species)


    def __init__(self, age, weight):
        self.age = age
        self.weight = weight
        self.w_birth = 8
        self.sigma_birth = 1.5
        self.beta = 0.9
        self.eta = 0.05
        self.a_half = 40
        self.phi_age = 0.6
        self.w_half = 10
        self.phi_weight = 0.1
        self.mu = 0.25
        self.gamma = 0.2
        self.zeta = 3.5
        self.xi = 1.2
        self.omega = 0.4
        self.F = 10
        self.DeltaPhiMax = None

        self.fit = 0

    def fitness(self):
        if self.weight <= 0:
            self.fit = 0
        else:
            self.fit = (1/(1+math.exp(self.phi_age*(self.age-self.a_half)))) * (1/(1+math.exp(-self.phi_weight*(self.weight-self.w_half))))
            return self.fit

    #def feeding(self):
        #self.weight







