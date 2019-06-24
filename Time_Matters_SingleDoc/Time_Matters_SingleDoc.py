from Time_Matters_SingleDoc.InvertedIndex import kw_ext
from Time_Matters_SingleDoc.GetDateScores import dt_frames
from langdetect import detect


def Time_Matters_SingleDoc(txt, temporal_tagger=[], time_matters_parameters=[], score_type='single', debug_mode=False):
    try:
        yake_lang = detect(txt)
    except:
        yake_lang = 'en'
    tt_name, language, document_type, document_creation_time, date_granularity, \
    num_of_keywords, N, TH, n_contextual_window = verify_input_data(temporal_tagger, time_matters_parameters)

    inverted_index, words_array, dates_array, sentence_array, date_dictionary, new_text = kw_ext(yake_lang,language, txt, num_of_keywords, document_type,
                                                                        document_creation_time, date_granularity, tt_name)

    relevant_dates, DiceMatrix = dt_frames(inverted_index, words_array, dates_array, n_contextual_window,
                                         TH, N, score_type)

    dates_array_score = []
    for k in range(len(relevant_dates)):
        dates_array_score.append((relevant_dates[k][0], relevant_dates[k][1]))
    final_score_output = get_final_output(inverted_index, dates_array_score, debug_mode, date_dictionary)

    if score_type == 'multiple' and debug_mode:
        n_txt = text_refactor(new_text, final_score_output)
        return final_score_output, dates_array, words_array, inverted_index, DiceMatrix, n_txt
    elif score_type == 'multiple' and not debug_mode:
        return final_score_output, sentence_array
    elif score_type == 'single' and debug_mode:
        n_txt = text_refactor(new_text, final_score_output)
        return final_score_output, dates_array, words_array, inverted_index, DiceMatrix, n_txt
    elif score_type == 'single' and not debug_mode:
        return final_score_output
    else:
        print('You must select a valid type of score.\n'
              'options:\n'
              '     single;\n'
              '     multiple;')
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
    n_contextual_window = 'none'
    N = 'max'
    TH = 0.05
    try:
        num_of_keywords = time_matters_parameters[0]
        n_contextual_window = time_matters_parameters[1]
        N = time_matters_parameters[2]
        TH = time_matters_parameters[3]
    except:
        pass
    return tt_name, language, document_type, document_creation_time, date_granularity, \
           num_of_keywords, N, TH, n_contextual_window


def get_final_output(dictionary, list_dates_score, debug_mode, date_dictionary):
    final_output= {}
    if debug_mode:
        for n_lt in range(len(list_dates_score)):
            dict_date_info = (dictionary[list_dates_score[n_lt][0]][2])
            total_offset = []

            # get all offset from dates
            for offset in dict_date_info:
                total_offset += dict_date_info[offset][1]


            for n_expression in range(len(total_offset)):
                new_word = date_dictionary[list_dates_score[n_lt][0]][n_expression].replace(' ', '_')
                if new_word not in final_output:
                    final_output[new_word] = [list_dates_score[n_lt][1], [total_offset[n_expression]]]
                else:
                    final_output[new_word][1].append(total_offset[n_expression])

        return final_output
    else:
        for n_lt in range(len(list_dates_score)):
            dict_date_info = (dictionary[list_dates_score[n_lt][0]][2])
            total_offset=[]

            # get all offset from dates
            for offset in dict_date_info:
                total_offset += dict_date_info[offset][1]

            for n_expression in range(len(total_offset)):
                if date_dictionary[list_dates_score[n_lt][0]][n_expression] not in final_output:
                    final_output[date_dictionary[list_dates_score[n_lt][0]][n_expression]] = list_dates_score[n_lt][1]

        return final_output

def text_refactor(new_text, final_score_output):

    tokenize_text = new_text.split()
    for i in final_score_output:
        offset = final_score_output[i][1]
        new_word = i.replace(' ', '_')
        for n_ofset in offset:
            tokenize_text[n_ofset] = new_word
    n_txt = " ".join(tokenize_text)

    return n_txt