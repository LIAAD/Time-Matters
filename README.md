
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
pip install git+https://github.com/LIAAD/Time-Matters.git
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
#### Python
```` bash
from Time_Matters_SingleDoc import Time_Matters_SingleDoc, Time_Matters_SingleDoc_PerSentence

text= '''
The Carnation Revolution (Portuguese: Revolução dos Cravos), also known as the 25th of April (Portuguese: 25 de Abril), was initially a 25 April 1974 military coup in Lisbon which overthrew the authoritarian Estado Novo regime.[1] The revolution began as a coup organised by the Armed Forces Movement (Portuguese: Movimento das Forças Armadas, MFA), composed of military officers who opposed the regime, but it was soon coupled with an unanticipated, popular civil resistance campaign. The revolution led to the fall of the Estado Novo, the end of 48 years of authoritarian rule in Portugal, and Portugal's withdrawal from its African colonies.
'''
````
#### Analyze all dates from entire text
##### With default parameters.
```` bash
Time_Matters_SingleDoc(text, language="English")
````
##### Output
``` bash
[('xxxx-04-25', 0.986, [11]), ('1974-04-25', 0.962, [19]), ('p48y', 0.952, [83])]
```
##### With all the parameters.
``` bash
Time_Matters_SingleDoc(text, language='English', contextual_window_distance=10, threshold=0.05, max_array_len=0, max_keywords=10, analisys_sentence=True, heideltime_document_type='news', heideltime_document_creation_time='1939-05-31', heideltime_date_granularity='year')
```
##### Output
``` bash
[('xxxx', 0.986, [11]), ('1974', 0.939, [19])]
```
#### Analyze dates per text sentence
##### With default parameters.
``` bash
dates, sentences = Time_Matters_SingleDoc_PerSentence(text, 'English')
print(dates)
print(sentences[1])
```
##### Output
``` bash
[[('1974-04-25', [(0, 1.0, [19])]), ('xxxx-04-25', [(0, 0.997, [11])])], [('p48y', [(2, 0.997, [14])])]]
[1] The revolution began as a coup organised by the Armed Forces Movement (Portuguese: Movimento das Forças Armadas, MFA), composed of military officers who opposed the regime, but it was soon coupled with an unanticipated, popular civil resistance campaign.
```
##### With all the parameters.
``` bash
dates, sentences = Time_Matters_SingleDoc_PerSentence(text, language='English', contextual_window_distance=10, threshold=0.05, max_array_len=0, max_keywords=10, analisys_sentence=True, heideltime_document_type='news', heideltime_document_creation_time='1939-05-31', heideltime_date_granularity='year')
print(dates)
print(sentences[1])
```
##### Output
``` bash
[[('1974', [(0, 1.0, [19])]), ('xxxx', [(0, 0.997, [11])])]]
[1] The revolution began as a coup organised by the Armed Forces Movement (Portuguese: Movimento das Forças Armadas, MFA), composed of military officers who opposed the regime, but it was soon coupled with an unanticipated, popular civil resistance campaign.
```
### Time-Matters-MultipleDocs
.......to do

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

- Campos, R., Dias, G., Jorge, A. and Nunes, C. (2017). Identifying Top Relevant Dates for Implicit Time Sensitive Queries. In Information Retrieval Journal. Springer, Vol 20(4), pp 363-398 [pdf](https://link.springer.com/article/10.1007/s10791-017-9302-1)

Other related papers may be found here:

- Campos, R., Dias, G., Jorge, A., and Nunes, C. (2014). GTE-Cluster: A Temporal Search Interface for Implicit Temporal Queries. In M. de Rijke et al. (Eds.), Lecture Notes in Computer Science - Advances in Information Retrieval - 36th European Conference on Information Retrieval (ECIR2014). Amesterdam, Netherlands, 13 - 16 April. (Vol. 8416-2014, pp. 775 - 779) [pdf](https://link.springer.com/chapter/10.1007/978-3-319-06028-6_94#page-1)

- Campos, R., Jorge, A., Dias, G. and Nunes, C. (2012). Disambiguating Implicit Temporal Queries by Clustering Top Relevant Dates in Web Snippets. In Proceedings of The 2012 IEEE/WIC/ACM International Joint Conferences on Web Intelligence and Intelligent Agent Technologies Macau, China, 04 - 07 December, Vol. 1, pp 1 - 8. IEEE Computer Society Press. [pdf](https://ieeexplore.ieee.org/document/6511858?tp=&arnumber=6511858&url=http:%2F%2Fieeexplore.ieee.org%2Fxpls%2Fabs_all.jsp%3Farnumber%3D6511858)


