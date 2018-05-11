#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = parse_requirements('requirements.txt')
test_requirements = parse_requirements('requirements_dev.txt')

setup(
    name='zkpytb',
    version='0.0.8',
    description="A collection of useful functions by Zertrin",
    long_description=readme + '\n\n' + history,
    author="Marc Gallet",
    author_email='zertrin@gmail.com',
    url='https://github.com/zertrin/zkpytb',
    project_urls={
        'Documentation': 'https://zkpytb.readthedocs.io/',
        'Say Thanks!': 'https://saythanks.io/to/zertrin',
        'Source': 'https://github.com/zertrin/zkpytb',
        'Tracker': 'https://github.com/zertrin/zkpytb/issues',
    },
    packages=find_packages(include=['zkpytb']),
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.4, <4',
    license="MIT license",
    zip_safe=False,
    keywords='zkpytb',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
