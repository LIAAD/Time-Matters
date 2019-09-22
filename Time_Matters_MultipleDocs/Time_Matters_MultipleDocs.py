from Time_Matters_MultipleDocs.GetDateScoresMD import GetDataScores
from Time_Matters_MultipleDocs.Inverted_Index_MD import main_inverted_index_md
from Time_Matters_MultipleDocs.validate_inputMD import verify_temporal_tagger,  verify_score_type, verify_time_matters, verify_temporal_data, verify_time_matters_input

def Time_Matters_MultipleDocs(list_of_docs, temporal_tagger=[], time_matters=[], score_type='ByCorpus', debug_mode=False):

    result_validation_score_type = verify_score_type(score_type, debug_mode)


    tt_name, language, document_type, document_creation_time, date_granularity, begin_date, end_date = verify_temporal_data(temporal_tagger)
    n_gram, num_of_keywords, N, TH, n_contextual_window = verify_time_matters_input(time_matters, score_type)
    result_validation_temporal_tagger = verify_temporal_tagger(tt_name, language, document_type, date_granularity, document_creation_time)
    result_validation_time_matters = verify_time_matters(n_gram, num_of_keywords, N, n_contextual_window, TH, score_type)

    if result_validation_time_matters == {} or result_validation_temporal_tagger == {} or result_validation_score_type == {}:
        print([])
        return []

    import time
    total_start_time = time.time()

    inverted_index, all_docs_relevant_words, \
    all_docs_candidate_date, all_docs_ExecTimeDictionary, \
    KeyWords_dictionary, DateDictionary, \
    kw_exec_time, ii_exec_time, \
    SentencesNormalized, SentencesTokens, \
    TextTokens, all_docs_TempExpressions, TextNormalized = main_inverted_index_md(language, list_of_docs,
                                                                                  num_of_keywords, document_type, document_creation_time, date_granularity, tt_name, n_gram, score_type, begin_date, end_date)

    gte_dictionary, DiceMatrix, dice_exec_time, gte_exec_time = GetDataScores(inverted_index, all_docs_relevant_words, all_docs_candidate_date, n_contextual_window, TH, N, score_type)
    total_exec_time = (time.time() - total_start_time)
    Sorted_Score = {}
    if score_type == 'ByCorpus':
        for dt in gte_dictionary:
            # get a dict of tempExpressions
            dict_tempExpresions = {}
            dict_tempExpresions[dt] = {}
            for corpus_id in all_docs_TempExpressions:
                x = [i[1] for i in all_docs_TempExpressions[corpus_id] if i[0].lower() == dt]
                if x:
                    dict_tempExpresions[dt][corpus_id] = x

            Sorted_Score[dt] = [gte_dictionary[dt], dict_tempExpresions[dt]]
    elif score_type == 'ByDoc':
        for dt in gte_dictionary:
            last_occurrence = 0
            for doc_id in gte_dictionary[dt]:

                max_occurrences = len(inverted_index[dt][2][doc_id][1])
                gte_dictionary[dt][doc_id].append([])

                for i in range(max_occurrences):
                    gte_dictionary[dt][doc_id][1].append(DateDictionary[dt][doc_id][0])
                last_occurrence += max_occurrences

        Sorted_Score = sort_ByDoc_output(gte_dictionary)

    elif score_type == 'ByDocSentence':
        for dt in gte_dictionary:
            last_occurrence = 0
            for doc_id in gte_dictionary[dt]:
                for docSentence_id in gte_dictionary[dt][doc_id]:
                    max_occurrences = len(inverted_index[dt][2][doc_id][2][docSentence_id][1])
                    gte_dictionary[dt][doc_id][docSentence_id].append([])
                    for i in range(max_occurrences):
                        gte_dictionary[dt][doc_id][docSentence_id][1].append(DateDictionary[dt][doc_id][0])
                    last_occurrence += max_occurrences
        Sorted_Score = sort_ByDocSentence_output(gte_dictionary)


    if debug_mode:
        ExecTimeDictionary = {'TotalTime': total_exec_time}

        ExecTimeDictionary.update(all_docs_ExecTimeDictionary)

        ExecTimeDictionary['YAKE'] = kw_exec_time
        ExecTimeDictionary['InvertedIndex'] = ii_exec_time
        ExecTimeDictionary['DICE_Matrix'] = dice_exec_time
        ExecTimeDictionary['GTE'] = gte_exec_time

        return [Sorted_Score, all_docs_TempExpressions, KeyWords_dictionary, TextNormalized, TextTokens, SentencesNormalized, SentencesTokens, inverted_index, DiceMatrix, ExecTimeDictionary]
    elif not debug_mode:
        return [Sorted_Score, all_docs_TempExpressions, KeyWords_dictionary, TextNormalized, TextTokens, SentencesNormalized, SentencesTokens]


def sort_ByDoc_output(Score):
    import operator

    temporal_dictionary = {}
    for kv in Score:
        list_date_score = []
        for doc in Score[kv]:
            list_date_score.append(Score[kv][doc][0])
        temporal_dictionary[kv] = max(list_date_score)

    sorted_dt = sorted(temporal_dictionary.items(), key=operator.itemgetter(1), reverse=True)

    final_op = {}
    sorted_dates = [i[0] for i in sorted_dt]
    for dt in sorted_dates:
        final_op[dt] = Score[dt]
    return final_op


def sort_ByDocSentence_output(Score):
    import operator

    temporal_dictionary = {}
    for kv in Score:
        list_date_score = []
        for doc in Score[kv]:

            for set in Score[kv][doc]:

                list_date_score.append(Score[kv][doc][set][0])
        temporal_dictionary[kv] = max(list_date_score)
    sorted_dt = sorted(temporal_dictionary.items(), key=operator.itemgetter(1), reverse=True)

    final_op = {}
    sorted_dates = [i[0] for i in sorted_dt]
    for dt in sorted_dates:
        final_op[dt] = Score[dt]
    return final_op
