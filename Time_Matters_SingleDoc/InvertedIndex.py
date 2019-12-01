from yake import KeywordExtractor as YakeKW
import nltk
import time
import re


# *****************************************************************
# function that manage the workflow for creation of inverted_index
def main_inverted_index(yake_ln, lang, text, num_of_keywords, document_type, document_creation_time, date_granularity, date_extractor, n_gram, begin_date, end_date):

    if date_extractor == 'rule_based':
        # =============================== Date Extractor ===============================================
        candidate_dates_array, new_text, date_dictionary, TempExpressions, ExecTimeDictionary = rule_based(text, date_granularity, begin_date, end_date)

        # =============================== Keyword Extractor ===========================================================
        KeyWords_dictionary, relevant_words_array, kw_exec_time = kw_ext(yake_ln, new_text, num_of_keywords, n_gram)
    else:
        # =============================== Date Extractor ==============================================================
        candidate_dates_array, new_text, date_dictionary, TempExpressions, ExecTimeDictionary = py_heideltime(text, lang, document_type, document_creation_time, date_granularity)
        # =============================== Keyword Extractor ==========================================================
        KeyWords_dictionary, relevant_words_array, kw_exec_time = kw_ext(yake_ln, new_text, num_of_keywords, n_gram)

    from yake.highlight import TextHighlighter
    th = TextHighlighter(max_ngram_size=n_gram)
    textNormalized = th.highlight(new_text, relevant_words_array)

    # =====================================================================================================
    # =============================== Inverted Index ===============================================
    ii_start_time = time.time()
    inverted_index, words_array, dates_array, sentence_array, sentence_tokens = create_inverted_index(relevant_words_array, candidate_dates_array, textNormalized)
    ii_exec_time = (time.time() - ii_start_time)
    # ===========================================================================================================

    words_array, KeyWords_dictionary = verify_keywords(inverted_index, relevant_words_array, KeyWords_dictionary, candidate_dates_array)
    text_tokens = tokenizer(textNormalized)

    return inverted_index, KeyWords_dictionary, words_array, dates_array, sentence_array, date_dictionary, TempExpressions, textNormalized, kw_exec_time, sentence_tokens, text_tokens, ii_exec_time, ExecTimeDictionary


def verify_keywords(inverted_index, words_array, KeyWords_dictionary, candidate_dates_array):
    KeyWords_dictionary = {w: KeyWords_dictionary[w] for w in words_array if w in inverted_index and w not in candidate_dates_array}
    words_array = [kw for kw in words_array if kw in inverted_index and kw not in candidate_dates_array]
    return words_array, KeyWords_dictionary


def test_trans(text):
    return text.translate(str.maketrans('', '', '!,:.;?()"\n'))


# *****************************************************************
# keywords extraction using yake
def kw_ext(yake_ln, text, num_of_keywords, n_gram):
    kw_start_time = time.time()
    sample = YakeKW(lan=yake_ln, n=n_gram, top=num_of_keywords)
    keywords = sample.extract_keywords(text)
    KeyWords_dictionary = {}

    for ki in range(len(keywords)):
        KeyWords_dictionary[keywords[ki][0]] = keywords[ki][1]


    relevant_words_array = list(KeyWords_dictionary.keys())

    kw_exec_time = (time.time() - kw_start_time)

    return KeyWords_dictionary, relevant_words_array, kw_exec_time


# ***********************************************************************************
# Create inverted Index
def create_inverted_index(relevant_words_list, candidate_dates_list, text):
    sentence_array = sentence_tokenizer(text)
    inverted_index = {}
    last_pos = 0
    sf = 0
    sentence_tokens_list = []

    for sentence_id in range(len(sentence_array)):

        tokenize_sentence = tokenizer(sentence_array[sentence_id])

        sentence_tokens_list.append(tokenize_sentence)
        sf += 1
        inverted_index = get_occurrence(tokenize_sentence, inverted_index, sentence_id, last_pos)
        last_pos += len(tokenize_sentence)

    return inverted_index, relevant_words_list, list(candidate_dates_list), sentence_array, sentence_tokens_list


def tokenizer(text):
    tokens_list = re.findall('(<d>.*?</d>|<kw>.*?</kw>|\w+)', text)
    return tokens_list


def get_occurrence(tokenize_sentence, inverted_index, sentence_id, last_pos):

    for i, w in enumerate(tokenize_sentence):
        term = w.lower().replace('<d>', '').replace('</d>', '').replace('<kw>', '').replace('</kw>', '')

        if re.match('^<kw>', w.lower()) or re.match('^<d>', w.lower()):
            if term not in inverted_index:
                inverted_index[term] = [0, 1, {}]
            if sentence_id not in inverted_index[term][2]:
                pos = i + last_pos
                inverted_index[term][2][sentence_id] = [0, [pos]]
            else:
                pos = i + last_pos
                inverted_index[term][2][sentence_id][1].append(pos)

            # increment Sentence frenquency
            inverted_index[term][0] = len(inverted_index[term][2])

            # increment total frequency
            x = inverted_index[term][2].values()
            totalfreq = 0
            for i in list(x):
                totalfreq += len(i[1])
            inverted_index[term][1] = totalfreq

        try:
            ct = len(inverted_index[term][2][sentence_id][1])
            inverted_index[term][2][sentence_id][0] = ct

        except:
            pass
    return inverted_index


# ************************************************************
# **************** text tokenizer by sentence **************
def sentence_tokenizer(text):
    # usage of nltk to tokenize the text by sentences
    sentences = nltk.sent_tokenize(text)
    return sentences


# *************************************************************************************
# **************************** Date extraction from text ******************************
# *************************************************************************************
def py_heideltime(text, language, heideltime_document_type, heideltime_document_creation_time, heideltime_date_granularity):
    from py_heideltime import py_heideltime

    result = py_heideltime(text, language, heideltime_date_granularity, heideltime_document_type, heideltime_document_creation_time)
    date_dictionary = {}
    dates = []
    for ct in range(len(result[0])):

        if result[0][ct][0].lower() not in date_dictionary:
            date_dictionary[result[0][ct][0].lower()] = [result[0][ct][1]]
            dates.append(result[0][ct][0].lower())

        elif result[0][ct][0].lower() in date_dictionary:
            date_dictionary[result[0][ct][0].lower()].append(result[0][ct][1])
            dates.append(result[0][ct][0].lower())

    return dates, result[1], date_dictionary, result[0], result[3]


def rule_based(text, date_granularity, begin_date, end_date):
    from py_rule_based import py_rule_based
    result = py_rule_based(text, date_granularity, begin_date, end_date)
    date_dictionary = {}
    dates = []
    for ct in range(len(result[0])):

        if result[0][ct][0].lower() not in date_dictionary:
            date_dictionary[result[0][ct][0].lower()] = [result[0][ct][1]]
            dates.append(result[0][ct][0].lower())

        elif result[0][ct][0].lower() in date_dictionary:
            date_dictionary[result[0][ct][0].lower()].append(result[0][ct][1])
            dates.append(result[0][ct][0].lower())
    return dates, result[1], date_dictionary, result[0], result[2]