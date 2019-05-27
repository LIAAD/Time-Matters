
# Time-Matters

Time matters is a python package that aims to score the relevance of temporal expressions found within a piece of text. Unlike previous metadata and query log-based approaches, we achieve this goal based on information extracted from document content.

Towards this goal, we define a Generic Temporal Similarity measure (GTE) that makes use of co-occurrences of words (extracted through [YAKE!](https://github.com/LIAAD/yake) keyword extractor [system](http://yake.inesctec.pt)) and temporal expressions (extracted by means of [Heideltime](https://github.com/JMendes1995/py_heideltime) temporal tagger) based on corpus statistics.

This python package has been developed by Jorge Mendes under the supervision of [Professor Ricardo Campos](http://www.ccc.ipt.pt/~ricardo/) in the scope of the Final Project of the Computer Science degree of the [Polytechnic Institute of Tomar](http://portal2.ipt.pt/), Portugal.



The module are composed by:
    
   - Date extraction with [py_heideltime](https://github.com/JMendes1995/py_heideltime.git) / [java heideltime](https://github.com/HeidelTime/heideltime).
    
   - Keyword extraction with [YAKE](https://github.com/LIAAD/yake).
    
   - Creation of a inverted index to organize the following data:
        - Frequency the keyword or date that occur on text.
        - how many sentences that keyword or date appears.
        - offset of date and keyword.

   - Calculate the similarity of the relevant words with the canditate to relevant date.

## Install Time_Matters

``` bash
pip install git+https://github.com/JMendes1995/Time_Matters.git
```
### Install External Dependencies
``` bash
pip install git+https://github.com/LIAAD/yake

pip install git+https://github.com/JMendes1995/py_heideltime
```
You should also have [java JDK](https://www.oracle.com/technetwork/java/javase/downloads/index.html) and [perl](https://www.perl.org/get.html) installed in your machine for heideltime dependencies.
##### Linux users
    If your user does not have permission executions on python lib folder, you should execute the following command:
    sudo chmod 111 /usr/local/lib/<YOUR PYTHON VERSION>/dist-packages/py_heideltime/HeidelTime/TreeTaggerLinux/bin/*
    
## How to use Time_Matters
### Python
``` bash
from time_matters import timeMatters
text = '''
Thurs August 31st - News today that they are beginning to evacuate the London children tomorrow. Percy is a billeting officer. I can't see that they will be much safer here.
'''
```

#### Analyze all dates from entire text
##### With default parameters.
``` bash
timeMatters(text, 'English')
```
##### Output
``` bash
[{'Date': 'xxxx-08-31', 'Score': 1.0}, {'Date': 'present_ref', 'Score': 1.0}, {'Date': 'xxxx-xx-xx', 'Score': 1.0}]
```
##### With all the parameters.
``` bash
timeMatters(text, language='English', contextual_window_distance=10, threshold=0.05, max_array_len=0, max_keywords=10, analisys_sentence=True, heideltime_document_type='news', heideltime_document_creation_time='1939-05-31')
```
##### output
```` bash
[{'Date': '1939-09-01', 'Score': 0.9976303317535546}, {'Date': '1939-08-31', 'Score': 0.8974358974358964}]
````
#### Analyze dates per text sentence
##### With default parameters.
``` bash
timeMattersPerSentence(text, 'English')
```
##### output
``` bash
[{'sentence1': {0: {'Date': 'xxxx-08-31', 'Score': 1.0}, 1: {'Date': 'present_ref', 'Score': 1.0}, 2: {'Date': 'xxxx-xx-xx', 'Score': 1.0}}}, {'sentence2': {}}, {'sentence3': {}}]
```
##### With all the parameters.
``` bash
timeMattersPerSentence(text, language='English', contextual_window_distance=10, threshold=0.05, max_array_len=0, max_keywords=10, heideltime_document_type='news', heideltime_document_creation_time='1939-05-31')
```
##### output
```` bash
[{'sentence1': {0: {'Date': '1939-09-01', 'Score': 0.9976303317535546}, 1: {'Date': '1939-08-31', 'Score': 0.8974358974358964}}}, {'sentence2': {}}, {'sentence3': {}}]
````
## API
https://time-matters-api.herokuapp.com/

### Python CLI -  Command Line Interface
``` bash
$ time_matters --help

Options:
  -t, --text TEXT                 insert text, text should be surrounded by
                                  quotes “” (e.g., “Thurs August 31st”)
  -l, --language TEXT             [required] Language text is required and
                                  should be surrounded by quotes “”. Options:
                                  English, Portuguese, Spanish, Germany,
                                  Dutch, Italian, French (e.g., “English”).
                                  [required]
  -dps, --date_per_sentence TEXT  select if want to analyze per sentence
  -cwd, --context_window_distance INTEGER
                                  max distance between words
  -th, --threshold FLOAT          minimum DICE threshold similarity values
  -n, --max_array_len INTEGER     size of the context vector
  -ky, --max_keywords INTEGER     max keywords
  -icwd, --ignore_contextual_window_distance TEXT
                                  ignore contextual window distance
  -aps, --analysis_sentence TEXT  DICE Calculation per sentence
  -dt, --heideltime_document_type TEXT
                                  Type of the document text should be
                                  surrounded by quotes “”. Options: News,
                                  Narrative, Colloquial, Scientific (e.g.,
                                  “News”).
  -dct, --heideltime_document_creation_time TEXT
                                  Document creation date in the format YYYY-
                                  MM-DD should be surrounded by quotes (e.g.,
                                  “2019-05-30”). Note that this date will only
                                  be taken into account when News or
                                  Colloquial texts are specified.
  -i, --input_file TEXT           text path should be surrounded by quotes
                                  (e.g., “text.txt”)
  --help                          Show this message and exit.
```

### External modules used:
    - YAKE
    - numpy
    - nltk
    - Pandas
    - regex
    - py_heideltime/Heideltime

### Please cite the following work when using Time-Matters:

 Campos, R., Dias, G., Jorge, A. and Nunes, C. (2017). Identifying Top Relevant Dates for Implicit Time Sensitive Queries. In Information Retrieval Journal. Springer, Vol 20(4), pp 363-398
 
 Strötgen, Gertz: Multilingual and Cross-domain Temporal Tagging. Language Resources and Evaluation, 2013. [pdf](https://link.springer.com/article/10.1007%2Fs10579-012-9179-y) [bibtex](https://dbs.ifi.uni-heidelberg.de/files/Team/jannik/publications/stroetgen_bib.html#LREjournal2013)


