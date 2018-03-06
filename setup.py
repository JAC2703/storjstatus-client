#!/usr/bin/env python3

from setuptools import setup

setup(name='storjstatus-client',
      version=VERSION,
      description='Storj utility for reporting farmer statistics',
      license='Apache2',
      packages=['storjstatus'],
      version='0.2.0',
      author='James Coyle',
      author_email='james.coyle@jamesdcoyle.net',
      python_requires='>=3.5',
      url='https://www.storjstatus.com/install-client',
      install_requires=[
            'requests==2.18.4',
            'python-crontab==2.2.8',
            'jstyleson==0.0.2',
      ],
      entry_points={
          'console_scripts': [
              'storjstatus-register=storjstatus:register',
              'storjstatus-send=storjstatus:send'
          ]
      }
 )
