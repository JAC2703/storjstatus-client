#!/usr/bin/env python3

from setuptools import setup
from pip.req import parse_requirements

exec(open('storjstatus/version.py').read())

def dependencies():
    return parse_requirements('requirements.txt', session=False)

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='storjstatus',
      version=__version__,
      description='A utility for reporting Storj farmer statistics',
      long_description=readme(),
      license='MIT',
      packages=['storjstatus'],
      author='James Coyle',
      author_email='james.coyle@jamesdcoyle.net',
      python_requires='>=3.5',
      url='https://www.storjstatus.com/install-client',
      install_requires=[str(ir.req) for ir in dependencies()],
      entry_points={
          'console_scripts': [
              'storjstatus-register=storjstatus:register',
              'storjstatus-send=storjstatus:send'
          ]
      }
 )
