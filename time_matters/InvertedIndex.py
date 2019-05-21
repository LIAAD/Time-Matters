from yake import KeywordExtractor as YakeKW
import string
import nltk
from py_heideltime import heideltime


# *****************************************************************
# words extraction using wake
def kw_ext(lang, text, max_keywords):
    sample = YakeKW(lan=lang, n=1, top=max_keywords)
    dates, new_text = candidate_years(text)
    keywords = sample.extract_keywords(new_text)
    relevant_words = []
    # insert only the relevant words to the array.
    for ki in range(len(keywords)):
        relevant_words.append(keywords[ki][0])
    print('Keywords =', relevant_words)
    main_dict = word_mapping(relevant_words, new_text, dates)
    return main_dict


# *********************************************************************
#  creation of inverted index.
def word_mapping(relevant_array, text, dates_array):
    print("====================== Inverted index ================")
    # Creation on arrays to set sentences and words tokenized.
    sentence_array = sentence_tokenizer(text)
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
def candidate_years(text):
    years = []
    list_dates = heideltime(text)
    new_text = text
    for ct in range(len(list_dates)):
        if list_dates[ct][0] not in years:
            years.append(list_dates[ct][0].lower())
        try:
            new_text = new_text.replace(list_dates[ct][1], list_dates[ct][0])
        except:
            pass
    print('Candidate_Dates = ', years)
    return years, new_text


def word_tokenizer(text):
    k = nltk.word_tokenize(text)
    # removed the punctuation in text
    tokens_filtered = [token.lower() for token in k if token not in string.punctuation]
    return tokens_filtered
