from Time_Matters_SingleDoc import *
from langdetect import detect
from Time_Matters_SingleDoc.InvertedIndex import kw_ext, get_occurrence, tokenizer, verify_keywords

def main_inverted_index_md(lang, list_of_docs, num_of_keywords,  document_type, document_creation_time, date_granularity, date_extractor):
    list_of_striped_docs = []
    initial_inverted_index = {}

    all_docs_candidate_date = []
    all_docs_relevant_words = []
    current_offset = 0

    for id_doc in range(len(list_of_docs)):
        try:
            yake_lang = detect(list_of_docs[id_doc])
        except:
            yake_lang = 'en'

        KeyWords_dictionary, relevant_words_array, candidate_dates_array, new_text, \
        date_dictionary, time_tagger_start_time,\
        kw_exec_time = kw_ext(yake_lang, lang, list_of_docs[id_doc], num_of_keywords, document_type, document_creation_time, date_granularity, date_extractor)

        # Create II per sentence
        sentence_II = BySentence_Inverted_index(relevant_words_array, candidate_dates_array, new_text)

        # Create II per Doc
        initial_inverted_index = ByDoc_inverted_index(new_text, relevant_words_array, candidate_dates_array, initial_inverted_index, id_doc, sentence_II)

        relevant_words_array, KeyWords_dictionary = verify_keywords(initial_inverted_index, relevant_words_array, KeyWords_dictionary)
        all_docs_candidate_date += candidate_dates_array
        all_docs_relevant_words += relevant_words_array

    inverted_index = set_document_frequency(initial_inverted_index, all_docs_candidate_date, all_docs_relevant_words)

    return inverted_index, all_docs_relevant_words, all_docs_candidate_date


def ByDoc_inverted_index(doc, relevant_words_array, candidate_dates_array, inverted_index, id_doc, sentence_II):
    total_array = relevant_words_array + candidate_dates_array

    tokenize_Doc = tokenizer(doc)
    last_pos = 0
    inverted_index = get_occurrence(tokenize_Doc, relevant_words_array, inverted_index, id_doc, last_pos)

    for term in total_array:
        try:
            inverted_index[term][2][id_doc].append(sentence_II[term][2])
        except:
            pass

    return inverted_index


def BySentence_Inverted_index(relevant_words_array, candidate_dates_array, new_text):

    from Time_Matters_SingleDoc.InvertedIndex import create_inverted_index

    inverted_index, \
    relevant_words_list, candidate_dates_list, \
    sentence_array, sentence_tokens_list = create_inverted_index(relevant_words_array, candidate_dates_array, new_text)


    return inverted_index


def set_document_frequency(initial_inverted_index, all_docs_candidate_date, all_docs_relevant_words):
    total_array = all_docs_candidate_date + all_docs_relevant_words
    for w in total_array:
        total_freq = 0
        for x in initial_inverted_index[w][2]:
            total_freq += len(initial_inverted_index[w][2][x][1])
        initial_inverted_index[w][1] = total_freq
    return initial_inverted_index


# ************************************************************
# **************** text tokenizer by sentence **************
def sentence_tokenizer(text):
    # usage of nltk to tokenize the text by sentences
    sentences = nltk.sent_tokenize(text)
    return sentences
