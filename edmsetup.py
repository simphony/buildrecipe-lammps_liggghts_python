# Basic template for edm setup.
# Copy this file to retrieve the buildcommons repository
# This template can be used as is on trivial "setup.py only"
# packages.
# It requires the additional files:
# - a packageinfo.py containing the relevant data.
# - an endist.dat file, containing the relevant data.
import sys
import click
import os
import subprocess
import shutil

from packageinfo import BUILD, VERSION, NAME, LIGGGHTS_VERSION

# The version of the buildcommon to checkout.
BUILDCOMMONS_VERSION="v0.1"


def bootstrap_devenv():
    try:
        os.makedirs(".devenv")
    except OSError:
        pass

    if not os.path.exists(".devenv/buildrecipes-common"):
        subprocess.check_call([
            "git", "clone", "-b", BUILDCOMMONS_VERSION,
            "http://github.com/simphony/buildrecipes-common.git",
            ".devenv/buildrecipes-common"
            ])
    sys.path.insert(0, ".devenv/buildrecipes-common")


bootstrap_devenv()
import buildcommons as common  # noqa

workspace = common.workspace()
common.edmenv_setup()
clone_dir = os.path.join(workspace, "lammps-"+VERSION)


@click.group()
def cli():
    pass


@cli.command()
def egg():
    try:
        shutil.rmtree("build")
    except OSError:
        pass
    os.makedirs("build/usr/bin")
    os.makedirs("build/python")

    if not os.path.exists(clone_dir):
        common.run("git clone --branch r"+VERSION+" http://git.lammps.org/lammps-ro.git "+clone_dir)
        common.run("git clone --branch "+LIGGGHTS_VERSION+" --depth 1 git://github.com/CFDEMproject/LIGGGHTS-PUBLIC.git "+os.path.join(clone_dir, "myliggghts"))

    shutil.copy("files/Makefile.centos6",
        os.path.join(clone_dir, "src", "MAKE", "MACHINES", "Makefile.centos6"))
    shutil.copy(
        "files/Makefile.centos6",
        os.path.join(clone_dir, "myliggghts", "src", "MAKE", "Makefile.centos6"))

    # Build lammps executable
    common.run("make -C "+os.path.join(clone_dir, "src")+" centos6 -j 3")
    shutil.copy(os.path.join(clone_dir, "src", "lmp_centos6"), "build/usr/bin/lammps")

    # Build the shared library
    common.run("make -C "+os.path.join(clone_dir, "src")+" centos6 -j 3 mode=shlib")
    with common.cd(os.path.join(clone_dir, "python")):
        common.edmenv_run("python install.py ../../build/python")

    # Build liggghts
    common.run("make -C "+os.path.join(clone_dir, "myliggghts", "src")+" centos6 -j 3")
    shutil.copy(os.path.join(clone_dir, "myliggghts", "src", "lmp_centos6"), "build/usr/bin/liggghts")

    common.local_repo_to_edm_egg(".", name=NAME, version=VERSION, build=BUILD)


@cli.command()
def upload_egg():
    egg_path = "endist/{NAME}-{VERSION}-{BUILD}.egg".format(
        NAME=NAME,
        VERSION=VERSION,
        BUILD=BUILD)
    click.echo("Uploading {} to EDM repo".format(egg_path))
    common.upload_egg(egg_path)
    click.echo("Done")


@cli.command()
def clean():
    common.clean(["endist", ".devenv", "build", clone_dir, "lammps_bin.egg-info", "dist"])


cli()
