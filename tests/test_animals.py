
from biosim.animals import Herbivore
import numpy as np

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


def test_low_animalweight_birth():
    """
    Test that the birth function return False if the animal weight it lower than the babyweight.
    """
    sheep = Herbivore(20,1)
    for N in range(20):
        p_birth = min(1, sheep.gamma * sheep.fit * (N - 1))
        assert sheep.birth(p_birth) == False

def test_low_babyweight():
    """
    Test that the birth function returns False if the babyweight is lower than a constant.
    """
    sheep = Herbivore(30, 20)
    baby_weight = sheep.zeta * (sheep.w_birth + sheep.sigma_birth)
    for N in range(20):
        while baby_weight > 0:
            baby_weight -= 1
            p_birth = min(1, sheep.gamma * sheep.fit * (N - 1))
            assert sheep.birth(p_birth) == False


def test_birth_healthy_animal():
    """
    Test that the birth function only returns False with a possibility of p_birth.
    """

    for year in range(500):
        sheep = Herbivore(30, 50)
        assert sheep.birth(1)


