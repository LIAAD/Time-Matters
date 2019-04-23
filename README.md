
# Time_Matters


This project consists on a extractor of relevants dates from texts.

the module are composed by 2 parts

    - Creation of a inverted indext to organize the following data:
        - Frequency the word or date that occour on text,
        - how many sentences that word or date appears.
        - Exact position on sentence that the word or date appears.
        
    - Calculate the similarity of the relevante words and the canditate to relevante date.
    
    
    
 
### Install Time_Matters
``` bash
pip install git+https://github.com/JMendes1995/Time_Matters.git
# install requirements.txt
pip install -r requirements.txt
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
timeMatters(text, max_distance=5, threshold=0.05, max_array_len=0)
```

### External modules used:
    - YAKE
    - numpy
    - nltk
    - Pandas
    - regex
    - langdetext
