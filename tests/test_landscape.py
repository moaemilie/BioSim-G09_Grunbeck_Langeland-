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

import pytest_mock

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


def test_aging_negative_age():
    """
    Test that the if input age is negative the animals wil die
    """
    herb_info = [{'age': -5, 'weight': 6}, ]
    carn_info = [{'age': -20, 'weight': 6}, ]
    landscape = Lowland(herb_info, carn_info)

    landscape.death()

    assert len(landscape.herb_pop) == 0 and len(landscape.carn_pop) == 0


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


def test_weightloss():
    """
    Test that the weight is lower after the weight loss function
    """
    herb_info = [{'age': 5, 'weight': 6},]
    carn_info = [{'age': 20, 'weight': 6},]
    landscape = Lowland(herb_info, carn_info)

    sheep = landscape.herb_pop[0]
    wolf = landscape.carn_pop[0]

    herb_first_weight = sheep.weight
    carn_first_weight = wolf.weight

    landscape.weightloss()

    assert sheep.weight < herb_first_weight and wolf.weight < carn_first_weight


def test_weightloss_zero_weight():
    """
    Test that the weight doesent become negative
    """
    herb_info = [{'age': 5, 'weight': 0},]
    carn_info = [{'age': 20, 'weight': 0},]
    landscape = Lowland(herb_info, carn_info)

    sheep = landscape.herb_pop[0]
    wolf = landscape.carn_pop[0]

    landscape.weightloss()

    assert sheep.weight >= 0 and wolf.weight >= 0


def test_fitness():
    """
    Tests that the fitness always lies between 0 and 1
    """
    herb_info = [{'age': 5, 'weight': 6}, {'age': 10, 'weight': 5}]
    carn_info = [{'age': 20, 'weight': 6}, {'age': 3, 'weight': 7}]
    landscape = Lowland(herb_info, carn_info)
    assert [0 <= herb.fitness() <= 1 for herb in landscape.herb_pop] and [0 <= carn.fitness() <= 1 for carn in
                                                                          landscape.carn_pop]


def test_birth():
    """
    Test that there wil be born animals for both carnivores and herbivores, when they are healthy.
    """
    herb_info = [{'age': 20, 'weight': 50}, {'age': 30, 'weight': 60}, {'age': 20, 'weight': 70},
                 {'age': 10, 'weight': 10}, {'age': 30, 'weight': 30}, {'age': 20, 'weight': 9}]
    carn_info = [{'age': 20, 'weight': 50}, {'age': 30, 'weight': 60}, {'age': 20, 'weight': 70},
                 {'age': 10, 'weight': 10}, {'age': 30, 'weight': 30}, {'age': 20, 'weight': 9}]

    landscape = Highland(herb_info, carn_info)
    n_herbs = landscape.get_num_herb()
    n_carns = landscape.get_num_carn()

    for year in range(1000):
        landscape.birth()

    n_herbs_afther = landscape.get_num_herb()
    n_carns_afther = landscape.get_num_carn()

    assert n_herbs < n_herbs_afther and n_carns < n_carns_afther


def test_birth_p1(mocker):
    """
    Test that there wil be added an animal if its 100% likely that birth function in animal returns True.
    """


    herb_info = [{'age': 20, 'weight': 50}]
    carn_info = [{'age': 10, 'weight': 10}]

    landscape = Highland(herb_info, carn_info)
    sheep = landscape.herb_pop[0]
    mocker.patch('biosim.animals.Herbivore.birth', ReturnValue = True)
    sheep.babyweight = 9

    landscape.birth()

    assert len(landscape.herb_pop) == 2


def test_feeding_herb_no_weight():
    """
    Test that a herbivore does not eat when his weight is 0 or less.
    """
    landscape = Lowland([{'age': 5, 'weight': 0}], [])
    sheep = landscape.herb_pop[0]
    start_weight = sheep.weight

    landscape.feeding()
    end_weight = sheep.weight

    assert start_weight == end_weight


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
    new_params = {'F': 100}
    sheep.set_params(new_params)

    landscape.feeding()

    assert sheep.fodder == 50


