from setuptools import setup, find_packages
from setuptools.command.install import install as _install


setup(name='time_matters',
      version='1.2',
      description='module that discover the relevant dates from a text',
      author='Jorge Alexandre Rocha Mendes',
      author_email='mendesjorge49@gmail.com',
      url='https://github.com/JMendes1995/Time_Matters.git',
      packages=find_packages(),
      include_package_data=True,
      entry_points={
          'console_scripts': [
              'time_matters=time_matters.cli:Dates'
          ]
      }
      )
