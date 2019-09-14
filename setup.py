from setuptools import setup, find_packages

import os
requirementPath = 'requirements.txt'

if os.path.isfile(requirementPath):
    with open('requirements.txt') as f:
        requires = f.readlines()

install_requires = [item.strip() for item in requires]

setup(name='Time-Matters',
      version='1.0',
      description='get the relevance score of temporal expressions found within a text (single document) or a set of texts (multiple documents)',
      author='Jorge Alexandre Rocha Mendes',
      author_email='mendesjorge49@gmail.com',
      url='https://github.com/LIAAD/Time-Matters',
      include_package_data=True,
      packages=find_packages(),
      install_requires=install_requires,
      entry_points={
          'console_scripts': [
              'Time_Matters_SingleDoc=Time_Matters_SingleDoc.cli:Dates',
              'Time_Matters_MultipleDocs = Time_Matters_MultipleDocs.cli:Dates'
          ]
      }
      )
