# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

from biosim.island import Island
import pytest
import textwrap
import math
import random


@pytest.fixture
def new_island():
    geogr = """\
               WWWW
               WLLW
               WHLW
               WWWW"""
    geogr = textwrap.dedent(geogr)
    new_island = Island(geogr)
    new_island.make_map()
    return new_island


@pytest.fixture
def population():
    return [{'species': 'Herbivore', 'age': 5, 'weight': 20}], [{'species': 'Carnivore', 'age': 5, 'weight': 20}]


def test_wrong_map():
    """
    Test that you get a KeyError if there is a unknown letter in the map.
    """
    geogr = """\
               WWWW
               WLPW
               WHLW
               WWWW"""
    geogr = textwrap.dedent(geogr)
    new_island = Island(geogr)
    with pytest.raises(NameError):
        new_island.make_map()


def test_surrounded_by_water():
    """
        Test that you get a KeyError if the island is not surrounded by water.
        """
    geogr = """\
               WWWW
               WLLW
               WHLW
               WWLL"""
    geogr = textwrap.dedent(geogr)
    new_island = Island(geogr)
    with pytest.raises(ValueError):
        new_island.make_map()


def test_correct_num_row_col(new_island):
    """
    Test if correct amount of rows and columns are found.
    """
    assert (new_island.map_rows, new_island.map_rows) == (4, 4)


def test_add_animals_outside_map(new_island, population):
    """
    Test that you get an error if you place the animals outside the map.
    """
    with pytest.raises(IndexError):
        new_island.add_animals((5, 5), population[0], population[1])


def test_add_animals_in_water(new_island, population):
    """
    Test that you get an error if you place the animals in water.
    """
    with pytest.raises(ValueError):
        new_island.add_animals((1, 1), population[0], population[1])


def test_add_animals(new_island, population):
    new_island.add_animals((2, 2), population[0], population[1])
    num_herb = len(new_island.island_map[1][1].herb_pop)
    num_carn = len(new_island.island_map[1][1].carn_pop)
    assert num_herb == 1 and num_carn == 1


def test_get_num_herb(new_island, population):
    new_island.add_animals((2, 2), population[0], population[1])
    assert new_island.get_num_herb() == 1


def test_get_num_carn(new_island, population):
    new_island.add_animals((2, 2), population[0], population[1])
    assert new_island.get_num_carn() == 1


def test_aging(new_island, population):
    new_island.add_animals((2, 2), population[0], population[1])
    herb = new_island.island_map[1][1].herb_pop[0]
    carn = new_island.island_map[1][1].carn_pop[0]
    new_island.aging()
    assert (herb.age, carn.age) == (6, 6)


def test_weightloss(new_island, population):
    new_island.add_animals((2, 2), population[0], population[1])
    herb = new_island.island_map[1][1].herb_pop[0]
    carn = new_island.island_map[1][1].carn_pop[0]
    expected = (20 - (20 * herb.default_params['eta']), 20 - (20 * carn.default_params['eta']))
    new_island.weightloss()
    assert (herb.weight, carn.weight) == expected


def test_fitness(new_island, population):
    new_island.add_animals((2, 2), population[0], population[1])
    herb = new_island.island_map[1][1].herb_pop[0]
    carn = new_island.island_map[1][1].carn_pop[0]
    new_island.fitness()
    herb_expected_fit = (1 / (1 + math.exp(herb.default_params["phi_age"] * (herb.age - herb.default_params["a_half"])))
                         * (1 / (1 + math.exp((-herb.default_params["phi_weight"])
                                              * (herb.weight - herb.default_params["w_half"])))))
    carn_expected_fit = (1 / (1 + math.exp(carn.default_params["phi_age"] * (carn.age - carn.default_params["a_half"])))
                         * (1 / (1 + math.exp((-carn.default_params["phi_weight"])
                                              * (carn.weight - carn.default_params["w_half"])))))
    assert herb.fit == herb_expected_fit, carn.fit == carn_expected_fit


def test_feeding_herbivore(new_island, population):
    new_island.add_animals((2, 2), population[0], None)
    herb = new_island.island_map[1][1].herb_pop[0]
    herb_expected_weight = 20 + (herb.default_params["beta"] * herb.default_params['F'])
    new_island.feeding()
    assert herb.weight == herb_expected_weight


