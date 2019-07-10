from Time_Matters_SingleDoc.InvertedIndex import main_inverted_index
from Time_Matters_SingleDoc.GetDateScores import GetDataScores
from langdetect import detect
from Time_Matters_SingleDoc.validate_input import *
from Time_Matters_SingleDoc.format_output import *


def Time_Matters_SingleDoc(txt, temporal_tagger=[], time_matters=[], score_type='ByDoc', debug_mode=False):
    try:
        yake_lang = detect(txt)
    except:
        yake_lang = 'en'
    import time
    total_start_time = time.time()
    tt_name, language, document_type, document_creation_time, date_granularity, num_of_keywords, N, TH, n_contextual_window = verify_input_data(
        temporal_tagger, time_matters)

    # input validation
    result_validation_time_matters = verify_time_matters(num_of_keywords, N, n_contextual_window, TH)
    result_validation_score_type = verify_score_type(score_type, debug_mode)
    result_validation_temporal_tagger = verify_temporal_tagger(tt_name, language, document_type, date_granularity, document_creation_time)

    if result_validation_time_matters == {} or result_validation_temporal_tagger == {} or result_validation_score_type == {} and debug_mode:
        print({})
        from sys import exit
        exit()
    # creation of inverted index
    inverted_index, words_array, dates_array, ListOfSentences, date_dictionary, NormalizedText, time_tagger_start_time, kw_exec_time, ii_exec_time = main_inverted_index(
        yake_lang, language, txt, num_of_keywords, document_type, document_creation_time, date_granularity, tt_name)

    gte_dictionary, DiceMatrix, dice_exec_time, gte_exec_time = GetDataScores(inverted_index, words_array, dates_array,
                                                                              n_contextual_window,
                                                                              TH, N, score_type)
    total_exec_time = (time.time() - total_start_time)
    if debug_mode and tt_name == 'py_heideltime':
        execution_time_list = {'TotalTime': total_exec_time,
                               tt_name: time_tagger_start_time,
                               'YAKE': kw_exec_time,
                               'InvertedIndex': ii_exec_time,
                               'DICE_Matrix': dice_exec_time,
                               'GTE': gte_exec_time}

        final_score_output, n_txt, candidate_dates_dictionary, normalized_candidate_date_dictionary, = main_format_score_debug(
            tt_name, inverted_index, gte_dictionary, debug_mode, date_dictionary, score_type, NormalizedText,
            dates_array)

        from Time_Matters_SingleDoc.InvertedIndex import sentence_tokenizer
        ListOfSentences = sentence_tokenizer(NormalizedText)
        return n_txt, NormalizedText, ListOfSentences, final_score_output, candidate_dates_dictionary, normalized_candidate_date_dictionary, words_array, inverted_index, DiceMatrix, execution_time_list
    elif debug_mode and tt_name == 'rule_based':
        execution_time_list = {'TotalTime': total_exec_time,
                               tt_name: time_tagger_start_time,
                               'YAKE': kw_exec_time,
                               'InvertedIndex': ii_exec_time,
                               'DICE_Matrix': dice_exec_time,
                               'GTE': gte_exec_time}

        final_score_output, candidate_dates_list = main_format_score_debug(tt_name, inverted_index, gte_dictionary,
                                                                           debug_mode, date_dictionary, score_type,
                                                                           NormalizedText, dates_array)
        return NormalizedText, final_score_output, ListOfSentences, candidate_dates_list, words_array, inverted_index, DiceMatrix, execution_time_list

    elif not debug_mode:
        final_score_output, NormalizedCandidateDates = main_format_score_no_debug(tt_name, inverted_index, gte_dictionary, debug_mode,
                                                        date_dictionary, score_type, dates_array)
        return final_score_output, NormalizedCandidateDates
