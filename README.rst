Build Recipe: LAMMPS Python
---------------------------

This recipe builds the Enthought egg for LAMMPS. It provides a python layer and a compiled library.

Provisioning
------------

Machine supported: CentOS 6.5.
To collect the necessary dependencies for installation, do::

    make provision

Usage
-----

To create the egg::

    make egg

The resulting egg will be in the `dist` directory

