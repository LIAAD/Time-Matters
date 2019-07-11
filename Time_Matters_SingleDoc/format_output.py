
def main_format_score_debug(tt_name, inverted_index, gte_dictionary, debug_mode, date_dictionary, score_type, NormalizedText):
    final_score_output = {}

    if tt_name == 'py_heideltime' and score_type == 'ByDoc':
        final_score_output = py_heideltime_sigleDoc_debug(final_score_output, date_dictionary, inverted_index, gte_dictionary)
        normal_text = text_refactor(NormalizedText, final_score_output)
        candidate_dates_dictionary, normalized_candidate_date_dictionary = format_cantidate_dictionary(date_dictionary)
        return final_score_output, normal_text, candidate_dates_dictionary, normalized_candidate_date_dictionary

    elif tt_name == 'py_heideltime' and score_type == 'BySentence':
        final_score_output = py_heideltime_MultiScore_format(inverted_index, gte_dictionary, debug_mode, date_dictionary)
        normal_text = text_multi_refactor(NormalizedText, final_score_output)
        candidate_dates_dictionary, normalized_candidate_date_dictionary = format_cantidate_dictionary(date_dictionary)
        return final_score_output, normal_text, candidate_dates_dictionary, normalized_candidate_date_dictionary

    elif tt_name == 'rule_based' and score_type == 'ByDoc':
        final_score_output = rule_based_score_format(inverted_index, gte_dictionary)
        return final_score_output, date_dictionary
    elif tt_name == 'rule_based' and score_type == 'BySentence':
        final_score_output = rule_based_MultiScore_format(inverted_index, gte_dictionary)

        return final_score_output, date_dictionary


def main_format_score_no_debug(tt_name, inverted_index, gte_dictionary, debug_mode, date_dictionary, score_type):
    if tt_name == 'py_heideltime' and score_type == 'ByDoc':
        final_score_output = py_heideltime_score_format(inverted_index, gte_dictionary, date_dictionary)
        candidate_dates_dictionary, normalized_candidate_date_dictionary = format_cantidate_dictionary(date_dictionary)
        return final_score_output, normalized_candidate_date_dictionary

    elif tt_name == 'py_heideltime' and score_type == 'BySentence':
        final_score_output = py_heideltime_MultiScore_format(inverted_index, gte_dictionary, debug_mode, date_dictionary)
        candidate_dates_dictionary, normalized_candidate_date_dictionary = format_cantidate_dictionary(date_dictionary)
        return final_score_output, normalized_candidate_date_dictionary

    elif tt_name == 'rule_based'  and score_type == 'ByDoc':
        return gte_dictionary, date_dictionary
    elif tt_name == 'rule_based' and score_type == 'BySentence':
        return gte_dictionary, date_dictionary


def py_heideltime_score_format(inverted_index, gte_dictionary, date_dictionary):
    final_output= {}
    for date in gte_dictionary:
        # get all offset from dates
        total_offset = get_total_offset(inverted_index, date)
        final_output = create_final_output(final_output, gte_dictionary, date_dictionary, total_offset, date)
    return final_output


def create_final_output(final_output, list_dates_score, date_dictionary, total_offset, date):
    for n_expression in range(len(total_offset)):
        try:
            if date_dictionary[date][n_expression] not in final_output:
                final_output[date_dictionary[date][n_expression]] = list_dates_score[date]
        except:
            return final_output
    return final_output


def py_heideltime_MultiScore_format(inverted_index, gte_dictionary, debug_mode, date_dictionary):
    final_output = gte_dictionary
    ultimate_score = {}
    for date in gte_dictionary:
        total_offset = []

        for id_sentence in gte_dictionary[date]:
            total_offset += inverted_index[date][2][id_sentence][1]
            try:
                final_output[date][id_sentence].append(inverted_index[date][2][id_sentence][1])
            except:
                pass

        if debug_mode:
            ultimate_score = create_offset_py_heideltime_MultiScore_format_debug(gte_dictionary, date_dictionary, total_offset,
                                                                date, ultimate_score, inverted_index, debug_mode)
        else:
            ultimate_score = create_offset_py_heideltime_MultiScore_format_no_debug(gte_dictionary, date_dictionary, total_offset,
                                                           date, ultimate_score, inverted_index, debug_mode)
    return ultimate_score


def rule_based_MultiScore_format(inverted_index, list_dates_score):
    final_output = {}
    for date in list_dates_score:
        if date not in final_output:
            final_output[date] = {}
        final_output[date] = {sent_id: [list_dates_score[date][sent_id][0], inverted_index[date][2][sent_id][1]] for sent_id in list_dates_score[date]}
    return final_output