def test_no_food_left():
    """
    Test that if an animal eats the rest of the food its nothing left
    """
    animal_info = [{'age': 5, 'weight': 6}]

    landscape = Highland(animal_info, [])
    sheep = landscape.herb_pop[0]

    new_f_max = {'f_max': 50}
    landscape.set_f_max(new_f_max)
    new_params = {'F': 100}
    sheep.set_params(new_params)

    landscape.feeding()

    assert landscape.default_f_max['f_max'] == 0


def test_feeding_to_much_food():
    """
    Test that if its to much food the function eats F and leaves the food that's left.
    """
    animal_info = [{'age': 5, 'weight': 6}]

    landscape = Highland(animal_info, [])
    sheep = landscape.herb_pop[0]

    new_f_max = {'f_max': 500}
    landscape.set_f_max(new_f_max)

    new_params = {'F': 100}
    sheep.set_params(new_params)

    landscape.feeding()

    assert landscape.default_f_max['f_max'] == 500 - sheep.default_params['F']


def test_herb_feed_dessert():
    """
    Tests that the herbivore doesnt eat anything in the dessert
    """
    animal_info = [{'age': 5, 'weight': 6}]

    landscape = Desert(animal_info, [])
    sheep = landscape.herb_pop[0]

    weight_first = sheep.weight

    landscape.feeding()

    assert sheep.weight == weight_first


def test_herb_feeding_sorting():
    """
    Test that herbivores are sorted reversed by their fitness in the feeding function
    """
    herb_info = [{'age': 1, 'weight': 1}, {'age': 2, 'weight': 2}, {'age': 3, 'weight': 3}]
    carn_info = [{'age': 1, 'weight': 1}, {'age': 2, 'weight': 2}, {'age': 3, 'weight': 3}]

    landscape = Highland(herb_info, carn_info)

    landscape.feeding()

    herb1 = landscape.herb_pop[0]
    herb2 = landscape.herb_pop[1]
    herb3 = landscape.herb_pop[2]

    herb1.fitness()
    herb2.fitness()
    herb3.fitness()

    assert herb1.fit < herb2.fit < herb3.fit


def test_carn_feeding_sorting():
    """
    Test that Carnevore are sorted by their fitness in the feeding function
    """
    herb_info = [{'age': 1, 'weight': 1}, {'age': 2, 'weight': 2}, {'age': 3, 'weight': 3}]
    carn_info = [{'age': 1, 'weight': 1}, {'age': 2, 'weight': 2}, {'age': 3, 'weight': 3}]

    landscape = Highland(herb_info, carn_info)

    landscape.feeding()

    carn1 = landscape.carn_pop[0]
    carn2 = landscape.carn_pop[1]
    carn3 = landscape.carn_pop[2]

    carn1.fitness()
    carn2.fitness()
    carn3.fitness()

    assert carn1.fit > carn2.fit > carn3.fit


def test_carn_weight_zero():
    """
    Test that the herbivore doesnt die if the carnevore weight is zero.
    """
    herb_info = [{'age': 1, 'weight': 1}]
    carn_info = [{'age': 5, 'weight': 0}]

    landscape = Highland(herb_info, carn_info)
    sheep = landscape.herb_pop[0]

    landscape.feeding()

    assert sheep.weight != 0


def test_carn_kill(mocker):
    """
    Test that if a carnevore kills a herbevore that the herbevore is removed from the population
    """
    herb_info = [{'age': 1, 'weight': 1}]
    carn_info = [{'age': 30, 'weight': 30}]

    landscape = Highland(herb_info, carn_info)

    mocker.patch('biosim.animals.Carnivore.kill', ReturnValue = True)

    landscape.feeding()

    assert len(landscape.herb_pop) == 0


