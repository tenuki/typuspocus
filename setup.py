#!/usr/bin/env python
from distutils.core import setup

setup(
    # metadata
    name = 'typuspocus',
    version = '0.4.2',
    maintainer = 'Facundo Batista',
    maintainer_email = '',
    description = "Game about a magician that needs to cast spells typing "\
                  "them to go through his particular adventure.",
    long_description = "",
    license = 'GNU GPL v2',
    keywords = ['game', 'grossini', 'pygame', 'magician'],
    url = 'https://launchpad.net/typuspocus/',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Graphical',
        'Framework :: PyGame',
        'Intended Audience :: Gamers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Topic :: Game',
    ],

    # content
    packages = ['typuspocus'],

    # scripts
    scripts = ['typuspocus/typuspocus'],

    # dependencies
    requires = [
        'pygame',
    ],
)