def test_feeding_carnivore(new_island, population, mocker):
    mocker.patch('biosim.animals.Carnivore.kill', ReturnValue=True)

    new_island.add_animals((2, 2), population[0], population[1])
    herb = new_island.island_map[1][1].herb_pop[0]
    carn = new_island.island_map[1][1].carn_pop[0]
    carn_expected_weight = 20 + (
                carn.default_params["beta"] * (20 + (herb.default_params["beta"] * herb.default_params['F'])))
    new_island.feeding()

    assert carn.weight == carn_expected_weight, new_island.island_map[1][1].get_num_herb == 0


def test_death_prob(new_island, population, mocker):

    mocker.patch('biosim.animals.Animals.death', ReturnValue=True)

    new_island.add_animals((2, 2), population[0], population[1])
    new_island.death()

    assert new_island.get_num_herb() == 0, new_island.get_num_carn() == 0


def test_death_zero_weight(new_island, population):

    new_island.add_animals((2, 2), population[0], population[1])
    new_island.death()
    herb = new_island.island_map[1][1].herb_pop[0]
    carn = new_island.island_map[1][1].carn_pop[0]
    herb.weight = 0
    carn.weight = 0
    new_island.death()

    assert new_island.get_num_herb() == 0, new_island.get_num_carn() == 0


def test_birth(new_island, mocker):

    mocker.patch('biosim.animals.Animals.birth', ReturnValue=True)

    new_island.add_animals((2, 2), [{'species': 'Herbivore', 'age': 5, 'weight': 20}, {'species': 'Herbivore', 'age': 5, 'weight': 20}],
                           [{'species': 'Carnivore', 'age': 5, 'weight': 20}, {'species': 'Carnivore', 'age': 5, 'weight': 20}])

    for animal in new_island.island_map[1][1].herb_pop + new_island.island_map[1][1].carn_pop:
        animal.babyweight = 20

    new_island.birth()

    assert new_island.get_num_herb() == 2 * 2, new_island.get_num_carn() == 2 * 2


def test_actually_move(new_island, population, mocker):

    mocker.patch('biosim.animals.Animals.move_animal', ReturnValue=True)

    new_island.add_animals((2, 2), population[0], population[1])

    new_island.move_island()

    num_in_cell = new_island.island_map[1][1].get_num_herb() + new_island.island_map[1][1].get_num_carn()
    num_on_island = new_island.get_num_herb() + new_island.get_num_carn()

    assert num_in_cell == 0, num_on_island == 2


def test_move_in_chosen_direction(new_island, population, mocker):

    new_island.add_animals((2, 2), population[0], population[1])

    mocker.patch('biosim.island.Island.move_island.choose_neighbor', ReturnValue=new_island.island_map[2][1])

    new_island.move_island()

    num_in_cell_pre_move = new_island.island_map[1][1].get_num_herb() + new_island.island_map[1][1].get_num_carn()
    num_in_cell_post_move = new_island.island_map[2][1].get_num_herb() + new_island.island_map[2][1].get_num_carn()
    num_on_island = new_island.get_num_herb() + new_island.get_num_carn()

    assert num_in_cell_pre_move == 0, num_in_cell_post_move == 2


def test_animal_not_move_to_water():
    geogr = """\
               WWW
               WHW
               WWW"""
    geogr = textwrap.dedent(geogr)
    new_island = Island(geogr)
    new_island.make_map()

    new_island.add_animals((2,2), [{'species': 'Herbivore', 'age': 5, 'weight': 20}], [{'species': 'Carnivore', 'age': 5, 'weight': 20}] )


    cell = new_island.island_map[1][1]
    for year in range(10):
        new_island.move_island()
        assert (len(cell.herb_pop)) == 1


def test_move_animal():


    geogr = """\
               WWW
               WHW
               WWW"""
    geogr = textwrap.dedent(geogr)
    new_island = Island(geogr)
    new_island.make_map()

    new_island.add_animals((2,2), [{'species': 'Herbivore', 'age': 5, 'weight': 20}], [{'species': 'Carnivore', 'age': 5, 'weight': 20}] )

    counter = 0
    years = 10

    for year in range(years):
        new_island.move()
        counter += 1

    assert counter == 1