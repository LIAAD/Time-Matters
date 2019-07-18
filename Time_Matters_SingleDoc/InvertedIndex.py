from yake import KeywordExtractor as YakeKW
import nltk
import time
import re


# *****************************************************************
# function that manage the workflow for creation of inverted_index
def main_inverted_index(yake_ln, lang, text, num_of_keywords, document_type, document_creation_time, date_granularity, date_extractor):
    KeyWords_dictionary, relevant_words_array, candidate_dates_array, new_text, \
    date_dictionary, time_tagger_start_time, kw_exec_time = kw_ext(yake_ln, lang, text, num_of_keywords, document_type, document_creation_time, date_granularity, date_extractor)

    ii_start_time = time.time()
    inverted_index, words_array, dates_array, sentence_array, sentence_tokens = create_inverted_index(relevant_words_array, candidate_dates_array, new_text, date_extractor)

    words_array, KeyWords_dictionary = verify_keywords(inverted_index, words_array, KeyWords_dictionary)
    text_tokens = tokenizer(new_text)

    ii_exec_time = (time.time() - ii_start_time)
    return inverted_index, KeyWords_dictionary, words_array, dates_array, sentence_array, date_dictionary, new_text, time_tagger_start_time, kw_exec_time, sentence_tokens, text_tokens, ii_exec_time


def verify_keywords(inverted_index, words_array, KeyWords_dictionary):
    KeyWords_dictionary = {w: KeyWords_dictionary[w] for w in words_array if w in inverted_index}
    words_array = [kw for kw in words_array if kw in inverted_index]
    return words_array, KeyWords_dictionary

# *****************************************************************
# keywords extraction using wake
def kw_ext(yake_ln, lang, text, num_of_keywords, document_type, document_creation_time, date_granularity, date_extractor):
    time_tagger_start_time = time.time()
    candidate_dates_array, new_text, date_dictionary = candidate_years_selection(text, lang, document_type,
                                                                       document_creation_time, date_granularity,
                                                                       date_extractor)
    time_tagger_exec_time = (time.time() - time_tagger_start_time)

    kw_start_time = time.time()
    sample = YakeKW(lan=yake_ln, n=1, top=num_of_keywords)
    keywords = sample.extract_keywords(new_text)
    KeyWords_dictionary = {}

    for ki in range(len(keywords)):
        KeyWords_dictionary[keywords[ki][0]]= keywords[ki][1]

    kw_exec_time = (time.time() - kw_start_time)

    relevant_words_array = list(KeyWords_dictionary.keys())
    return KeyWords_dictionary, relevant_words_array, candidate_dates_array, new_text, date_dictionary, time_tagger_exec_time, kw_exec_time


# ***********************************************************************************
# Create inverted Index
def create_inverted_index(relevant_words_list, candidate_dates_list, text, date_extractor):
    sentence_array = sentence_tokenizer(text)
    words_dates_list = relevant_words_list + candidate_dates_list
    inverted_index = {}

    last_pos = 0
    sf = 0
    sentence_tokens_list = []
    import re
    for sentence_id in range(len(sentence_array)):

        tokenize_sentence = tokenizer(sentence_array[sentence_id])

        sentence_tokens_list.append(tokenize_sentence)
        sf += 1
        inverted_index = get_occurrence(tokenize_sentence, relevant_words_list, words_dates_list, inverted_index, sentence_id, last_pos)
        last_pos += len(tokenize_sentence)

    return inverted_index, relevant_words_list, list(candidate_dates_list), sentence_array, sentence_tokens_list


def tokenizer(text):
    tokens_list = re.findall('(<d>.*?</d>|\w+)', text)
    return tokens_list

