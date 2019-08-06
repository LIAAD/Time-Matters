from Time_Matters_SingleDoc.InvertedIndex import kw_ext
from Time_Matters_MultipleDoc.GetDateScoresMD import GetDataScores
from Time_Matters_MultipleDoc.Inverted_Index_MD import main_inverted_index_md
from langdetect import detect
from Time_Matters_MultipleDoc.validate_inputMD import verify_input_data, verify_temporal_tagger, verify_time_matters, verify_score_type


def Time_Matters_MultipleDoc(list_of_docs, temporal_tagger=[], time_matters=[], score_type='ByCorpus', debug_mode=False):

    tt_name, language, document_type, document_creation_time, date_granularity, \
    n_gram, num_of_keywords, N, TH, n_contextual_window = verify_input_data(temporal_tagger, time_matters)

    result_validation_time_matters = verify_time_matters(n_gram, num_of_keywords, N, n_contextual_window, TH, score_type)
    result_validation_score_type = verify_score_type(score_type, debug_mode)
    result_validation_temporal_tagger = verify_temporal_tagger(tt_name, language, document_type, date_granularity, document_creation_time)

    if result_validation_time_matters == {} or result_validation_temporal_tagger == {} or result_validation_score_type == {} and debug_mode:
        print({})
        raise SystemExit

    import time
    total_start_time = time.time()

    inverted_index, all_docs_relevant_words, \
    all_docs_candidate_date, all_docs_ExecTimeDictionary, \
    KeyWords_dictionary, DateDictionary, \
    kw_exec_time, ii_exec_time, \
    SentencesNormalized, SentencesTokens, \
    TextTokens, all_docs_TempExpressions, TextNormalized = main_inverted_index_md(language, list_of_docs, num_of_keywords, document_type, document_creation_time, date_granularity, tt_name, n_gram, score_type)

    gte_dictionary, DiceMatrix, dice_exec_time, gte_exec_time = GetDataScores(inverted_index, all_docs_relevant_words, all_docs_candidate_date, n_contextual_window, TH, N, score_type)
    total_exec_time = (time.time() - total_start_time)
    Sorted_Score = {}
    if score_type == 'ByCorpus':
        for dt in gte_dictionary:
            Sorted_Score[dt] = [gte_dictionary[dt], DateDictionary[dt]]
    elif score_type == 'ByDoc':
        for dt in gte_dictionary:
            last_occurrence = 0
            for doc_id in gte_dictionary[dt]:

                max_occurrences = len(inverted_index[dt][2][doc_id][1])
                gte_dictionary[dt][doc_id].append([])

                for i in range(max_occurrences):
                    gte_dictionary[dt][doc_id][1].append(DateDictionary[dt][doc_id][i])
                last_occurrence += max_occurrences

        Sorted_Score = sort_ByDoc_output(gte_dictionary)
    elif score_type == 'ByDocSentence':
        for dt in gte_dictionary:
            last_occurrence = 0
            for doc_id in gte_dictionary[dt]:
                for docSentence_id in gte_dictionary[dt][doc_id]:
                    max_occurrences = len(inverted_index[dt][2][doc_id][2][2][docSentence_id][1])
                    gte_dictionary[dt][doc_id][docSentence_id].append([])
                    for i in range(max_occurrences):
                        gte_dictionary[dt][doc_id][docSentence_id][1].append(DateDictionary[dt][doc_id][i])
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
