
# Time-Matters

Time matters is a python package that aims to score the relevance of temporal expressions found within a text (single document) or a set of texts (multiple documents). Unlike previous metadata and query log-based approaches, we achieve this goal based on information extracted from document content. 

Towards this goal, we define a Generic Temporal Similarity measure (GTE) that makes use of co-occurrences of words (extracted through [YAKE!](https://github.com/LIAAD/yake) keyword extractor [system](http://yake.inesctec.pt)) and temporal expressions (extracted by means of [Heideltime](https://github.com/JMendes1995/py_heideltime) temporal [tagger](https://heideltime.ifi.uni-heidelberg.de/heideltime/)) based on corpus statistics.

Our assumption is that the relevance of a candidate date (retrieved by heideltime) may be determined with regards to the relevant words (retrieved by YAKE!) that it co-occurs with (within a context window of n terms, where n is to be defined). That is: the more a given candidate date is correlated with the most relevant keywords of a document (or documents), the more relevant the candidate date is.

This package is the result of a research conducted by Ricardo Campos during his [PhD](http://www.ccc.ipt.pt/~ricardo/ficheiros/PhDThesis_RCampos.pdf) at the [University of Porto](https://www.up.pt/). The algorithm was initially implemented in C#, and has now been made available as a Python package by Jorge Mendes under the supervision of [Professor Ricardo Campos](http://www.ccc.ipt.pt/~ricardo/) in the scope of the Final Project of the Computer Science degree of the [Polytechnic Institute of Tomar](http://portal2.ipt.pt/), Portugal.

Time-Matters consists of two modules that may be executed independently:
- Time-Matters-SingleDoc
- Time-Matters-MultipleDocs

The first, aims to determine the relevance of temporal expressions within a single document. 

The latter, aims to determine the relevance of temporal expressions within multiple documents. 
    
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
Temporal expressions in Time-Matters can be identified through:
- [Heideltime Temporal Tagger](https://github.com/JMendes1995/py_heideltime)
- Rule-based approach

The first uses a Python wrapper of Heideltime Temporal Tagger (state-of-the-art in this kind of task). It is able to detect a huge number of different types of temporal expressions, yet, depending on the size of the text it may require a considerable amount of (linear) time to execute (approximately 4.5s for 600 tokens; 6s for 1200 tokens; 15s for 2600 tokens; 30s for 5000 tokens; 60s para 10000 tokens; 120s for 20000 tokens.

The second makes use of a rule-based approach which is able to detect the following patterns:..... While not as good as Heideltime it can be used when efficiency is a requirement.

### Time-Matters-SingleDoc
Time-Matters-SingleDoc aims to score temporal expressions found within a single text. Given an identified temporal expression it offers the user two options: 
(1) to retrieve a unique score for each temporal expression found, regardless it occurs multiple times in different parts of the text, that is multiple occurrences of a date (e.g., 2019....... 2019) in different sentences, will always return the same score (e.g., 0.92);

(2) to retrieve a different score for each occurrence of a temporal expression, that is, multiple occurrences of a date (e.g., 2019....... 2019) in different sentences, will return multiple scores (e.g., 0.92 for the occurrence of 2019 in sentence 1; and 0.77 for the occurrence of 2019 in sentence 2); 

How to work with each one will be explained next. But before, both the libraries as well as the text need to be imported.

```` bash
from Time_Matters_SingleDoc import Time_Matters_SingleDoc, Time_Matters_SingleDoc_PerSentence

text= '''
The Carnation Revolution (Portuguese: Revolução dos Cravos), also known as the 25th of April (Portuguese: 25 de Abril), was initially a 25 April 1974 military coup in Lisbon which overthrew the authoritarian Estado Novo regime.[1] The revolution began as a coup organised by the Armed Forces Movement (Portuguese: Movimento das Forças Armadas, MFA), composed of military officers who opposed the regime, but it was soon coupled with an unanticipated, popular civil resistance campaign. The revolution led to the fall of the Estado Novo, the end of 48 years of authoritarian rule in Portugal, and Portugal's withdrawal from its African colonies.
'''
````
#### Option 1: Get (a unique) score for each temporal expression found within the text
Output: to retrieve a unique score for each temporal expression, regardless it occurs multiple times in different parts of the text, that is multiple occurrences of a date (e.g., 2019....... 2019) in different sentences, will always return the same score (e.g., 0.92);

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
#### Option 2: Get (multiple) scores for each temporal expression found within the text
Output: to retrieve a different score for each occurrence of a temporal expression, that is, multiple occurrences of a date (e.g., 2019....... 2019) in different sentences, will return multiple scores (e.g., 0.92 for the occurrence of 2019 in sentence 1; and 0.77 for the occurrence of 2019 in sentence 2).

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
#### Python CLI -  Command Line Interface Time-Matters-SingleDoc
``` bash
$ Time_Matters_SingleDoc --help

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
  -dg, --date_granularity TEXT    Value of granularity should be surrounded by
                                  quotes “”. Options: Year, Month, day (e.g.,
                                  “Year”).
  -i, --input_file TEXT           text path should be surrounded by quotes
                                  (e.g., “text.txt”)
  --help                          Show this message and exit.
```

### Time-Matters-MultipleDoc
```` bash
from Time_Matters_MultipleDoc import Time_Matters_MultipleDoc

list_of_docs = ['''Born and raised on the Portuguese island of Madeira, Ronaldo was diagnosed with a racing heart at age 15. He underwent an operation to treat his condition, and began his senior club career playing for Sporting CP, before signing with Manchester United at age 18 in 2003.''',
                '''As a child, Ronaldo played for amateur team Andorinha from 1992 to 1995,[14] where his father was the kit man,[15] and later spent two years with Nacional. In 1997, aged 12, he went on a three-day trial with Sporting CP, who signed him for a fee of £1,500.[16][17] He subsequently moved from Madeira to Alcochete, near Lisbon, to join Sporting's other youth players at the club's football academy.''',
                '''Ronaldo made his official debut for Juventus in their opening Serie A match on 18 August, a 3–2 away win over Chievo.[289] On 16 September, his fourth appearance for Juventus, he scored his first goal, which was immediately followed by a second, in a 2–1 home win over Sassuolo; the latter was the 400th league goal of his career.[290][291] On 19 September, in his first Champions League match for Juventus, he was sent off in the 29th minute for "violent conduct"—the first time in 154 Champions League appearances—in an eventual 2–0 away win over Valencia''']
````
##### With default parameters.
```` bash
dates, docs = Time_Matters_MultipleDoc(list_of_docs, language='English')

print(dates)
print(docs)
````
##### With all the parameters.
``` bash
Time_Matters_MultipleDoc, language='English', contextual_window_distance=10, threshold=0.05, max_array_len=0, max_keywords=10, analisys_sentence=True, heideltime_document_type='news', heideltime_document_creation_time='1939-05-31', heideltime_date_granularity='year')
print(dates)
print(docs)
```
##### Output
``` bash
[[('2003', [(0, 1.0, [47])])], [('1992', [(1, 1.0, [11])]), ('1995', [(1, 1.0, [13])]), ('p2y', [(1, 1.0, [26])]), ('1997', [(1, 0.952, [30])]), ('p3d', [(1, 0.952, [37])])], [('xxxx-09-19', [(2, 0.9915, [62])]), ('xxxx-08-18', [(2, 0.9884999999999999, [15])]), ('xxxx-09-16', [(2, 0.985, [24])])]]
['Born and raised on the Portuguese island of Madeira, Ronaldo was diagnosed with a racing heart at age 15. He underwent an operation to treat his condition, and began his senior club career playing for Sporting CP, before signing with Manchester United at age 18 in 2003.', 
"As a child, Ronaldo played for amateur team Andorinha from 1992 to 1995,[14] where his father was the kit man,[15] and later spent two years with Nacional. In 1997, aged 12, he went on a three-day trial with Sporting CP, who signed him for a fee of £1,500.[16][17] He subsequently moved from Madeira to Alcochete, near Lisbon, to join Sporting's other youth players at the club's football academy.", 
'Ronaldo made his official debut for Juventus in their opening Serie A match on 18 August, a 3–2 away win over Chievo.[289] On 16 September, his fourth appearance for Juventus, he scored his first goal, which was immediately followed by a second, in a 2–1 home win over Sassuolo; the latter was the 400th league goal of his career.[290][291] On 19 September, in his first Champions League match for Juventus, he was sent off in the 29th minute for "violent conduct"—the first time in 154 Champions League appearances—in an eventual 2–0 away win over Valencia']

```
#### Python CLI -  Command Line Interface Time_Matters_MultipleDoc
``` bash
$ Time_Matters_MultipleDoc --help

Options:
  -d, --dir TEXT                  Directory path that cointain the docs should
                                  be surrounded by quotes (e.g., “/test”)
  -l, --language TEXT             [required] Language text is required and
                                  should be surrounded by quotes “”. Options:
                                  English, Portuguese, Spanish, Germany,
                                  Dutch, Italian, French (e.g., “English”).
                                  [required]
  -cwd, --context_window_distance INTEGER
                                  max distance between words
  -th, --threshold FLOAT          minimum DICE threshold similarity values
  -n, --max_array_len INTEGER     size of the context vector
  -ky, --max_keywords INTEGER     max keywords
  -icwd, --ignore_contextual_window_distance TEXT
                                  ignore contextual window distance
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
  -dg, --heideltime_date_granularity TEXT
                                  Value of granularity should be surrounded by
                                  quotes “”. Options: Year, Month, day (e.g.,
                                  “Year”).
  --help                          Show this message and exit.
```

## API
https://time-matters-api.herokuapp.com/

### Publications
If you use Time-Matters please cite the appropriate paper. In general, this will be:

- Campos, R., Dias, G., Jorge, A. and Nunes, C. (2017). Identifying Top Relevant Dates for Implicit Time Sensitive Queries. In Information Retrieval Journal. Springer, Vol 20(4), pp 363-398 [pdf](https://link.springer.com/article/10.1007/s10791-017-9302-1)

Other related papers may be found here:

- Campos, R., Dias, G., Jorge, A., and Nunes, C. (2014). GTE-Cluster: A Temporal Search Interface for Implicit Temporal Queries. In M. de Rijke et al. (Eds.), Lecture Notes in Computer Science - Advances in Information Retrieval - 36th European Conference on Information Retrieval (ECIR2014). Amesterdam, Netherlands, 13 - 16 April. (Vol. 8416-2014, pp. 775 - 779) [pdf](https://link.springer.com/chapter/10.1007/978-3-319-06028-6_94#page-1)

- Campos, R., Jorge, A., Dias, G. and Nunes, C. (2012). Disambiguating Implicit Temporal Queries by Clustering Top Relevant Dates in Web Snippets. In Proceedings of The 2012 IEEE/WIC/ACM International Joint Conferences on Web Intelligence and Intelligent Agent Technologies Macau, China, 04 - 07 December, Vol. 1, pp 1 - 8. IEEE Computer Society Press. [pdf](https://ieeexplore.ieee.org/document/6511858?tp=&arnumber=6511858&url=http:%2F%2Fieeexplore.ieee.org%2Fxpls%2Fabs_all.jsp%3Farnumber%3D6511858)

### Awards
Winner of the [Fraunhofer Portugal Challenge 2013 PhD Contest](https://www.aicos.fraunhofer.pt/en/news_and_events_aicos/news_archive/older_archive/fraunhofer-portugal-challenge-2013-winners.html)

