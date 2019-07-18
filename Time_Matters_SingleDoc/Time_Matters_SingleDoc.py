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
    tt_name, language, document_type, document_creation_time, date_granularity, num_of_keywords, N, TH, n_contextual_window = verify_input_data(temporal_tagger, time_matters)

    # input validation
    result_validation_time_matters = verify_time_matters(num_of_keywords, N, n_contextual_window, TH)
    result_validation_score_type = verify_score_type(score_type, debug_mode)
    result_validation_temporal_tagger = verify_temporal_tagger(tt_name, language, document_type, date_granularity, document_creation_time)

    if result_validation_time_matters == {} or result_validation_temporal_tagger == {} or result_validation_score_type == {} and debug_mode:
        print({})
        raise SystemExit
    # creation of inverted index
    inverted_index, RelevantKWs, words_array, dates_array, \
    ListOfSentences, NormalizedCandidateDates, Text, time_tagger_start_time, kw_exec_time, sentence_tokens_list, \
    ii_exec_time = main_inverted_index(yake_lang, language, txt, num_of_keywords, document_type, document_creation_time, date_granularity, tt_name)


    gte_dictionary, DiceMatrix, dice_exec_time, gte_exec_time = GetDataScores(inverted_index, words_array, dates_array, n_contextual_window, TH, N, score_type)

    Score = {}
    if score_type == 'ByDoc':

        for dt in gte_dictionary:
            Score[dt] = [gte_dictionary[dt], NormalizedCandidateDates[dt]]
    else:

        for dt in gte_dictionary:
            last_occurrence = 0
            for sentence_id in gte_dictionary[dt]:
                #print(sentence_id)
                max_occurrences = len(inverted_index[dt][2][sentence_id][1])

                listtt = [NormalizedCandidateDates[dt][last_occurrence] for i in range(0, max_occurrences)]
                last_occurrence += max_occurrences
                gte_dictionary[dt][sentence_id].append(listtt)
        Score = gte_dictionary


    total_exec_time = (time.time() - total_start_time)
    if debug_mode:
        execution_time_list = {'TotalTime': total_exec_time,
                               tt_name: time_tagger_start_time,
                               'YAKE': kw_exec_time,
                               'InvertedIndex': ii_exec_time,
                               'DICE_Matrix': dice_exec_time,
                               'GTE': gte_exec_time}

        return Text, sentence_tokens_list, Score, NormalizedCandidateDates, RelevantKWs, inverted_index, DiceMatrix, execution_time_list
    elif not debug_mode:
        return Score, NormalizedCandidateDates, Text, sentence_tokens_list
