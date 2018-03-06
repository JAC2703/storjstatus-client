#!/usr/bin/env python3

from setuptools import setup, find_packages

exec(open('storjstatus/version.py').read())

setup(name='storjstatus',
      version=__version__,
      description='Storj utility for reporting farmer statistics',
      license='MIT',
      packages=['storjstatus'],
      author='James Coyle',
      author_email='james.coyle@jamesdcoyle.net',
      python_requires='>=3.5',
      url='https://www.storjstatus.com/install-client',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'storjstatus-register=storjstatus:register',
              'storjstatus-send=storjstatus:send'
          ]
      }
 )
