
from biosim.animals import Herbivore

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
    Test that if the the weight loss makes the weight zero or bellow zero that the animal dies.
    """
    sheep = Herbivore(0, 30)
    sheep.weightloss()
    assert sheep.death() == True

def test_eating():
    sheep = Herbivore(0, 30)
    F_line = 2
    delta_eating = 2 * sheep.beta
    new_weight = sheep.weight + delta_eating
    assert new_weight == sheep.eating(F_line)

