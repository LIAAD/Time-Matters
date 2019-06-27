from yake import KeywordExtractor as YakeKW
from Time_Matters_SingleDoc import *
import nltk
from langdetect import detect


def main_inverted_index_md(lang, list_of_docs, num_of_keywords,  document_type, document_creation_time, date_granularity, date_extractor):
    list_of_striped_docs = []
    initial_inverted_index = {}

    all_docs_candidate_date = []
    all_docs_relevant_words = []
    for id_doc in range(len(list_of_docs)):
        try:
            yake_lang = detect(list_of_docs[id_doc])
        except:
            yake_lang = 'en'
        relevant_words_array, candidate_dates_array, new_text, date_dictionary = kw_ext(yake_lang, lang, list_of_docs[id_doc],
                                                                             num_of_keywords, document_type,
                                                                             document_creation_time, date_granularity,date_extractor)

        initial_inverted_index = create_inverted_index_md(new_text, relevant_words_array, candidate_dates_array, initial_inverted_index, id_doc)
        list_of_striped_docs.append(new_text)

        all_docs_candidate_date += candidate_dates_array
        all_docs_relevant_words += relevant_words_array

    inverted_index = set_document_frequency(initial_inverted_index, all_docs_candidate_date, all_docs_relevant_words)
    join_docs = ' '.join(list_of_striped_docs)
    return inverted_index, all_docs_relevant_words, all_docs_candidate_date, list_of_striped_docs, join_docs

def create_inverted_index_md(doc, relevant_words_array, candidate_dates_array, inverted_index_dictionary, id_doc):
    total_array = relevant_words_array + candidate_dates_array
    striped_doc = test_trans(doc).split()

    for dt in total_array:
        last_pos = 0
        totalfreq = 0
        search_str = dt
        if dt not in inverted_index_dictionary:
            inverted_index_dictionary[dt] = [0,0,{}]

        for i, w in enumerate(striped_doc):
            if w.lower() == search_str:
                if id_doc not in inverted_index_dictionary[dt][2]:
                    pos = i + last_pos
                    inverted_index_dictionary[dt][2][id_doc] = [0, [pos]]

                else:
                    pos = i + last_pos

                    inverted_index_dictionary[dt][2][id_doc][1].append(pos)
        try:
            ct = len(inverted_index_dictionary[dt][2][id_doc][1])
            totalfreq += ct
            inverted_index_dictionary[dt][2][id_doc][0] = ct

        except:
            pass
        last_pos += len(striped_doc)
        inverted_index_dictionary[dt][0] = len(inverted_index_dictionary[dt][2])

    return inverted_index_dictionary


def set_document_frequency(initial_inverted_index, all_docs_candidate_date, all_docs_relevant_words):
    total_array = all_docs_candidate_date + all_docs_relevant_words
    for w in total_array:
        total_freq = 0
        for x in initial_inverted_index[w][2]:
            total_freq += len(initial_inverted_index[w][2][x][1])
        initial_inverted_index[w][1] = total_freq
    return initial_inverted_index