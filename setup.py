#!/usr/bin/env python
#coding:utf-8

import os
import setuptools
here = os.path.abspath(os.path.dirname(__file__))
from distutils.core import setup


install_requires = [
        'bottle',
        'gunicorn',
        'peewee'
    ]

setup(name='demobill',
      version='1.03',
      description='Demonstration Billing Server',
      author='Dmitry Vysochin',
      author_email='dmitry.vysochin@gmail.com',
      url='https://github.com/veryevilzed/rk_payserv',
      install_requires=install_requires,
      packages=['demobill',],
      entry_points = {
            'console_scripts': [
                'demobill = demobill.demobill:main'
            ]
        }
     )