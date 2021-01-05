# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'



class Animals:

    animal_count = 0


    @classmethod
    def count_new_animal(cls):
        cls.animal_count += 1

    @classmethod
    def num_animals(cls):
        return cls.animal_count

    def __init__(self, age, weight, species):
        self.age = age
        self.weight = weight
        self.species = species

        if self.species == 'Herbivore' or 'herbivore':
            class Herbivore(Animals):

                def __init__(self, age, weight):
                    self.age = age
                    self.weight = weight
                    self.w_birth = 8


                def fitness(self):



                def feeding(self):



                def birth(self):












