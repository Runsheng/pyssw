# packing import
try:
    from setuptools import setup, Extension
    from setuptools.command import install_lib, sdist, build_clib
except ImportError:
    from distutils.core import setup, Extension
    from distutils.command import install_lib, sdist, build_clib


# std import
import os
from os.path import join as pjoin

import subprocess
import sys


# self import
from pyssw import __version__


# read the description from the readme file
with open('README.md', "r") as f:
    LONG_DESC = f.read()


# Package paths, globle #
PACKAGE_PATH = os.path.abspath(os.path.dirname(__file__))
MODULE_PATH = pjoin(PACKAGE_PATH, 'pyssw')
PYSSW_BUILT = False

# Platform-dependent binary for `make` commands
MAKE_BIN = 'mingw32-make' if sys.platform == 'win32' else 'make'

# C library build helpers #
def pClean():
    '''
    Run `make clean`
    '''
    proc = subprocess.Popen(
        '{} clean'.format(MAKE_BIN),
        shell=True,
        cwd=MODULE_PATH,
    )
    proc.wait()


def pBuild():
    '''
    Run `make clean && make`
    '''
    proc = subprocess.Popen(
        '{} clean; {}'.format(MAKE_BIN, MAKE_BIN),
        shell=True,
        cwd=MODULE_PATH,
    )
    proc.wait()


# replace the build_clib/install_lib/sdist class
class CustomBuildClib(build_clib.build_clib):
    '''
    Custom C library builder,
    library builds.
    Installed and invoked internally by `setuptools`
    '''
    def run(self):
        global PYSSW_BUILT
        # Build primer3 prior to building the extension, if not already built
        if not PYSSW_BUILT :
            pClean()
            pBuild()
            PYSSW_BUILT = True
        super().run()

class CustomInstallLib(install_lib.install_lib):
    '''
    Custom library installer to ensure that binaries are installed
    Installed and invoked internally by `setuptools`
    '''
    def run(self):
        global PYSSW_BUILT
        if not PYSSW_BUILT:
            pClean()
            pBuild()
            PYSSW_BUILT = True
        super().run()

class CustomSdist(sdist.sdist):
    '''
    Custom sdist packager, ensures that build artifacts are removed
    prior to packaging.
    Installed and invoked internally by `setuptools`
    '''
    def run(self):
        global PYSSW_BUILT
        # Clean up the primer3 build prior to sdist command to remove
        # binaries and object/library files
        pClean()
        PYSSW_BUILT = False
        # Remove the build lib
        os.remove(os.path.join(MODULE_PATH, 'libssw.so'))
        super().run()


ssw_ext = Extension(
    name='pyssw.ssw',
    sources=["pyssw/ssw.c"], # all sources are compiled into a single binary file
)


setup(
    name='pyssw',
    version=__version__,
    packages=['pyssw'],
    url='github.com/runsheng/pyssw',
    license='MIT',
    author='Runsheng',
    author_email='runsheng.lee@gmail.com',
    description='Python wrapper for SSW alignment',
    long_description=LONG_DESC,
    cmdclass={
        'install_lib': CustomInstallLib,
        'sdist': CustomSdist,
        'build_clib': CustomBuildClib,
    },
    ext_modules=[ssw_ext
    ]
)
