from yake import KeywordExtractor as YakeKW
import string
import nltk

# *****************************************************************
# words extraction using wake
def kw_ext(yake_ln, lang, text,num_of_keywords,  document_type, document_creation_time, date_granularity, date_extractor):
    sample = YakeKW(lan=yake_ln, n=1, top=num_of_keywords)
    dates, new_text = candidate_years(text, lang, document_type, document_creation_time, date_granularity, date_extractor)
    keywords = sample.extract_keywords(new_text)
    relevant_words = []
    # insert only the relevant words to the array.
    for ki in range(len(keywords)):
        relevant_words.append(keywords[ki][0])
    inverted_index, words_array, dates_array, sentence_array = word_mapping(relevant_words, new_text, dates)
    return inverted_index, words_array, dates_array, sentence_array


# *********************************************************************
#  creation of inverted index.
def word_mapping(relevant_array, text, dates_array):
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
    return myDictObj, relevant_array, dates_array, sentence_array


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
        positionalList, last_value = text_info(sentence_index+1, word, tokens_filtered, last_value, myDictObj,  positionalList)


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
def candidate_years(text, language, document_type, document_creation_time, date_granularity, date_extractor):
    if date_extractor == 'py_heideltime':
        candidate_dates_array, new_text = py_heideltime(text, language, document_type, document_creation_time,
                      date_granularity)
        return candidate_dates_array, new_text
    else:
        candidate_dates_array, new_text = rule_based(text, date_granularity)
        return candidate_dates_array, new_text


def py_heideltime(text, language, heideltime_document_type, heideltime_document_creation_time, heideltime_date_granularity):
    from py_heideltime import py_heideltime
    years = []
    list_dates = py_heideltime(text, language, heideltime_date_granularity, heideltime_document_type, heideltime_document_creation_time)

    new_text = text
    for ct in range(len(list_dates)):
        if list_dates[ct][0] not in years:
            years.append(list_dates[ct][0].lower())
        try:
            new_text = new_text.replace(list_dates[ct][1], list_dates[ct][0])
        except:
            pass
    return years, new_text


def rule_based(text, date_granularity):
    dates_list = []
    import re
    striped_text = text.replace('(', '').replace(')', '').replace('–', '-')
    match = re.findall('\d{2,4}[-/.]\d{2}[-/.]\d{2,4}|\d{2,4}[-/.]\d{2,4}|\d{4}', striped_text, re.MULTILINE)
    try:
        for dt in match:
            provisional_list = []
            if dt not in dates_list and date_granularity == '':
                dates_list.append(dt)
            elif dt not in dates_list and date_granularity != '':
                if re.match('\w{2,4}[-/.]\w{2}[-/.]\w{2,4}', str(dt)):
                    if date_granularity.lower() == 'year':
                        years = re.findall('\w{4}', str(dt))
                        dates_list.append((years[0]))
                        provisional_list.append((dt, years[0]))
                    elif date_granularity.lower() == 'month':
                        months = re.findall('\w{2}[-/.]\w{4}|\w{4}[-/.]\w{2}', str(dt))
                        dates_list.append((months[0]))
                        provisional_list.append((dt, months[0]))
                        print(provisional_list)
                    elif date_granularity.lower() == 'day':
                        days = re.findall('\w{2,4}[-/.]\w{2}[-/.]\w{2,4}', str(dt))
                        dates_list.append((days[0]))
                        provisional_list.append((dt, days[0]))
                    striped_text = striped_text.replace(provisional_list[0][0], provisional_list[0][1])
            else:
                pass
    except ValueError:
        pass
    #striped_text = striped_text.replace(list_dates[ct][1], list_dates[ct][0])
    #print('date_list = ' +str(dates_list))
    return dates_list, striped_text


def word_tokenizer(text):
    k = nltk.word_tokenize(text)
    # removed the punctuation in text
    tokens_filtered = [token.lower() for token in k if token not in string.punctuation]
    return tokens_filtered
