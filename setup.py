#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 17:47:10 2019

@author: zackkingbackup
"""

from setuptools import setup

setup(name='myetl',
      version='0.1',
      description='Sample Project - ETL',
      url='https://github.com/brentvukmer/sample-project-data-engineer',
      author='Zack King',
      author_email='zack121992@gmail.com',
      license='',
      packages=['myetl'],
      install_requires=[
              'numpy',
              'pandas',
              'pytz'
      ],
      zip_safe=False)