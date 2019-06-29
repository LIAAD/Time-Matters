
## Table of Contents
[Time-Matters](#Time-Matters)
<br>
[Quick Start](#Quick-Start)
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
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Default Parameters](#SD-Default-Parameters)
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[All the Parameters](#SD-All-the-Parameters)
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Debug](#SD-Debug)
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Python Cli](#SD-Python-CLI)
<br>
[How to use Time-Matters-MultipleDocs](#How-to-use-Time-Matters-MultipleDocs)
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

[[Table of Contents]](#Table-of-Contents)

## Quick Start
If you don't need to understand in detail the algorithm behind Time-Matters, i.e., if you want to play with this package without getting into details, I suggest you to do one of two things:

(1) If you want to extract scores for temporal expressions found within a single text (assuming the default parameters, and a single score for each temporal expression found (regardless it occurs in differente sentences)) go [here](#SD-Default-Parameters).

(2) If you want to extract scores for temporal expressions found within multiples texts (assuming the default parameters, and a single score for each temporal expression found (regardless it occurs in differente documents)) go [here](#MD-Default-Parameters).

## What is Time-Matters
Time matters is a python package that aims to score the relevance of temporal expressions found within a text (single document) or a set of texts (multiple documents). 

The first (Time-Matters-SingleDoc) aims to determine the relevance of temporal expressions within a single document. 

The latter (Time-Matters-MultipleDocs), aims to determine the relevance of temporal expressions within multiple documents. 

[[Table of Contents]](#Table-of-Contents)

## Rationale
Our assumption is that the relevance of a candidate date (d<sub>j</sub>) may be determined with regards to the relevant terms (W<sub>j</sub><sup>\*</sup>) that it co-occurs with in a given context (where a context can be a window of _n_ terms in a sentence, the sentence itself, or even a corpus of documents in case we are talking about a collection of multiple documents). That is: the more a given candidate date (d<sub>j</sub>) is correlated with the most relevant keywords (W<sub>j</sub><sup>\*</sup>) of a document (or documents), the more relevant the candidate date is.

[[Table of Contents]](#Table-of-Contents)

## How does it works?
Unlike previous metadata and query log-based approaches, we achieve this goal based on information extracted from the document's contents. 

[[Table of Contents]](#Table-of-Contents)

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
Let W<sub>T</sub> = {w<sub>1</sub>; w<sub>2</sub>; w<sub>3</sub>; w<sub>4</sub>; w<sub>5</sub>; w<sub>6</sub>} be the set of distinct relevant keywords, D<sub>T</sub> = {d<sub>1</sub>; d<sub>2</sub>; d<sub>3</sub>; d<sub>4</sub>;} the set of candidate dates and (W<sub>j</sub><sup>*</sup>) as the set of relevant words W<sub>T</sub> that co-occur (within a given search space - to be defined) with each of the four candidate dates D<sub>T</sub> found in the text (or texts, in case we are talking about multiple documents).
<br>
<br>
The following picture shows the list of six keywords W<sub>T</sub> that co-occur with the four candidate dates D<sub>T</sub>. In each column, the "X" indicate the keywords belonging to the (W<sub>j</sub><sup>*</sup>). For the sake of understanding we consider d<sub>1</sub> to be "2010", and w<sub>1</sub> to be "Haiti". By looking at the picture we can understand that the candidate date 2010, occurs (within a given search space, for instance a sentence) with the relevant keywords w<sub>1</sub>, w<sub>2</sub> and w<sub>3</sub>. For instance, it could have occurred (hyphotetically) with w<sub>1</sub> on sentence one, with w<sub>2</sub> and w<sub>3</sub> on sentence two.

<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/coOccurrences.jpg" width="350">
</p>

[[Table of Contents]](#Table-of-Contents)

##### Relevant Keywords
Relevant keywords in Time-Matters can be identified through YAKE!, a keyword extractor system ([ECIR'18](http://www.ecir2018.org) Best Short Paper) which is available not only on a [demo-based](http://yake.inesctec.pt) purpose, but also through a [Python package](https://github.com/LIAAD/yake). In this work, relevant keywords (num_of_keywords) equals to *n*, where *n* is any number > 0.

If you are interested in knowing more about YAKE! please refer to the [Publications](#Publications) section where you can find a few papers about it.

[[Table of Contents]](#Table-of-Contents)

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

[[Table of Contents]](#Table-of-Contents)

### Temporal Similarity Measure
To model this temporal relevance, we define a Generic Temporal Similarity measure (GTE) that makes use of co-occurrences of keywords and temporal expressions as a means to identify relevant d<sub>j</sub> dates within a text _T<sub>i</sub>_.

GTE ranges between 0 and 1, and is defined as follows:<br>
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/GTE1.jpg" width="350">
</p>

In the equation, `median` is the median function, `IS` is the InfoSimba similarity measure, and `W`<sub>l, j</sub> represents one of the several terms of (`W`<sub>j</sub><sup>\*</sup>), that co-occur with the candidate date `d`<sub>j</sub> within a text `t`<sub>i</sub>. A more detailed description of the median function and of the IS similarity measure will be given next.

[[Table of Contents]](#Table-of-Contents)

#### InfoSimba
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

[[Table of Contents]](#Table-of-Contents)

###### Context Vectors
Each context vector `X` (that is, `W`<sub>l, j</sub>) and `Y` (that is, `d`<sub>j</sub>) consists of N terms (where n is any value > 0, or the word 'max' if, instead, we want to consider all the terms) with a DICE similarity greater than a given threshold (TH, where TH is any value > 0, thus guaranteeing that the terms co-occur between them). For instance, to determine the context vector of a candidate date `d`<sub>j</sub> only those keywords `(w`<sub>1</sub>`,w`<sub>2</sub>`,...,w`<sub>k</sub>`)` and candidate dates `(d`<sub>1</sub>`,d`<sub>2</sub>`,...,d`<sub>t</sub>`)` having a minimum `DICE similarity > TH` with `(.,d`<sub>j</sub>`)` are eligible for the N-size context vector.

A representation of the context vectors is given in the following figure. Again for sake of understanding we consider d<sub>j</sub> to be "2010" and w<sub>l, j</sub> to be "haiti":<br>
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/VectorRepresentation2.jpg" width="250">
</p>

By looking at the picture we can observe that both vectors X (that is, `W`<sub>l, j</sub>) and Y (that is, `d`<sub>j</sub>) are represented by `N` terms (keywords such as `w`<sub>1</sub> and candidate dates such as `d`<sub>1</sub>) with a `DICE similarity value > TH`.

[[Table of Contents]](#Table-of-Contents)

###### Computing DICE
In order to compute the similarity between terms, we need to extract statistical information from the corpus. In our case, a corpus can be a single document or multiple documents.
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/Corpus.jpg" width="450">
</p>

Extracting this statistical information is grounded on three factors: (1) the type of `Corpus` (single document or multiple documents); (2) the `Search Space` that should be taken into account when accounting for individual term occurrences; and the (3) `n-contextual window` that should be taken into account when accounting for the co-occurrences between the terms.

<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/Corpus2.jpg" width="1150">
</p>

When looking at the figure, it becomes clear that in the case of the `Single Doc`, the` Search Space` (that is, the space considered in accounting for the individual occurrences of the terms) are the `sentences` of the document. In turn, the counting of the co-occurrences between terms, can be done in the space of a sentence (`Full Sentence`), or within a (` Window of n-terms, n> 0`) in the space of a sentence.

In the case of the **` Mutiple Docs`**, there are two hypotheses for the `Search Space` (that is, for the space considered in the counting of the individual occurrences of the terms): the` Sentence` space and the `Documents` space. In case the search space is **`Sentence`**, the counting of co-occurrences between terms can be done in the space of a sentence (`Full Sentence`), or in a (`Window of n-terms, n> 0`) in the space of a sentence. In case the search space is the  **`Document`**, the counting of co-occurrences between the terms can be done in the space of a document (`Full Document`), or in a (`Window of n-terms , n> 0`) in the space of a document (ensuring that the terms co-occur in the same sentence).

In the following we describe each one of them in more detail.

<b>Single Document</b> <br>
In the case of a single document, individual occurrences of terms (keywords and candidate dates) are counted on the document's sentences. Co-occurrences of terms, in turn, are counted within the two following *n_contextual_window*'s:

- <b>sentence</ b> (*n_contextual_window = "full_sentence"*), in which co-occurrence between terms is accounted for at the *sentence* level.
- <b> window of n terms </ b> (*n_contextual_window = n, where n> 0*), in which co-occurrence between terms is counted in a window of *n* terms defined in the search space of a *sentence*.

Such a contextual window requires each term to be stored in an Inverted Index with the following structure:
{key: [SF, TotFreq, {SentID : [Freq, [OffSets]],......}]}

where `key` is the term (a relevant keyword or a candidate date that is found in the document), `SF` is the Sentence Frequency (i.e., the number of document sentences where the term occurs, `TotFreq` is the total frequency of the term in the document, `SentID` is the ID of the sentence where the term appears, `Freq` is the frequency of the term in that particular sentence, and `OffSets` is the the list of offsets where the term appears in that particular sentence. For instance, a term with the following structure '2010': [2, 3, {1: [1, [6]], 5: [2, [87, 96]]}] means that it has 3 occurrences in 2 different sentences. In the sentence with ID 1, it occurs 1 time in position 6. In sentence with ID 5, it occurs 2 times in position 87 and 96.

Once this structure is defined, we can then compute the similarities between terms. In order to better understand this process, we consider the following figure:
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/nContextualWindow2.jpg" width="250">
</p>
By looking at the picture, we can observe a document consisting of three sentences. In the picture, x and y represent two different terms, and n represent the n-contextual window distance between them.

<br>In our work, similarities between terms are computed using [Dice coefficient](https://www.jstor.org/stable/1932409?seq=1#page_scan_tab_contents) as follows:
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/DICE1.jpg" width="175">
</p>

where |x| counts the number of distinct sentences where x appears, |y| counts the number of distinct sentences where y occurs, and |x| intersected with |y| counts the number of distinct sentences where both terms co-occur together within the defined context window.

In this first example, `sentences` is the `search space` considered for counting the occurrence of terms, while the <b>full sentence</b> and a <b>window of n terms</b> are the *n_contextual_window*'s considered to register the co-occurrences between terms.

For the first case (the <b>full sentence</b>), we consider to count co-occurrences between terms within the full sentence, meaning that the distance between terms will simply not be taken into account, that is, co-occurrences between terms will be counted regardless the distance between them, and as long as they appear in the same sentence. Thus, we will have a |x| of 3 (as x occurs in 3 distinct sentences), a |y| of 2 (as y occurs in 2 distinct sentences), and a |x| intersected with |y| of 2 (as both terms only occur together - within the search space sentence - in 2 distinct sentences). This would result in the following DICE similarity value:
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/DICE2.jpg" width="200">
</p>

For the second case (a <b>window of n tokens</b>), we consider to count co-occurrences within a window of n tokens, that is, co-occurrences between terms will be counted as long as they appear together in the same sentence, in a window of n tokens. For the purposes of this example, we consider a window where `n = 10`. Thus, we will have a |x| of 3 (as x occurs in 3 distinct sentences), a |y| of 2 (as y occurs in 2 distinct sentences), and a |x| intersected with |y| of 1 (as both terms only occur together - within the search space sentence and a window of 10 tokens - in the second sentence. Indeed, if we look carefully at sentences 1 we will observe that x and y dist 12 tokens between them, which is greater than 10). This would result in the following DICE similarity value:
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/DICE3.jpg" width="200">
</p>

<b>Multiple Documents</b> <br>
In the case of multiple documents, individual occurrences of terms (keywords and candidate dates) can be counted on (a) document's; and on (b) document's sentences. 

For the first (<b>documents</b>), Co-occurrences of terms, are counted within the two following *n_contextual_window*'s:

- the <b>full document</b> itself (n_contextual_window = "full_document"), that is, the system will look for co-occurrences between terms that co-occur within the search space of a document;
- a <b>window of n terms</b> (n_contextual_window = n, where n > 0), that is, the system will look for co-occurrences between terms that co-occur within a window of n terms within the search space of a document;


For the second (<b>sentences</b>), Co-occurrences of terms, are counted within the two following *n_contextual_window*'s:

- the <b>full sentence</b> itself (n_contextual_window = "full_sentence"), that is, the system will look for co-occurrences between terms that co-occur within the search space of a document sentence;
- a <b>window of n terms</b> (n_contextual_window = n, where n is any value > 0), that is, the system will look for co-occurrences between terms that co-occur within a window of n terms within the search space of a document sentence;

In order to compute the similarities between terms under this kind of contextual windows, we consider an Inverted Index with the following structure:
{key: [DF, TotFreq, {DocID : [DocFreq, [DocOffSets], {SentID : [SentFreq, [SentOffsets]]},......}]}

where `key` is the term (a relevant keyword or a candidate date that is found within the corpus of documents), `DF` is the Document Frequency (i.e., the number of documents where the term occurs, `TotFreq` is the total frequency of the term in the set of documents, `DocID` is the ID of the document where the term appears, `DocFreq` is the frequency of the term in that particular document, `DocOffSets` is the the list of offsets where the term appears in that particular document, `SentID` is the ID of the sentence where the term appears in that particular document, `SentFreq` is the frequency of the term in that particular sentence of the document, and `SentOffSets` is the the list of offsets where the term appears in that particular sentence of the document.

For instance, a term with the following structure '2010': [2, 3, {1: [1, [6], {1 : [1, [6]]}], 5: [3, [87, 96, 106], {8: [1, [87]], 10: [2, [96, 106]]}     ]}] means that it has 3 occurrences in 2 different documents. In the document with ID 1, it occurs 1 time in position 6, or, if seen at the sentence level, it occurs 1 time in the sentence with ID 1 at position 6. In document with ID 5, it occurs 3 times in position 87, 96 and 106, or, if seen at the sentence level, it occurs 1 time in the sentence with ID 8 at position 87, and 2 times in the sentence with ID 10 at positions 96 and 106.

Once this structure is defined, we can then compute the similarities between terms. In order to better understand this process, we consider the following figure:
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/nContextualWindow3.jpg" width="250">
</p>

By looking at the picture, we can observe a corpus consisting of three documents. In the picture, x and y represent two different terms, and n represent the n-contextual window distance between them.

<br>In our work, similarities between terms are computed using [Dice coefficient](https://www.jstor.org/stable/1932409?seq=1#page_scan_tab_contents) as follows:
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/DICE1.jpg" width="175">
</p>

where |x| counts the number of distinct documents or sentences (depending on the search space considered) where x appears, |y| counts the number of distinct documents or document sentences (depending on the search space considered) where y appears, and |x| intersected with |y| counts the number of distinct documents or document sentences (depending on the search space considered) where both terms co-occur together within the defined context window.

In this example we begin by considering `documents` to be the search space where individual occurrences are counted, and the two following *n_contextual_window*'s where co-occurrences between terms are counted: the <b>full document</b> and a <b>window of n terms</b>.

For the first case (search space: <b>documents</b>; window: <b>full document</b>), we consider to count co-occurrences between terms within the <b>full document</b>, meaning that the n-contextual window distance will simply not be taken into account, that is, co-occurrences between terms will be counted regardless the distance between them, and as long as they appear in the same document. Thus, we will have a |x| of 3 (as x occurs in 3 distinct documents), a |y| of 2 (as y occurs in 2 distinct documents), and a |x| intersected with |y| of 2 (as both terms only occur together - within the search space document - in two distinct documents). This would result in the following DICE similarity value:
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/DICE2.jpg" width="200">
</p>

For the second case (search space: <b>documents</b>; window: a <b>window of n terms</b>), we consider to count co-occurrences within a <b>window of n tokens</b>, that is, co-occurrences between terms will be counted as long as they appear together in the same document and sentence, in a window of n tokens. For the purposes of this example, we consider a window where `n = 10`. Thus, we will have a |x| of 3 (as x occurs in 3 distinct documents), a |y| of 2 (as y occurs in 2 distinct documents), and a |x| intersected with |y| of 1 (as both terms only occur together - within the search space document and a window of 10 tokens - in document 1 (indeed they occur twice is under this restriction). This would result in the following DICE similarity value:
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/DICE3.jpg" width="200">
</p>

Next, we begin by considering `sentences` to be the search space where individual occurrences are counted, and the two following *n_contextual_window*'s where co-occurrences between terms are counted: the <b>full sentence</b> and a <b>window of n terms</b>.

For the first case (search space: <b>sentences</b>; window: <b>full sentence</b>), we consider to count co-occurrences within the <b>full sentence </b>, meaning that the n-contextual window distance will simply not be taken into account, that is, co-occurrences between terms will be counted regardless the distance between them, and as long as they appear in the same sentence. Thus, we will have a |x| of 5 (as x occurs in 5 distinct document sentences, 3 in document one, 1 in document two, and 1 in document three), a |y| of 4 (as y occurs in 4 distinct documents, 2 in document one, and 2 n document two), and a |x| intersected with |y| of 2 (as both terms only occur together - within the search space sentences - in two distinct sentences). This would result in the following DICE similarity value:
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/DICE4.jpg" width="200">
</p>

For the second case (search space: <b>sentences</b>; window: a <b>window of n terms</b>), we consider to count co-occurrences within a <b>window of n tokens</b>, that is, co-occurrences between terms will be counted as long as they appear together in the same document and sentence, in a window of n tokens. For the purposes of this example, we consider a window where `n = 10`. Thus, we will have a |x| of 5 (as x occurs in 5 distinct sentences), a |y| of 4 (as y occurs in 4 distinct sentences), and a |x| intersected with |y| of 1 (as both terms only occur together - within the search space sentence and a window of 10 tokens - in just one sentence (in document 1). Indeed, if the terms also occur at sentence 1 of document 1, yet with a distance of 12 tokens between them, which is greater than 10). This would result in the following DICE similarity value:
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/DICE5.jpg" width="200">
</p>


<b>DICE Matrix</b> <br>
The calculated DICE similarities will then be stored in a matrix that keeps all the similarities between all the terms (keywords `(w`<sub>1</sub>`,w`<sub>2</sub>`,...,w`<sub>k</sub>`)` and candidate dates `(d`<sub>1</sub>`,d`<sub>2</sub>`,...,d`<sub>t</sub>`)` (see the figure bellow for illustrative purposes) under the search space defined.
<p align="center">
  <img src="http://www.ccc.ipt.pt/~ricardo/images/DICE_matrix3.jpg" width="400">
</p>

###### Compute GTE Scores for each Candidate Date
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

[[Table of Contents]](#Table-of-Contents)

#### Median Function
All these similarity values are then combined through the median measure (a measure of central tendency). In our running example this would represent a final score of `median[0.439, 0.606, 0.439] = 0.439`.

[[Table of Contents]](#Table-of-Contents)

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

[[Table of Contents]](#Table-of-Contents)

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

[[Table of Contents]](#Table-of-Contents)

#### _SD Default Parameters_
<hr>

This configuration assumes "py_heideltime" as default temporal tagger (more about this [here](#Text-Representation) and [here](#Temporal-Expressions)), "ByDoc" as the default score_type(more about this [here](#How-to-use-Time-Matters-SingleDoc)) and the default parameters of time_matters.
```` bash
Time_Matters_SingleDoc(text)
````
The output is a dictionary where the key is the temporal expression (as it was found on the document) and value is the score given by GTE.

While 'py_heideltime' is the default temporal tagger, a 'rule_based' approach can be used instead.
```` bash
Time_Matters_SingleDoc(text, temporal_tagger=['rule_based'])
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
 'Yesterday': 0}

#rule_based results
{'1975': 1.0, '2011': 0.966, '2010': 0.913, '1500': 0.862, '1564': 0.856}
```

In addition, one can also specify multiple scores instead of single scores, that is, multiple occurrences of a temporal expression in different sentences (e.g., "As of 2010..."; "...the quake in 2010 was..."), will return multiple (eventually different) scores (e.g., 0.2 for its occurrence in sentence 1; and 0.982 for its occurrence in the other sentence). 

```` bash
Time_Matters_SingleDoc(text, score_type='BySentence')
````

###### Output
The output here, is a dictionary where the key is the temporal expression (as it was found on the document) and the value is a list of tuples with two elements (the first returns the sentence ID, the second returns the score of the temporal expression in that particular sentence).
``` bash
#py_heideltime results
{'2011': [(0, 0.831)],
 '2010': [(1, 0.2), (5, 0.982)],
 '1564': [(2, 0.827)],
 'January 12, 2010': [(4, 0.68)],
 '12 January 2011': [(5, 1.0)],
 'the afternoon of February 11, 1975': [(6, 0)],
 'Yesterday': [(7, 0)]}
 ```

[[Table of Contents]](#Table-of-Contents)

#### _SD All the Parameters_
<hr>

Besides the *temporal_tagger* and the *score_type* we can also specify the time matters parameters, which consists of a list of four elements:
- *num_of_keywords*: number of YAKE! keywords to extract from the text. Default value is *10* (but any value > 0 is considered) meaning that the system will extract 10 relevant keywords from the text. More about this [here](#Text-Representation) and [here](#Relevant-Keywords). 
- *n_contextual_window*: defines the n-contextual window distance. Default value is "*full_sentence*" (but a n-window where n > 0 can be considered as alternative), that is, the system will look for co-occurrences between terms that occur within the search space of a sentence; More about this [here](#Computing-Dice).
- *N*: size of the context vector for X and Y at InfoSimba. Default value is '*max*' (but any value > 0 is considered) meaning that the context vector should have the maximum number of n-terms co-occurring with X (likewise with Y). More about this [here](#Context-Vectors).
- *TH*: minimum threshold value from which terms are eligible to the context vector X and Y at InfoSimba. Default value is *0.05* (but any value > 0 is considered) meaning that any terms co-occuring between them with a DICE similarity value > 0.05 are eligible for the n-size vector. More about this [here](#Context-Vectors).

In addition, one can also specify additional parameters for the temporal_tagger. This is particularly evident when the temporal_tagger is py_heideltime, for which we can specify the 'language', the 'date_granularity', the 'document_type' and the 'document_creation_time'. More about py_heideltime parameters [here](https://github.com/JMendes1995/py_heideltime/#How-to-use-py_heideltime).

``` bash
Time_Matters_SingleDoc(text, temporal_tagger=['py_heideltime', 'English', 'full', 'news', '2019-06-01'], time_matters=[10, 'full_sentence', 'max', 0.05], score_type='ByDoc')
```
Obviously, we can also specify a multiple value for the score_type as seen before:
``` bash
Time_Matters_SingleDoc(text, temporal_tagger=['py_heideltime', 'English', 'full', 'news', '2019-06-01'], time_matters=[10, 'full_sentence', 'max', 0.05], score_type='BySentence')
```

###### Output
The output is the same as above (as the parameters specified here are exactly the same as the default above ones).

[[Table of Contents]](#Table-of-Contents)

#### _SD Debug_
We also offer the user a debug mode where users can access a more detailed version of the results, namely access to the `Text`, `TextNormalized`, `Score`, `CandidateDates`, `NormalizedCandidateDates`, `RelevantKWs`, `IIndex`, `Dice_Matrix`.

- <b>Text</b>: a slightly normalized version of the input text, where temporal expressions with more than one token are joined with an underscore. By doing this, we guarantee that temporal expressions are easily identified in the text by means of its offset. This may be used for example to highlight or underline a given temporal expression in the context of some GUI.
- <b>NormalizedText</b>: a normalized version of the input text, where temporal expressions appear normalized (according to the temporal tagger used). For instance, the temporal expression `the afternoon of February 11, 1975` will appear as `1975-02-11taf` in the text. This may be used in the DICE_Matrix (more on this bellow) to understand where normalized temporal expressions do appear in the text.
- <b>Score</b>: the output of the score in debug mode depends whether we are using 'ByDoc' or 'BySentence' score. For <b>ByDoc</b> score, the output will be a dictionary, where the key is the temporal expression (as it was found in the text), and the value is a list with two positions (the first is the score determined by Time-Matters; the second is a list of offsets where the temporal expression can be found in the text. Recall that indexes in Python start in 0). For instance, `{'2010': [0.982, [6, 87, 96]]}` means that the temporal expression `2010` has a score of `0.982` and appears at position `6`, `87` and `96`. Similarly, `'the_afternoon_of_February_11,_1975': [0, [103]]` means that the temporal expression `the_afternoon_of_February_11,_1975` has a zero score and appears at position `103`. For <b>BySentence</b> score, the output will be a dictionary, where the key is the temporal expression (as it was found in the text), and the value is another dictionary where the key is the sentence id, and the value is a list with two positions (the first is the score determined by Time-Matters; the second is a list of offsets where the temporal expression can be found in that particular sentence). For instance, `{'2010': {'1': [0.2, [6]]}, {'5': [0.982, [87, 96]]}}` means that the temporal expression `2010` has a score of `0.2` in sentence id `1` where appears at position `6`, and a score of `0.982` in sentence id `5` where appears at position `87` e `96`.
- <b>CandidateDates</b>: a dictionary of the candidates dates (as they appear on the text) and their corresponding normalized version. For instance, the two following entries: `'January_12,_2010': '2010-01-12',`; `'2010-01-12': '2010-01-12'`, means that the two temporal expressions `January_12,_2010` and `2010-01-12` are both normalized to `2010-01-12`. In our algorithm, candidate dates are detected by a `rule_based` solution or by using [py_heideltime](https://github.com/JMendes1995/py_heideltime). If you want to know more about the role of each one in Time-Matters, please refer to the following [link](#Text-Representation).
- <b>NormalizedCandidateDates</b>: a dictionary of the normalized version of the candidates dates and their corresponding instances (as they appear on the text). For instance, the entry : `'2010-01-12' : ['January_12,_2010', '2010-01-12']`, means that the normalized temporal expression `2010-01-12` has at least one entry in the text as `January_12,_2010` and another one as `2010-01-12`. In our algorithm, candidate dates are detected by a `rule_based` solution or by using [py_heideltime](https://github.com/JMendes1995/py_heideltime). If you want to know more about the role of each one in Time-Matters, please refer to the following [link](#Text-Representation).
- <b>RelevantKWs</b>: a list of the relevant keywords used by our algorithm in the process of assigning a score to temporal expressions. In our algorithm, keywords are detected by [YAKE!](https://github.com/LIAAD/yake). If you want to know more about the role of YAKE! in Time-Matters, please refer to the following [link]((#Text-Representation).
- <b>IIndex</b>: An inverted index of the document, most notably of its relevant keywords and candidate dates. As other inverted indexes it follows the following dictionary structure: `{'term' : [SF, TotFreq, {SentenceID : [Offsets]}]`, where `SF` is the `Sentence Frequency`, `TotFreq` is the `total frequency` of the term, `SentenceID` is the `ID of the sentence` (knowing that IDs start on 0), and `[Offsets]` is a list of offsets, that is, a list of the position(s) where the term appears in the text. For instance, a term with the following structure `'2010': [2, 3, {1: [1, [6]], 5: [2, [87, 96]]}]` means that it has 3 occurrences in 2 different sentences. In the sentence with ID 1, it occurs 1 time in position 6. In sentence with ID 5, it occurs 2 times in position 87 and 96.
- <b>Dice_Matrix</b>: It retrieves the DICE matrix (in pandas format) between each term according to the n-contextual window distance defined. For instance, a DICE similarity of 1 between `prime` and `minister` means that, whenever each of these terms occur, they always occur together. If you want to know more about the role of DICE in our algorithm please refer to this [link](#Computing-Dice).

``` bash
Text, TextNormalized, Score, CandidateDates, NormalizedCandidateDates, RelevantKWs, IIndex, Dice_Matrix = Time_Matters_SingleDoc(text, debug_mode=True)
```
[[Table of Contents]](#Table-of-Contents)


#### SD Python CLI
##### Help
``` bash
$ Time_Matters_SingleDoc --help
```

##### Usage Examples
Usage_examples (make sure that the input parameters are within quotes):

Default Parameters:
This configuration assumes "py_heideltime" as default temporal tagger, "ByDoc" as the default score_type and the default parameters of time_matters.

``` bash
Time_Matters_SingleDoc -i "['text', 'August 31st']"
```

All the Parameters:
``` bash
All the Parameters: Time_Matters_SingleDoc -i "['text', '2019-12-31']" -tt "['py_heideltime','English', 'full', 'news', '2019-05-05']" -tm "[10,'full_sentence', 'max', 0.05]" -st ByDoc -dm False
```

##### Options
``` bash
  [required]: either specify a text or an input_file path.
  ----------------------------------------------------------------------------------------------------------------------------------
  -i, --input               A list that specifies the type of input: a text or a file path
                            Example:
                                    "['text', 'August 31st']"
                                    "['path', 'c:\text.txt']"

```

``` bash
 [not required]
 ----------------------------------------------------------------------------------------------------------------------------------
  -tt, --temporal_tagger   Specifies the temporal tagger and the corresponding parameters.
                           Default: "py_heideltime"
			   Options:
			   	    "py_heideltime"
				    "rule_based"
				 
			   py_heideltime (parameters):
			   ____________________________
			   - temporal_tagger_name
			     Options:
				     "py_heideltime"

			   - language
			     Default: "English"
			     Options:
			   	      "English";
				      "Portuguese";
				      "Spanish";
				      "Germany";
				      "Dutch";
				      "Italian";
				      "French".

		          - date_granularity
			    Default: "full"
			    Options:
			           "full": means that all types of granularity will be retrieved, from the coarsest to the 
					   finest-granularity.
			           "day": means that for the date YYYY-MM-DD-HH:MM:SS it will retrieve YYYY-MM-DD;
				   "month": means that for the date YYYY-MM-DD-HH:MM:SS only the YYYY-MM will be retrieved;
				   "year": means that for the date YYYY-MM-DD-HH:MM:SS only the YYYY will be retrieved;

			  - document_type
			    Default: "News"
			    Options:
			  	    "News": for news-style documents - default param;
				    "Narrative": for narrative-style documents (e.g., Wikipedia articles);
				    "Colloquial": for English colloquial (e.g., Tweets and SMS);
				    "Scientific": for scientific articles (e.g., clinical trails).

			  - document_creation_time
			    Document creation date in the format YYYY-MM-DD. Taken into account when "News" or "Colloquial" texts
		            are specified.
		            Example: "2019-05-30".

			  - Example: "['py_heideltime','English', 'full', 'news', '2019-05-05']"	 

		          
			  Rule_Based (parameters):
		          ____________________________
			  - temporal_tagger_name
			    Options:
			  	    "rule_based"

			  - date_granularity
			    Default: "full"
			    Options:
			           "full": means that all types of granularity will be retrieved, from the coarsest to the 
					   finest-granularity.
			           "day": means that for the date YYYY-MM-DD-HH:MM:SS it will retrieve YYYY-MM-DD;
				   "month": means that for the date YYYY-MM-DD-HH:MM:SS only the YYYY-MM will be retrieved;
				   "year": means that for the date YYYY-MM-DD-HH:MM:SS only the YYYY will be retrieved;

			  - Example: "['rule_based','full']"
```

``` bash
 [not required]
 ----------------------------------------------------------------------------------------------------------------------------------
  -tm, --time_matters     Specifies information about Time-Matters, namely:
			  - num_of_keywords: number of YAKE! keywords to extract from the text
			    Default: 10
			    Options:
				    any integer > 0

		          - n_contextual_window: defines the search space where co-occurrences between terms may be counted.
			    Default: "full_sentence"
			    Options:
                                    "full_sentence": the system will look for co-occurrences between terms that occur within the search 
				                    space of a sentence;
			            n: where n is any value > 0, that is, the system will look for co-occurrences between terms that 
				       occur within a window of n terms;
				       
		          - N: N-size context vector for InfoSimba vectors
			    Default: "max"
			    Options: 
			            "max": where "max" is given by the maximum number of terms eligible to be part of the vector
				    any integer > 0
				    
			  - TH: all the terms with a DICE similarity > TH threshold are eligible to the context vector of InfoSimba
			    Default: 0.05
			    Options: 
				    any integer > 0


			  - Example: "[10, 'full_sentence', 'max', 0.05]"
```

``` bash
 [not required]
 ----------------------------------------------------------------------------------------------------------------------------------
  -st, --score_type       Specifies the type of score for the temporal expression found in the text
  			  Default: "single"
                          Options:
                                  "single": returns a single score regardless the temporal expression occurs in different sentences;
                                  "multiple": returns multiple scores (one for each sentence where it occurs)
			  - Example: "[10, 'full_sentence', 'max', 0.05]"
```

``` bash
 [not required]
 ----------------------------------------------------------------------------------------------------------------------------------
  -dm, --debug_mode      Returns detailed information about the results
  	                 Default: False
			 Options:
			          False: when set to False debug mode is not activated
				  True: activates debug mode. In that case it returns 
                                        "Text";
					"NormalizedText"
					"Score"
					"CandidateDates"
					"NormalizedCandidateDates"
					"RelevantKWs"
					"InvertedIndex"
					"Dice_Matrix

  --help                 Show this message and exit.
```
[[Table of Contents]](#Table-of-Contents)

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
