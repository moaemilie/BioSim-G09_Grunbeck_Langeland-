# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

from biosim.island import Island
import pytest

def test_wrong_map():
    """
    Test that you get a KeyError if its a unknown letter in the map
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
                WWHHHHLLLLLLLWWWWWWW
                WWWHHHHLLLLLLLWWWWWWW
                WWWWWWWWWWWWWWWWWWWWW"""
    new_island = Island(geogr)
    with pytest.raises(KeyError):
        new_island.make_map()