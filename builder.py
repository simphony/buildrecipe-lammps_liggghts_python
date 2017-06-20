import sys
import click
import os
import shutil
import subprocess
from packageinfo import BUILD, VERSION, NAME


def bootstrap_common():
    if not os.path.exists("buildrecipes-common"):
        subprocess.check_call([
            "git", "clone",
            "git@github.com:simphony/buildrecipes-common.git",
            ])
    sys.path.insert(0, "buildrecipes-common")

bootstrap_common()
import common

workspace = common.workspace()
common.edmenv_setup()

endist_dat_template = """
build = {BUILD}
version = '{VERSION}'
name = '{NAME}'
add_files = [("build/python/", '.*', '/')]
"""

clone_dir="lammps-"+VERSION

if not os.path.exists(workspace):
    os.makedirs(workspace)


def write_endist_dat():
    with open("endist.dat", "w") as f:
        f.write(endist_dat_template.format(NAME=NAME,
            VERSION=VERSION,
            BUILD=BUILD))



@click.group()
def cli():
    pass


@cli.command()
def egg():
    if not os.path.exists(clone_dir):
        common.run("git clone --branch r"+VERSION+" http://git.lammps.org/lammps-ro.git "+clone_dir)

    shutil.copy("files/Makefile.centos6",
        os.path.join(clone_dir, "src", "MAKE", "MACHINES", "Makefile.centos6"))

    common.run("make -C "+os.path.join(clone_dir, "src")+" centos6 -j 3 mode=shlib")

    os.makedirs("build/python")

    with common.cd(os.path.join(clone_dir, "python")):
        common.edmenv_run("python install.py ../../build/python")

    common.edmenv_run("python setup.py bdist_egg")
    write_endist_dat()
    common.run("edm repack-egg dist/{NAME}-{VERSION}-py2.7.egg".format(
        NAME=NAME, VERSION=VERSION))


@cli.command()
def upload_egg():
    egg_path = "dist/{NAME}-{VERSION}-{BUILD}.egg".format(
        NAME=NAME,
        VERSION=VERSION,
        BUILD=BUILD)
    click.echo("Uploading {} to EDM repo".format(egg_path))

    common.upload_egg(egg_path)

    click.echo("Done")


@cli.command()
def clean():
    common.clean(["build", workspace, clone_dir, "lammps_bin.egg-info", "dist", "buildrecipes-common"])


cli()
