from setuptools import setup, find_packages
from setuptools.command.install import install as _install


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
      packages=find_packages(),
      include_package_data=True,
      cmdclass={'install': Install},
      dependency_links=['git+https://github.com/LIAAD/yake',
                        'git+https://github.com/JMendes1995/py_heideltime'],
      entry_points={
          'console_scripts': [
              'time_matters=time_matters.cli:Dates'
          ]
      }
      )
