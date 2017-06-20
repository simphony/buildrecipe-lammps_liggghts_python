Build Recipe: LAMMPS Python
---------------------------

This recipe builds the Enthought egg for LAMMPS. It provides a python layer and a compiled library.

Usage
-----

To create the egg::

    python builder.py egg

The resulting egg will be in the `dist` directory

To upload the egg to EDM repo, use::

    python builder.py upload_egg

