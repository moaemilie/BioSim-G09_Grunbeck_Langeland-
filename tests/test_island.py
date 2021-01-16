# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

from biosim.island import Island
import pytest
import textwrap


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
    new_island.aging()
    assert (new_island.island_map[1][1].herb_pop[0].age, new_island.island_map[1][1].carn_pop[0].age) == (6, 6)

def test_weightloss(new_island, population):
    new_island.add_animals((2, 2), population[0], population[1])
    new_island.weightloss()
    herb_eta = new_island.island_map[1][1].herb_pop[0].default_params['eta']
    carn_eta = new_island.island_map[1][1].carn_pop[0].default_params['eta']
    expected = (20-(20*herb_eta), 20-(20*carn_eta))
    assert (new_island.island_map[1][1].herb_pop[0].weight, new_island.island_map[1][1].carn_pop[0].weight) == expected

#def test_fitness(new_island, population):
#    new_island.add_animals((2, 2), population[0], population[1])
#    new_island.fitness()
#    assert

def test_birth(new_island, population, mocker):
    new_island.add_animals((2, 2), population[0], population[1])

    def mock_birth(self, n):
        return True

    mocker.patch('biosim.animals.Herbivore.birth', mock_birth)
    mocker.patch('biosim.animals.Carnivore.birth', mock_birth)
    new_island.birth()

    assert (new_island[1][1].get_num_herb + 1, new_island[1][1].get_num_carn + 1) == (2, 2)


def feeding(new_island, population):
    new_island.add_animals((2, 2), population[0], population[1])
    new_island.feeding()
    assert

def death(new_island, population):
    new_island.add_animals((2, 2), population[0], population[1])
    new_island.feeding()
    assert


# def test_move(new_island):
#    assert pass
