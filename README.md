
# Time-Matters

Time matters is a python package that aims to score the relevance of temporal expressions found within a text (single document) or a set of texts (multiple documents). Unlike previous metadata and query log-based approaches, we achieve this goal based on information extracted from document content. 

In order to accomplish this objetive, we define a Generic Temporal Similarity measure (GTE) that makes use of co-occurrences of words (extracted through [YAKE!](https://github.com/LIAAD/yake) keyword extractor system) and temporal expressions (extracted by means of a self-defined rule-based solution or a temporal tagger such as [Heideltime](https://heideltime.ifi.uni-heidelberg.de/heideltime/) or [Sutime](https://nlp.stanford.edu/software/sutime.shtml)) based on corpus statistics.

Our assumption is that the relevance of a candidate date may be determined with regards to the relevant words that it co-occurs with (within a context window of n terms, where n is to be defined). That is: the more a given candidate date is correlated with the most relevant keywords of a document (or documents), the more relevant the candidate date is.

This package is the result of a research conducted by Ricardo Campos during his [PhD](http://www.ccc.ipt.pt/~ricardo/ficheiros/PhDThesis_RCampos.pdf) at the [University of Porto](https://www.up.pt/). The algorithm, initially implemented in C#, has now been made available as a Python package by Jorge Mendes under the supervision of [Professor Ricardo Campos](http://www.ccc.ipt.pt/~ricardo/) in the scope of the Final Project of the Computer Science degree of the [Polytechnic Institute of Tomar](http://portal2.ipt.pt/), Portugal.

Time-Matters consists of two modules that may be executed independently:
- Time-Matters-SingleDoc
- Time-Matters-MultipleDocs

The first, aims to determine the relevance of temporal expressions within a single document. 

The latter, aims to determine the relevance of temporal expressions within multiple documents. 
    
## How to Install Time-Matters

``` bash
pip install git+https://github.com/LIAAD/Time-Matters.git
```
#### Install External Dependencies
Time-Matters rests on the extraction of relevant keywords and temporal expressions found in the text.

For the first (that is, the extraction of relevant keywords), we resort to YAKE! keyword extractor. More about the extraction of relevant keywords below.

``` bash
pip install git+https://github.com/LIAAD/yake
```


For the latter (that is, the extraction of temporal expressions), we resort to three possibilities:
- rule-based approach
- heideltime python wrapper
- sutime python wrapper


The first, is an internal self-defined rule-based approach which is directly embedded in the code, thus, it doesn't require any additional procedure. However, if your plan is to use Heideltime or Sutime (or even both) you need to install the following packages. More about the extraction of temporal expressions below.
``` bash
pip install git+https://github.com/JMendes1995/py_heideltime
pip install git+https://github.com/FraBle/python-sutime
```

You should also have [java JDK](https://www.oracle.com/technetwork/java/javase/downloads/index.html) and [perl](https://www.perl.org/get.html) installed in your machine for heideltime and sutime dependencies (note that none of this is needed should your plan is to only use a rule-based approach).

#### External modules used (only for informative purposes):
    - YAKE
    - numpy
    - nltk
    - Pandas
    - regex
    - py_heideltime
    - python-sutime
    
##### Linux users
    If your user does not have permission executions on python lib folder, you should execute the following command:
    sudo chmod 111 /usr/local/lib/<YOUR PYTHON VERSION>/dist-packages/py_heideltime/HeidelTime/TreeTaggerLinux/bin/*
    
## What do we use for relevant keywords detection and temporal expressions identification in Time-Matters?
#### Relevant keywords
Relevant keywords in Time-Matters can be identified through YAKE!, a keyword extractor system ([ECIR'18](http://www.ecir2018.org) Best Short Paper) which is available not only on a [demo-based](http://yake.inesctec.pt) purpose, but also through a [Python package](https://github.com/LIAAD/yake). If you are interested in knowing more about YAKE! please refer to the [Publications](#Publications) section where you can find a few papers about it.

#### Temporal expressions
Temporal expressions in Time-Matters can be identified through:
- [Heideltime Temporal Tagger](https://heideltime.ifi.uni-heidelberg.de/heideltime/) by means of a [Python wrapper package](https://github.com/JMendes1995/py_heideltime)
- [Sutime Temporal Tagger](https://nlp.stanford.edu/software/sutime.shtml) by means of a [Python wrapper package](https://github.com/FraBle/python-sutime)
- Rule-based approach

The first uses a Python wrapper of Heideltime Temporal Tagger (state-of-the-art in this kind of task). It is able to detect a huge number of different types of temporal expressions, yet, depending on the size of the text it may require a considerable amount of (linear) time to execute (approximately 4.5s for 600 tokens; 6s for 1,200 tokens; 15s for 2,600 tokens; 30s for 5k tokens; 60s para 10k tokens; 120s for 20k tokens). If you are interested in knowing more about Heideltime please refer to the [Publications](#Publications) section where you can find a few papers about it.

The second uses a Python wrapper of Sutime Temporal Tagger (also state-of-the-art in this kind of task). Likewise Heideltime, it is able to detect a huge number of different types of temporal expressions. However, while it is more efficient (time-performance) than Heideltime, [currently](https://github.com/FraBle/python-sutime#Supported-Languages) it only works for English. If you are interested in knowing more about Sutime please refer to the [Publications](#Publications) section where you can find a few papers about it.

Finally, we also make use of a self-defined rule-based approach which is able to detect the following patterns:
- yyyy(./-)mm(./-)dd
- dd(./-)mm(-/-)yyyy
- yyyy(./-)yyyy
- yyyys
- yyyy

While not as good (i.e., effective) as Heideltime or Sutime, it can be used when efficiency (time-performance) is a requirement.

## How to use Time-Matters-SingleDoc
Time-Matters-SingleDoc aims to score temporal expressions found within a single text. Given an identified temporal expression it offers the user two options: 

- to retrieve a <b>unique</b> score for each temporal expression found, regardless it occurs multiple times in different parts of the text, that is multiple occurrences of a date in different sentences (e.g., 2019....... 2019), will always return the same score (e.g., 0.92);

- to retrieve a <b>multiple</b> (eventually different) score for each occurrence of a temporal expression, that is, multiple occurrences of a date in different sentences (e.g., 2019....... 2019), will return multiple (eventually different) scores (e.g., 0.92 for the occurrence of 2019 in sentence 1; and 0.77 for the occurrence of 2019 in sentence 2); 

How to work with each one will be explained next. But before, both the libraries as well as the text need to be imported.

```` bash
from Time_Matters_SingleDoc import Time_Matters_SingleDoc, Time_Matters_SingleDoc_PerSentence

text= '''
The Carnation Revolution (Portuguese: Revolução dos Cravos), also known as the 25th of April (Portuguese: 25 de Abril), was initially a 25 April 1974 military coup in Lisbon which overthrew the authoritarian Estado Novo regime.[1] The revolution began as a coup organised by the Armed Forces Movement (Portuguese: Movimento das Forças Armadas, MFA), composed of military officers who opposed the regime, but it was soon coupled with an unanticipated, popular civil resistance campaign. The revolution led to the fall of the Estado Novo, the end of 48 years of authoritarian rule in Portugal, and Portugal's withdrawal from its African colonies.
'''
````
#### Option 1 
<b>Get (a unique) score for each temporal expression found within the text</b>
Output objetive: to retrieve a unique score for each temporal expression, regardless it occurs multiple times in different parts of the text, that is multiple occurrences of a date in different sentences (e.g., 2019....... 2019), will always return the same score (e.g., 0.92);

##### With default parameters.
```` bash
Time_Matters_SingleDoc(text, temporal_tager=['py_heideltime'], score_type='single')
````
###### Output
``` bash
[('xxxx-04-25', 0.9935, [11]), ('1974-04-25', 0.9935, [19]), ('p48y', 0.919, [83])]
```
##### With all the parameters.
``` bash
Time_Matters_SingleDoc(text, language='English', contextual_window_distance=10, threshold=0.05, max_array_len=0, max_keywords=10, analisys_sentence=True, heideltime_document_type='news', heideltime_document_creation_time='1939-05-31', heideltime_date_granularity='year')
```
###### Output
``` bash
[('xxxx', 0.986, [11]), ('1974', 0.939, [19])]
```
#### Option 2
<b>Get (multiple) scores for each temporal expression found within the text</b>
Output  objetive: to retrieve a different score for each occurrence of a temporal expression, that is, multiple occurrences of a date in different sentences (e.g., 2019....... 2019), will return multiple (eventually different) scores (e.g., 0.92 for the occurrence of 2019 in sentence 1; and 0.77 for the occurrence of 2019 in sentence 2).

##### With default parameters.
``` bash
dates, sentences = Time_Matters_SingleDoc_PerSentence(text, 'English')
print(dates)
print(sentences[1])
```
###### Output
``` bash
[('2019-04-25', [(1, 0.99)], [11]), ('1974-04-25', [(1, 0.99)], [19])]
[1] The revolution began as a coup organised by the Armed Forces Movement (Portuguese: Movimento das Forças Armadas, MFA), composed of military officers who opposed the regime, but it was soon coupled with an unanticipated, popular civil resistance campaign.
```
##### With all the parameters.
``` bash
dates, sentences = Time_Matters_SingleDoc(text, temporal_tagger=['py_heideltime', 'English', 'day', 'news', '1974-04-26'], time_matters_parameters=[10, 'none', 'max', 0.05], score_type='multiple', debug_mode=False)
print(dates)
print(sentences[1])
```
###### Output
``` bash
[('1974-04-25', [(1, 0.99)], [11, 19])]
[1] The revolution began as a coup organised by the Armed Forces Movement (Portuguese: Movimento das Forças Armadas, MFA), composed of military officers who opposed the regime, but it was soon coupled with an unanticipated, popular civil resistance campaign.
```
#### Python CLI -  Command Line Interface Time-Matters-SingleDoc
``` bash
$ Time_Matters_SingleDoc --help

 Usage_examples (make sure that the input parameters should be within quotes):
  Default Parameters: Time_Matters_SingleDoc -i "['text', 'August 31st']" -tt "['py_heideltime','English']"
  All the Parameters: Time_Matters_SingleDoc -i "['text', 'August 31st']" -tt "['py_heideltime','English', 'days', 'news', '2019-05-05']" -tm "[10,'none', 'max', 0.05]" -st single -dm False

Options:
  [required]: that is, need to specify one of the two options (text or path).
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  -i, --input LIST                      A list that specifies the type of input: a text or path
                                        Example:
                                                "['text', 'August 31st']"
                                                "['path', 'text.txt']"



  [not required]
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  -tt, --temporal_tagger LIST           Specifies the temporal tagger (“heideltime”, “rule-based”) and the corresponding parameters.
                                        py_heideltime
                                            parameters:

                                                temporal_tagger_name
                                                    options:
                                                            "py_heideltime"
                                                language
                                                    options:
                                                            "English";
                                                            "Portuguese";
                                                            "Spanish";
                                                            "Germany";
                                                            "Dutch";
                                                            "Italian";
                                                            "French".

                                                date_granularity
                                                    options:
                                                            "year" (means that for the date YYYY-MM-DD only the YYYY will be retrieved);
                                                            "month" (means that for the date YYYY-MM-DD only the YYYY-MM will be retrieved);
                                                            "day" - (default param. Means that for the date YYYY-MM-DD it will retrieve YYYY-MM-DD).

                                                document_type
                                                    options:
                                                            "News" for news-style documents - default param;
                                                            "Narrative" for narrative-style documents (e.g., Wikipedia articles);
                                                            "Colloquial" for English colloquial (e.g., Tweets and SMS);
                                                            "Scientific" for scientific articles (e.g., clinical trails).

                                                document_creation_time
                                                     Document creation date in the format YYYY-MM-DD. Taken into account when "News" or "Colloquial"
                                                     texts are specified.
                                                     Example: "2019-05-30".

                                            Example:
                                                "['py_heideltime','English', 'days', 'news', '2019-05-05']"

                                        Rule_Based
                                            parameters:

                                                temporal_tagger_name
                                                    options:
                                                            "rule_based"

                                                date_granularity
                                                    options:
                                                            "year" (means that for the date YYYY-MM-DD only the YYYY will be retrieved);
                                                            "month" (means that for the date YYYY-MM-DD only the YYYY-MM will be retrieved);
                                                            "day" - (default param. Means that for the date YYYY-MM-DD it will retrieve YYYY-MM-DD).

                                            Example:
                                                "['rule_based','days']"

  [not required]
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  -tm, --time_matters LIST              specifies information about the Time-Matters
                                            the number of YAKE! keywords to extract from the text (num_of_keywords),
                                            information regarding the construction of the vocabulary context vector (context_vector_size,
                                            threshold_sim_value), and information concerning the scope of search (context_window_distance)
				
                                            context_vector_size
                                            	Option:
                                               	 	"max"; Means that will be considered the maximun number of words in context vector
                                                    Intiger
                                            context_window_distance:
                                            	Option:
                                                	"none"; Means that doesen't matter the distence between words
                                                     Intiger (default= 10)
                                            Example:
                                                "[num_of_keywords=10, context_window_distance=10, context_vector_size='max', threshold_sim_value=0.05]"

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  -st, --score_type TEXT                Specifies the type of score
                                        Options:
                                                "single" Single score per date;
                                                "Multiple" Multiple score depending which sentence that the date appears;


  -dm, --debug_mode BOOLEAN             Return the following data:
                                                "Candidates dates list";
                                                "Relevante words list, extracted by YAKE!";
                                                "Inverted Index"
                                                "Dice Matrix"
                                                "Relevant dates list with the score and offset"



  --help                                Show this message and exit.
```

## How to use Time-Matters-MultipleDoc
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
###### Output
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

## Publications
### Time-Matters
If you use Time-Matters please cite the appropriate paper. In general, this will be:

- Campos, R., Dias, G., Jorge, A. and Nunes, C. (2017). Identifying Top Relevant Dates for Implicit Time Sensitive Queries. In Information Retrieval Journal. Springer, Vol 20(4), pp 363-398 [pdf](https://link.springer.com/article/10.1007/s10791-017-9302-1)

Other Time-Matters related papers may be found here:

- Campos, R., Dias, G., Jorge, A., and Nunes, C. (2014). GTE-Cluster: A Temporal Search Interface for Implicit Temporal Queries. In M. de Rijke et al. (Eds.), Lecture Notes in Computer Science - Advances in Information Retrieval - 36th European Conference on Information Retrieval (ECIR2014). Amesterdam, Netherlands, 13 - 16 April. (Vol. 8416-2014, pp. 775 - 779) [pdf](https://link.springer.com/chapter/10.1007/978-3-319-06028-6_94#page-1)

- Campos, R., Jorge, A., Dias, G. and Nunes, C. (2012). Disambiguating Implicit Temporal Queries by Clustering Top Relevant Dates in Web Snippets. In Proceedings of The 2012 IEEE/WIC/ACM International Joint Conferences on Web Intelligence and Intelligent Agent Technologies Macau, China, 04 - 07 December, Vol. 1, pp 1 - 8. IEEE Computer Society Press. [pdf](https://ieeexplore.ieee.org/document/6511858?tp=&arnumber=6511858&url=http:%2F%2Fieeexplore.ieee.org%2Fxpls%2Fabs_all.jsp%3Farnumber%3D6511858)

### YAKE!
YAKE! papers may be found here:

- Campos R., Mangaravite V., Pasquali A., Jorge A.M., Nunes C., and Jatowt A. (2018). A Text Feature Based Automatic Keyword Extraction Method for Single Documents. In: Pasi G., Piwowarski B., Azzopardi L., Hanbury A. (eds). Advances in Information Retrieval. ECIR 2018 (Grenoble, France. March 26 – 29). Lecture Notes in Computer Science, vol 10772, pp. 684 - 691. [pdf](https://link.springer.com/chapter/10.1007/978-3-319-76941-7_63). [<b>ECIR'18 Best Short Paper</b>]

- Campos R., Mangaravite V., Pasquali A., Jorge A.M., Nunes C., and Jatowt A. (2018). YAKE! Collection-independent Automatic Keyword Extractor. In: Pasi G., Piwowarski B., Azzopardi L., Hanbury A. (eds). Advances in Information Retrieval. ECIR 2018 (Grenoble, France. March 26 – 29). Lecture Notes in Computer Science, vol 10772, pp. 806 - 810. [pdf](https://link.springer.com/chapter/10.1007/978-3-319-76941-7_80)

### Heideltime
Heideltime papers may be found here:

- Strötgen, J., and Gertz, M. (2013). Multilingual and Cross-domain Temporal Tagging. In: Language Resources and Evaluation, 47(3), pp. 269-298. [pdf](https://link.springer.com/article/10.1007%2Fs10579-012-9179-y)

or [here](https://github.com/HeidelTime/heideltime#Publications)

### Sutime
Sutime papers may be found here:

- Chang, A., Manning, C.D. (2012). SUTIME: A Library for Recognizing and Normalizing Time Expressions. In: 8th International Conference on Language Resources and Evaluation (LREC'12). Istanbul, Turkey, May 23-25. pp 3735–3740. [pdf](https://nlp.stanford.edu/pubs/lrec2012-sutime.pdf)

## Awards
Winner of the [Fraunhofer Portugal Challenge 2013 PhD Contest](https://www.aicos.fraunhofer.pt/en/news_and_events_aicos/news_archive/older_archive/fraunhofer-portugal-challenge-2013-winners.html)

## Contact
For any inquires about Time-Matters please contact [Ricardo Campos](http://www.ccc.ipt.pt/~ricardo/): ricardo.campos@ipt.pt
