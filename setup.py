#!/usr/bin/env python3

"""Setup file for Typus Pocus."""

import os

from setuptools import setup

DESCRIPTION = """
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
    name='typuspocus',
    version='1.0',
    author='Facundo Batista',
    author_email='facundo@taniquetil.com.ar',
    description=DESCRIPTION,
    url='https://launchpad.net/typuspocus/',
    packages=['typuspocus'],
    entry_points={
        'console_scripts': ["typuspocus = typuspocus.game:main"],
    },
    package_data={
        'typuspocus': recursive(
            'typuspocus', ['audiencia', 'escenario', 'icons', 'locale', 'music', 'sounds'])
    },
)
