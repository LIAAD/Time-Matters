
# Time_Matters

### Install Time_Matters
``` bash
pip install git+https://github.com/JMendes1995/Time_Matters.git
```

### How to use Time_Matters
``` bash
from time_matters import timeMatters
text = '''
Albert Einstein published the theory of special relativity in 1905, building on many theoretical results and empirical findings obtained by Albert A. Michelson, Hendrik Lorentz, Henri Poincaré and others. Max Planck, Hermann Minkowski and others did subsequent work.
Einstein developed general relativity between 1907 and 1915, with contributions by many others after 1915. The final form of general relativity was published in 1916.
'''
# assuming default parameters
timeMatters(text)

#with all parameters
timeMatters(text, window=5, threshold=0.05, max_array_len=0)
```
