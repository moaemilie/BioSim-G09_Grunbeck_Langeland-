
from biosim.animals import Animals

def test_animal_aging():
    years = 4
    Zebra = Animals(0,2,'Herbivore')

    for _ in range(years):
        Zebra.aging()
    assert Zebra.age == 4

