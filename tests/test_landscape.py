# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

from biosim.landscape import Landscape
from biosim.landscape import Lowland
import pytest
import random

random.seed(123456)
from biosim.landscape import Landscape
from biosim.landscape import Lowland
from biosim.landscape import Highland
from biosim.landscape import Desert
from biosim.landscape import Water

from biosim.animals import Herbivore
from biosim.animals import Carnivore

def test_set_f_max():
    """
    Tests if the default f_max is being replaced by the new one.
    """
    new_f_max = {'f_max': 1}

    Landscape.set_f_max(new_f_max)
    assert Landscape.default_f_max == new_f_max


def test_set_right_f_max():
    """
    Tests that a KeyError is raised if the new f_max has a wrong key input.
    """
    new_f_max = {'f': 1}

    with pytest.raises(KeyError):
        Landscape.set_f_max(new_f_max)


def test_get_num_herb():
    """
    Tests if the right amount of herbivores is returned.
    """
    herb_info = [{'age': 5, 'weight': 6}, {'age': 10, 'weight': 5}]
    carn_info = [{'age': 20, 'weight': 6}, {'age': 3, 'weight': 7}]
    N_herb = 2
    landscape = Lowland(herb_info, carn_info)

    assert landscape.get_num_herb() == N_herb


def test_get_num_carn():
    """
    Tests if the right amount of carnivores is returned.
    """
    herb_info = [{'age': 5, 'weight': 6}, {'age': 10, 'weight': 5}]
    carn_info = [{'age': 20, 'weight': 6}, {'age': 3, 'weight': 7}]
    N_carn = 2
    landscape = Lowland(herb_info, carn_info)

    assert landscape.get_num_carn() == N_carn


def test_fitness():
    """
    Tests that the fitness always lies between 0 and 1
    """
    herb_info = [{'age': 5, 'weight': 6}, {'age': 10, 'weight': 5}]
    carn_info = [{'age': 20, 'weight': 6}, {'age': 3, 'weight': 7}]
    landscape = Lowland(herb_info, carn_info)
    assert [0 <= herb.fitness() <= 1 for herb in landscape.herb_pop] and [0 <= carn.fitness() <= 1 for carn in
                                                                          landscape.carn_pop]


def test_aging():
    """
    Test that correct number of years are added
    """
    years = 5
    landscape = Landscape([{'age': 5, 'weight': 6}], [{'age': 10, 'weight': 5}])
    herb_age = landscape.herb_pop[0].age
    carn_age = landscape.carn_pop[0].age

    for _ in range(years):
        landscape.aging()

    herb_new_age = landscape.herb_pop[0].age
    carn_new_age = landscape.carn_pop[0].age

    herb_delta_age = herb_new_age - herb_age
    carn_delta_age = carn_new_age - carn_age

    assert carn_delta_age == years and herb_delta_age == years


def test_aging_higher():
    """
    Test that the age doesnt become lower than the initial age after the function aging.
    """
    years = 10
    landscape = Landscape([{'age': 5, 'weight': 6}], [{'age': 10, 'weight': 5}])
    herb_age = landscape.herb_pop[0].age
    carn_age = landscape.carn_pop[0].age

    for _ in range(years):
        landscape.aging()

    herb_new_age = landscape.herb_pop[0].age
    carn_new_age = landscape.carn_pop[0].age

    assert herb_new_age > herb_age and carn_new_age > carn_age


def test_feeding_herb_no_weight():
    """
    Test that a herbivore does not eat when his weight is 0 or less.
    """
    landscape = Lowland([{'age': 5, 'weight': 0}], [])

    landscape.feeding()


def test_feeding_no_food():
    """
    Test that the animal doesnt eat if the F is zero.
    """
    animal_info = [{'age': 5, 'weight': 6}]

    landscape = Highland(animal_info, [])
    sheep = landscape.herb_pop[0]
    sheep.fitness()
    fitness_before = sheep.fit

    new_f_max = {'f_max': 0}
    landscape.set_f_max(new_f_max)
    landscape.feeding()

    sheep.fitness()
    fitness_afther = sheep.fit

    assert fitness_before == fitness_afther


def test_feeding_little_food():
    """
    Test that if its to little food the animal eats the food that's left.
    """
    animal_info = [{'age': 5, 'weight': 6}]

    landscape = Highland(animal_info, [])
    sheep = landscape.herb_pop[0]

    new_f_max = {'f_max': 50}
    landscape.set_f_max(new_f_max)
    new_params = {'w_birth': 8, 'sigma_birth': 1.5, 'beta': 0.9, 'eta': 0.05, 'a_half': 40,
                      'phi_age': 0.6, 'w_half': 10, 'phi_weight': 0.1, 'mu': 0.25, 'gamma': 0.2,
                      'zeta': 3.5, 'xi': 1.2, 'omega': 0.4, 'F': 100, 'DeltaPhiMax': None}
    sheep.set_params(new_params)

    landscape.feeding()

    assert sheep.fodder == landscape.default_f_max['f_max']


def test_feeding_to_much_food():
    """
    Test that if its to much food the function eats F and leaves the food that's left.
    """
    animal_info = [{'age': 5, 'weight': 6}]

    landscape = Highland(animal_info, [])
    sheep = landscape.herb_pop[0]

    new_f_max = {'f_max': 500}
    landscape.set_f_max(new_f_max)

    new_params = {'w_birth': 8, 'sigma_birth': 1.5, 'beta': 0.9, 'eta': 0.05, 'a_half': 40,
                  'phi_age': 0.6, 'w_half': 10, 'phi_weight': 0.1, 'mu': 0.25, 'gamma': 0.2,
                  'zeta': 3.5, 'xi': 1.2, 'omega': 0.4, 'F': 100, 'DeltaPhiMax': None}
    sheep.set_params(new_params)

    landscape.feeding()

    assert landscape.default_f_max['f_max'] == 500 - sheep.default_params['F']
