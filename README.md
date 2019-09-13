
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
[How to use Time-Matters](#How-to-use-Time-Matters)
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
import nltk
nltk.download('punkt')

Time-Matters rests on the extraction of relevant keywords and temporal expressions found in the text.

For the first (that is, the extraction of relevant keywords), we resort to [YAKE!](https://github.com/LIAAD/yake) keyword extractor.

``` bash
pip install git+https://github.com/LIAAD/yake
```

For the latter (that is, the extraction of temporal expressions), we resort to two possibilities:
- [rule-based approach](https://github.com/JMendes1995/py_rule_based)
- [heideltime python wrapper](https://github.com/JMendes1995/py_heideltime)

The first, is an internal self-defined rule-based approach developed in regex. The latter is a Python wrapper for the well-known Heideltime temporal tagger.

To work with both within the Time-Matters package the following packages should be installed:
``` bash
pip install git+https://github.com/JMendes1995/py_rule_based
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
    - py_rule_based
    
##### Linux users
    If your user does not have permission executions on python lib folder, you should execute the following command:
    sudo chmod 111 /usr/local/lib/<YOUR PYTHON VERSION>/dist-packages/py_heideltime/HeidelTime/TreeTaggerLinux/bin/*

## How to use Time-Matters
We highly recommend you to resort to this [Python Notebook](notebook.ipynb) should you want to play with Time-Matters. In any case you can read the following sections to familiarize with Time-Matters.

## How to use Time-Matters-SingleDoc
Time-Matters-SingleDoc aims to score temporal expressions found within a single text. Given an identified temporal expression it offers the user two scoring options:

- <b>ByDoc</b>: it retrieves a unique <b>single</b> score for each temporal expression found in the document, regardless it occurs multiple times in different parts of the text, that is, multiple occurrences of a temporal expression in different sentences (e.g., 2019....... 2019), will always return the same score (e.g., 0.92);

- <b>BySentence</b>: to retrieve a <b>multiple</b> (eventually different) score for each occurrence of a temporal expression found in the document, that is, multiple occurrences of a temporal expression in different sentences (e.g., 2019....... 2019), will return multiple (eventually different) scores (e.g., 0.92 for the occurrence of 2019 in sentence 1; and 0.77 for the occurrence of 2019 in sentence 2);

While the first one evaluates the score of a given candidate date in the context of a text, with regards to all the relevant keywords that it co-occurs with (regardless if it's on sentence 1 or 2), the second, evaluates the score of a given candidate date with regards to the sentences where it occurs (thus taking into account only the relevant keywords of each sentence (within the search space defined)). 

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

#### Score
The structure of the score depends on the type of extraction considered: `ByDoc` or `BySentence`.

##### ByDoc
<hr>
Getting temporal scores by doc is possible through the following code. This configuration assumes "py_heideltime" as default temporal tagger, "ByDoc" as the default score_type and the default parameters of time_matters. In this configuration, a single score will be retrieved for a temporal expression regardless it occurs in different sentences.

```` bash
results = Time_Matters_SingleDoc(text)
#results = Time_Matters_SingleDoc(text, score_type="ByDoc")
````

The output is a dictionary where the key is the normalized temporal expression and the value is a list with two positions. The first is the score of the temporal expression. The second is a list of the instances of the temporal expression (as they were found in the text). Example: `'2011-01-12': [0.5, ['2011-01-12', '12 January 2011']],`, means that the normalized temporal expression `2011-01-12` has a score of 0.5 and occurs twice in the text. The first time as `2011-01-12`, and the second time as `12 January 2011`.

```` bash
results[0]

{'2011-01-12': [1.0, ['12 January 2011']],
 '2010': [0.983, ['2010', '2010', '2010']],
 '1564': [0.799, ['1564']],
 '2010-01-12': [0.743, ['January 12, 2010']],
 '2011': [0.568, ['2011']],
 '1975-02-11taf': [0, ['the afternoon of February 11, 1975']],
 '1975-02-10': [0, ['Yesterday']]}
````

##### BySentence
<hr>

Getting temporal scores by sentence is possible through the following code. This configuration assumes "py_heideltime" as default temporal tagger, "BySentence" as the score_type and the default parameters of time_matters. In this configuration, multiple occurrences of a temporal expression in different sentences (e.g., "As of 2010..."; "...the quake in 2010 was..."), will return multiple (eventually different) scores (e.g., 0.2 for its occurrence in sentence 1; and 0.982 for its occurrence on the other sentence).

```` bash
results = Time_Matters_SingleDoc(text, score_type='BySentence')
````

The output is a dictionary where the key is the normalized temporal expression and the value is a dictionary (where the key is the sentenceID and the value is a list with two positions. The first is the score of the temporal expression in that particular sentence. The second is a list of the instances of the temporal expression (as they were found in the text in that particular sentence). Example: `{'2010': {1: [0.2, ['2010']], 5: [0.983, ['2010', '2010']]}}`, means that the normalized temporal expression `2010` has a score of 0.2 in the sentence with ID 1, and a score of 0.983 in the sentence with ID 5 (where it occurs two times).

```` bash
results[0]

{'2011': {0: [0.831, ['2011']]},
 '2010': {1: [0.2, ['2010']], 5: [0.983, ['2010', '2010']]},
 '1564': {2: [0.828, ['1564']]},
 '2010-01-12': {4: [0.68, ['January 12, 2010']]},
 '2011-01-12': {5: [1.0, ['12 January 2011']]},
 '1975-02-11taf': {6: [0, ['the afternoon of February 11, 1975']]},
 '1975-02-10': {7: [0, ['Yesterday']]}}
````
#### Remaining Output
<hr>

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

If you want to know how to execute Time-Matters SingleDoc through the prompt please refer to this [link](../../wiki/How-to-use-Time-Matters-SingleDoc#Cli).


## How to use Time-Matters-MultipleDocs
Time-Matters-MultipleDocs aims to score temporal expressions found within multiple texts. Given an identified temporal expression it offers the user three scoring options:

- <b>ByCorpus</b>: it retrieves a unique <b>single</b> score for each temporal expression found in the corpus of documents, regardless it occurs multiple times in different documents, that is, multiple occurrences of a temporal expression in different documents, will always return the same score (e.g., 0.92);

- <b>ByDoc</b>: to retrieve a <b>multiple</b> (eventually different) score for each occurrence of a temporal expression found in the set of documents, that is, multiple occurrences of a temporal expression in different documents, will return multiple (eventually different) scores (e.g., 0.92 for the occurrence of 2019 in document 1; and 0.77 for the occurrence of 2019 in document 2);

- <b>ByDocSentence</b>: to retrieve a multiple (eventually different) score for each occurrence of a temporal expression found in a given document, that is, multiple occurrences of a temporal expression in different sentences (e.g., 2019....... 2019) of a document, will return <b>multiple</b> (eventually different) scores (e.g., 0.92 for the occurrence of 2019 in sentence 1 of document 1; and 0.77 for the occurrence of 2019 in sentence 2 of document 1);

While the first one evaluates the score of a given candidate date in the context of a corpus of texts, with regards to all the relevant keywords that it co-occurs with (regardless if it's on document 1 or document 2), the second, evaluates the score of a given candidate date with regards to the documents where it occurs (thus taking into account only the relevant keywords of each document (within the search space defined)). Finally, the third evaluates the score of a given candidate date with regards to the documents and sentences where it occurs (thus taking into account only the relevant keywords of each sentence of a given document (within the search space defined)).

How to work with each one will be explained next. Before that, we explain how to import the libraries and a set of text documents. We suggest you to play with your own texts, or in alternative, to download a set of 28 documents ([MultiDocTexts.zip](MultiDocTexts.zip)) that we make available in this git as a running example. In any case, if you want to use the following code, don't forget to put the texts under a folder named `data/MultiDocTexts`. 

```` bash
from Time_Matters_MultipleDocs import Time_Matters_MultipleDocs

import os
path = 'data/MultiDocTexts'
ListOfDocs = []
for file in os.listdir (path) :
    with open(os.path.join(path, file),'r') as f:
        txt = f.read()
        ListOfDocs.append(txt)  
````

#### Score
The structure of the score depends on the type of extraction considered: `ByCorpus`, `ByDoc` or `ByDoc&Sentence`.

##### ByCorpus
<hr>

Getting temporal scores by a corpus of documents is possible through the following code: `results = Time_Matters_MultipleDocs(ListOfDocs)` This configuration assumes "py_heideltime" as the default temporal tagger, "ByCorpus" as the default score_type and the default parameters of time_matters. In this configuration, a single score will be retrieved for a temporal expression regardless it occurs in different documents.

Running this code, however, will take a considerable amount of time (depending on the PC used) as Heideltime temporal tagger will be running on top of 28 texts. If you want a quicker solution (though not effective) you should use a rule-based approach instead (more about this on the Optional Parameters section). Also letting `py_heideltime` getting all the possible temporal expressions from the text might become too cumbersome. For that reason, we opt to set the date granularity to year and the document timestamp to ´2013-04-15´ (the date of the Boston marathon bombings).

```` bash
results = Time_Matters_MultipleDocs(ListOfDocs, temporal_tagger=['py_heideltime', 'English', 'year', 'news', '2013-04-15'])
#results = Time_Matters_MultipleDocs(ListOfDocs, score_type="ByCorpus", temporal_tagger=['py_heideltime', 'English', 'year', 'news', '2013-04-15'])
````

The output is a dictionary where the key is the normalized temporal expression and the value is a list with two positions. The first is the score of the temporal expression. The second is a dictionary of the instances of the temporal expression (as they were found in each document). Example: `{'2011-01-12': [1.0, {0: ['2011-01-12', '12 January 2011'], 6: ['2011-01-12']}]}`, means that the normalized temporal expression `2011-01-12` has a score of 1 and occurs twice (the first time as `2011-01-12`, and the second time as `12 January 2011`) in document 0 and one time (as '2011-01-12') in document 6. 

```` bash
Score = results[0]
Score
````

##### ByDoc
<hr>

Getting temporal scores by document is possible through the following code. This configuration assumes "py_heideltime" as default temporal tagger, "ByDoc" as the score_type and the default parameters of time_matters. In this configuration, multiple occurrences of a temporal expression in different documents, will return multiple (eventually different) scores (e.g., 0.92 for the occurrence of 2019 in sentence 1 of document 1; and 0.77 for the occurrence of 2019 in sentence 2 of document 1). Once again, we apply the `year` granularity to avoid getting too many fine-grained temporal expressions. Yet, you are more than welcome to alternatively run the following code: `results = Time_Matters_MultipleDocs(ListOfDocs, score_type='ByDoc')`.

```` bash
results = Time_Matters_MultipleDocs(ListOfDocs, score_type='ByDoc', temporal_tagger=['py_heideltime', 'English', 'year', 'news', '2013-04-15'])
````

The output is a dictionary where the key is the normalized temporal expression and the value is a dictionary (where the key is the DocID and the value is a list with two positions. The first is the score of the temporal expression in that particular document. The second is a list of the instances of the temporal expression (as they were found in the text in that particular document). Example: `{'2010': {1: [0.2, ['2010']], 5: [0.983, ['2010', '2010']]}}`, means that the normalized temporal expression `2010` has a score of 0.2 in the document with ID 1, and a score of 0.983 in the document with ID 5 (where it occurs two times).

```` bash
Score = results[0]
Score
````

##### ByDocSentence
<hr>

Getting temporal scores by document & sentence is possible through the following code. This configuration assumes "py_heideltime" as default temporal tagger, "ByDoc&Sentence" as the score_type and the default parameters of time_matters. In this configuration, multiple occurrences of a temporal expression in different sentences of a given document, will return multiple (eventually different) scores (e.g., 0.2 for its occurrence in document 1; and 0.982 for its occurrence in document 2). Once again, we apply the `year` granularity to avoid getting too many fine-grained temporal expressions. Yet, you are more than welcome to alternatively run the following code: `results = Time_Matters_MultipleDocs(ListOfDocs, score_type='ByDocSentence')`.

```` bash
results = Time_Matters_MultipleDocs(ListOfDocs, score_type='ByDocSentence', temporal_tagger=['py_heideltime', 'English', 'year', 'news', '2013-04-15'])
````

The output is a dictionary where the key is the normalized temporal expression and the value is a dictionary (where the key is the DocID and the value is a new dictionary (where the key is the sentenceID and the value is list with two positions. The first is the score of the temporal expression in that particular sentence. The second is a list of the instances of the temporal expression (as they were found in the text in that particular setencent of that document)). Example: `{'2011': {0: {5: [0.983, ['2010', '2010']], {6: [0.183, ['2010']]}}`, means that the normalized temporal expression `2011` has a score of 0.983 in the sentence with ID 5 (where it occurs twice) of docID 0, and a score of 0.183 in the sentence with ID 6 of docID 0.

```` bash
Score = results[0]
Score
````
#### Remaining Output
<hr>

We highly recommend you to have a look at the [wiki Output](../../wiki/How-to-use-Time-Matters-MultipleDocs#Output) section where more information about the remaining output (Temporal Expressions; Relevant Keywords; Text Normalized; Text Tokens; Sentences Normalized; Sentences Tokens) is given to the user.

[[Back to the Table of Contents]](#Table-of-Contents)


#### Optional Parameters
<hr>

We highly recommend you to have a look at the [wiki Optional Parameters](../../wiki/How-to-use-Time-Matters-MultipleDocs#Optional-Parameters) section where a description of the advanced options (related to the temporal tagger and to time-matters) is offered to the user.


#### Debug
<hr>

We highly recommend you to have a look at the [wiki Debug Mode](../../wiki/How-to-use-Time-Matters-MultipleDocs#Debug-Mode) section where an explanation of the debug structures (Inverted Index, Dice Matrix, Execution Time) is offered to the user.


#### CLI
<hr>

If you want to know how to execute Time-Matters MultipleDocs through the prompt please refer to this [link](../../wiki/How-to-use-Time-Matters-MultipleDocs#Cli).

## API
https://time-matters.inesctec.pt/api

## Publications
### Time-Matters
If you use Time-Matters please cite the appropriate paper. In general, this will be:

- Campos, R., Dias, G., Jorge, A. and Nunes, C. (2017). Identifying Top Relevant Dates for Implicit Time Sensitive Queries. In Information Retrieval Journal. Springer, Vol 20(4), pp 363-398 [[pdf]](https://link.springer.com/article/10.1007/s10791-017-9302-1)

Other Time-Matters related papers may be found here:

- Campos, R., Dias, G., Jorge, A. and Nunes, C. (2016). GTE-Rank: a Time-Aware Search Engine to Answer Time-Sensitive Queries. In Information Processing & Management an International Journal. Elsevier, Vol 52(2), pp. 273-298 [[pdf]](https://www.sciencedirect.com/science/article/abs/pii/S0306457315001016)

- Campos, R., Dias, G., Jorge, A., and Nunes, C. (2014). GTE-Cluster: A Temporal Search Interface for Implicit Temporal Queries. In M. de Rijke et al. (Eds.), Lecture Notes in Computer Science - Advances in Information Retrieval - 36th European Conference on Information Retrieval (ECIR2014). Amesterdam, Netherlands, 13 - 16 April. (Vol. 8416-2014, pp. 775 - 779) [[pdf]](https://link.springer.com/chapter/10.1007/978-3-319-06028-6_94#page-1)

- Campos, R., Jorge, A., Dias, G. and Nunes, C. (2012). Disambiguating Implicit Temporal Queries by Clustering Top Relevant Dates in Web Snippets. In Proceedings of The 2012 IEEE/WIC/ACM International Joint Conferences on Web Intelligence and Intelligent Agent Technologies Macau, China, 04 - 07 December, Vol. 1, pp 1 - 8. IEEE Computer Society Press. [[pdf]](https://ieeexplore.ieee.org/document/6511858?tp=&arnumber=6511858&url=http:%2F%2Fieeexplore.ieee.org%2Fxpls%2Fabs_all.jsp%3Farnumber%3D6511858)

### YAKE!
YAKE! papers may be found here:

- Campos R., Mangaravite V., Pasquali A., Jorge A.M., Nunes C., and Jatowt A. (2019). YAKE! Keyword Extraction from Single Documents using Multiple Local Features. In Information Sciences. Elsevier, Vol XX(X), pp. XX-XX [[pdf]](https://linkinghub.elsevier.com/retrieve/pii/S0020025519308588).

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
