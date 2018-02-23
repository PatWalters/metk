#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

try:
    import rstcheck
    found_errors = False

    readme_errors = list(rstcheck.check(readme))
    if len(readme_errors) > 0:
        sys.stderr.write('\nErrors in README.rst [(line #, error)]\n' +
                         str(readme_errors) + '\n')
        found_errors = True

    history_errors = list(rstcheck.check(history))
    if len(history_errors) > 0:
        sys.stderr.write('\nErrors in HISTORY.rst [(line #, error)]\n' +
                         str(history_errors) + '\n')

        found_errors = True

    if 'sdist' in sys.argv or 'bdist_wheel' in sys.argv:
        if found_errors is True:
            sys.stderr.write('\n\nEXITING due to errors encountered in'
                             ' History.rst or Readme.rst.\n\nSee errors above\n\n')
            sys.exit(1)

except Exception as e:
    sys.stderr.write('WARNING: rstcheck library found, '
                     'unable to validate README.rst or HISTORY.rst\n')


requirements = [
    "argparse",
    "numpy",
    "pandas",
    "matplotlib",
    "scipy",
    "docopt"
]

test_requirements = [
    "argparse",
    "numpy",
    "pandas",
    "matplotlib",
    "scipy",
    "docopt",
    "mock",
    "unittest2"
]

setup(
    name='modelevaltoolkit',
    version='0.1.0',
    description='Model Evaluation Toolkit',
    long_description=readme + '\n\n' + history,
    author='Pat Walters <add@email.com>',
    author_email='need@toaddemail.com',
    url='https://github.com/PatWalters/metk',
    packages=[
        'modelevaltoolkit'
    ],
    package_dir={'modelevaltoolkit':
                 'modelevaltoolkit'},
    include_package_data=True,
    install_requires=requirements,
    license="Other",
    zip_safe=False,
    keywords='metk',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'License :: Free for non-commercial use',
        'Natural Language :: English',
        'Environment :: Console',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Chemistry'
    ],
    scripts = ['modelevaltoolkit/metk.py',
               'modelevaltoolkit/metk_plots.py',
               'modelevaltoolkit/metk_report.py',
               'modelevaltoolkit/metk_util.py'
               ],
    test_suite='tests',
    tests_require=test_requirements
)
