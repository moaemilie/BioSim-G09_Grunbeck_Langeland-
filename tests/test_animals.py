
from biosim.animals import Animals

class testAnimals:

    def test_animal_count(self, Animal):
        """
        Tests if the animal counter counts correct.
        """

        # set all members to their initial value

        animals = [Animals(1, 5, 'Herbivore'), Animals(1,2,'Herbivore')]
        assert Animals.num_animals() == len(animals)

