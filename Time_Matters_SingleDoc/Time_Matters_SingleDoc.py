
from Time_Matters_SingleDoc.InvertedIndex import main_inverted_index
from Time_Matters_SingleDoc.GetDateScores import GetDataScores
from langdetect import detect
from Time_Matters_SingleDoc.validate_input import *


def Time_Matters_SingleDoc(txt, temporal_tagger=[], time_matters=[], score_type='ByDoc', debug_mode=False):
    try:
        yake_lang = detect(txt)
    except:
        yake_lang = 'en'
    import time
    total_start_time = time.time()

    tt_name, language, document_type, document_creation_time, date_granularity, begin_date, end_date = verify_temporal_data(temporal_tagger)
    n_gram, num_of_keywords, N, TH, n_contextual_window = verify_time_matters_input(time_matters)
    # input validation
    result_validation_time_matters = verify_time_matters(n_gram, num_of_keywords, N, n_contextual_window, TH)
    result_validation_score_type = verify_score_type(score_type, debug_mode)
    result_validation_temporal_tagger = verify_temporal_tagger(tt_name, language, document_type, date_granularity, document_creation_time, begin_date, end_date)

    if result_validation_time_matters == {} or result_validation_temporal_tagger == {} or result_validation_score_type == {}:
        print([])
        return []
    # creation of inverted index
    inverted_index, RelevantKWs, words_array, dates_array, \
    SentencesNormalized, DateDictionary, TempExpressions, TextNormalized, kw_exec_time, SentencesTokens, TextTokens,\
    ii_exec_time, TimeTaggerExecTimeDictionary = main_inverted_index(yake_lang, language, txt, num_of_keywords, document_type, document_creation_time, date_granularity, tt_name, n_gram, begin_date, end_date)

    gte_dictionary, DiceMatrix, dice_exec_time, gte_exec_time = GetDataScores(inverted_index, words_array, dates_array, n_contextual_window, TH, N, score_type)

    Sorted_Score = {}
    if score_type == 'ByDoc':
        for dt in gte_dictionary:

            Sorted_Score[dt] = [gte_dictionary[dt], DateDictionary[dt]]
    else:

        for dt in gte_dictionary:
            last_occurrence = 0

            for sentence_id in gte_dictionary[dt]:

                max_occurrences = len(inverted_index[dt][2][sentence_id][1])
                gte_dictionary[dt][sentence_id].append([])

                for i in range(max_occurrences):
                    gte_dictionary[dt][sentence_id][1].append(DateDictionary[dt][i])
                last_occurrence += max_occurrences

        Sorted_Score = sort_BySentence_output(gte_dictionary)
    total_exec_time = (time.time() - total_start_time)
    if debug_mode:
        ExecTimeDictionary = {'TotalTime': total_exec_time}

        ExecTimeDictionary.update(TimeTaggerExecTimeDictionary)

        ExecTimeDictionary['YAKE'] = kw_exec_time
        ExecTimeDictionary['InvertedIndex'] = ii_exec_time
        ExecTimeDictionary['DICE_Matrix'] = dice_exec_time
        ExecTimeDictionary['GTE'] = gte_exec_time

        return [Sorted_Score, TempExpressions, RelevantKWs, TextNormalized, TextTokens, SentencesNormalized, SentencesTokens, inverted_index, DiceMatrix, ExecTimeDictionary]
    elif not debug_mode:

        return [Sorted_Score, TempExpressions, RelevantKWs, TextNormalized, TextTokens, SentencesNormalized, SentencesTokens]


def sort_BySentence_output(Score):
    import operator

    temporal_dictionary = {}
    for kv in Score:
        list_date_score = []
        for sentence in Score[kv]:
            list_date_score.append(Score[kv][sentence][0])
        temporal_dictionary[kv] = max(list_date_score)

    sorted_dt = sorted(temporal_dictionary.items(), key=operator.itemgetter(1), reverse=True)

    final_op = {}
    sorted_dates = [i[0] for i in sorted_dt]
    for dt in sorted_dates:
        final_op[dt] = Score[dt]
    return final_op



