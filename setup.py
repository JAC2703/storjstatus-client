#!/usr/bin/env python3

from setuptools import setup

VERSION = '0.1.0'

setup(name='storjalytics-client',
      version=VERSION,
      description='Storj utility for reporting farmer statistics',
      license='Apache2',
      packages=['storjalytics'],
      author='James Coyle',
      author_email='james.coyle@jamesdcoyle.net',
      python_requires='>=3.5',
      url='https://wwwgit.jamescoyle.net/james.coyle/storjalytics-client',
      install_requires=[
            'requests==2.18.4',
            'python-crontab==2.2.5'
      ],
      entry_points={
          'console_scripts': [
              'storjalytics-register=storjalytics:register',
              'storjalytics-send=storjalytics:send'
          ]
      }
 )
