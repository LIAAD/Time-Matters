
from Time_Matters_SingleDoc.InvertedIndex import main_inverted_index
from Time_Matters_SingleDoc.GetDateScores import GetDataScores
from langdetect import detect
from Time_Matters_SingleDoc.validate_input import *


def remove_duplicates(string_list):
    return list(dict.fromkeys(string_list))

def Time_Matters_SingleDoc(txt, temporal_tagger=[], time_matters=[], score_type='ByDoc', debug_mode=False):
    try:
        yake_lang = detect(txt)
    except:
        yake_lang = 'en'
    import time
    total_start_time = time.time()
    tt_name, language, document_type, document_creation_time, date_granularity, n_gram, num_of_keywords, N, TH, n_contextual_window = verify_input_data(temporal_tagger, time_matters)

    # input validation
    result_validation_time_matters = verify_time_matters(n_gram, num_of_keywords, N, n_contextual_window, TH)
    result_validation_score_type = verify_score_type(score_type, debug_mode)
    result_validation_temporal_tagger = verify_temporal_tagger(tt_name, language, document_type, date_granularity, document_creation_time)

    if result_validation_time_matters == {} or result_validation_temporal_tagger == {} or result_validation_score_type == {} and debug_mode:
        print({})
        raise SystemExit

    # creation of inverted index
    inverted_index, RelevantKWs, words_array, dates_array, \
    SentencesNormalized, DateDictionary, TempExpressions, TextNormalized, kw_exec_time, SentencesTokens, TextTokens,\
    ii_exec_time, TimeTaggerExecTimeDictionary = main_inverted_index(yake_lang, language, txt, num_of_keywords, document_type, document_creation_time, date_granularity, tt_name, n_gram)


    gte_dictionary, DiceMatrix, dice_exec_time, gte_exec_time = GetDataScores(inverted_index, words_array, dates_array, n_contextual_window, TH, N, score_type)

    Score = {}
    if score_type == 'ByDoc':
        for dt in gte_dictionary:

            Score[dt] = [gte_dictionary[dt], DateDictionary[dt]]
    else:

        for dt in gte_dictionary:
            last_occurrence = 0

            for sentence_id in gte_dictionary[dt]:

                max_occurrences = len(inverted_index[dt][2][sentence_id][1])
                gte_dictionary[dt][sentence_id].append([])

                for i in range(max_occurrences):
                    gte_dictionary[dt][sentence_id][1].append(DateDictionary[dt][i])
                last_occurrence += max_occurrences

        Score = gte_dictionary

    total_exec_time = (time.time() - total_start_time)
    if debug_mode:
        ExecTimeDictionary = {'TotalTime': total_exec_time,
                               'YAKE': kw_exec_time,
                               'InvertedIndex': ii_exec_time,
                               'DICE_Matrix': dice_exec_time,
                               'GTE': gte_exec_time}

        ExecTimeDictionary.update(TimeTaggerExecTimeDictionary)
        return Score, TempExpressions, RelevantKWs, TextNormalized, TextTokens, SentencesNormalized, SentencesTokens, inverted_index, DiceMatrix, ExecTimeDictionary
    elif not debug_mode:

        return Score, TempExpressions, RelevantKWs, TextNormalized, TextTokens, SentencesNormalized, SentencesTokens
