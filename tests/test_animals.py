
from biosim.animals import Animals
from biosim.animals import Herbivore
import pytest
import random
import math
import statistics as stats
ALPHA = 0.05
random.seed(123456)

def test_sett_parameters():
    """
    Test if the default parametres is being replaced by the new ones.
    """
    new_params = {'w_birth': 1, 'sigma_birth': 1, 'beta': 1, 'eta': 1, 'a_half': 1,
                      'phi_age': 1, 'w_half': 1, 'phi_weight': 1, 'mu': 1, 'gamma': 1,
                      'zeta': 1, 'xi': 1, 'omega': 1, 'F': 1, 'DeltaPhiMax': 1}

    Animals.set_params(new_params)
    assert Animals.default_params == new_params


def test_sett_wring_parameters():
    """
    Test if the new parameters are wrong there wil be raised a KeyError.
    """
    new_params = {'w_birth': 1, 'sigma_birth': 1, 'beta': 1, 'eta': 1, 'a_half': 1,
                      'phi_age': 1, 'w_half': 1, 'phi_weight': 1, 'mu': 1, 'gamma': 1,
                      'zeta': 1, 'xi': 1, 'omega': 1, 'F': 1, 'My': 1}

    with pytest.raises(KeyError):
        Animals.set_params(new_params)


def test_new_params():
    """
    Test that if the default params is being replaced by new params, that the new params is being used.
    """
    sheep1 = Herbivore(5,6)
    sheep1.fitness()
    default_fitness = sheep1.fit

    new_params = {'w_birth': 1, 'sigma_birth': 1, 'beta': 1, 'eta': 1, 'a_half': 1,
                  'phi_age': 1, 'w_half': 1, 'phi_weight': 1, 'mu': 1, 'gamma': 1,
                  'zeta': 1, 'xi': 1, 'omega': 1, 'F': 1, 'DeltaPhiMax': 1}

    sheep2 = Herbivore(5,6)
    sheep2.set_params(new_params)
    sheep2.fitness()
    new_fitness = sheep2.fit

    assert not new_fitness == default_fitness

def test_animal_aging():
    """
    Tests that the aging function counts correctly
    """
    years = 4
    sheep = Herbivore(0,2)

    for _ in range(years):
        sheep.aging()
    assert sheep.age == 4


def test_animal_fitness():
    """
    Tests that the fitness always lies between 0 and 1
    """
    sheep = Herbivore(4,30)
    assert sheep.fitness() >= 0 and sheep.fitness() <= 1


def test_weightloss():
    """
    Test that the weightloss function returns the true value.
    """
    sheep = Herbivore(4, 30)
    delta_weight = 30 * sheep.eta
    animal_weight = 30
    assert sheep.weightloss() == animal_weight - delta_weight


def test_weight_loss_death():
    """
    Test that if the the weight loss makes the weight is bellow zero that the animal dies.
    """
    sheep = Herbivore(30, 0)
    sheep.weightloss()
    assert sheep.death()


def test_death_certain():
    """
    Test that if the the weight is zero the animal dies.
    """
    sheep = Herbivore(4,0)
    for _ in range(100):
        assert sheep.death()


def test_eating():
    """
    Tests that the eating function works as exspected.
    """
    sheep = Herbivore(0, 30)
    F_line = 2
    delta_eating = 2 * sheep.beta
    new_weight = sheep.weight + delta_eating
    assert new_weight == sheep.eating(F_line)


#def test_low_animalweight_birth():
    #"""
    #Test that the birth function return False if the animal weight it lower than the babyweight.
    #"""
    #sheep = Herbivore(20,1)
        #assert sheep.birth() == False



#def test_birth_p0():
    #"""
    #Test that the birth function returns False when there is only one animal. (propability of birth = 0).
    #"""
    #sheep = Herbivore(0, 30)
    #assert sheep.birth(1) == False


#def test_death_distribution():
    #"""
    #Test if the number of animals that dies follows a normal distribution
    #Må finne hva sannsynlighetene konvergerer mot
    #"""
    #num_animals = 100
    #sheeps = [Herbivore(random.randint(0, 50), random.randint(0, 50)) for _ in range(num_animals)]
    #p = []
    #for sheep in sheeps:
    #    sheep.fitness()
    #    p.append(sheep.weight*(1-sheep.fit))

    #p_mean = stats.mean(p)
    #norm_mean = num_animals * p_mean

    #var = num_animals * p_mean * (1 - p_mean)
    #Z = (num_animals - norm_mean) / math.sqrt(var)
    #phi = 2 * stats.norm.cdf(-abs(Z))
    #assert phi > ALPHA








#def test_birth_distribution():
    #"""
    #Test if the number of animals thats added follows a binomial distribution
    #"""