def create_offset_py_heideltime_MultiScore_format_debug(gte_dictionary, date_dictionary, total_offset, date, ultimate_score, inverted_index, debug_mode):
    try:
        for n_expression in range(len(total_offset)):
            new_date_format = get_new_date_format(date_dictionary, debug_mode, date, n_expression)
           # print(new_date_format)
            for sent_id in gte_dictionary[date]:
                # if debug mode insert score and offset
                if total_offset[n_expression] in inverted_index[date][2][sent_id][1]:
                    if date_dictionary[date][n_expression] not in ultimate_score:
                        ultimate_score[new_date_format] = {sent_id: gte_dictionary[date][sent_id]}
                    else:
                        ultimate_score[new_date_format][sent_id] = gte_dictionary[date][sent_id]
    except:
        return ultimate_score

    return ultimate_score


def create_offset_py_heideltime_MultiScore_format_no_debug(gte_dictionary, date_dictionary, total_offset, date, ultimate_score, inverted_index, debug_mode):
    try:
        for n_expression in range(len(total_offset)):
            new_date_format = get_new_date_format(date_dictionary, debug_mode, date, n_expression)
            for sent_id in gte_dictionary[date]:
                # if debug mode insert score and offset
                if total_offset[n_expression] in inverted_index[date][2][sent_id][1]:
                    if date_dictionary[date][n_expression] not in ultimate_score:
                        ultimate_score[new_date_format] = {sent_id: gte_dictionary[date][sent_id][0]}
                    else:
                        ultimate_score[new_date_format][sent_id] = gte_dictionary[date][sent_id][0]
    except:
        return ultimate_score
    return ultimate_score


def get_new_date_format(date_dictionary, debug_mode, date, n_expression):
    if debug_mode:
        new_date_format = date_dictionary[date][n_expression].replace(' ', '_')
    else:
        new_date_format = date_dictionary[date][n_expression]
    return new_date_format


def py_heideltime_sigleDoc_debug(dictionary_result, date_dictionary, inverted_index, gte_dictionary):

    for date in gte_dictionary:
        # get all offset from dates
        total_offset = get_total_offset(inverted_index, date)

        try:
            for n_expression in range(len(date_dictionary[date])):
                new_date_format = date_dictionary[date][n_expression].replace(' ', '_')

                #insert in new output dictionary
                if new_date_format not in dictionary_result and total_offset != []:
                    dictionary_result[new_date_format] = [gte_dictionary[date], [total_offset[n_expression]]]

                elif total_offset != []:
                    dictionary_result[new_date_format][1].append(total_offset[n_expression])
        except:
            pass

    return dictionary_result


def text_refactor(new_text, final_score_output):
    tokenize_text = new_text.split()
    for date in final_score_output:
        new_date_format = date.replace(' ', '_')

        offset = [final_score_output[date][1][0] for i in final_score_output[date]]
        for n_ofset in offset:
            tokenize_text[n_ofset] = new_date_format

    n_txt = " ".join(tokenize_text)
    return n_txt


def text_multi_refactor(new_text, final_score_output):
    tokenize_text = new_text.split()

    for i in final_score_output:
        offset = [final_score_output[i][date_sentence][1][0] for date_sentence in final_score_output[i]]
        new_date_format = i.replace(' ', '_')

        for n_ofset in offset:
            tokenize_text[n_ofset] = new_date_format
    n_txt = " ".join(tokenize_text)
    return n_txt


def format_cantidate_dictionary(date_dictionary):
    from Time_Matters_SingleDoc.GetDateScores import remove_duplicates

    candidate_date_dictionary = {dt.replace(' ', '_'): normalized_date for normalized_date in date_dictionary
                                 for dt in date_dictionary[normalized_date]}

    normalized_candidate_date_dictionary = {normalized_date: remove_duplicates(date_dictionary[normalized_date])
                                            for normalized_date in date_dictionary}

    return candidate_date_dictionary, normalized_candidate_date_dictionary


def rule_based_score_format(inverted_index, gte_dictionary):
    final_output = {}

    for date in gte_dictionary:

        total_offset = get_total_offset(inverted_index, date)
        final_output[date] = [gte_dictionary[date], total_offset]
    return final_output


def get_total_offset(inverted_index, date):
    dict_date_info = (inverted_index[date][2])
    total_offset = []
    for offset in dict_date_info:
        total_offset += dict_date_info[offset][1]
    return total_offset
