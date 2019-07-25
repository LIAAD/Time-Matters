
## Table of Contents
[Time-Matters](#Time-Matters)
<br>
[What is Time-Matters](#What-is-Time-Matters)
<br>
[Rationale](#Rationale)
<br>
[Documentation](#Documentation)
<br>
[How to Install Time-Matters](#How-to-Install-Time-Matters)
<br>
[How to use Time-Matters-SingleDoc](#How-to-use-Time-Matters-SingleDoc)
<br>
[How to use Time-Matters-MultipleDocs](#How-to-use-Time-Matters-MultipleDocs)
<br>
[API](#API)
<br>
[Publications](#Publications)
<br>
[Awards](#Awards)
<br>
[License](#License)
<br>
[Contact](#Contact)

# Time-Matters

Time matters is the result of research conducted by Ricardo Campos during his [PhD](http://www.ccc.ipt.pt/~ricardo/ficheiros/PhDThesis_RCampos.pdf) at the [University of Porto](https://www.up.pt/). The algorithm, initially implemented in C#, has now been made available as a Python package by [Jorge Mendes](https://github.com/JMendes1995) under the supervision of [Professor Ricardo Campos](http://www.ccc.ipt.pt/~ricardo/) in the scope of the Final Project of the Computer Science degree of the [Polytechnic Institute of Tomar](http://portal2.ipt.pt/), Portugal.

## What is Time-Matters
Time matters is a python package that aims to score the relevance of temporal expressions found within a text (single document) or a set of texts (multiple documents). 

The first (Time-Matters-SingleDoc) aims to determine the relevance of temporal expressions within a single document. 

The latter (Time-Matters-MultipleDocs), aims to determine the relevance of temporal expressions within multiple documents. 

## Rationale
Our assumption is that the relevance of a candidate date (d<sub>j</sub>) may be determined with regards to the relevant terms (W<sub>j</sub><sup>\*</sup>) that it co-occurs with in a given context (where a context can be a window of _n_ terms in a sentence, the sentence itself, or even a corpus of documents in case we are talking about a collection of multiple documents). That is: the more a given candidate date (d<sub>j</sub>) is correlated with the most relevant keywords (W<sub>j</sub><sup>\*</sup>) of a document (or documents), the more relevant the candidate date is.

## Documentation
Check out our wiki [Documentation](../../wiki) for full details about Time-Matters.

## How to Install Time-Matters

``` bash
pip install git+https://github.com/LIAAD/Time-Matters.git
```
#### Install External Dependencies
Time-Matters rests on the extraction of relevant keywords and temporal expressions found in the text.

For the first (that is, the extraction of relevant keywords), we resort to [YAKE!](https://github.com/LIAAD/yake) keyword extractor.

``` bash
pip install git+https://github.com/LIAAD/yake
```

For the latter (that is, the extraction of temporal expressions), we resort to two possibilities:
- rule-based approach
- [heideltime python wrapper](https://github.com/JMendes1995/py_heideltime)

The first, is an internal self-defined rule-based approach which is directly embedded in the code, thus, it doesn't require any additional procedure. However, if your plan is to use Heideltime you need to install the following packages.
``` bash
pip install git+https://github.com/JMendes1995/py_heideltime
```

You should also have [java JDK](https://www.oracle.com/technetwork/java/javase/downloads/index.html) and [perl](https://www.perl.org/get.html) installed in your machine for heideltime dependencies (note that none of this is needed should your plan is to only use a rule-based approach).

[[Back to the Table of Contents]](#Table-of-Contents)

#### External modules used (only for informative purposes):
    - YAKE
    - numpy
    - nltk
    - Pandas
    - regex
    - py_heideltime
    
##### Linux users
    If your user does not have permission executions on python lib folder, you should execute the following command:
    sudo chmod 111 /usr/local/lib/<YOUR PYTHON VERSION>/dist-packages/py_heideltime/HeidelTime/TreeTaggerLinux/bin/*
    
## How to use Time-Matters-SingleDoc
Time-Matters-SingleDoc aims to score temporal expressions found within a single text. Given an identified temporal expression it offers the user two scoring options:

- <b>ByDoc</b>: it retrieves a unique <b>single</b> score for each temporal expression found in the document, regardless it occurs multiple times in different parts of the text, that is, multiple occurrences of a temporal expression in different sentences (e.g., 2019....... 2019), will always return the same score (e.g., 0.92);

- <b>BySentence</b>: to retrieve a <b>multiple</b> (eventually different) score for each occurrence of a temporal expression found in the document, that is, multiple occurrences of a temporal expression in different sentences (e.g., 2019....... 2019), will return multiple (eventually different) scores (e.g., 0.92 for the occurrence of 2019 in sentence 1; and 0.77 for the occurrence of 2019 in sentence 2);

While the first one evaluates the score of a given candidate date in the context of a text, with regards to all the relevant keywords that it co-occurs with (regardless if it's on sentence 1 or 2), that is, both w<sub>1</sub>, as well as w<sub>2</sub> and w<sub>3</sub> will be considered in the computation of the temporal score of d<sub>1</sub> given by the GTE equation, i.e., (Median([IS(d<sub>1</sub>, w<sub>1</sub>); IS(d<sub>1</sub>, w<sub>2</sub>); IS(d<sub>1</sub>, w<sub>3</sub>)])): 
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/coOccurrences1.jpg" width="300">
</p>

The second, evaluates the score of a given candidate date with regards to the sentences where it occurs (thus taking into account only the relevant keywords of each sentence (within the search space defined)). This means that, if 2010 co-occurs with w<sub>1</sub> in sentence 1, only this relevant keyword will be considered to compute the temporal score of 2010 for this particular sentence. Likewise, if 2010 co-occurs with w<sub>2</sub> and with w<sub>3</sub> in sentence 2, only these relevant keywords will be considered to compute the temporal score of 2010 for this particular sentence. This means that we would have a temporal score of 2010 for sentence 1 computed by GTE equation as follows: (Median([IS(d<sub>1</sub>, w<sub>1</sub>)])), and a temporal score of 2010 for sentence 2 computed by GTE equation as follows: (Median([IS(d<sub>1</sub>, w<sub>2</sub>); IS(d<sub>1</sub>, w<sub>3</sub>)]))
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/coOccurrences2.jpg" width="300">
</p>

How to work with each one will be explained next. But before, both the libraries, as well as the text, need to be imported.

```` bash
from Time_Matters_SingleDoc import Time_Matters_SingleDoc

text= "2011 Haiti Earthquake Anniversary. As of 2010 (see 1500 photos here), the following major earthquakes "\
    "have been recorded in Haiti. The first great earthquake mentioned in histories of Haiti occurred in "\
    "1564 in what was still the Spanish colony. It destroyed Concepción de la Vega. On January 12, 2010, "\
    "a massive earthquake struck the nation of Haiti, causing catastrophic damage inside and around the "\
    "capital city of Port-au-Prince. On the first anniversary of the earthquake, 12 January 2011, "\
    "Haitian Prime Minister Jean-Max Bellerive said the death toll from the quake in 2010 was more "\
    "than 316,000, raising the figures in 2010 from previous estimates. I immediately flashed back to the afternoon "\
    "of February 11, 1975 when, on my car radio, I first heard the news. Yesterday..."
````

[[Back to the Table of Contents]](#Table-of-Contents)

#### ByDoc
<hr>

Getting temporal scores by doc is possible through the following code. This configuration assumes "py_heideltime" as default temporal tagger (more about this  [[here|Text-Representation#Temporal-Expressions]]), "ByDoc" as the default score_type and the default parameters of time_matters. In this configuration, a single score will be retrieved for a temporal expression regardless it occurs in different sentences.

```` bash
Score, TempExpressions, RelevantKWs, TextNormalized, TextTokens, SentencesNormalized, SentencesTokens = Time_Matters_SingleDoc(text)
#Score, TempExpressions, RelevantKWs, TextNormalized, TextTokens, SentencesNormalized, SentencesTokens = Time_Matters_SingleDoc(text, score_type="ByDoc")
````

#### BySentence
<hr>

Getting temporal scores by sentence is possible through the following code. This configuration assumes "py_heideltime" as default temporal tagger (more about this [[here|Text-Representation#Temporal-Expressions]]), "BySentence" as the score_type and the default parameters of time_matters. In this configuration, multiple occurrences of a temporal expression in different sentences (e.g., "As of 2010..."; "...the quake in 2010 was..."), will return multiple (eventually different) scores (e.g., 0.2 for its occurrence in sentence 1; and 0.982 for its occurrence on the other sentence).

```` bash
Score, NormalizedCandidateDates = Time_Matters_SingleDoc(text, score_type='BySentence')
````

#### Output
In the following, we explain the output obtained by the execution of the previous code (be it ByDoc or BySentence).
The structure of the score depends on the type of extraction considered: `ByDoc` or `BySentence`.

- <b>Score (for ByDoc)</b>:  A dictionary where the key is the normalized temporal expression and the value is a list with two positions. The first is the score of the temporal expression. The second is a list of the instances of the temporal expression (as they were found in the text). Example: `'2011-01-12': [0.5, ['2011-01-12', '12 January 2011']],`, means that the normalized temporal expression `2011-01-12` has a score of 0.5 and occurs twice in the text. The first time as `2011-01-12`, and the second time as `12 January 2011`.

```` bash
{'2011-01-12': [1.0, ['12 January 2011']],
 '2010': [0.983, ['2010', '2010', '2010']],
 '1564': [0.799, ['1564']],
 '2010-01-12': [0.743, ['January 12, 2010']],
 '2011': [0.568, ['2011']],
 '1975-02-11taf': [0, ['the afternoon of February 11, 1975']],
 '1975-02-10': [0, ['Yesterday']]}
````

- <b>Score (for BySentence)</b>:  A dictionary where the key is the normalized temporal expression and the value is a dictionary (where the key is the sentenceID and the value is a list with two positions. The first is the score of the temporal expression in that particular sentence. The second is a list of the instances of the temporal expression (as they were found in the text in that particular sentence). Example: `{'2010': {1: [0.2, ['2010']], 5: [0.983, ['2010', '2010']]}}`, means that the normalized temporal expression `2010` has a score of 0.2 in the sentence with ID 1, and a score of 0.983 in the sentence with ID 5 (where it occurs two times).

```` bash
{'2011': {0: [0.831, ['2011']]},
 '2010': {1: [0.2, ['2010']], 5: [0.983, ['2010', '2010']]},
 '1564': {2: [0.828, ['1564']]},
 '2010-01-12': {4: [0.68, ['January 12, 2010']]},
 '2011-01-12': {5: [1.0, ['12 January 2011']]},
 '1975-02-11taf': {6: [0, ['the afternoon of February 11, 1975']]},
 '1975-02-10': {7: [0, ['Yesterday']]}}
````

We highly recommend you to have a look at the [wiki Output](../../wiki/How-to-use-Time-Matters-SingleDoc#Output) section where more information about the remaining output (Temporal Expressions; Relevant Keywords; Text Normalized; Text Tokens; Sentences Normalized; Sentences Tokens) is given to the user.

[[Back to the Table of Contents]](#Table-of-Contents)


#### Optional Parameters
<hr>

We highly recommend you to have a look at the [wiki Optional Parameters](../../wiki/How-to-use-Time-Matters-SingleDoc#Optional-Parameters) section where a description of the advanced options (related to the temporal tagger and to time-matters) is offered to the user.


#### Debug
<hr>

We highly recommend you to have a look at the [wiki Debug Mode](../../wiki/How-to-use-Time-Matters-SingleDoc#Debug-Mode) section where an explanation of the debug structures (Inverted Index, Dice Matrix, Execution Time) is offered to the user.


#### CLI
<hr>

If you want to know how to execute Time-Matters through the prompt please refer to this [link](../../wiki/How-to-use-Time-Matters-SingleDoc#Cli).


## How to use Time-Matters-MultipleDocs
Time-Matters-MultipleDosc aims to score temporal expressions found within multiple texts. Given an identified temporal expression it offers the user three scoring options:

TODO TODOTODOTODO TODOTODOTODOTODOTODOTODOTODOTODOTODOTODOTODOTODOTODO

- <b>ByDoc</b>: it retrieves a unique <b>single</b> score for each temporal expression found in the document, regardless it occurs multiple times in different parts of the text, that is, multiple occurrences of a temporal expression in different sentences (e.g., 2019....... 2019), will always return the same score (e.g., 0.92);

- <b>BySentence</b>: to retrieve a <b>multiple</b> (eventually different) score for each occurrence of a temporal expression found in the document, that is, multiple occurrences of a temporal expression in different sentences (e.g., 2019....... 2019), will return multiple (eventually different) scores (e.g., 0.92 for the occurrence of 2019 in sentence 1; and 0.77 for the occurrence of 2019 in sentence 2);

While the first one evaluates the score of a given candidate date in the context of a text, with regards to all the relevant keywords that it co-occurs with (regardless if it's on sentence 1 or 2), that is, both w<sub>1</sub>, as well as w<sub>2</sub> and w<sub>3</sub> will be considered in the computation of the temporal score of d<sub>1</sub> given by the GTE equation, i.e., (Median([IS(d<sub>1</sub>, w<sub>1</sub>); IS(d<sub>1</sub>, w<sub>2</sub>); IS(d<sub>1</sub>, w<sub>3</sub>)])): 
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/coOccurrences1.jpg" width="300">
</p>

The second, evaluates the score of a given candidate date with regards to the sentences where it occurs (thus taking into account only the relevant keywords of each sentence (within the search space defined)). This means that, if 2010 co-occurs with w<sub>1</sub> in sentence 1, only this relevant keyword will be considered to compute the temporal score of 2010 for this particular sentence. Likewise, if 2010 co-occurs with w<sub>2</sub> and with w<sub>3</sub> in sentence 2, only these relevant keywords will be considered to compute the temporal score of 2010 for this particular sentence. This means that we would have a temporal score of 2010 for sentence 1 computed by GTE equation as follows: (Median([IS(d<sub>1</sub>, w<sub>1</sub>)])), and a temporal score of 2010 for sentence 2 computed by GTE equation as follows: (Median([IS(d<sub>1</sub>, w<sub>2</sub>); IS(d<sub>1</sub>, w<sub>3</sub>)]))
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/coOccurrences2.jpg" width="300">
</p>

How to work with each one will be explained next. But before, both the libraries, as well as the text, need to be imported.




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

- Campos, R., Dias, G., Jorge, A. and Nunes, C. (2017). Identifying Top Relevant Dates for Implicit Time Sensitive Queries. In Information Retrieval Journal. Springer, Vol 20(4), pp 363-398 [[pdf]](https://link.springer.com/article/10.1007/s10791-017-9302-1)

Other Time-Matters related papers may be found here:

- Campos, R., Dias, G., Jorge, A. and Nunes, C. (2016). GTE-Rank: a Time-Aware Search Engine to Answer Time-Sensitive Queries. In Information Processing & Management an International Journal. Elsevier, Vol 52(2), pp 273-298 [[pdf]](https://www.sciencedirect.com/science/article/abs/pii/S0306457315001016)

- Campos, R., Dias, G., Jorge, A., and Nunes, C. (2014). GTE-Cluster: A Temporal Search Interface for Implicit Temporal Queries. In M. de Rijke et al. (Eds.), Lecture Notes in Computer Science - Advances in Information Retrieval - 36th European Conference on Information Retrieval (ECIR2014). Amesterdam, Netherlands, 13 - 16 April. (Vol. 8416-2014, pp. 775 - 779) [[pdf]](https://link.springer.com/chapter/10.1007/978-3-319-06028-6_94#page-1)

- Campos, R., Jorge, A., Dias, G. and Nunes, C. (2012). Disambiguating Implicit Temporal Queries by Clustering Top Relevant Dates in Web Snippets. In Proceedings of The 2012 IEEE/WIC/ACM International Joint Conferences on Web Intelligence and Intelligent Agent Technologies Macau, China, 04 - 07 December, Vol. 1, pp 1 - 8. IEEE Computer Society Press. [[pdf]](https://ieeexplore.ieee.org/document/6511858?tp=&arnumber=6511858&url=http:%2F%2Fieeexplore.ieee.org%2Fxpls%2Fabs_all.jsp%3Farnumber%3D6511858)

### YAKE!
YAKE! papers may be found here:

- Campos R., Mangaravite V., Pasquali A., Jorge A.M., Nunes C., and Jatowt A. (2018). A Text Feature Based Automatic Keyword Extraction Method for Single Documents. In: Pasi G., Piwowarski B., Azzopardi L., Hanbury A. (eds). Advances in Information Retrieval. ECIR 2018 (Grenoble, France. March 26 – 29). Lecture Notes in Computer Science, vol 10772, pp. 684 - 691. [[pdf]](https://link.springer.com/chapter/10.1007/978-3-319-76941-7_63). [<b>ECIR'18 Best Short Paper</b>]

- Campos R., Mangaravite V., Pasquali A., Jorge A.M., Nunes C., and Jatowt A. (2018). YAKE! Collection-independent Automatic Keyword Extractor. In: Pasi G., Piwowarski B., Azzopardi L., Hanbury A. (eds). Advances in Information Retrieval. ECIR 2018 (Grenoble, France. March 26 – 29). Lecture Notes in Computer Science, vol 10772, pp. 806 - 810. [[pdf]](https://link.springer.com/chapter/10.1007/978-3-319-76941-7_80)

### InfoSimba
InfoSimba similarity measure papers may be found here:
- Dias, G., Alves, E., & Lopes, J. (2007). Topic Segmentation Algorithms for Text Summarization and Passage Retrieval: An Exhaustive Evaluation. In AAAI 2007: Proceedings of the 22nd Conference on Artificial Intelligence (pp. 1334 - 1340). Vancouver, Canada. July 22 – 26.: AAAI Press.
[[pdf]](https://pdfs.semanticscholar.org/b9ef/4f739ae625f753c0ffc687369a6f335c22c1.pdf?_ga=2.179772898.733053942.1561296709-837078907.1557947535)

### Heideltime
Heideltime papers may be found here:

- Strötgen, J., and Gertz, M. (2013). Multilingual and Cross-domain Temporal Tagging. In: Language Resources and Evaluation, 47(3), pp. 269-298. [[pdf]](https://link.springer.com/article/10.1007%2Fs10579-012-9179-y)

or [here](https://github.com/HeidelTime/heideltime#Publications)

## Awards
Winner of the [Fraunhofer Portugal Challenge 2013 PhD Contest](https://www.aicos.fraunhofer.pt/en/news_and_events_aicos/news_archive/older_archive/fraunhofer-portugal-challenge-2013-winners.html)

## License

## Contact
For any inquires about Time-Matters please contact [Ricardo Campos](http://www.ccc.ipt.pt/~ricardo/): ricardo.campos@ipt.pt
