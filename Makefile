LAMMPS_VERSION ?= 13864

egg: clean
	git clone --branch r$(LAMMPS_VERSION) http://git.lammps.org/lammps-ro.git lammps-$(LAMMPS_VERSION)
	cp files/Makefile.centos6 lammps-$(LAMMPS_VERSION)/src/MAKE/MACHINES/
	$(MAKE) -C lammps-$(LAMMPS_VERSION)/src centos6 -j 3 mode=shlib
	mkdir -p build/python
	cd lammps-$(LAMMPS_VERSION)/python; python install.py ../../build/python 
	python setup.py bdist_egg
	prepack_eggs=`ls dist/*.egg`; edm repack-egg dist/lammps_python-*.egg; rm $$prepack_eggs

provision:
	sudo yum install openmpi openmpi-devel https://package-data.enthought.com/edm/rh5_x86_64/1.7/edm_1.7.0_x86_64.rpm

clean:
	rm -rf dist build lammps-$(LAMMPS_VERSION) *.egg-info