def get_occurrence(tokenize_sentence, words_list, words_dates_list, inverted_index, sentence_id, last_pos):

    for i, w in enumerate(tokenize_sentence):
        term = w.lower().replace('<d>', '').replace('</d>', '')

        if term in words_list or re.match('^<d>', w.lower()):
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
def candidate_years_selection(text, language, document_type, document_creation_time, date_granularity, date_extractor):
    if date_extractor == 'py_heideltime':
        candidate_dates_array, new_text, date_dictionary = py_heideltime(text, language, document_type,
                                                                         document_creation_time,
                                                                         date_granularity)
        return candidate_dates_array, new_text, date_dictionary
    elif date_extractor == 'rule_based':
        candidate_dates_array, new_text, date_dictionary = rule_based(text, date_granularity)
        return candidate_dates_array, new_text, date_dictionary


def py_heideltime(text, language, heideltime_document_type, heideltime_document_creation_time, heideltime_date_granularity):
    from py_heideltime import py_heideltime

    list_dates, normalized_text, tagged_text = py_heideltime(text, language, heideltime_date_granularity, heideltime_document_type,
                               heideltime_document_creation_time)
    date_dictionary = {}
    dates = []
    for ct in range(len(list_dates)):

        if list_dates[ct][0].lower() not in date_dictionary:
            date_dictionary[list_dates[ct][0].lower()] = [list_dates[ct][1]]
            dates.append(list_dates[ct][0].lower())

        elif list_dates[ct][0].lower() in date_dictionary:
            date_dictionary[list_dates[ct][0].lower()].append(list_dates[ct][1])
            dates.append(list_dates[ct][0].lower())

    return dates, normalized_text, date_dictionary


def rule_based(text, date_granularity):
    dates_list = []
    date_dictionary = {}
    import re

    try:
        striped_text = text.replace('(', '').replace(')', '').replace('–', '-')
    except:
        striped_text = text
    match = re.findall('\d{2,4}[-/.]\d{2}[-/.]\d{2,4}|\d{4}[-/.]\d{2}[-/.]\d{2}|\d{4}[-/.]\d{4}|\d{4}[-/.]\d{2}|\d{2}[-/.]\d{4} |\d{4}s|\d{4}', striped_text, re.MULTILINE)
    try:
        for dt in match:
            provisional_list = []

            if dt not in dates_list and date_granularity == 'full':
                dates_list.append(dt)
                date_dictionary[dt] = dt
                striped_text = striped_text.replace(dt, '<d>'+dt+'</d>')

            elif dt not in dates_list and date_granularity != 'full':

                try:
                    if date_granularity.lower() == 'year':

                        dt, dates_list, provisional_list, \
                        date_dictionary,striped_text  = date_granularity_format(dt, dates_list, provisional_list, date_dictionary, '\d{4}', striped_text)

                    elif date_granularity.lower() == 'month':

                        dt, dates_list, provisional_list, \
                        date_dictionary, striped_text = date_granularity_format(dt, dates_list, provisional_list, date_dictionary,'\d{2}[-/.]\d{4}|\d{4}[-/.]\d{2}', striped_text)

                    elif date_granularity.lower() == 'day':

                        dt, dates_list, provisional_list, \
                        date_dictionary, striped_text = date_granularity_format(dt, dates_list, provisional_list, date_dictionary,'\d{2,4}[-/.]\d{2}[-/.]\d{2,4}', striped_text)


                    striped_text = striped_text.replace(provisional_list[0][0], '<d>'+provisional_list[0][1]+'</d>')

                except:
                    pass
            else:
                pass
    except ValueError:
        pass

    return dates_list, striped_text, date_dictionary


def date_granularity_format(dt, dates_list, provisional_list, date_dictionary, granularity_rule, text):

    years = re.findall(granularity_rule, str(dt))
    dates_list.append((years[0]))
    provisional_list.append((dt, years[0]))

    if years[0] not in date_dictionary:
        date_dictionary[years[0]] = [dt]
    else:
        date_dictionary[years[0]].append(dt)


    return dt, dates_list, provisional_list, date_dictionary, text