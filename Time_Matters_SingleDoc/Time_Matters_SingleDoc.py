from Time_Matters_SingleDoc.InvertedIndex import kw_ext
from Time_Matters_SingleDoc.GetDateScores import dt_frames
from langdetect import detect


def Time_Matters_SingleDoc(txt, temporal_tagger=[], time_matters_parameters=[], score_type='single', debug_mode=False):
    try:
        yake_lang = detect(txt)
    except:
        yake_lang = 'en'
    tt_name, language, document_type, document_creation_time, date_granularity, \
    num_of_keywords, context_vector_size, threshold_sim_value, context_window_distance = verify_input_data(temporal_tagger, time_matters_parameters)

    inverted_index, words_array, dates_array, sentence_array = kw_ext(yake_lang,language, txt, num_of_keywords, document_type,
                                                                        document_creation_time, date_granularity, tt_name)

    relevant_dates, DiceMatrix = dt_frames(inverted_index, words_array, dates_array, context_window_distance,
                                         threshold_sim_value, context_vector_size, score_type)

    dates_array_score = []
    for k in range(len(relevant_dates)):
        dates_array_score.append((relevant_dates[k][0], relevant_dates[k][1]))
    final_score_output = get_final_output(inverted_index, dates_array_score)

    if score_type == 'multiple' and debug_mode:
        return final_score_output, dates_array, words_array, inverted_index, DiceMatrix, sentence_array
    elif sentence_array == 'multiple' and not debug_mode:
        return final_score_output, sentence_array
    elif score_type == 'single' and debug_mode:
        return final_score_output, dates_array, words_array, inverted_index, DiceMatrix, sentence_array
    elif score_type == 'single' and not debug_mode:
        return final_score_output
    else:
        print('You must choose one type of score.\n'
              'options:\n'
              '     single;\n'
              '     multiple')
        return []


def verify_input_data(temporal_tagger, time_matters_parameters):

    tt_name = 'py_heideltime'
    language = 'English'
    document_type = 'news'
    document_creation_time = ''
    date_granularity = ''
    # Verify the values for temporal Tagger parameters.
    try:
        tt_name = temporal_tagger[0].lower()
        if tt_name == 'py_heideltime':
            language = temporal_tagger[1]
            date_granularity = temporal_tagger[2].lower()
            document_type = temporal_tagger[3]
            document_creation_time = temporal_tagger[4]
        elif tt_name == 'rule_based':
            date_granularity = temporal_tagger[1].lower()
    except:
        pass
    num_of_keywords = 10
    context_window_distance = 'none'
    context_vector_size = 'max'
    threshold_sim_value = 0.05
    try:
        num_of_keywords = time_matters_parameters[0]
        context_window_distance = time_matters_parameters[1]
        context_vector_size = time_matters_parameters[2]
        threshold_sim_value = time_matters_parameters[3]
    except:
        pass
    return tt_name, language, document_type, document_creation_time, date_granularity, \
           num_of_keywords, context_vector_size, threshold_sim_value, context_window_distance


def get_final_output(dictionary, list_dates_score):
    final_output= []
    for lt in list_dates_score:
        dict_date_info = (dictionary[lt[0]][2])
        total_offset=[]
        for offset in dict_date_info:
            total_offset += dict_date_info[offset][1]

        final_output.append((lt[0],lt[1],total_offset))
    return final_output
