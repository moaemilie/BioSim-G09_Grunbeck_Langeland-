# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'


from biosim.animals import Animals
from biosim.animals import Herbivore
from biosim.animals import Carnivore
import pytest
import random
import math
import scipy.stats as stats
from unittest import mock

ALPHA = 0.05
random.seed(123456)

def test_set_parameters():
    """
    Test if the default parametres is being replaced by the new ones.
    """
    new_params = {'w_birth': 1, 'sigma_birth': 1, 'beta': 1, 'eta': 1, 'a_half': 1,
                      'phi_age': 1, 'w_half': 1, 'phi_weight': 1, 'mu': 1, 'gamma': 1,
                      'zeta': 1, 'xi': 1, 'omega': 1, 'F': 1, 'DeltaPhiMax': 1}

    Herbivore.set_params(new_params)
    assert Herbivore.default_params == new_params


def test_set_wrong_parameters():
    """
    Test that if the new parameters are wrong there will be raised a KeyError.
    """
    new_params = {'w_birth': 1, 'sigma_birth': 1, 'beta': 1, 'eta': 1, 'a_half': 1,
                      'phi_age': 1, 'w_half': 1, 'phi_weight': 1, 'mu': 1, 'gamma': 1,
                      'zeta': 1, 'xi': 1, 'omega': 1, 'F': 1, 'My': 1}

    with pytest.raises(KeyError):
        Herbivore.set_params(new_params)


def test_new_params():
    """
    Test that if the default params is being replaced by new params, that the new params is being used.
    """
    sheep1 = Herbivore({'age':5,'weight':6})
    sheep1.fitness()
    default_fitness = sheep1.fit

    new_params = {'w_birth': 1, 'sigma_birth': 1, 'beta': 1, 'eta': 1, 'a_half': 1,
                  'phi_age': 1, 'w_half': 1, 'phi_weight': 1, 'mu': 1, 'gamma': 1,
                  'zeta': 1, 'xi': 1, 'omega': 1, 'F': 1, 'DeltaPhiMax': 1}

    sheep2 = Herbivore({'age': 5, 'weight': 6})
    sheep2.set_params(new_params)
    sheep2.fitness()
    new_fitness = sheep2.fit

    assert not new_fitness == default_fitness


def test_animal_aging():
    """
    Tests that the aging function counts correctly
    """
    years = 4
    sheep = Herbivore({'age':0,'weight':2})

    for _ in range(years):
        sheep.aging()
    assert sheep.age == 4


def test_weightloss():
    """
    Test that the weightloss function returns the true value.
    """
    sheep = Herbivore({'age':4,'weight':30})
    delta_weight = 30 * sheep.default_params['eta']
    animal_weight = 30
    assert sheep.weightloss() == animal_weight - delta_weight


def test_animal_fitness():
    """
    Tests that the fitness always lies between 0 and 1
    """
    sheep = Herbivore({'age':4,'weight':30})
    assert sheep.fitness() >= 0 and sheep.fitness() <= 1


def test_low_animalweight_birth():
    """
    Test that the birth function return False if the animal weight it lower than the babyweight.
    """
    sheep = Herbivore({'age': 20,'weight': 1})
    assert not sheep.birth(10)


def test_birth_p0():
    """
    Test that the birth function returns False when there is only one animal. (propability of birth = 0).
    """
    sheep = Herbivore({'age': 10, 'weight': 30})
    assert not sheep.birth(1)


def test_birth_p1(mocker):
    """
    Test if the function birth() with a probability 1 always return True.
    """
    sheep = Herbivore({'age': 5, 'weight': 50})
    mocker.patch('biosim.animals.Carnivore.fitness', ReturnValue=0.1)
    assert sheep.birth(100)


def test_birth_t_test(mocker):
    """
    Using a one sample t-test to see if the birth mean is statisticaly different from a known mean.
    """
    stats.ttest_1samp(TestSample1, popmean=0)


def test_eating():
    """
    Tests that the eating function works as exspected.
    """
    sheep = Herbivore({'age':0,'weight':30})
    F_line = 2
    delta_eating = 2 * sheep.default_params['eta']
    new_weight = sheep.weight + delta_eating
    assert new_weight == sheep.eating(F_line)


def test_kill_p0():
    """
    Test that herbivore does not get killed if fitness is higher than the fitness of the carnivore
    """
    wolf = Carnivore({'age':5,'weight':10})
    sheep = Herbivore({'age':5,'weight':10})
    sheep.fitness()
    assert not wolf.kill(sheep.fit)


def test_kill_p1():
    """
    Test that if p=1 that the function always returns true.
    """
    wolf = Carnivore({'age':5,'weight':10})
    sheep = Herbivore({'age':5,'weight':1})

    new_params = {'w_birth': 6, 'sigma_birth': 1, 'beta': 0.75, 'eta': 0.125, 'a_half': 40,
                      'phi_age': 0.3, 'w_half': 4, 'phi_weight': 0.4, 'mu': 0.4, 'gamma': 0.8,
                      'zeta': 3.5, 'xi': 1.1, 'omega': 0.8, 'F': 50, 'DeltaPhiMax': 0.5}
    wolf.set_params(new_params)

    sheep.fitness()
    assert wolf.kill(sheep.fit)


def test_kill_when_zero_weight():
    """
    Test that if the carenvores weight is zero the kill function wil return False.
    """
    wolf = Carnivore({'age': 20, 'weight': 0})
    assert not wolf.kill(0.5)


def test_kill_when_negative_weight():
    """
    Test that if the carenvores weight is zero the kill function wil return False.
    """
    wolf = Carnivore({'age': 20, 'weight': -5})
    assert not wolf.kill(0.5)


def test_death_distribution():
    """
    Test if the number of animals that dies follows a normal distribution
    """
    num_animals = 100
    sheeps = [Herbivore({'age': random.randint(0, 50), 'weight': random.randint(0, 50)}) for _ in range(num_animals)]
    p_sum = 0
    n = 0

    for sheep in sheeps:
        sheep.fitness()
        p_sum += (sheep.default_params["omega"] * (1 - sheep.fit))
        n += sheep.death()

    p_mean = p_sum / num_animals

    norm_mean = num_animals * p_mean
    var = num_animals * p_mean * (1 - p_mean)

    Z = (n - norm_mean) / math.sqrt(var)
    phi = 2 * stats.norm.cdf(-abs(Z))

    assert phi > ALPHA


def test_weight_loss_death():
    """
    Test that if the the weight loss makes the weight is bellow zero that the animal dies.
    """
    sheep = Herbivore({'age':30,'weight':0})
    sheep.weightloss()
    assert sheep.death()


def test_death_certain():
    """
    Test that if the the weight is zero the animal dies.
    """
    sheep = Herbivore({'age': 4,'weight': 0})
    for _ in range(100):
        assert sheep.death()



