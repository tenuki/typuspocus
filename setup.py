#!/usr/bin/env python

"""setup -- setuptools setup file for Typus Pocus."""

__author__ = "Facundo Batista"
__author_email__ = "facundo en taniquetil punto com punto ar"
__version__ = "0.4.2"
__date__ = "2010-03-07"

from distutils.core import setup

__description__ = """
Game about a magician that needs to cast spells typing them to go through
his particular adventure.
"""

setup(
    name = 'typuspocus',
    version = __version__,
    author = __author__,
    author_email = __author_email__,
    description = __description__,
    url = 'https://launchpad.net/typuspocus/',

    packages = ['typuspocus'],

    package_data = {'typuspocus': ['audiencia', 'escenario', 'icons', 'locale',
                                   'music', 'sounds']},

    zip_safe = False,
    )
