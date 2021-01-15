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
    new_island.find_num_row_col()
    return new_island


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


def test_find_num_row_col(new_island):
    """
    Test if correct amount of rows and columns are found.
    """
    assert new_island.find_num_row_col() == (4, 4)


def test_add_animals_outside_map(new_island):
    """
    Test that you get an error if you place the animals outside the map.
    """
    with pytest.raises(ValueError):
        new_island.add_animals((5, 5), [{'species': 'Herbivore', 'age': 5, 'weight': 20}], [{'species': 'Carnivore', 'age': 5, 'weight': 20}])


def test_add_animals_in_water(new_island):
    """
    Test that you get an error if you place the animals in water.
    """
    with pytest.raises(ValueError):
        new_island.add_animals((1, 1), [{'species': 'Herbivore', 'age': 5, 'weight': 20}], [{'species': 'Carnivore', 'age': 5, 'weight': 20}])


def test_add_animals(new_island):
    new_island.add_animals((2, 2), [{'species': 'Herbivore', 'age': 5, 'weight': 20}], [{'species': 'Carnivore', 'age': 5, 'weight': 20}])
    num_herb = len(new_island.island_map[2 - 1][2 - 1].herb_pop)
    num_carn = len(new_island.island_map[2 - 1][2 - 1].carn_pop)
    assert num_herb == 1 and num_carn == 1


def test_get_num_herb(new_island):
    new_island.add_animals((2, 2), [{'species': 'Herbivore', 'age': 5, 'weight': 20}], [{'species': 'Carnivore', 'age': 5, 'weight': 20}])
    assert new_island.get_num_herb() == 1

# def test_move(new_island):
#    assert pass
