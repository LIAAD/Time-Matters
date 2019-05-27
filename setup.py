from setuptools import setup, find_packages

import os
requirementPath = 'requirements.txt'

if os.path.isfile(requirementPath):
    with open('requirements.txt') as f:
        requires = f.readlines()

install_requires = [item.strip() for item in requires]

setup(name='time_matters',
      version='1.2',
      description='module that discover the relevant dates from a text',
      author='Jorge Alexandre Rocha Mendes',
      author_email='mendesjorge49@gmail.com',
      url='https://github.com/JMendes1995/Time_Matters.git',
      include_package_data=True,
      install_requires=install_requires,
      entry_points={
          'console_scripts': [
              'time_matters=time_matters.cli:Dates'
          ]
      }
      )
