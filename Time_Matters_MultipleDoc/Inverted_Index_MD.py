from Time_Matters_SingleDoc import *
from langdetect import detect
from Time_Matters_SingleDoc.InvertedIndex import kw_ext, get_occurrence, tokenizer, verify_keywords


def main_inverted_index_md(lang, list_of_docs, num_of_keywords,  document_type, document_creation_time, date_granularity, date_extractor, n_gram):
    list_of_striped_docs = []
    inverted_index = {}

    all_docs_candidate_date = []
    all_docs_relevant_words = []
    current_offset = 0
    for id_doc in range(len(list_of_docs)):
        try:
            yake_ln = detect(list_of_docs[id_doc])
        except:
            yake_ln = 'en'

        if date_extractor == 'rule_based':
            # =============================== Keyword Extractor ===============================================
            KeyWords_dictionary, relevant_words_array, kw_exec_time = kw_ext(yake_ln, list_of_docs[id_doc], num_of_keywords, n_gram)
            # =============================== Date Extractor ===============================================
            time_tagger_start_time = time.time()
            candidate_dates_array, new_text, date_dictionary = rule_based(list_of_docs[id_doc], date_granularity, relevant_words_array, n_gram)
            time_tagger_exec_time = (time.time() - time_tagger_start_time)
            if n_gram > 1:
                new_text = format_text_more_gram(new_text, relevant_words_array, n_gram)
            else:
                new_text = format_text(new_text, relevant_words_array)
        else:
            # =============================== Date Extractor ===============================================
            time_tagger_start_time = time.time()
            candidate_dates_array, new_text, date_dictionary = py_heideltime(list_of_docs[id_doc], lang, document_type,
                                                                             document_creation_time, date_granularity)


            time_tagger_exec_time = (time.time() - time_tagger_start_time)

            # =============================== Keyword Extractor ===============================================
            KeyWords_dictionary, relevant_words_array, kw_exec_time = kw_ext(yake_ln, new_text, num_of_keywords, n_gram)
            if n_gram > 1:
                new_text = format_text_more_gram(new_text, relevant_words_array, n_gram)
            else:
                new_text = format_text(new_text, relevant_words_array)

        # Create II per sentence
        sentence_II = BySentence_Inverted_index(relevant_words_array, candidate_dates_array, new_text)
        #print(sentence_II)
        # Create II per Doc
        inverted_index = ByDoc_inverted_index(new_text, relevant_words_array, candidate_dates_array, inverted_index, id_doc, sentence_II)

        relevant_words_array, KeyWords_dictionary = verify_keywords(inverted_index, relevant_words_array, KeyWords_dictionary)
        all_docs_candidate_date += candidate_dates_array
        all_docs_relevant_words += relevant_words_array

    return inverted_index, all_docs_relevant_words, all_docs_candidate_date


def ByDoc_inverted_index(doc, relevant_words_array, candidate_dates_array, inverted_index, id_doc, sentence_II):
    total_array = relevant_words_array + candidate_dates_array

    tokenize_Doc = tokenizer(doc)
    last_pos = 0
    inverted_index = get_occurrence(tokenize_Doc, inverted_index, id_doc, last_pos)

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

