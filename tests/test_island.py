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


def test_wrong_map_letter():
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
    with pytest.raises(ValueError):
        new_island.make_map()


def test_wrong_map_row_length():
    """
    Test that you get a KeyError if the rows of the map input have different lengths.
    """
    geogr = """\
               WWWW
               WLLHW
               WHLW
               WWWW"""
    geogr = textwrap.dedent(geogr)
    new_island = Island(geogr)
    with pytest.raises(ValueError):
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


def test_correct_num_row_col():
    """
    Test if correct amount of rows and columns are found.
    """
    geogr = """\
               WWWW
               WLLW
               WHLW
               WHHW
               WWWW"""
    geogr = textwrap.dedent(geogr)
    new_island = Island(geogr)
    new_island.make_map()
    assert (new_island.map_rows, new_island.map_columns) == (5, 4)


def test_add_animals_outside_map(new_island, population):
    """
    Test that you get an error if you place the animals outside the map.
    """
    with pytest.raises(ValueError):
        new_island.add_animals_island((5, 4), population[0], population[1])


def test_add_animals_in_water(new_island, population):
    """
    Test that you get an error if you place the animals in water.
    """
    with pytest.raises(ValueError):
        new_island.add_animals_island((1, 1), population[0], population[1])


def test_add_animals(new_island, population):
    new_island.add_animals_island((2, 2), population[0], population[1])
    num_herb = len(new_island.island_map[1][1].herb_pop)
    num_carn = len(new_island.island_map[1][1].carn_pop)
    assert num_herb == 1 and num_carn == 1


def test_get_num_herb(new_island, population):
    new_island.add_animals_island((2, 2), population[0], population[1])
    assert new_island.get_num_herb_island() == 1


def test_get_num_carn(new_island, population):
    new_island.add_animals_island((2, 2), population[0], population[1])
    assert new_island.get_num_carn_island() == 1


def test_aging(new_island, population):
    new_island.add_animals_island((2, 2), population[0], population[1])
    herb = new_island.island_map[1][1].herb_pop[0]
    carn = new_island.island_map[1][1].carn_pop[0]
    new_island.aging_island()
    assert (herb.age, carn.age) == (6, 6)


def test_weightloss(new_island, population):
    new_island.add_animals_island((2, 2), population[0], population[1])
    herb = new_island.island_map[1][1].herb_pop[0]
    carn = new_island.island_map[1][1].carn_pop[0]
    expected = (20 - (20 * herb.default_params['eta']), 20 - (20 * carn.default_params['eta']))
    new_island.weightloss_island()
    assert (herb.weight, carn.weight) == expected


def test_fitness(new_island, population):
    new_island.add_animals_island((2, 2), population[0], population[1])
    herb = new_island.island_map[1][1].herb_pop[0]
    carn = new_island.island_map[1][1].carn_pop[0]
    new_island.fitness_island()
    herb_expected_fit = (1 / (1 + math.exp(herb.default_params["phi_age"] * (herb.age - herb.default_params["a_half"])))
                         * (1 / (1 + math.exp((-herb.default_params["phi_weight"])
                                              * (herb.weight - herb.default_params["w_half"])))))
    carn_expected_fit = (1 / (1 + math.exp(carn.default_params["phi_age"] * (carn.age - carn.default_params["a_half"])))
                         * (1 / (1 + math.exp((-carn.default_params["phi_weight"])
                                              * (carn.weight - carn.default_params["w_half"])))))
    assert herb.health == herb_expected_fit, carn.health == carn_expected_fit


def test_feeding_herbivore(new_island, population):
    new_island.add_animals_island((2, 2), population[0], None)
    herb = new_island.island_map[1][1].herb_pop[0]
    herb_expected_weight = 20 + (herb.default_params["beta"] * herb.default_params['F'])
    new_island.feeding_island()
    assert herb.weight == herb_expected_weight


def test_feeding_carnivore(new_island, population, mocker):
    mocker.patch('biosim.animals.Carnivore.kill', ReturnValue=True)

    new_island.add_animals_island((2, 2), population[0], population[1])
    herb = new_island.island_map[1][1].herb_pop[0]
    carn = new_island.island_map[1][1].carn_pop[0]
    carn_expected_weight = 20 + (
                carn.default_params["beta"] * (20 + (herb.default_params["beta"] * herb.default_params['F'])))
    new_island.feeding_island()

    assert carn.weight == carn_expected_weight, new_island.island_map[1][1].get_num_herb == 0


