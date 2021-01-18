# -*- encoding: utf-8 -*-
"""

"""

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

import textwrap
from biosim.simulation import BioSim
import pytest

@pytest.fixture
def set_geog():
    geogr = """\
WWWW
WLDW
WHLW
WWWW
"""
    geogr = textwrap.dedent(geogr)
    return geogr

def set_ini_pop(species):
    ini_herbs = [{'loc': (10, 10),
                  'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(5)]}]

    ini_carns = [{'loc': (10, 10),
                  'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20} for _ in range(5)]}]

    if species == 'Herbivore':
        return ini_herbs
    elif species == 'Carnivore':
        return ini_carns

def test_year():
    """
    Tests that the property year that it shows right year
    """
    sim = BioSim("WWWW\nWLDW\nWHLW\nWWWW", [], seed = 1)
    sim.simulate(5)

    assert sim.year == 5


    #sim = BioSim("WWWW\nWLDW\nWHLW\nWWWW", [{'loc': (2, 2),
                  #'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(5)]}], seed = 1)
