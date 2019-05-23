
# Time_Matters

Time matters is a extractor of relevant dates from text.

This Project has been developed by Jorge Mendes under the supervision of [Professor Ricardo Campos](http://www.ccc.ipt.pt/~ricardo/) in the scope of the Final Project of the Computer Science degree of the [Polytechnic Institute of Tomar](http://portal2.ipt.pt/), Portugal.

The module are composed by:
    
   - Date extraction with [py_heideltime](https://github.com/JMendes1995/py_heideltime.git) / [java heideltime](https://github.com/HeidelTime/heideltime).
    
   - Keyword extraction with [YAKE](https://github.com/LIAAD/yake).
    
   - Creation of a inverted index to organize the following data:
        - Frequency the keyword or date that occur on text.
        - how many sentences that keyword or date appears.
        - offset of date and keyword.

   - Calculate the similarity of the relevant words with the canditate to relevant date.



### Install Time_Matters

In order to use Time_Matters you must have [java JDK](https://www.oracle.com/technetwork/java/javase/downloads/index.html) and [perl](https://www.perl.org/get.html) installed in your machine for heideltime dependencies.

``` bash
Git clone https://github.com/JMendes1995/Time_Matters.git
cd Time_Matters
python setup.py install
pip install -r requirements.txt
```
##### Linux users
    If your user had not execution permitions on python lib folder, you should execute the following command:
    sudo chmod 111 /usr/local/lib/<YOUR PYTHON VERSION>/dist-packages/py_heideltime/HeidelTime/TreeTaggerLinux/bin/*
    
### How to use Time_Matters
### Python
``` bash
from time_matters import timeMatters
text = '''
Albert Einstein published the theory of special relativity in 1905, building on many theoretical results and empirical findings obtained by Albert A. Michelson, Hendrik Lorentz, Henri Poincaré and others. Max Planck, Hermann Minkowski and others did subsequent work.
Einstein developed general relativity between 1907 and 1915, with contributions by many others after 1915. The final form of general relativity was published in 1916.
'''
```

##### Analyze all dates from entire text
``` bash
# assuming default parameters
timeMatters(text)

# with all paramiters
timeMatters(text, contextual_window_distance=10, threshold=0.05, max_array_len=0, max_keywords=10, analisys_sentence=True, heideltime_document_type='news', heideltime_document_creation_time='')

print(output)
```
##### output
```` bash
[{'Date': '1905', 'Score': 0.9980984799637649}, {'Date': '1907', 'Score': 0.9885848306283148}, {'Date': '1915', 'Score': 0.9467018487599099}, {'Date': '1916', 'Score': 0.8163265306122448}]
````
##### Analyze dates per text sentence
``` bash
# assuming default parameters
timeMattersPerSentence(text)

# with all paramiters
timeMattersPerSentence(text, contextual_window_distance=10, threshold=0.05, max_array_len=0, max_keywords=10, heideltime_document_type='news', heideltime_document_creation_time='')

print(output)
```
##### output
```` bash
[{'Sentence 1': {'Date': '1905', 'Score': 1.0}}, {'Sentence 3': {'Date': '1907', 'Score': 1.0}}, {'Sentence 3': {'Date': '1915', 'Score': 0.8908296943231436}}, {'Sentence 4': {'Date': '1916', 'Score': 1.0}}]
````
### API
https://time-matters-api.herokuapp.com/

### Python CLI -  Command Line Interface
``` bash
$ time_matters --help

Options:
  -t, --text TEXT                 insert text
  -dps, --date_per_sentence TEXT  select if want to analyze per sentence
  -cwd, --context_window_distance INTEGER
                                  max distance between words
  -th, --threshold FLOAT          minimum DICE threshold similarity values
  -n, --max_array_len INTEGER     size of the context vector
  -ky, --max_keywords INTEGER     max keywords
  -icwd, --ignore_contextual_window_distance TEXT
                                  ignore contextual window distance
  -aps, --analysis_sentence TEXT  DICE Calculation per sentence
  -td, --heideltime_document_type TEXT
                                  Type of the document specified by <file>
                                  (options: News, Narrative, Colloquial,
                                  Scientific).
  -dct, --heideltime_document_creation_time TEXT
                                  Creation date of document only valid format
                                  (YYYY-MM-DD).only will be considered if
                                  document type are News or colloquial.
  -i, --input_file TEXT           input text file
  --help                          Show this message and exit.
```

### External modules used:
    - YAKE
    - numpy
    - nltk
    - Pandas
    - regex
    - langdetext
    - py_heideltime/Heideltime

### Please cite the following work when using Time-Matters:

 Campos, R., Dias, G., Jorge, A. and Nunes, C. (2017). Identifying Top Relevant Dates for Implicit Time Sensitive Queries. In Information Retrieval Journal. Springer, Vol 20(4), pp 363-398
 
 Strötgen, Gertz: Multilingual and Cross-domain Temporal Tagging. Language Resources and Evaluation, 2013. [pdf](https://link.springer.com/article/10.1007%2Fs10579-012-9179-y) [bibtex](https://dbs.ifi.uni-heidelberg.de/files/Team/jannik/publications/stroetgen_bib.html#LREjournal2013)


