#!/usr/bin/env python

"""setup -- setuptools setup file for Typus Pocus."""

__author__ = "Facundo Batista"
__author_email__ = "facundo en taniquetil punto com punto ar"
__version__ = "0.4.3"
__date__ = "2010-03-07"

import glob
import os

from distutils.core import setup

__description__ = """
Game about a magician that needs to cast spells typing them to go through
his particular adventure.
"""

def recursive(base, dirs):
    all_files = []
    for d in dirs:
        for basedir, dirnames, filenames in os.walk(os.path.join(base, d)):
            all_files.extend(os.path.join(basedir, x) for x in filenames)

    # remove the base dir
    lenbase = len(base) + 1
    return [x[lenbase:] for x in all_files]

setup(
    name = 'typuspocus',
    version = __version__,
    author = __author__,
    author_email = __author_email__,
    description = __description__,
    url = 'https://launchpad.net/typuspocus/',

    packages = ['typuspocus'],

    package_data = {
        'typuspocus': recursive('typuspocus',
                                ['audiencia', 'escenario', 'icons',
                                 'locale', 'music', 'sounds'])
    },
    )
