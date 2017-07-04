import os
from setuptools import setup
from packageinfo import NAME, VERSION

# main setup configuration class
setup(
    name=NAME,
    version=VERSION,
    author='SimPhoNy Project',
    description='LAMMPS, LIGGGHTS and non-simphony python interface',
    zip_safe=False,
    )
