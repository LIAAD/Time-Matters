from yake import KeywordExtractor as YakeKW
import nltk
import time


# *****************************************************************
# function that manage the workflow for creation of inverted_index
def main_inverted_index(yake_ln, lang, text, num_of_keywords, document_type, document_creation_time, date_granularity,
                        date_extractor):
    relevant_words_array, candidate_dates_array, new_text, date_dictionary, time_tagger_start_time, kw_exec_time = kw_ext(
        yake_ln, lang, text,
        num_of_keywords, document_type,
        document_creation_time, date_granularity, date_extractor)
    ii_start_time = time.time()
    inverted_index, words_array, dates_array, sentence_array = create_inverted_index(relevant_words_array,
                                                                                     candidate_dates_array, new_text)
    ii_exec_time = (time.time() - ii_start_time)
    return inverted_index, words_array, dates_array, sentence_array, date_dictionary, new_text, time_tagger_start_time, kw_exec_time, ii_exec_time


# *****************************************************************
# keywords extraction using wake
def kw_ext(yake_ln, lang, text, num_of_keywords, document_type, document_creation_time, date_granularity,
           date_extractor):
    time_tagger_start_time = time.time()
    candidate_dates_array, new_text, date_dictionary = candidate_years_selection(text, lang, document_type,
                                                                       document_creation_time, date_granularity,
                                                                       date_extractor)
    time_tagger_exec_time = (time.time() - time_tagger_start_time)

    kw_start_time = time.time()
    sample = YakeKW(lan=yake_ln, n=1, top=num_of_keywords)
    keywords = sample.extract_keywords(new_text)
    relevant_words_array = []

    for ki in range(len(keywords)):
        relevant_words_array.append(keywords[ki][0])

    kw_exec_time = (time.time() - kw_start_time)
    return relevant_words_array, candidate_dates_array, new_text, date_dictionary, time_tagger_exec_time, kw_exec_time


def test_trans(text):
    return text.translate(str.maketrans('', '', '!"#$%&\'()*+,:.;<=>?@[\\]^`{|}~'))


# ***********************************************************************************
# Create inverted Index
def create_inverted_index(relevant_words_list, candidate_dates_list, text):
    sentence_array = sentence_tokenizer(text)
    words_dates_list = relevant_words_list + candidate_dates_list
    dictionary = {}

    for dt in words_dates_list:
        last_pos = 0
        totalfreq = 0
        search_str = dt
        dictionary[dt] = [0, 0, {}]

        for n in range(len(sentence_array)):
            strip_text = test_trans(sentence_array[n]).split()
            for i, w in enumerate(strip_text):
                if w.lower() == search_str:
                    if n not in dictionary[dt][2]:
                        pos = i + last_pos
                        dictionary[dt][2][n] = [0, [pos]]

                    else:
                        pos = i + last_pos

                        dictionary[dt][2][n][1].append(pos)
            try:
                ct = len(dictionary[dt][2][n][1])
                totalfreq += ct
                dictionary[dt][2][n][0] = ct
            except:
                pass
            last_pos += len(strip_text)
        dictionary[dt][0] = len(dictionary[dt][2])
        dictionary[dt][1] = totalfreq
    return dictionary, relevant_words_list, candidate_dates_list, sentence_array


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
        date_dictionary = {}
        candidate_dates_array, new_text = rule_based(text, date_granularity)
        return candidate_dates_array, new_text, date_dictionary


def py_heideltime(text, language, heideltime_document_type, heideltime_document_creation_time,
                  heideltime_date_granularity):
    from py_heideltime import py_heideltime

    list_dates = py_heideltime(text, language, heideltime_date_granularity, heideltime_document_type,
                               heideltime_document_creation_time)
    date_dictionary = {}
    dates = []
    new_text = text
    for ct in range(len(list_dates)):
        if list_dates[ct][0].lower() not in date_dictionary:
            date_dictionary[list_dates[ct][0].lower()] = [list_dates[ct][1]]
            dates.append(list_dates[ct][0].lower())
        elif list_dates[ct][0].lower() in date_dictionary:
            date_dictionary[list_dates[ct][0].lower()].append(list_dates[ct][1])
        try:
            import re

            new_text = new_text.replace(list_dates[ct][1], list_dates[ct][0])

        except:
            pass
        #print(new_text)
    return dates, new_text, date_dictionary


def rule_based(text, date_granularity):
    dates_list = []
    import re

    try:
        striped_text = text.replace('(', '').replace(')', '').replace('–', '-')
    except:
        striped_text = text
    match = re.findall('\d{2,4}[-/.]\d{2}[-/.]\d{2,4}|\d{4}[-/.]\d{2}[-/.]\d{2}|\d{4}[-/.]\d{4}|\d{4}[-/.]\d{2}|\d{2}[-/.]\d{4} |\d{4}s|\d{4}',
                       striped_text, re.MULTILINE)
    print(match)
    try:
        for dt in match:
            provisional_list = []
            if dt not in dates_list and date_granularity == 'full':
                dates_list.append(dt)
            elif dt not in dates_list and date_granularity != 'full':
                try:
                    if date_granularity.lower() == 'year':
                        years = re.findall('\w{4}', str(dt))
                        dates_list.append((years[0]))
                        provisional_list.append((dt, years[0]))
                    elif date_granularity.lower() == 'month':
                        months = re.findall('\w{2}[-/.]\w{4}|\w{4}[-/.]\w{2}', str(dt))
                        dates_list.append((months[0]))
                        provisional_list.append((dt, months[0]))
                    elif date_granularity.lower() == 'day':
                        days = re.findall('\w{2,4}[-/.]\w{2}[-/.]\w{2,4}', str(dt))
                        dates_list.append((days[0]))
                        provisional_list.append((dt, days[0]))

                    striped_text = striped_text.replace(provisional_list[0][0], provisional_list[0][1])
                except:
                    pass
            else:
                pass
    except ValueError:
        pass
    # print('date_list = ' +str(dates_list))
    return dates_list, striped_text
