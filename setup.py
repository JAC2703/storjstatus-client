#!/usr/bin/env python3

from setuptools import setup
from pip.req import parse_requirements
import pypandoc

exec(open('storjstatus/version.py').read())

dependencies = parse_requirements('requirements.txt', session=False)

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(name='storjstatus',
      version=__version__,
      description='A utility for reporting Storj farmer statistics',
      long_description=long_description,
      license='MIT',
      packages=['storjstatus'],
      author='James Coyle',
      author_email='james.coyle@jamesdcoyle.net',
      python_requires='>=3.5',
      url='https://www.storjstatus.com/install-client',
      install_requires=[str(ir.req) for ir in dependencies],
      entry_points={
          'console_scripts': [
              'storjstatus-register=storjstatus:register',
              'storjstatus-send=storjstatus:send'
          ]
      }
 )
