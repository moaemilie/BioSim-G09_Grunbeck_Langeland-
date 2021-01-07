
from biosim.animals import Animals

def test_animal_aging():
    """
    Tests that the aging function counts correctly
    """
    years = 4
    Zebra = Animals(0,2,'Herbivore')

    for _ in range(years):
        Zebra.aging()
    assert Zebra.age == 4


def test_animal_fitnes():

    Lion = Animals(4,30,'Herbivore')
    assert Lion.fitness() < 0 and Lion.fitness() > 1