from setuptools import setup, find_packages
setup(name='time_matters',
      version='1.2',
      description='module that discover the relevant dates from a text',
      author='Jorge Alexandre Rocha Mendes',
      author_email='mendesjorge49@gmail.com',
      url='https://github.com/JMendes1995/Time_Matters.git',
      packages=find_packages(include=['time_matters', 'nltk', 'pandas', 'langdetect', 'tabulate', 'click']),
      py_modules=['time_matters'],
      install_requires=["yake", "py_heideltime"],
      dependency_links=['https://github.com/LIAAD/yake.git#egg=yake', 'https://github.com/JMendes1995/py_heideltime.git#egg=py_heideltime']
)



