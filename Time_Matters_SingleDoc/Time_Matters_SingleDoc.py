from Time_Matters_SingleDoc.InvertedIndex import main_inverted_index
from Time_Matters_SingleDoc.GetDateScores import dt_frames
from langdetect import detect
from Time_Matters_SingleDoc.validate_input import verify_input_data
from Time_Matters_SingleDoc.format_output import *


def Time_Matters_SingleDoc(txt, temporal_tagger=[], time_matters=[], score_type='single', debug_mode=False):
    try:
        yake_lang = detect(txt)
    except:
        yake_lang = 'en'
    tt_name, language, document_type, document_creation_time, date_granularity, \
    num_of_keywords, N, TH, n_contextual_window = verify_input_data(temporal_tagger, time_matters)

    inverted_index, words_array, dates_array, sentence_array, date_dictionary, new_text = main_inverted_index(yake_lang,language, txt, num_of_keywords, document_type,
                                                                        document_creation_time, date_granularity, tt_name)

    relevant_dates, DiceMatrix = dt_frames(inverted_index, words_array, dates_array, n_contextual_window,
                                         TH, N, score_type)
    dates_array_score = []
    for k in range(len(relevant_dates)):
        dates_array_score.append((relevant_dates[k][0], relevant_dates[k][1]))
    if tt_name == 'py_heideltime':
        final_score_output = get_final_output(inverted_index, dates_array_score, debug_mode, date_dictionary)
    else:
        final_score_output = get_final_output_rule_based(inverted_index, dates_array_score, debug_mode)

    if score_type == 'multiple' and debug_mode:
        n_txt = text_refactor(new_text, final_score_output, tt_name)
        return n_txt, final_score_output, dates_array, words_array, inverted_index, DiceMatrix
    elif score_type == 'multiple' and not debug_mode:
        return final_score_output
    elif score_type == 'single' and debug_mode:
        n_txt = text_refactor(new_text, final_score_output, tt_name)
        return n_txt, final_score_output, dates_array, words_array, inverted_index, DiceMatrix
    elif score_type == 'single' and not debug_mode:
        return final_score_output
    else:
        print('You must select a valid score_type.\n'
              'options:\n'
              '     single;\n'
              '     multiple;')
        return []

