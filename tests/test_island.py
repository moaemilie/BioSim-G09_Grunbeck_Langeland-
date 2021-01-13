# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

from biosim.island import Island
import pytest
import textwrap


def test_wrong_map():
    """
    Test that you get a KeyError if there is a unknown letter in the map.
    """
    geogr = """\
                WWWWWWWWWWWWWWWWWWWWW
                WWWWWWWWHWWPWLLLLLLLW
                WHHHHHLLLLWWLLLLLLLWW
                WHHHHHHHHHWWLLLLLLWWW
                WHHHHHLLLLLLLLLLLLWWW
                WHHHHHLLLDDLLLHLLLWWW
                WHHLLLLLDDDLLLHHHHWWW
                WWHHHHLLLDDLLLHWWWWWW
                WHHHLLLLLDDLLLLLLLWWW
                WHHHHLLLLDDLLLLWWWWWW
                WWHHHHLLLLLLLWWWWWWWW
                WWWHHHHLLLLLLLWWWWWWW
                WWWWWWWWWWWWWWWWWWWWW"""
    geogr = textwrap.dedent(geogr)
    new_island = Island(geogr)
    with pytest.raises(NameError):
        new_island.make_map()


def test_surrounded_by_water():
    """
        Test that you get a KeyError if the island is not surrounded by water.
        """
    geogr = """\
               WWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWHWWWWLLLLLLLW
               WHHHHHLLLLWWLLLLLLLWW
               WHHHHHHHHHWWLLLLLLWWW
               WHHHHHLLLLLLLLLLLLWWW
               WHHHHHLLLDDLLLHLLLWWW
               WHHLLLLLDDDLLLHHHHWWW
               WWHHHHLLLDDLLLHWWWWWW
               WHHHLLLLLDDLLLLLLLWWW
               WHHHHLLLLDDLLLLWWWWWW
               WWHHHHLLLLLLLLWWWWWWW
               WWWHHHHLLLLLLLWWWWWWW
               WWWWWWWWWWWWWWWWWWWLL"""
    geogr = textwrap.dedent(geogr)
    new_island = Island(geogr)
    with pytest.raises(ValueError):
        new_island.make_map()


def test_find_num_row_col():
    geogr = """\
               WWWW
               WLLW
               WHLW
               WWWW"""
    geogr = textwrap.dedent(geogr)
    new_island = Island(geogr)
    new_island.make_map()
    assert new_island.find_num_row_col() == (4, 4)

def test_add_animals_outside_map():
    """
    Test that you get an error if you place the animals outside the map.
    """
    geog = """\
            WWW
            WHW
            WWW"""
    geog = textwrap.dedent(geog)

    new_island = Island(geog)
    new_island.make_map()
    new_island.find_num_row_col()

    with pytest.raises(ValueError):
        new_island.add_animals((6, 6), 5, 5)

def test_add_animals_in_water():
    """
    Test that you get an error if you place the animals in water.
    """
    geog = """\
            WWW
            WHW
            WWW"""
    geog = textwrap.dedent(geog)

    new_island = Island(geog)
    new_island.make_map()
    new_island.find_num_row_col()

    with pytest.raises(ValueError):
        new_island.add_animals((1, 1), 5, 5)

