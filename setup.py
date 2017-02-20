#!/usr/bin/env python

from setuptools import setup

setup(name='finance4py',
      version='0.2.1',
      description='finance analysis and backtesting tools in python',
      author='Sheng-Huai Wang',
      author_email='m10215059@csie.ntust.edu.tw',
      license='BSD',
      url='https://github.com/m10215059/finance4py/',
      install_requires=['pandas>=0.18.0', 'pandas-datareader>=0.2.0', 'matplotlib>=1.5.1'],
      packages=['finance4py'],
     )