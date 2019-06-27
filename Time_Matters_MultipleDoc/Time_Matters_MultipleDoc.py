from Time_Matters_SingleDoc.InvertedIndex import kw_ext
from Time_Matters_SingleDoc.GetDateScores import dt_frames
from Time_Matters_MultipleDoc.Inverted_Index_MD import main_inverted_index_md
from langdetect import detect
from Time_Matters_SingleDoc.validate_input import verify_input_data
from Time_Matters_SingleDoc.format_output import *


def Time_Matters_MultipleDoc(list_of_docs, temporal_tagger=[], time_matters=[], debug_mode=False):
    score_type = 'multiple'
    tt_name, language, document_type, document_creation_time, date_granularity, \
    num_of_keywords, N, TH, n_contextual_window = verify_input_data(temporal_tagger, time_matters)

    inverted_index, all_docs_relevant_words, \
    all_docs_candidate_date, list_of_striped_docs, join_docs = main_inverted_index_md(language, list_of_docs,
                                                                                      num_of_keywords, document_type,
                                                                        document_creation_time, date_granularity, tt_name)
    print(inverted_index)


    relevant_dates, DiceMatrix = dt_frames(inverted_index, all_docs_relevant_words, all_docs_candidate_date, n_contextual_window,
                                         TH, N, score_type)
    #print(DiceMatrix)
    print(relevant_dates)
    #dates_array_score = []
    #for k in range(len(relevant_dates)):
    #    dates_array_score.append((relevant_dates[k][0], relevant_dates[k][1]))
    #if tt_name == 'py_heideltime':
    #    final_score_output = get_final_output(inverted_index, dates_array_score, debug_mode, date_dictionary)
   # else:
    #    final_score_output = get_final_output_rule_based(inverted_index, dates_array_score, debug_mode)

    #if debug_mode:
     #   n_txt = text_refactor(new_text, final_score_output, tt_name)
      #  return final_score_output, dates_array, words_array, inverted_index, DiceMatrix, n_txt
    #else:
     #   return final_score_output