def test_carn_gain_weight(mocker):
    """
    Test that the carnivore gains the correct weight after eating a herbivore
    """
    herb_info = [{'age': 1, 'weight': 1}]
    carn_info = [{'age': 30, 'weight': 30}]

    landscape = Highland(herb_info, carn_info)

    mocker.patch('biosim.animals.Carnivore.kill', ReturnValue = True)

    sheep = landscape.herb_pop[0]
    wolf = landscape.carn_pop[0]

    new_f_max = {'f_max': 0}

    landscape.set_f_max(new_f_max)

    landscape.feeding()

    assert wolf.weight == 30 + wolf.default_params["beta"] * 1


def test_carn_appetite(mocker):
    """
    Tests that the carnevore stops eating after its full.
    """
    herb_info = [{'age': 1, 'weight': 7}, {'age': 1, 'weight': 7}, {'age': 1, 'weight': 7}]
    carn_info = [{'age': 30, 'weight': 30}]

    landscape = Highland(herb_info, carn_info)

    mocker.patch('biosim.animals.Carnivore.kill', ReturnValue=True)

    wolf = landscape.carn_pop[0]

    wolf.set_params({'F': 5})

    landscape.feeding()

    assert len(landscape.herb_pop) == 2


def test_herb_death():
    """
    Test that the herbivores with zero weight and dies random is removed from the population
    """
    herb_info = [{'age': 1, 'weight': 0}, {'age': 1, 'weight': 5}]
    carn_info = []

    landscape = Highland(herb_info, carn_info)
    num_herb_before = len(landscape.herb_pop)

    landscape.death()

    num_herb_after = len(landscape.herb_pop)

    assert num_herb_before > num_herb_after


def test_carn_death():
    """
    Test that the carnivores with zero weight and dies random is removed from the population
    """
    herb_info = []
    carn_info = [{'age': 1, 'weight': 0}, {'age': 1, 'weight': 5}]

    landscape = Highland(herb_info, carn_info)
    num_carn_before = len(landscape.carn_pop)

    landscape.death()

    num_carn_after = len(landscape.carn_pop)

    assert num_carn_before > num_carn_after


def test_move_not_water():
    """
    Test that move_landscape returns True if the landscape type is not water.
    """
    herb_info = [{'age': 1, 'weight': 10}, {'age': 1, 'weight': 50}]
    carn_info = [{'age': 1, 'weight': 10}, {'age': 1, 'weight': 50}]

    landscape = Highland(herb_info, carn_info)

    assert landscape.move_landscape()


def test_move_water():
    """
    Test that move_landscape returns False if the landscape type is water.
    """
    herb_info = [{'age': 1, 'weight': 10}, {'age': 1, 'weight': 50}]
    carn_info = [{'age': 1, 'weight': 10}, {'age': 1, 'weight': 50}]

    landscape = Water(herb_info, carn_info)

    assert not landscape.move_landscape()


def test_immigants_added():
    """
    Test that the immigrants are added to the population
    """
    herb_info = []
    carn_info = []

    landscape = Highland(herb_info, carn_info)

    landscape.herb_immigrants = [{'age': 30, 'weight': 30}]
    landscape.carn_immigrants = [{'age': 30, 'weight': 30}]


    landscape.add_immigrants()

    assert len(landscape.herb_pop) == 1 and len(landscape.carn_pop) == 1


def test_add_immigrants_default_value():
    """
    Test that you can sett nothing as innpult and the default value wil be used
    """

    landscape = Highland()


    landscape.herb_immigrants = [{'age': 30, 'weight': 30}]
    landscape.carn_immigrants = [{'age': 30, 'weight': 30}]

    landscape.add_immigrants()

    assert len(landscape.herb_pop) == 1 and len(landscape.carn_pop) == 1


def test_add_animals():
    """
    Tests that the new animals are added to the list with old animales.
    """
    herb_info = [{'age': 1, 'weight': 1}]
    carn_info = [{'age': 1, 'weight': 1}]

    landscape = Highland(herb_info, carn_info)

    new_herbs = [{'age': 2, 'weight': 2}]
    new_carns = [{'age': 2, 'weight': 2}]

    landscape.add_animals(new_herbs, new_carns)

    assert len(landscape.herb_pop) == 2 and len(landscape.carn_pop) == 2

