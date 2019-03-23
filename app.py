from yake import KeywordExtractor as YakeKW
import numpy as np
import datefinder
from nltk.tokenize import sent_tokenize, TweetTokenizer
import string


def kw_ext(text):
    sample = YakeKW(n=1, top=3)
    keywords = sample.extract_keywords(text)
    np_kw = np.array(keywords)
    relevant_words = []
    for w in np_kw[:, :1]:
        relevant_words.append(w[0])
    word_mapping(relevant_words, text)


def word_mapping(relevant_array, text):
    print("======================== Relevant words =========================")
    print("\n")
    print("====================== Relevant words map in text ================")

    # Creation on arrays to set sentences and words tokenized.
    sentence_array = sentence_tokenizer(text)
    dates_array = candidate_years(text)
    myDictObj = {'RelevantWords': [], 'candidate_dates': []}
    for i in range(len(relevant_array)):
        # sentence_word_info(relevant_array[i], sentence_array)
        # ***************************************************************************************
        # insert on list my dict list values to put json form
        myDictObj['RelevantWords'].append({'word': [{'index': i, 'name': relevant_array[i]}]})
        my_dict = myDictObj['RelevantWords'][i]['word']
        word_info(relevant_array[i], sentence_array, my_dict)
    for dt_i in range(len(dates_array)):
        myDictObj['candidate_dates'].append({'years': [{'index': dt_i, 'value': dates_array[dt_i]}]})
        my_dictt = myDictObj['candidate_dates'][dt_i]['years']
        word_info(dates_array[dt_i], sentence_array, my_dictt)
    print(myDictObj)


def word_info(word, sentence_array, my_dict):
    # ******************************************
    # number of sentences that the word appears.
    word_count_freq = 0
    word_sentence_freq = 0
    last_value= 0
    normalizer_words_array = []
    for sentence_index in range(len(sentence_array)):
        words = TweetTokenizer()
        tokens = words.tokenize(sentence_array[sentence_index].lower())
        tokens_filtered = [token for token in tokens if token not in string.punctuation]
        words_sentence_array = []

        # *******************************************
        # Count number of times that the word appears
        for words in tokens_filtered:
            if words == word:
                word_count_freq += 1
                words_sentence_array.append(words.lower())
            normalizer_words_array.append(words.lower)
        # ***************************************************
        # Count how many sentences the word appears.
        if word in words_sentence_array:
            word_sentence_freq += 1
    # ***********************************************************
    # returnable information about relevant words in text
        insert_into_dict(word_sentence_freq, word_count_freq, my_dict)
        last_value = text_info(sentence_index, word, tokens_filtered, last_value, my_dict)


def insert_into_dict(word_sentence_freq, word_count_freq, my_dict):
    my_dict[0]['new_val'] = [{'words_sentence_frequency': word_sentence_freq, 'total_word_frequency': word_count_freq}]
    print(my_dict)


def text_info(sentence_index, word, tokens_filtered, lastvalue, my_dict):
    for count, ele in enumerate(tokens_filtered, 1):
        if ele == word:
            if 'sentence_'+str(sentence_index) in my_dict[0].keys():
                my_dict[0]['sentence_' + str(sentence_index)][0]['Offset'].append(count+lastvalue)
            else:
                my_dict[0]['sentence_' + str(sentence_index)] = [{'Offset': []}]
                my_dict[0]['sentence_' + str(sentence_index)][0]['Offset'].append(count+lastvalue)
    return count+lastvalue


def sentence_tokenizer(text):
    sent_token = sent_tokenize(text)
    return sent_token

# *************************************************************************************
# ********************data referent to data extracted in text**************************


def candidate_years(text):
    dates = list(datefinder.find_dates(text))
    years = []
    for d in dates:
        years.append(str(d.year))
    return years


if __name__ == '__main__':
    f = open('text.txt', 'r')
    message = f.read()
    print(message)
    print('===========================================================================')
    kw_ext(message)
