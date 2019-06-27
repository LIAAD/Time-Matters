
## Table of Contents
[Time-Matters](#Time-Matters)
<br>
[What is Time-Matters](#What-is-Time-Matters)
<br>
[Rationale](#Rationale)
<br>
[How does it works](#How-does-it-works)
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Text Representation](#Text-Representation)
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Relevant Keywords](#Relevant-Keywords)
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Temporal Expressions](#Temporal-Expressions)
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Temporal Similarity Measure](#Temporal-Similarity-Measure)
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[InfoSimba](#InfoSimba)
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Context Vectors](#Context-Vectors)
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Computing DICE](#Computing-DICE)
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Median Function](#Median-Function)
<br>
[How to Install Time-Matters](#How-to-Install-Time-Matters)
<br>
[How to use Time-Matters-SingleDoc](#How-to-use-Time-Matters-SingleDoc)
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Single Score](#Single-Score)
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Default Parameters](#Default-Parameters)
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[All the Parameters](#All-the-Parameters)
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Multiple Scores](#Multiple-Scores)
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Default Parameters](#Default-parameters)
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[All the Parameters](#All-the-parameters)
<br>
[How to use Time-Matters-MultipleDocs](#How-to-use-Time-Matters-MultipleDocs)
<br>
[Debug](#Debug)
<br>
[API](#API)
<br>
[Publications](#Publications)
<br>
[Awards](#Awards)
<br>
[Contact](#Contact)

# Time-Matters

Time matters is the result of a research conducted by Ricardo Campos during his [PhD](http://www.ccc.ipt.pt/~ricardo/ficheiros/PhDThesis_RCampos.pdf) at the [University of Porto](https://www.up.pt/). The algorithm, initially implemented in C#, has now been made available as a Python package by [Jorge Mendes](https://github.com/JMendes1995) under the supervision of [Professor Ricardo Campos](http://www.ccc.ipt.pt/~ricardo/) in the scope of the Final Project of the Computer Science degree of the [Polytechnic Institute of Tomar](http://portal2.ipt.pt/), Portugal.

## What is Time-Matters
Time matters is a python package that aims to score the relevance of temporal expressions found within a text (single document) or a set of texts (multiple documents). 

The first (Time-Matters-SingleDoc) aims to determine the relevance of temporal expressions within a single document. 

The latter (Time-Matters-MultipleDocs), aims to determine the relevance of temporal expressions within multiple documents. 

## Rationale
Our assumption is that the relevance of a candidate date (d<sub>j</sub>) may be determined with regards to the relevant terms (W<sub>j</sub><sup>\*</sup>) that it co-occurs with in a given context (where a context can be a window of _n_ terms in a sentence, the sentence itself, or even a corpus of documents in case we are talking about a collection of multiple documents). That is: the more a given candidate date (d<sub>j</sub>) is correlated with the most relevant keywords (W<sub>j</sub><sup>\*</sup>) of a document (or documents), the more relevant the candidate date is.

## How does it works?
Unlike previous metadata and query log-based approaches, we achieve this goal based on information extracted from the document's contents. 

### Text Representation
Each _T<sub>i</sub>_, for _i = 1,...,n_, that is, each text, is represented by a number of relevant keywords and a number of candidate temporal expressions. In what follows, we assume that each text _T<sub>i</sub>_ is composed by two different sets denoted _W<sub>T<sub>i</sub></sub>_ and _D<sub>T<sub>i</sub></sub>_:<br>
<p align="center"> 
T<sub>i</sub> = (W<sub>T<sub>i</sub></sub>, D<sub>T<sub>i</sub></sub>)	
</p>

where _W<sub>T<sub>i</sub></sub>_ = {_w<sub>1,i</sub>, w<sub>2,i</sub>, ..., w<sub>k,i</sub></sub>_} is the set of the _k_ most relevant terms associated with a text _T<sub>i</sub>_ and _D<sub>T<sub>i</sub></sub>_ = {_d<sub>1,i</sub>, d<sub>2,i</sub>, ..., d<sub>t,i</sub></sub>_} is the set of the _t_ candidate temporal expressions associated with a text _T<sub>i</sub>_. Moreover, <br>
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/Wt.jpg" width="100">
</p>
is the set of distinct relevant keywords extracted, within a text or a set of texts T, i.e., the relevant vocabulary. Similarly, <br>
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/Dt.jpg" width="100">
</p>
is defined as the set of distinct candidate temporal expressions extracted from a text or a set of texts T.<br>
<br>
To illustrate our algorithm we present the following running example:
Let W<sub>T</sub> = {w<sub>1</sub>; w<sub>2</sub>; w<sub>3</sub>; w<sub>4</sub>; w<sub>5</sub>; w<sub>6</sub>} be the set of distinct relevant keywords, D<sub>T</sub> = {d<sub>1</sub>; d<sub>2</sub>; d<sub>3</sub>; d<sub>4</sub>;} the set of candidate dates and (W<sub>j</sub><sup>*</sup>) as the set of relevant words W<sub>T</sub> that co-occur with each of the four candidate dates D<sub>T</sub> in the search space (to be defined).
<br>
<br>
The following picture shows the list of six keywords W<sub>T</sub> that co-occur with the four candidate dates D<sub>T</sub>. In each column, the "X" indicate the keywords belonging to the (W<sub>j</sub><sup>*</sup>). For the sake of understanding we consider d<sub>1</sub> to be "2010", and w<sub>1</sub> to be "Haiti".
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/coOccurrences.jpg" width="350">
</p>

##### Relevant Keywords
Relevant keywords in Time-Matters can be identified through YAKE!, a keyword extractor system ([ECIR'18](http://www.ecir2018.org) Best Short Paper) which is available not only on a [demo-based](http://yake.inesctec.pt) purpose, but also through a [Python package](https://github.com/LIAAD/yake). In this work, relevant keywords (num_of_keywords) equals to *n*, where *n* is any number > 0.

If you are interested in knowing more about YAKE! please refer to the [Publications](#Publications) section where you can find a few papers about it.

##### Temporal Expressions
Temporal expressions in Time-Matters can be identified through:
- [Heideltime Temporal Tagger](https://heideltime.ifi.uni-heidelberg.de/heideltime/) by means of a [Python wrapper package](https://github.com/JMendes1995/py_heideltime)
- Rule-based approach

The first (temporal_tagger = "py_heideltime") uses a Python wrapper of Heideltime Temporal Tagger (state-of-the-art in this kind of task). It is able to detect a huge number of different types of temporal expressions, yet, depending on the size of the text it may require a considerable amount of time to execute. In this work, we set py_heideltime to its default parameters (that is, Language='English' and document_type='news'). If you are interested in knowing more about Heideltime please refer to the [Publications](#Publications) section where you can find a few papers about it.

The second (temporal_tagger = "rule_based") makes use of a self-defined rule-based approach which is able to detect the following patterns:
- yyyy(./-)mm(./-)dd
- dd(./-)mm(./-)yyyy
- yyyy(./-)yyyy
- yyyys
- yyyy

While not as good (i.e., effective) as Heideltime, it can be used when efficiency (time-performance) is a requirement.

### Temporal Similarity Measure
To model this temporal relevance, we define a Generic Temporal Similarity measure (GTE) that makes use of co-occurrences of keywords and temporal expressions as a means to identify relevant d<sub>j</sub> dates within a text _T<sub>i</sub>_.

GTE ranges between 0 and 1, and is defined as follows:<br>
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/GTE1.jpg" width="350">
</p>

In the equation, `median` is the median function, `IS` is the InfoSimba similarity measure, and `W`<sub>l, j</sub> represents one of the several terms of (`W`<sub>j</sub><sup>\*</sup>), that co-occur with the candidate date `d`<sub>j</sub> within a text `t`<sub>i</sub>. A more detailed description of the median function and of the IS similarity measure will be given next.

##### InfoSimba
In this work, we apply the InfoSimba (IS) second-order similarity measure, a measure supported by corpus-based token correlations proposed by [Dias et al. (2007)](https://pdfs.semanticscholar.org/b9ef/4f739ae625f753c0ffc687369a6f335c22c1.pdf?_ga=2.179772898.733053942.1561296709-837078907.1557947535). While first order association measures (e.g., DICE) evaluate the relatedness between two tokens as they co-occur in a given context (e.g., a sentence, a paragraph, a corpus), second order measures are based on the principle that two words are similar if their corresponding context vectors are also similar. 
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/First_vs_Second1.jpg" width="350">
</p>

The intuition behind second order similarity measures is that two terms having many co-occurring words often carry the same sense in such a way that the information content of both words is likely to share similar terms. For instance, the similarity between the terms ‘‘professor’’ and ‘‘teacher’’ is expected to rest on a number of common co-occurring words such as student, school, etc. Likewise, the similarity between the terms '2010' and 'haiti' is expected to be related with terms about the earthquake. Adopting one such solution, will enable to overcome the problem of data sparseness in cases when two terms, despite being similar, do not co-occur frequently in a corpus.

InfoSimba is defined as follows:<br>
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/IS1.jpg" width="300">
</p>

IS calculates the correlation between all pairs of two context vectors X and Y, where X is the context vector representation of `W`<sub>l, j</sub>, Y is the context vector representation of `d`<sub>j</sub> and DICE is the DICE similarity measure.


###### Context Vectors
Each context vector `X` (that is, `W`<sub>l, j</sub>) and `Y` (that is, `d`<sub>j</sub>) consists of N terms (where n is any value > 0, or the word 'max' if, instead, we want to consider all the terms) with a DICE similarity greater than a given threshold (TH, where TH is any value > 0, thus guaranteeing that the terms co-occur between them). For instance, to determine the context vector of a candidate date `d`<sub>j</sub> only those keywords `(w`<sub>1</sub>`,w`<sub>2</sub>`,...,w`<sub>k</sub>`)` and candidate dates `(d`<sub>1</sub>`,d`<sub>2</sub>`,...,d`<sub>t</sub>`)` having a minimum `DICE similarity > TH` with `(.,d`<sub>j</sub>`)` are eligible for the N-size context vector.

A representation of the context vectors is given in the following figure. Again for sake of understanding we consider d<sub>j</sub> to be "2010" and w<sub>l, j</sub> to be "haiti":<br>
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/VectorRepresentation2.jpg" width="250">
</p>

By looking at the picture we can observe that both vectors X (that is, `W`<sub>l, j</sub>) and Y (that is, `d`<sub>j</sub>) are represented by `N` terms (keywords such as `w`<sub>1</sub> and candidate dates such as `d`<sub>1</sub>) with a `DICE similarity value > TH`.

###### Computing DICE
In order to compute the similarity between terms, we begin by setting a n-contextual window distance (n_contextual_window) which defines the search space where co-occurrences between terms may be counted. To this regard, we consider two possible search spaces:
- the <b>full sentence</b> itself (n_contextual_window = "full_sentence"), that is, the system will look for co-occurrences between terms that occur within the search space of a sentence;
- a <b>window of n terms</b> (n_contextual_window = n, where n is any value > 0), that is, the system will look for co-occurrences between terms that occur within a window of n terms;

In order to better understand this process, we consider the following figure:
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/nContextualWindow1.jpg" width="250">
</p>
By looking at the picture, we can observe three segments (for instance, three sentences, in case we are working with a single document, or three documents should we be working with multiple documents). In the picture, x and y represent two different terms, and n represent the n-contextual window distance between them.

<br>In our work, similarities between terms are computed using [Dice coefficient](https://www.jstor.org/stable/1932409?seq=1#page_scan_tab_contents) as follows:
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/DICE1.jpg" width="175">
</p>

where |x| counts the number of distinct segments where x appears, |y| counts the number of distinct segments where y occurs, and |x| intersected with |y| counts the number of distinct segments where both terms occur together within the defined context window.

For the first case, we consider to count co-occurrences within the <b>full sentence</b>, meaning that the n-contextual window distance will simply not be taken into account, that is, co-occurrences between terms will be counted regardless the distance between them, and as long as they appear in the same sentence. Thus, we will have a |x| of 3 (as x occurs in 3 distinct segments), a |y| of 2 (as y occurs in 2 distinct segments), and a |x| intersected with |y| of 2 (as both terms only occur together - within the search space sentence - in two distinct sentences). This would result in the following DICE similarity value:
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/DICE2.jpg" width="200">
</p>

For the second case, we consider to count co-occurrences within a <b>window of n tokens</b>, that is, co-occurrences between terms will be counted as long as they appear together in the same sentence, in a window of n tokens. For the purposes of this example, we consider a window where `n = 10`. Thus, we will have a |x| of 3 (as x occurs in 3 distinct segments), a |y| of 2 (as y occurs in 2 distinct segments), and a |x| intersected with |y| of 1 (as both terms only occur together - within the search space of 10 tokens - in the second segment. Indeed, if look carefully at segment 1 we will observe that x and y dist 12 tokens between them, which is greater than 10). This would result in the following DICE similarity value:
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/DICE3.jpg" width="200">
</p>

The calculated DICE similarities will then be stored in a matrix that keeps all the similarities between all the terms (keywords `(w`<sub>1</sub>`,w`<sub>2</sub>`,...,w`<sub>k</sub>`)` and candidate dates `(d`<sub>1</sub>`,d`<sub>2</sub>`,...,d`<sub>t</sub>`)` (see the figure bellow) under the search space defined.
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/DICE_matrix3.jpg" width="400">
</p>

By looking at the similarities stored on the matrix we can then compute the final IS score for each candidate date. For instance, for d<sub>1</sub> = 2010, this means we will have to compute the similarities between (d<sub>1</sub>,w<sub>1</sub>), (d<sub>1</sub>,w<sub>2</sub>) and (d<sub>1</sub>,w<sub>3</sub>), as according to our example, d<sub>1</sub> co-occurs with each of this relevant keywords in a given search space.
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/coOccurrences1.jpg" width="300">
</p>

<br>In this example, we will only consider the calculation between d<sub>1</sub> = 2010 and w<sub>1</sub> = haiti. In order to construct each corresponding vector we will consider all the terms (thus N = maximum number) that co-occur the candidate vector (likewise with the keyword vector) having a DICE similarity > 0. This means that the vector representation of w<sub>1</sub> would consist of 9 elements (all but the w<sub>1</sub> itself will be selected) and the vector representation of d<sub>1</sub> would be made of 5 elements (that is all the terms with DICE similarities > 0, but itself will be selected). 
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/VectorRepresentation4.jpg" width="350">
</p>

<br>Given that the vectors have to have the same N size, we need to reduce the size of the w<sub>1</sub> vector, such that it ends with the same size of the d<sub>1</sub> vector. IS can now be computed as the corresponding similarity between each pairs of terms present in the N-size context vectors as depicted in following figure. Specifically, it will compute the level of relatedness between w<sub>3</sub> from the context vector of w<sub>1</sub> and the two other context terms of d<sub>1</sub>, i.e., w<sub>2</sub>, d<sub>4</sub>, d<sub>2</sub>, d<sub>3</sub> and w<sub>3</sub>, and then between d<sub>2</sub> and from the context vector of w<sub>1</sub> and the two other context terms of d<sub>1</sub>, and so on and so forth.
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/VectorRepresentation5.jpg" width="250">
</p>

<br>Instead, if we consider a size of N = 2 (for a matter of simplicity) we would have the following vector representation:
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/VectorRepresentation6.jpg" width="200">
</p>

<br> The final score of (d<sub>1</sub>,w<sub>1</sub>) which stems from applying the IS equation will be:
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/IS2.jpg" width="350">
</p>

<br>By looking at the similarities stored on the matrix we can then compute the final value as follows:
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/IS5.jpg" width="350">
</p>

<br>Similarly we should process the similarities between d<sub>1</sub> and the remaining words of (W<sub>d<sub>j</sub></sub><sup>\*</sup>), i.e., w<sub>2</sub> and w<sub>3</sub>. The final score of each computation is given as follows:
- IS(d<sub>1</sub>,w<sub>2</sub>) = 0.606
- IS(d<sub>1</sub>,w<sub>3</sub>)) = 0.439

Next, we describe the F aggregation function which is used to combine the several smilarity values sim(w<sub>l,j</sub>,d<sub>j</sub>), computed by IS.

##### Median Function
All these similarity values are then combined through the median measure (a measure of central tendency). In our running example this would represent a final score of `median[0.439, 0.606, 0.439] = 0.439`.

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
Time-Matters-SingleDoc aims to score temporal expressions found within a single text. Given an identified temporal expression it offers the user two options: 

- to retrieve a unique <b>single</b> score for each temporal expression found regardless it occurs multiple times in different parts of the text, that is, multiple occurrences of a temporal expression in different sentences (e.g., 2019....... 2019), will always return the same score (e.g., 0.92);

- to retrieve a <b>multiple</b> (eventually different) score for each occurrence of a temporal expression, that is, multiple occurrences of a temporal expression in different sentences (e.g., 2019....... 2019), will return multiple (eventually different) scores (e.g., 0.92 for the occurrence of 2019 in sentence 1; and 0.77 for the occurrence of 2019 in sentence 2); 

How to work with each one will be explained next. But before, both the libraries, as well as the text, need to be imported.

```` bash
from Time_Matters_SingleDoc import Time_Matters_SingleDoc

text= "2011 Haiti Earthquake Anniversary. As of 2010 (see 1500 photos here), the following major earthquakes "\
    "have been recorded in Haiti. The first great earthquake mentioned in histories of Haiti occurred in "\
    "1564 in what was still the Spanish colony. It destroyed Concepción de la Vega. On January 12, 2010, "\
    "a massive earthquake struck the nation of Haiti, causing catastrophic damage inside and around the "\
    "capital city of Port-au-Prince. On the first anniversary of the earthquake, 12 January 2011, "\
    "Haitian Prime Minister Jean-Max Bellerive said the death toll from the quake in 2010 was more "\
    "than 316,000, raising the figures from previous estimates. I immediately flashed back to the afternoon "\
    "of February 11, 1975 when, on my car radio, I first heard the news. Yesterday..."
````
#### Single Score
<hr>
Output objetive: to retrieve a unique score for each temporal expression, regardless it occurs multiple times in different parts of the text, that is, multiple occurrences of a temporal expression in different sentences (e.g., 2019....... 2019), will always return the same score (e.g., 0.92);

##### _Default Parameters_
Default temporal tagger is "py_heideltime" (More about this [here](#Text-Representation) and [here](#Temporal-Expressions)), and the score type is "single" (More about this [here](#How-to-use-Time-Matters-SingleDoc)) which means that having:
```` bash
Time_Matters_SingleDoc(text)
````
or:
```` bash
Time_Matters_SingleDoc(text, temporal_tagger=['py_heideltime'], score_type='single')
````
is exactly the same thing and produces the same results.

While 'py_heideltime' is the default temporal tagger, a 'rule_based' approach can be used instead.
```` bash
Time_Matters_SingleDoc(text, temporal_tagger=['rule_based'], score_type='single')
````

The following code is an attempt to print the results of Time-Matters for temporal expressions identified with 'py_heideltime' and 'rule_based'
```` bash
print(Time_Matters_SingleDoc(text, temporal_tagger=['py_heideltime'], score_type='single'))
print(Time_Matters_SingleDoc(text, temporal_tagger=['rule_based'], score_type='single'))
````

###### Output
The output is a dictionary where the key is the temporal expression (as it was found on the document) and value is the score given by GTE.
``` bash
#py_heideltime results
{'12 January 2011': 1.0,
 '2010': 0.982,
 '1564': 0.798,
 'January 12, 2010': 0.7425,
 '2011': 0.73,
 'the afternoon of February 11, 1975': 0,
 'yesterday': 0}

#rule_based results
{'1975': 1.0, '2011': 0.966, '2010': 0.913, '1500': 0.862, '1564': 0.856}
```

##### _All the Parameters_

Besides the *temporal_tagger* and the *score_type* we can also specify the time matters parameters, which consists of a list of four elements:
- *num_of_keywords*: number of YAKE! keywords to extract from the text. Default value is *10* (but any value > 0 is considered) meaning that the system will extract 10 relevant keywords from the text. More about this [here](#Text-Representation) and [here](#Relevant-Keywords). 
- *n_contextual_window*: defines the n-contextual window distance. Default value is "*full_sentence*" (but a n-window where n > 0 can be considered as alternative), that is, the system will look for co-occurrences between terms that occur within the search space of a sentence; More about this [here](#Computing-Dice).
- *N*: size of the context vector for X and Y at InfoSimba. Default value is '*max*' (but any value > 0 is considered) meaning that the context vector should have the maximum number of n-terms co-occurring with X (likewise with Y). More about this [here](#Context-Vectors).
- *TH*: minimum threshold value from which terms are eligible to the context vector X and Y at InfoSimba. Default value is *0.05* (but any value > 0 is considered) meaning that any terms co-occuring between them with a DICE similarity value > 0.05 are eligible for the n-size vector. More about this [here](#Context-Vectors).

In addition, one can also specify additional parameters for the temporal_tagger. This is particularly evident when the temporal_tagger is py_heideltime, for which we can specify the 'language', the 'date_granularity', the 'document_type' and the 'document_creation_time'. More about py_heideltime parameters [here](https://github.com/JMendes1995/py_heideltime/#How-to-use-py_heideltime).

``` bash
Time_Matters_SingleDoc(text, temporal_tagger=['py_heideltime', 'English', '', 'news', '2019-06-01'], time_matters=[10, 'full_sentence', 'max', 0.05], score_type='single')
```

###### Output
The output is the same as above (as the parameters specified here are exactly the same as the default above ones).

#### Multiple Scores
<hr>
Output  objetive: to retrieve a different score for each occurrence of a temporal expression, that is, multiple occurrences of a temporal expression in different sentences (e.g., 2019....... 2019), will return multiple (eventually different) scores (e.g., 0.92 for the occurrence of 2019 in sentence 1; and 0.77 for the occurrence of 2019 in sentence 2).

##### Default parameters
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
##### All the parameters
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

Usage_examples (make sure that the input parameters are within quotes):

  Default Parameters: Time_Matters_SingleDoc -i "['text', 'August 31st']" -tt "['py_heideltime','English']"
  All the Parameters: Time_Matters_SingleDoc -i "['text', 'August 31st']" -tt "['py_heideltime','English', 'days', 'news', '2019-05-05']" -tm "[10,'none', 'max', 0.05]" -st single -dm False

Options:
  [required]: either specify a text or an input_file path.
  ----------------------------------------------------------------------------------------------------------------------------------------
  -i, --input LIST               A list that specifies the type of input: a text or a file path
                                 Example:
                                         "['text', 'August 31st']"
                                         "['path', 'c:\text.txt']"



 [not required]
  ----------------------------------------------------------------------------------------------------------------------------------------
  -tt, --temporal_tagger LIST    Specifies the temporal tagger ("py_heideltime", "rule-based") and the corresponding parameters.
                                 default is "py_heideltime"
				 
				 py_heideltime (parameters):
				 ____________________________
				 - temporal_tagger_name
				   options:
					   "py_heideltime"

				 - Language of the text
				   options:
					   "English";
					   "Portuguese";
					   "Spanish";
					   "Germany";
					   "Dutch";
					   "Italian";
					   "French".

				 - date_granularity
				   options:
					   "year" (means that for the date YYYY-MM-DD only the YYYY will be retrieved);
					   "month" (means that for the date YYYY-MM-DD only the YYYY-MM will be retrieved);
					   "day" (means that for the date YYYY-MM-DD it will retrieve YYYY-MM-DD).

				 - document_type
				   options:
					   "News" for news-style documents - default param;
					   "Narrative" for narrative-style documents (e.g., Wikipedia articles);
					   "Colloquial" for English colloquial (e.g., Tweets and SMS);
					   "Scientific" for scientific articles (e.g., clinical trails).

				 - document_creation_time
				   Document creation date in the format YYYY-MM-DD. Taken into account when "News" or 
				   "Colloquial" texts are specified.
				   Example: "2019-05-30".

				 - Example: "['py_heideltime','English', 'days', 'news', '2019-05-05']"	 
				 
				 Rule_Based (parameters):
				 ____________________________
				 - temporal_tagger_name
				   options:
					   "rule_based"

				 - date_granularity
				   options:
					   "year" (means that for the date YYYY-MM-DD only the YYYY will be retrieved);
					   "month" (means that for the date YYYY-MM-DD only the YYYY-MM will be retrieved);
					   "day" (means that for the date YYYY-MM-DD it will retrieve YYYY-MM-DD).

				 - Example: "['rule_based','days']"

  [not required]
  ----------------------------------------------------------------------------------------------------------------------------------------
  -tm, --time_matters LIST        Specifies information about Time-Matters, namely:
				  - num_of_keywords: number of YAKE! keywords to extract from the text
				    options:
					    - default is 10, meaning it will extract 10 relevant keywords from the text
					    - other values can be used (e.g., 5, 15, etc)

				  - context_window_distance: co-occurrences between terms (where a term may be a relevant keyword or a 
				    temporal expression) are computed with regards to the distance here defined.
				    options:
                                            - default is "none", meaning that it will not consider a specified distance between terms, 
					      instead  it will consider as a co-occurrence, all the terms that co-occur within the
					      sentence being analyzed
					    - other values can be used. For instance, using a value of 10, means it will look for 
					      co-ocurrences within a window of 10 tokens (10 to the left and 10 to the right),
					      guaruanteeing that it will not go other sentences besides the one being analyzed. 
					    
				 Fazer DAQUI PARA A FRENTE
				 
					- information regarding the construction of the vocabulary context vector (context_vector_size,
                                            threshold_sim_value), and information concerning the scope of search ()
				
                                            context_vector_size
                                            	Option:
                                               	 	"max"; Means that will be considered the maximun number of words in context vector
                                                    Intiger

                                         Example: "[num_of_keywords=10, context_window_distance=10, context_vector_size='max', threshold_sim_value=0.05]"

  ----------------------------------------------------------------------------------------------------------------------------------------
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

## How to use Time-Matters-MultipleDocs
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

## Debug

## API
https://time-matters-api.herokuapp.com/

## Publications
### Time-Matters
If you use Time-Matters please cite the appropriate paper. In general, this will be:

- Campos, R., Dias, G., Jorge, A. and Nunes, C. (2017). Identifying Top Relevant Dates for Implicit Time Sensitive Queries. In Information Retrieval Journal. Springer, Vol 20(4), pp 363-398 [[pdf]](https://link.springer.com/article/10.1007/s10791-017-9302-1)

Other Time-Matters related papers may be found here:

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

## Contact
For any inquires about Time-Matters please contact [Ricardo Campos](http://www.ccc.ipt.pt/~ricardo/): ricardo.campos@ipt.pt
