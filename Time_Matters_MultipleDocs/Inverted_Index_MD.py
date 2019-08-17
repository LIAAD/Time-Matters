import time
from langdetect import detect
from Time_Matters_SingleDoc.InvertedIndex import kw_ext, get_occurrence, tokenizer, verify_keywords, rule_based, py_heideltime
from Time_Matters_SingleDoc.GetDateScores import remove_duplicates

def main_inverted_index_md(lang, list_of_docs, num_of_keywords, document_type, document_creation_time, date_granularity, date_extractor, n_gram, score_type):
    inverted_index = {}
    all_docs_candidate_date = []
    all_docs_relevant_words = []
    all_docs_text_list = []
    all_docs_KeyWords_dictionary = {}
    all_docs_candidateDates_dictionary = {}
    all_docs_exec_Time = {}
    all_docs_sentence_list = {}
    all_docs_sentence_tokens_list = {}
    all_docs_tokens = {}
    all_docs_TempExpressions = {}
    all_docs_kw_exec_time = 0
    all_docs_ii_exec_time = 0
    all_docs_text_norm_exec_time = 0
    TextNormalized_Dictionary = {}
    KeyWords_Dictionary_all_docs = {}
    for id_doc in range(len(list_of_docs)):
        try:
            yake_ln = detect(list_of_docs[id_doc])
        except:
            yake_ln = 'en'

        if date_extractor == 'rule_based':

            # =============================== Date Extractor ===============================================
            candidate_dates_array, new_text, date_dictionary, TempExpressions, ExecTimeDictionary = rule_based(list_of_docs[id_doc], date_granularity)
            # =============================== Keyword Extractor ===============================================
            KeyWords_dictionary, relevant_words_array, kw_exec_time = kw_ext(yake_ln, new_text, num_of_keywords, n_gram)
            all_docs_text_list.append(new_text)
        else:
            # =============================== Date Extractor ===============================================
            candidate_dates_array, new_text, date_dictionary, TempExpressions, ExecTimeDictionary = py_heideltime(list_of_docs[id_doc], lang, document_type, document_creation_time, date_granularity)
            # =============================== Keyword Extractor ===============================================
            KeyWords_dictionary, relevant_words_array, kw_exec_time = kw_ext(yake_ln, new_text, num_of_keywords, n_gram)
            all_docs_text_list.append(new_text)


        all_docs_exec_Time = {k: all_docs_exec_Time.get(k, 0) + ExecTimeDictionary.get(k, 0) for k in set(all_docs_exec_Time) | set(ExecTimeDictionary)}

        all_docs_kw_exec_time += kw_exec_time
        all_docs_candidateDates_dictionary = format_candidate_date_dictionary(date_dictionary, all_docs_candidateDates_dictionary, id_doc, score_type)

        all_docs_KeyWords_dictionary.update(KeyWords_dictionary)
        KeyWords_Dictionary_all_docs[id_doc] = KeyWords_dictionary
        all_docs_candidate_date += candidate_dates_array
        all_docs_relevant_words += relevant_words_array
        all_docs_TempExpressions[id_doc] = TempExpressions
        all_docs_candidate_date = remove_duplicates(all_docs_candidate_date)
        all_docs_relevant_words = remove_duplicates(all_docs_relevant_words)

    from yake.highlight import TextHighlighter
    th = TextHighlighter(max_ngram_size=n_gram)
    textNormalized = th.highlight(' ***+++doc_x+++*** '.join(all_docs_text_list), all_docs_relevant_words)

    all_docs = textNormalized.split(' ***+++doc_x+++*** ')

    # Create II per sentence and text normalization
    for doc_id in range(len(all_docs)):
        # Text normalization
        ii_start_time = time.time()
        # create inverted index
        sentence_II, sentence_array, sentence_tokens_list = BySentence_Inverted_index(all_docs_relevant_words, all_docs_candidate_date, all_docs[doc_id])
        ii_exec_time = (time.time() - ii_start_time)
        # Create II per Doc
        TextNormalized_Dictionary[doc_id] = all_docs[doc_id]
        all_docs_sentence_list[doc_id] = sentence_array
        all_docs_sentence_tokens_list[doc_id] = sentence_tokens_list
        all_docs_tokens[doc_id] = tokenizer(all_docs[doc_id])
        inverted_index = ByDoc_inverted_index(all_docs[doc_id], all_docs_relevant_words, all_docs_candidate_date, inverted_index, doc_id, sentence_II)
        all_docs_ii_exec_time += ii_exec_time

    filtered_all_docs_relevant_words, filtered_KeyWords_dictionary = verify_keywords(inverted_index, all_docs_relevant_words, all_docs_KeyWords_dictionary,all_docs_candidate_date)
    KeyWords_Dictionary_all_docs = verify_keywordsMD(KeyWords_Dictionary_all_docs, filtered_all_docs_relevant_words)
    all_docs_exec_Time['keyword_text_normalization'] = all_docs_text_norm_exec_time

    return inverted_index, filtered_all_docs_relevant_words, all_docs_candidate_date, all_docs_exec_Time, \
           KeyWords_Dictionary_all_docs, all_docs_candidateDates_dictionary, all_docs_kw_exec_time, all_docs_ii_exec_time, all_docs_sentence_list, all_docs_sentence_tokens_list, all_docs_tokens, all_docs_TempExpressions, TextNormalized_Dictionary


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

    return inverted_index, sentence_array, sentence_tokens_list


def format_candidate_date_dictionary(date_dictionary, all_docs_candidateDates_dictionary, id_doc, score_type):
    for dt_key in date_dictionary:

        if score_type != 'ByCorpus':
            if dt_key not in all_docs_candidateDates_dictionary:
                all_docs_candidateDates_dictionary[dt_key] = {}
            all_docs_candidateDates_dictionary[dt_key][id_doc] = date_dictionary[dt_key]
        elif score_type != 'ByDoc':
            if dt_key not in all_docs_candidateDates_dictionary:
                all_docs_candidateDates_dictionary[dt_key] = []
            all_docs_candidateDates_dictionary[dt_key] += date_dictionary[dt_key]

    return all_docs_candidateDates_dictionary


def verify_keywordsMD(KeyWords_Dictionary_all_docs, filtered_all_docs_relevant_words):
    new_dict = {}
    for doc_id in KeyWords_Dictionary_all_docs:
        new_dict[doc_id] = {}
        for kw in KeyWords_Dictionary_all_docs[doc_id]:
            if kw in filtered_all_docs_relevant_words:
                new_dict[doc_id][kw] = KeyWords_Dictionary_all_docs[doc_id][kw]


    return new_dict