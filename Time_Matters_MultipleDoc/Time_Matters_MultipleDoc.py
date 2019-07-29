from Time_Matters_SingleDoc.InvertedIndex import kw_ext
from Time_Matters_MultipleDoc.GetDateScores import GetDataScores
from Time_Matters_MultipleDoc.Inverted_Index_MD import main_inverted_index_md
from langdetect import detect
from Time_Matters_MultipleDoc.validate_input import verify_input_data


def Time_Matters_MultipleDoc(list_of_docs, temporal_tagger=[], time_matters=[], score_type='ByCorpus', debug_mode=False):

    tt_name, language, document_type, document_creation_time, date_granularity, \
    n_gram, num_of_keywords, N, TH, n_contextual_window = verify_input_data(temporal_tagger, time_matters)

    inverted_index, all_docs_relevant_words, \
    all_docs_candidate_date, ExecTimeDictionary = main_inverted_index_md(language, list_of_docs, num_of_keywords, document_type, document_creation_time, date_granularity, tt_name, n_gram)

    #print(inverted_index)
    print(all_docs_relevant_words)


    gte_dictionary, DiceMatrix, dice_exec_time, gte_exec_time = GetDataScores(inverted_index, all_docs_relevant_words, all_docs_candidate_date, n_contextual_window, TH, N, score_type)
    #print(DiceMatrix)
    #print(gte_dictionary)

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
    return inverted_index, DiceMatrix, gte_dictionary