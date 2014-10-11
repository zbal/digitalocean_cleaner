#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='digitalocean_cleaner',
    version='0.0.2',
    description='Digital Ocean Droplet cleaner.',
    url = 'https://github.com/zbal/digitalocean_cleaner',
    author='Vincent Viallet',
    author_email='vincent.viallet@gmail.com',
    license='MIT',
    scripts=[
        'bin/do_clean'
    ],
    package_dir={ 
        'do': 'lib',
    },
    packages=[
       'do',
    ],
    install_requires = [
        'dopy'
    ],
)
