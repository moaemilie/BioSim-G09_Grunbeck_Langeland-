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

@pytest.fixture
def herb():
    herb = Herbivore({'age': 7, 'weight': 10})
    return herb

@pytest.fixture
def carn():
    carn = Carnivore({'age': 7, 'weight': 10})
    return carn


@pytest.fixture
def reset_animal_defaults():
    # no setup
    yield
    Herbivore.set_params({'w_birth': 8.,
                          'sigma_birth': 1.5,
                          'beta': 0.9,
                          'eta': 0.05,
                          'a_half': 40.,
                          'phi_age': 0.6,
                          'w_half': 10.,
                          'phi_weight': 0.1,
                          'mu': 0.25,
                          'gamma': 0.2,
                          'zeta': 3.5,
                          'xi': 1.2,
                          'omega': 0.4,
                          'F': 10.})
    Carnivore.set_params({'w_birth': 6.,
                          'sigma_birth': 1.0,
                          'beta': 0.75,
                          'eta': 0.125,
                          'a_half': 40.,
                          'phi_age': 0.3,
                          'w_half': 4.,
                          'phi_weight': 0.4,
                          'mu': 0.4,
                          'gamma': 0.8,
                          'zeta': 3.5,
                          'xi': 1.1,
                          'omega': 0.8,
                          'F': 50.,
                          'DeltaPhiMax': 10.})



def test_set_parameters(reset_animal_defaults):
    """
    Test if the default parametres is being replaced by the new ones.
    """
    new_params = {'w_birth': 1, 'sigma_birth': 1, 'beta': 1, 'eta': 1, 'a_half': 1,
                      'phi_age': 1, 'w_half': 1, 'phi_weight': 1, 'mu': 1, 'gamma': 1,
                      'zeta': 1, 'xi': 1, 'omega': 1, 'F': 1, 'DeltaPhiMax': 1}

    Herbivore.set_params(new_params)
    assert Herbivore.default_params == new_params


def test_set_wrong_parameters(reset_animal_defaults):
    """
    Test that if the new parameters are wrong there will be raised a KeyError.
    """
    new_params = {'w_birth': 1, 'sigma_birth': 1, 'beta': 1, 'eta': 1, 'a_half': 1,
                      'phi_age': 1, 'w_half': 1, 'phi_weight': 1, 'mu': 1, 'gamma': 1,
                      'zeta': 1, 'xi': 1, 'omega': 1, 'F': 1, 'My': 1}

    with pytest.raises(KeyError):
        Herbivore.set_params(new_params)


def test_new_params(herb, reset_animal_defaults):
    """
    Test that if the default params is being replaced by new params, that the new params is being used.
    """
    sheep = herb
    sheep_default_fitness = (1 / (1 + math.exp(0.6 * (5 - 40))) *(1 / (1 + math.exp((-0.1) *(6 - 10)))))

    new_params = {'a_half': 50}
    sheep.set_params(new_params)

    assert sheep.fitness_animal() != sheep_default_fitness


def test_animal_aging(herb, carn):
    """
    Tests that the aging function counts correctly
    """
    years = 4

    sheep = herb
    wolf = carn

    for _ in range(years):
        sheep.aging_animal()
        wolf.aging_animal()
    assert sheep.age == 11 and wolf.age == 11


def test_weightloss(herb):
    """
    Test that the weightloss function returns the true value.
    """
    sheep = herb
    delta_weight = sheep.weight * sheep.default_params['eta']
    start_weight = sheep.weight
    sheep.weightloss_animal()
    assert sheep.weight == start_weight - delta_weight


def test_animal_fitness(herb):
    """
    Tests that the fitness always lies between 0 and 1
    """
    sheep = herb
    for year in range(10):
        sheep.weight += 1
        sheep.age += 1
        assert sheep.fitness_animal() >= 0 and sheep.fitness_animal() <= 1


def test_low_animalweight_birth(herb):
    """
    Test that the birth function return False if the animal weight it lower than the babyweight * xi.
    """
    sheep = herb
    sheep.set_params({'xi': 0.1})
    assert not sheep.birth_animal(10)