def test_death_prob(new_island, population, mocker):

    mocker.patch('biosim.animals.Animals.death_animal', ReturnValue=True)

    new_island.add_animals_island((2, 2), population[0], population[1])
    new_island.death_island()

    assert new_island.get_num_herb_island() == 0, new_island.get_num_carn_island() == 0


def test_death_zero_weight(new_island, population):

    new_island.add_animals_island((2, 2), population[0], population[1])
    new_island.death_island()
    herb = new_island.island_map[1][1].herb_pop[0]
    carn = new_island.island_map[1][1].carn_pop[0]
    herb.weight = 0
    carn.weight = 0
    new_island.death_island()

    assert new_island.get_num_herb_island() == 0, new_island.get_num_carn_island() == 0


def test_birth(new_island, mocker):

    mocker.patch('biosim.animals.Animals.birth_animal', ReturnValue=True)

    new_island.add_animals_island((2, 2), [{'species': 'Herbivore', 'age': 5, 'weight': 20}, {'species': 'Herbivore', 'age': 5, 'weight': 20}],
                                  [{'species': 'Carnivore', 'age': 5, 'weight': 20}, {'species': 'Carnivore', 'age': 5, 'weight': 20}])

    for animal in new_island.island_map[1][1].herb_pop + new_island.island_map[1][1].carn_pop:
        animal.babyweight = 20

    new_island.birth_island()

    assert new_island.get_num_herb_island() == 2 * 2, new_island.get_num_carn_island() == 2 * 2


def test_actually_move(population, mocker):
    geogr = """\
               WWWWWW
               WHHLLW
               WLHHLW
               WHHLLW
               WWWWWW"""
    geogr = textwrap.dedent(geogr)
    new_island = Island(geogr)
    new_island.make_map()

    mocker.patch('biosim.animals.Animals.move_animal', ReturnValue=True)

    new_island.add_animals_island((3, 3), population[0], population[1])

    new_island.move_island()
    new_island.add_immigrants_island()

    num_in_cell = new_island.island_map[2][2].get_num_herb_landscape() + new_island.island_map[1][1].get_num_carn_landscape()
    num_on_island = new_island.get_num_herb_island() + new_island.get_num_carn_island()

    assert num_in_cell == 0, num_on_island == 2


def test_animal_not_move_to_water(population):
    geogr = """\
               WWW
               WHW
               WWW"""
    geogr = textwrap.dedent(geogr)
    new_island = Island(geogr)
    new_island.make_map()

    new_island.add_animals_island((2, 2), population[0], population[1])

    for year in range(10):
        new_island.move_island()
        new_island.add_immigrants_island()
        assert (len(new_island.island_map[1][1].herb_pop)) == 1


def test_move_to_neighbor_cells(population, mocker):
    geogr = """\
               WWWWWW
               WHHLLW
               WLHHLW
               WHHLLW
               WWWWWW"""
    geogr = textwrap.dedent(geogr)
    new_island = Island(geogr)
    new_island.make_map()

    mocker.patch('biosim.animals.Animals.move_animal', ReturnValue=True)
    new_island.add_animals_island((3, 3), population[0])
    new_island.move_island()
    new_island.add_immigrants_island()
    num_in_neighbor_cells = sum([new_island.island_map[3][4].get_num_herb_landscape(), new_island.island_map[3][2].get_num_herb_landscape(),
                                 new_island.island_map[2][3].get_num_herb_landscape(), new_island.island_map[4][3].get_num_herb_landscape()])
    assert num_in_neighbor_cells == 1


# def test_move_only_once_a_year(new_island, population, mocker):
#
#     mocker.patch('biosim.animals.Animals.move_animal', ReturnValue=True)
#
#     new_island.add_animals((2,2), [{'species': 'Herbivore', 'age': 5, 'weight': 20}], [{'species': 'Carnivore', 'age': 5, 'weight': 20}] )
#     herb = new_island.island_map[1][1].herb_pop[0]
#     carn = new_island.island_map[1][1].carn_pop[0]
#
#     for year in range(years):
#         new_island.move_island()
#     [new_island.move_island() for year in range(10)]
#     assert


#def test_animals_move_differently(new_island, population):