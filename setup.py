'''
Setup file for BioSim package.

To create a package, run

python setup.py sdist

in the directory containing this file.

To create a zip archive, run

python setup.py sdist --formats=zip

The package will be placed in directory dist.

To install from the package, unpack it, move into the unpacked directory and
run

python setup.py install          # default location
python setup.py install --user   # per-user default location

See also
    http://docs.python.org/distutils
    http://docs.python.org/install
    http://guide.python-distribute.org/creation.html

'''

__author__ = 'Emilie Giltvedt Langeland & Lina Grünbeck / NMBU'

from setuptools import setup

setup(name='BioSim',
      version='0.1',
      description='A Simple Simulation of Animals on an Island.',
      author='Emilie Giltvedt Langeland & Lina Grünbeck / NMBU',
      requires=['matplotlib', 'numpy', 'random', 'math', 'textwrap', 'subprocess'],
      packages=['biosim'],
      scripts=['examples/example_simulation.py', 'examples/example_animals.py'],
      )
