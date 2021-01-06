# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

import math


class Animals:
    animal_count = 0


    def __init__(self, age, weight, species):
        self.age = age
        self.weight = weight
        self.species = species
        self.count_new_animal()



class Herbivore(Animals):
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

    #def birth(self):




