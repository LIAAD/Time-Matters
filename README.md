
# Time_Matters


This project consists on a extractor of relevants dates from texts.

the module are composed by:
    
    - Date extraction with Heideltime and replace in text the date expression for date format (yyyy-mm--dd).
    
    - Keyword extraction with YAKE.
    
    - Creation of a inverted indext to organize the following data:
        - Frequency the keyword or date that occour on text.,
        - how many sentences that keyword or date appears.
        - Exact position on sentence that the keyword or date appears.

    - Calculate the similarity of the relevant words with the canditate to relevant date.



### Install Time_Matters
``` bash
Git clone https://github.com/JMendes1995/Time_Matters.git
cd Time_Matters
python setup.py install
pip install -r requirements.txt
```
##### Recomendations
    In order to use time_matters you must have installed java jdk and perl in your machine for heideltime dependencies. 
    
    (Linux) if your user had not root permitions on python lib folder, you should execute the following command:
    sudo chmod +x /usr/local/lib/<YOUR PYTHON VERSION>/dist-packages/py_heideltime/HeidelTime/TreeTaggerLinux/bin/*
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
output = timeMatters(txt, contextual_window_distance=10, threshold=0.05, max_array_len=0, max_keywords=10, analisys_sentence=True)

print(output)
#output
[{'Date': '1905', 'Score': 0.9980984799637649}, {'Date': '1907', 'Score': 0.9885848306283148}, {'Date': '1915', 'Score': 0.9467018487599099}, {'Date': '1916', 'Score': 0.8163265306122448}]
```

##### Analyze dates per text sentence
``` bash
# assuming default parameters
timeMattersPerSentence(text)

# with all paramiters
output = timeMattersPerSentence(txt, contextual_window_distance=10, threshold=0.05, max_array_len=0, max_keywords=10)

print(output)
#output
[{'Sentence 1': {'Date': '1905', 'Score': 1.0}}, {'Sentence 3': {'Date': '1907', 'Score': 1.0}}, {'Sentence 3': {'Date': '1915', 'Score': 0.8908296943231436}}, {'Sentence 4': {'Date': '1916', 'Score': 1.0}}]
```
### API
https://time-matters-api.herokuapp.com/

### Python CLI -  Command Line Interface
``` bash
python cli.py --help

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
 1. Campos, R., Dias, G., Jorge, A. and Nunes, C. (2017). Identifying Top Relevant Dates for Implicit Time Sensitive Queries. In Information Retrieval Journal. Springer, Vol 20(4), pp 363-398
 2. Strötgen, Gertz: Multilingual and Cross-domain Temporal Tagging. Language Resources and Evaluation, 2013
 3. Strötgen, Gertz: A Baseline Temporal Tagger for All Languages. EMNLP'15. pdf bibtex
 4. Kuzey, Strötgen, Setty, Weikum: Temponym Tagging: Temporal Scopes for Textual Phrases. TempWeb'16. 

