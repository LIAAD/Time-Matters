
def main_format_score_debug(tt_name, inverted_index, relevant_dates, debug_mode, date_dictionary, score_type, NormalizedText, dates_array):
    final_score_output = {}

    if tt_name == 'py_heideltime' and score_type == 'single':
        final_score_output = py_heideltime_sigleDoc_debug(final_score_output, date_dictionary, inverted_index, relevant_dates)
        normal_text = text_refactor(NormalizedText, final_score_output, tt_name)
        candidate_dates_dictionary, normalized_candidate_date_dictionary = format_cantidate_dictionary(date_dictionary)
        return final_score_output, normal_text, candidate_dates_dictionary, normalized_candidate_date_dictionary

    elif tt_name == 'py_heideltime' and score_type == 'multiple':
        final_score_output = py_heideltime_MultiScore_format(inverted_index, relevant_dates, debug_mode, date_dictionary, tt_name)
        normal_text = text_multi_refactor(NormalizedText, final_score_output, tt_name)
        candidate_dates_dictionary, normalized_candidate_date_dictionary = format_cantidate_dictionary(date_dictionary)
        return final_score_output, normal_text, candidate_dates_dictionary, normalized_candidate_date_dictionary

    elif tt_name == 'rule_based' and score_type == 'single':
        final_score_output = rule_based_score_format(inverted_index, relevant_dates, debug_mode)
        return final_score_output, dates_array
    elif tt_name == 'rule_based' and score_type == 'multiple':
        final_score_output = rule_based_MultiScore_format(inverted_index, relevant_dates, debug_mode)
        return final_score_output, dates_array


def main_format_score_no_debug(tt_name, inverted_index, relevant_dates, debug_mode, date_dictionary, score_type):
    final_score_output = {}
    if tt_name == 'py_heideltime' and score_type == 'single':
        final_score_output = py_heideltime_score_format(inverted_index, relevant_dates, debug_mode, date_dictionary)
        return final_score_output

    elif tt_name == 'py_heideltime' and score_type == 'multiple':
        final_score_output = py_heideltime_MultiScore_format(inverted_index, relevant_dates, debug_mode, date_dictionary, tt_name)
        return final_score_output

    elif tt_name == 'rule_based'  and score_type == 'single':
        final_score_output = rule_based_score_format(inverted_index, relevant_dates, debug_mode)
        return final_score_output
    elif tt_name == 'rule_based' and score_type == 'multiple':
        final_score_output = rule_based_MultiScore_format(inverted_index, relevant_dates, debug_mode)
        return final_score_output


def py_heideltime_score_format(inverted_index, list_dates_score, debug_mode, date_dictionary):
    final_output= {}
    dictionary_result = {}
    for n_lt in range(len(list_dates_score)):
        dict_date_info = (inverted_index[list_dates_score[n_lt][0]][2])

        total_offset = []
        #print(date_dictionary[list_dates_score[n_lt][0]])
        #print(dict_date_info)
        # get all offset from dates
        for offset in dict_date_info:
            total_offset += dict_date_info[offset][1]
        final_output = create_final_output(final_output, list_dates_score, date_dictionary, total_offset, n_lt)

    return final_output


def py_heideltime_MultiScore_format(inverted_index, relevant_dates, debug_mode, date_dictionary, tt_name):
    final_output = relevant_dates
    ultimate_score = {}
    #print(relevant_dates)
    for date in relevant_dates:
        total_offset = []
        for id_sentence in relevant_dates[date]:
            total_offset += inverted_index[date][2][id_sentence][1]
            try:
                final_output[date][id_sentence].append(inverted_index[date][2][id_sentence][1])
            except:
                pass
        if debug_mode:
            ultimate_score = create_offset_py_heideltime_MultiScore_format_debug(relevant_dates, date_dictionary, total_offset,
                                                                date, ultimate_score, inverted_index, debug_mode)
        else:
            ultimate_score = create_offset_py_heideltime_MultiScore_format_no_debug(relevant_dates, date_dictionary, total_offset,
                                                                date, ultimate_score, inverted_index, debug_mode)
    return ultimate_score

def rule_based_MultiScore_format(inverted_index, list_dates_score, debug_mode):
    final_output = {}
    for date in list_dates_score:

        if debug_mode:
            if date not in final_output:
                final_output[date] = {}
            for sent_id in list_dates_score[date]:
                final_output[date][sent_id] = [list_dates_score[date][sent_id][0], inverted_index[date][2][sent_id][1]]
        else:
            return list_dates_score
    return final_output


