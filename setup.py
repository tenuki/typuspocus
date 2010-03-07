# -*- coding: utf-8 -*-
"""setup -- setuptools setup file for Typus Pocus."""

__author__ = "Facundo Batista"
__author_email__ = "facundo en taniquetil punto com punto ar"
__version__ = "0.4.2"
__date__ = "2010-03-07"

try:
    import setuptools
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

from setuptools import setup, find_packages

__description__ = """
Game about a magician that needs to cast spells typing them to go through his particular adventure.
"""

setup(
    name = 'typuspocus',
    version = __version__,
    author = __author__,
    author_email = __author_email__,
    description = __description__,
    url = 'https://launchpad.net/typuspocus/',

    packages = find_packages(),
    package_data={'': ['typuspocus/sounds/*']},

#    install_requires=['pyglet>=1.1.1',],
#    dependency_links=['http://code.google.com/p/pyglet/downloads/list',],

    entry_points = {
        'console_scripts': [
            'typuspocus = typuspocus.game:main',
        ],
    },

    include_package_data = True,
    zip_safe = False,
    )
