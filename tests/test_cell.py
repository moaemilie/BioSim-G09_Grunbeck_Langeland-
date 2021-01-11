# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

from biosim.cell import Cell
from biosim.cell import Lowland
import pytest
import random

random.seed(123456)


def test_set_f_max():
    """
    Tests if the default f_max is being replaced by the new one.
    """
    new_f_max = {'f_max': 1}

    Cell.set_f_max(new_f_max)
    assert Cell.default_f_max == new_f_max


def test_set_right_f_max():
    """
    Tests that a KeyError is raised if the new f_max has a wrong key input.
    """
    new_f_max = {'f': 1}

    with pytest.raises(KeyError):
        Cell.set_f_max(new_f_max)
