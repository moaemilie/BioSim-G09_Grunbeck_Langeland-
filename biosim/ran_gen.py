# -*- coding: utf-8 -*-

"""
Random generator.
"""

__author__ = 'Hans Ekkehard Plesser'
__email__ = 'hans.ekkehard.plesser@nmbu.no'


def list_rng(numbers):
    """
    Generator returning successive elements of numbers.
    """
    
    for n in numbers:
        yield n


def lcg_rng(seed):
    """
    Generator implementation of a linear congruential RNG.
    """
    
    r = seed
    a = 7**5
    m = 2**31 - 1

    while True:
        r = (a * r) % m
        yield r


if __name__ == '__main__':

    lig = list_rng([10, 20, 30])
    lcg = lcg_rng(123432)

    for _ in range(4):
        print(next(lig), next(lcg))
