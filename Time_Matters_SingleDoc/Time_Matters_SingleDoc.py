#from Time_Matters_SingleDoc.InvertedIndex import main_inverted_index
#from Time_Matters_SingleDoc.GetDateScores import dt_frames
#from langdetect import detect
#from Time_Matters_SingleDoc.validate_input import *
#from Time_Matters_SingleDoc.format_output import *

from InvertedIndex import main_inverted_index
from GetDateScores import dt_frames
from langdetect import detect
from validate_input import *
from format_output import *

def Time_Matters_SingleDoc(txt, temporal_tagger=[], time_matters=[], score_type='single', debug_mode=False):
    try:
        yake_lang = detect(txt)
    except:
        yake_lang = 'en'
    tt_name, language, document_type, document_creation_time, date_granularity, num_of_keywords, N, TH, n_contextual_window = verify_input_data(temporal_tagger, time_matters)

    # input validation
    verify_time_matters(num_of_keywords, N, n_contextual_window, TH)
    verify_score_type(score_type)

    # creation of inverted index
    inverted_index, words_array, dates_array, sentence_array, date_dictionary, NormalizedText = main_inverted_index(yake_lang,language, txt, num_of_keywords, document_type,document_creation_time, date_granularity, tt_name)

    relevant_dates, DiceMatrix = dt_frames(inverted_index, words_array, dates_array, n_contextual_window,
                                         TH, N, score_type)

    #print(relevant_dates)
    if debug_mode and tt_name == 'py_heideltime':
        final_score_output, n_txt, candidate_dates_dictionary, normalized_candidate_date_dictionary, = main_format_score_debug(tt_name, inverted_index, relevant_dates, debug_mode, date_dictionary, score_type, NormalizedText, dates_array)
        return n_txt, NormalizedText, final_score_output, candidate_dates_dictionary, normalized_candidate_date_dictionary, words_array, inverted_index, DiceMatrix

    elif debug_mode and tt_name == 'rule_based':
        final_score_output, candidate_dates_list = main_format_score_debug(tt_name, inverted_index, relevant_dates, debug_mode, date_dictionary, score_type, NormalizedText, dates_array)
        return NormalizedText, final_score_output, candidate_dates_list,  words_array, inverted_index, DiceMatrix

    elif not debug_mode:
        candidate_dates_dictionary = main_format_score_no_debug(tt_name, inverted_index, relevant_dates, debug_mode, date_dictionary, score_type)

        return candidate_dates_dictionary



