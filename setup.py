from setuptools import setup, find_packages
from setuptools.command.install import install as _install

import os
requirementPath = 'requirements.txt'
install_requires = []

if os.path.isfile(requirementPath):
    with open('requirements.txt') as f:
        requires = f.readlines()

install_requires = [item.strip() for item in requires if not "http" in item]
dependency_links = [item.strip() for item in requires if "http" in item]


class Install(_install):
    def run(self):
        _install.do_egg_install(self)
        import nltk
        nltk.download("punkt")


setup(name='time_matters',
      version='1.2',
      description='module that discover the relevant dates from a text',
      author='Jorge Alexandre Rocha Mendes',
      author_email='mendesjorge49@gmail.com',
      url='https://github.com/JMendes1995/Time_Matters.git',
      cmdclass={'install': Install},
      packages=find_packages(),
      dependency_links=dependency_links,
      entry_points={
          'console_scripts': [
              'time_matters=time_matters.cli:Dates'
          ]
      }
      )
