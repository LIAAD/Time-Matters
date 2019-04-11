from yake import KeywordExtractor as YakeKW
import numpy as np
import string
import nltk
import re
# *****************************************************************
# words extraction using wake
def kw_ext(text):
    sample = YakeKW(n=1, top=10)
    keywords = sample.extract_keywords(text)
    np_kw = np.array(keywords)
    relevant_words = []
    for w in np_kw[:, :1]:
        relevant_words.append(w[0])
    main_dict = word_mapping(relevant_words, text)
    return main_dict


# *********************************************************************
#  creation of inverted index.
def word_mapping(relevant_array, text):
    print("======================== Relevant words =========================")
    print("\n")
    print("====================== Relevant words map in text ================")
    # Creation on arrays to set sentences and words tokenized.
    sentence_array = sentence_tokenizer(text)
    tokens_filtered = word_tokenizer(text)
    dates_array = candidate_years(text, tokens_filtered)
    myDictObj = {}
    for i in range(len(relevant_array)):
        # ***************************************************************************************
        # insert on list my dict list values to put json form
        myDictObj[relevant_array[i]] = []
        word_info(relevant_array[i], sentence_array, myDictObj)
    for dt_i in range(len(dates_array)):
        myDictObj[dates_array[dt_i]] = []
        word_info(dates_array[dt_i], sentence_array, myDictObj)
    print(myDictObj)
    return myDictObj, relevant_array, dates_array


# ***********************************************************************************************
# text pre-processing
def word_info(word, sentence_array, myDictObj):
    # ******************************************
    # number of sentences that the word appears.
    word_count_freq = 0
    word_sentence_freq = 0
    last_value = 0
    normalizer_words_array = []
    positionalList = {}
    for sentence_index in range(len(sentence_array)):
        tokens_filtered = word_tokenizer(sentence_array[sentence_index])
        words_sentence_array = []

        # *******************************************
        # Count number of times that the word appears
        for words in tokens_filtered:
            if words == word:
                word_count_freq += 1
                words_sentence_array.append(words)
            normalizer_words_array.append(words)
        # ***************************************************
        # Count how many sentences the word appears.
        if word in words_sentence_array:
            word_sentence_freq += 1
    # ***********************************************************
    # returnable information about relevant words in text

        insert_into_dict(word, word_sentence_freq, word_count_freq, myDictObj,  positionalList)
        positionalList, last_value = text_info(sentence_index, word, tokens_filtered, last_value, myDictObj,  positionalList)


def insert_into_dict(word, word_sentence_freq, word_count_freq, myDictObj,  positionalList):
    myDictObj[word] = [word_sentence_freq, word_count_freq,  positionalList]


def text_info(sentence_index, word, tokens_filtered, lastvalue, myDictObj,  positionalList):
    count = 0
    for count, ele in enumerate(tokens_filtered, 1):
        if ele == word:
            if sentence_index in myDictObj[word][2]:
                myDictObj[word][2][sentence_index][0] += 1
                myDictObj[word][2][sentence_index][1].append(count + lastvalue)
            else:
                myDictObj[word][2][sentence_index] = [0, []]
                myDictObj[word][2][sentence_index][0] += 1
                myDictObj[word][2][sentence_index][1].append(count + lastvalue)
    return positionalList, count+lastvalue


# ************************************************************
# **************** text tokenizer by sentence **************
def sentence_tokenizer(text):
    # usage of nltk to tokenize the text by sentences
    sentences = nltk.sent_tokenize(text)
    return sentences


# *************************************************************************************
# ********************data referent to data extracted in text**************************
def candidate_years(text, tokens_filtered):
    years = []
    match = re.findall('\d{2,4}[-/.]\d{2}[-/.]\d{2,4}|\d{4}[-/]\d{4}|\d{4}', text, re.MULTILINE)
    try:
        for dt in match:
            if dt in tokens_filtered:
                years.append(dt)
    except ValueError:
        pass
    return years


def word_tokenizer(text):
    k = nltk.word_tokenize(text)
    tokens_filtered = [token.lower() for token in k if token not in string.punctuation]
    return tokens_filtered