def test_birth_p0(herb, carn):
    """
    Test that the birth function returns False when there is only one animal. (propability of birth = 0).
    """
    sheep = herb
    wolf = carn
    assert not sheep.birth_animal(1) and not wolf.birth_animal(1)


def test_birth_p1(herb, mocker):
    """
    Test if the function birth() with a probability 1 always return True.
    """
    sheep = Herbivore({'age': 5, 'weight': 50})
    mocker.patch('biosim.animals.Carnivore.fitness_animal', ReturnValue=0.1)
    assert sheep.birth_animal(100)


def test_birth_t_test(mocker):
    """
    Using a one sample t-test to see if the pobability of geting anything else than 0.5 when sat p = 0.5 is very low.
    """

    n = 100
    TestSample1 = []
    alpa = 0.05
    sheeps = [Herbivore({'age':5,'weight':10}) for _ in range(n)]
    for round in range(100):
        for sheep in sheeps:
            mocker.patch('biosim.animals.Carnivore.fitness_animal', ReturnValue=0.5/((n-1)*0.2))
            if sheep.birth_animal(n) == True:
                TestSample1.append(1)
            else:
                TestSample1.append(0)
    result = stats.ttest_1samp(TestSample1, 0.5)
    pvalue = result[1]
    assert pvalue < alpa


def test_eating_weightgain(herb):
    """
    Tests that the animal gains the correct value afther eating
    """
    sheep = herb
    fodder = 2
    first_weight = sheep.weight
    delta_weight = fodder * sheep.default_params['beta']
    new_weight = first_weight + delta_weight
    sheep.eating_animal(fodder)
    assert new_weight == sheep.weight


def test_kill_p0():
    """
    Test that herbivore does not get killed if its fitness is higher than the fitness of the carnivore
    """
    wolf = Carnivore({'age':1,'weight':1})
    sheep = Herbivore({'age':20,'weight':10})
    wolf.health = 0.2
    sheep.health = 0.9
    assert not wolf.kill(sheep.health)


def test_kill():
    """
    Test that herbivore does not get killed if fitness is higher than the fitness of the carnivore
    """
    wolf = Carnivore({'age':5,'weight':10})
    sheep = Herbivore({'age':5,'weight':10})
    wolf.fitness_animal()
    sheep.fitness_animal()
    for year in range(5):
        assert not wolf.kill(sheep.health)


def test_kill_p1(reset_animal_defaults):
    """
    Test that if p=1 that the function always returns true.
    """
    wolf = Carnivore({'age':5,'weight':10})
    sheep = Herbivore({'age':5,'weight':1})

    new_params = {'DeltaPhiMax': 0.5}
    wolf.set_params(new_params)

    sheep.fitness_animal()
    assert wolf.kill(sheep.health)


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
        sheep.fitness_animal()
        p_sum += (sheep.default_params["omega"] * (1 - sheep.health))
        n += sheep.death_animal()

    p_mean = p_sum / num_animals

    norm_mean = num_animals * p_mean
    var = num_animals * p_mean * (1 - p_mean)

    Z = (n - norm_mean) / math.sqrt(var)
    phi = 2 * stats.norm.cdf(-abs(Z))

    assert phi > ALPHA


def test_weight_loss_death():
    """
    Test that the animal dies if the weight loss makes the weight go bellow zero.
    """
    sheep = Herbivore({'age':30,'weight':0})
    sheep.weightloss_animal()
    assert sheep.death_animal()


def test_death_certain():
    """
    Test that if the the weight is zero the animal dies.
    """
    sheep = Herbivore({'age': 4,'weight': 0})
    for _ in range(100):
        assert sheep.death_animal()


def test_move_animal(reset_animal_defaults):
    """
    Test that the animal moves if the the formula for p_move equals 1.
    """
    sheep = Herbivore({'age': 4,'weight': 10})
    sheep.health = 0.5
    sheep.set_params({'mu': (1 / sheep.health)})
    assert sheep.move_animal()