def create_offset_py_heideltime_MultiScore_format_debug(list_dates_score, date_dictionary, total_offset, date, ultimate_score, inverted_index, debug_mode):
    for n_expression in range(len(total_offset)):
        new_date_format = get_new_date_format(date_dictionary, debug_mode, date, n_expression)
        try:
                for sent_id in list_dates_score[date]:
                    # if debug mode insert score and offset
                    if total_offset[n_expression] in inverted_index[date][2][sent_id][1]:
                        if date_dictionary[date][n_expression] not in ultimate_score:
                            ultimate_score[new_date_format] = {sent_id: list_dates_score[date][sent_id]}
                        else:
                            ultimate_score[new_date_format][sent_id] = list_dates_score[date][sent_id]
        except:
            return ultimate_score
    return ultimate_score


def create_offset_py_heideltime_MultiScore_format_no_debug(list_dates_score, date_dictionary, total_offset, date, ultimate_score, inverted_index, debug_mode):
    for n_expression in range(len(total_offset)):
        new_date_format = get_new_date_format(date_dictionary, debug_mode, date, n_expression)
        try:
                for sent_id in list_dates_score[date]:
                    # if debug mode insert score and offset
                    if total_offset[n_expression] in inverted_index[date][2][sent_id][1]:
                        if date_dictionary[date][n_expression] not in ultimate_score:
                            ultimate_score[new_date_format] = {sent_id: list_dates_score[date][sent_id][0]}
                        else:
                            ultimate_score[new_date_format][sent_id] = list_dates_score[date][sent_id][0]
        except:
            return ultimate_score
    return ultimate_score

def get_new_date_format(date_dictionary, debug_mode, date, n_expression):
    if debug_mode:
        # print(total_offset)
        new_date_format = date_dictionary[date][n_expression].replace(' ', '_')
    else:
        new_date_format = date_dictionary[date][n_expression]
    return new_date_format


def create_final_output(final_output, list_dates_score, date_dictionary, total_offset, n_lt):
    for n_expression in range(len(total_offset)):
        try:
            if date_dictionary[list_dates_score[n_lt][0]][n_expression] not in final_output:
                final_output[date_dictionary[list_dates_score[n_lt][0]][n_expression]] = list_dates_score[n_lt][1]
        except:
            return final_output
    return final_output


def py_heideltime_sigleDoc_debug(dictionary_result, date_dictionary, inverted_index, list_dates_score):
    for norm_date in list_dates_score:
        dict_date_info = (inverted_index[norm_date[0]][2])
        total_offset = []
        #print(date_dictionary[list_dates_score[n_lt][0]])
        #print(dict_date_info)
        # get all offset from dates

        for offset in dict_date_info:
            total_offset += dict_date_info[offset][1]

        for n_expression in range(len(total_offset)):
            new_date_format = date_dictionary[norm_date[0]][n_expression].replace(' ', '_')
            if new_date_format not in dictionary_result:
                dictionary_result[new_date_format] = [norm_date[1], []]
            dictionary_result[new_date_format][1].append(total_offset[n_expression])
    return dictionary_result


def text_refactor(new_text, final_score_output, tt_name):
    n_txt = ''
    if tt_name == 'rule_based':
        return new_text
    else:
        tokenize_text = new_text.split()
        for date in final_score_output:
            new_date_format = date.replace(' ', '_')
            for i in final_score_output[date]:
                offset = final_score_output[date][1]
                for n_ofset in offset:
                    tokenize_text[n_ofset] = new_date_format
            n_txt = " ".join(tokenize_text)
    return n_txt


def text_multi_refactor(new_text, final_score_output, tt_name):
    if tt_name == 'rule_based':
        return new_text
    else:

        tokenize_text = new_text.split()
        for i in final_score_output:
            offset = []
            for date_sentence in final_score_output[i]:
                try:
                    offset += final_score_output[i][date_sentence][1]
                except:
                    pass
            new_date_format = i.replace(' ', '_')
            for n_ofset in offset:
                tokenize_text[n_ofset] = new_date_format
        n_txt = " ".join(tokenize_text)
        return n_txt


def rule_based_score_format(inverted_index, list_dates_score, debug_mode):
    final_output = {}

    for lt in list_dates_score:
        dict_date_info = (inverted_index[lt[0]][2])
        total_offset=[]
        for offset in dict_date_info:
            total_offset += dict_date_info[offset][1]
        if not debug_mode:
            final_output[lt[0]] = lt[1]
        else:
            final_output[lt[0]] = [lt[1], total_offset]
    return final_output


def format_cantidate_dictionary(date_dictionary):
    from Time_Matters_SingleDoc.GetDateScores import remove_duplicates
    candidate_date_dictionary = {}
    normalized_candidate_date_dictionary = {}
    for noralized_date in date_dictionary:
        for dt in date_dictionary[noralized_date]:
            if dt not in candidate_date_dictionary:

                candidate_date_dictionary[dt.replace(' ', '_')] = noralized_date

        normalized_candidate_date_dictionary[noralized_date] = remove_duplicates(date_dictionary[noralized_date])
    return candidate_date_dictionary, normalized_candidate_date_dictionary
