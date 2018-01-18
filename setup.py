#!/usr/bin/python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(name='titlesearch',
      version='0.0.1',
      description='Small script to extract similar and translated titles from '
                  'light novels, novels, visual novels, mangas and animes',
      url='https://github.com/DaRealFreak/BakaUpdates',
      author='DaRealFreak',
      author_email='steffen.keuper@web.de',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'numpy', 'bs4', 'requests', 'html5lib',
      ],
      zip_safe=True)
