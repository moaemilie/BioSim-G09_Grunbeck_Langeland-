
from biosim.animals import Animals
from biosim.animals import Herbivore
import pytest

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
    #for N in range(20):
        #p_birth = min(1, sheep.gamma * sheep.fit * (N - 1))
        #assert sheep.birth(p_birth) == False



#def test_birth():
    #"""
    #Test that the birth function only returns True when propability of birth = 1.
    #"""




#def test_death_distribution():



