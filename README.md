
# Time-Matters

Time matters is a python package that aims to score the relevance of temporal expressions found within a text (single document) or a set of texts (multiple documents). Unlike previous metadata and query log-based approaches, we achieve this goal based on information extracted from document content. 

Towards this goal, we define a Generic Temporal Similarity measure (GTE) that makes use of co-occurrences of words (extracted through [YAKE!](https://github.com/LIAAD/yake) keyword extractor [system](http://yake.inesctec.pt)) and temporal expressions (extracted by means of [Heideltime](https://github.com/JMendes1995/py_heideltime) temporal [tagger](https://heideltime.ifi.uni-heidelberg.de/heideltime/) ) based on corpus statistics.

Our assumption is that the relevance of a candidate date (retrieved by heideltime) may be determined with regards to the relevant words (retrieved by YAKE!) that it co-occurs with, within a context window to be defined. That is: the more a given candidate date is correlated with the most relevant keywords of a document (or documents), the more relevant the candidate date is.

This python package has been developed by Jorge Mendes under the supervision of [Professor Ricardo Campos](http://www.ccc.ipt.pt/~ricardo/) in the scope of the Final Project of the Computer Science degree of the [Polytechnic Institute of Tomar](http://portal2.ipt.pt/), Portugal.

This package consists of two modules that may be executed independently:
- Time-Matters-SingleDoc
- Time-Matters-MultipleDocs

The first aims to determine the relevance of temporal expressions within a single document. 

The latter aims to determine the relevance of temporal expressions within multiple documents. 
    
## How to Install Time-Matters

``` bash
pip install git+https://github.com/LIAAD/Time_Matters.git
```
### Install External Dependencies
``` bash
pip install git+https://github.com/LIAAD/yake

pip install git+https://github.com/JMendes1995/py_heideltime
```
You should also have [java JDK](https://www.oracle.com/technetwork/java/javase/downloads/index.html) and [perl](https://www.perl.org/get.html) installed in your machine for heideltime dependencies.

### External modules used (only for informative purposes):
    - YAKE
    - numpy
    - nltk
    - Pandas
    - regex
    - py_heideltime/Heideltime
    
##### Linux users
    If your user does not have permission executions on python lib folder, you should execute the following command:
    sudo chmod 111 /usr/local/lib/<YOUR PYTHON VERSION>/dist-packages/py_heideltime/HeidelTime/TreeTaggerLinux/bin/*
    
## How to use Time-Matters

### Time-Matters-SingleDoc
.......to do

### Time-Matters-MultipleDocs
.......to do

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

### Publications
If you use Time-Matters please cite the appropriate paper. In general, this would be:

Campos, R., Dias, G., Jorge, A. and Nunes, C. (2017). Identifying Top Relevant Dates for Implicit Time Sensitive Queries. In Information Retrieval Journal. Springer, Vol 20(4), pp 363-398 [pdf](https://link.springer.com/article/10.1007/s10791-017-9302-1)

Other related papers may be found here:
Campos, R., Dias, G., Jorge, A., and Nunes, C. (2014). GTE-Cluster: A Temporal Search Interface for Implicit Temporal Queries. In M. de Rijke et al. (Eds.), Lecture Notes in Computer Science - Advances in Information Retrieval - 36th European Conference on Information Retrieval (ECIR2014). Amesterdam, Netherlands, 13 - 16 April. (Vol. 8416-2014, pp. 775 - 779) [pdf](https://link.springer.com/chapter/10.1007/978-3-319-06028-6_94#page-1)

Campos, R., Jorge, A., Dias, G. and Nunes, C. (2012). Disambiguating Implicit Temporal Queries by Clustering Top Relevant Dates in Web Snippets. In Proceedings of The 2012 IEEE/WIC/ACM International Joint Conferences on Web Intelligence and Intelligent Agent Technologies Macau, China, 04 - 07 December, Vol. 1, pp 1 - 8. IEEE Computer Society Press. [pdf](https://ieeexplore.ieee.org/document/6511858?tp=&arnumber=6511858&url=http:%2F%2Fieeexplore.ieee.org%2Fxpls%2Fabs_all.jsp%3Farnumber%3D6511858)


