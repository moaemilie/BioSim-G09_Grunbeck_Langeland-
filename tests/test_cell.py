# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

from biosim.landscape import Landscape
from biosim.landscape import Lowland
import pytest
import random

random.seed(123456)


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
    N_herb = 10
    N_carn = 10
    cell = Lowland(N_herb, N_carn)

    assert cell.get_num_herb() == N_herb


def test_get_num_carn():
    """
    Tests if the right amount of carnivores is returned.
    """
    N_herb = 10
    N_carn = 10
    cell = Lowland(N_herb, N_carn)

    assert cell.get_num_carn() == N_carn


def test_fitness():
    """
    Tests that the fitness always lies between 0 and 1
    """

    assert