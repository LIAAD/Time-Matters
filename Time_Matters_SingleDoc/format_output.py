
def main_format_score(tt_name, inverted_index, relevant_dates, debug_mode, date_dictionary, score_type, NormalizedText):
    final_score_output = {}
    if tt_name == 'py_heideltime' and score_type == 'single':
        final_score_output = py_heideltime_score_format(inverted_index, relevant_dates, debug_mode, date_dictionary)

    elif tt_name == 'py_heideltime' and score_type == 'multiple':
        final_score_output = py_heideltime_MultiScore_format(inverted_index, relevant_dates, debug_mode, date_dictionary, tt_name)

    elif tt_name == 'rule_based'  and score_type == 'single':
        final_score_output = rule_based_score_format(inverted_index, relevant_dates, debug_mode)

    elif tt_name == 'rule_based' and score_type == 'multiple':
        final_score_output = rule_based_MultiScore_format(inverted_index, relevant_dates, debug_mode)
    if debug_mode:
        n_txt = text_refactor(NormalizedText, final_score_output, tt_name)
        return final_score_output, n_txt
    else:
        return final_score_output, NormalizedText


def py_heideltime_score_format(dictionary, list_dates_score, debug_mode, date_dictionary):
    final_output= {}
    for n_lt in range(len(list_dates_score)):
        dict_date_info = (dictionary[list_dates_score[n_lt][0]][2])

        total_offset = []
        #print(date_dictionary[list_dates_score[n_lt][0]])
        #print(dict_date_info)
        # get all offset from dates
        for offset in dict_date_info:
            total_offset += dict_date_info[offset][1]
        if debug_mode:
            #print(total_offset)
            final_output = create_final_output_debug(final_output, list_dates_score, date_dictionary, total_offset, n_lt)
        else:
            final_output = create_final_output(final_output, list_dates_score, date_dictionary, total_offset, n_lt)
    return final_output


def py_heideltime_MultiScore_format(inverted_index, relevant_dates, debug_mode, date_dictionary, tt_name):
    final_output = relevant_dates
    ultimate_score = {}
    if not debug_mode:
        return relevant_dates
    for date in relevant_dates:
        total_offset = []
        for id_sentence in relevant_dates[date]:
            total_offset += inverted_index[date][2][id_sentence][1]
            try:
                final_output[date][id_sentence].append(inverted_index[date][2][id_sentence][1])
            except:
                pass

        ultimate_score = create_offset_py_heideltime_MultiScore_format(relevant_dates, date_dictionary, total_offset,
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

def create_offset_py_heideltime_MultiScore_format(list_dates_score, date_dictionary, total_offset, date, ultimate_score, inverted_index, debug_mode):
    for n_expression in range(len(total_offset)):
        new_word = get_new_word(date_dictionary, debug_mode, date, n_expression)
        try:
                for sent_id in list_dates_score[date]:

                    if total_offset[n_expression] in inverted_index[date][2][sent_id][1]:
                        if date_dictionary[date][n_expression] not in ultimate_score:

                            ultimate_score[new_word] = {sent_id: list_dates_score[date][sent_id]}
                        else:
                            ultimate_score[new_word][sent_id] = list_dates_score[date][sent_id]
        except:
            return ultimate_score
    return ultimate_score


def get_new_word(date_dictionary, debug_mode, date, n_expression):
    if debug_mode:
        # print(total_offset)
        new_word = date_dictionary[date][n_expression].replace(' ', '_')
    else:
        new_word = date_dictionary[date][n_expression]
    return new_word


def create_final_output(final_output, list_dates_score, date_dictionary, total_offset, n_lt):
    for n_expression in range(len(total_offset)):
        try:

            if date_dictionary[list_dates_score[n_lt][0]][n_expression] not in final_output:

                final_output[date_dictionary[list_dates_score[n_lt][0]][n_expression]] = list_dates_score[n_lt][1]
        except:
            return final_output
    return final_output


def create_final_output_debug(final_output, list_dates_score, date_dictionary, total_offset, n_lt):
    for n_expression in range(len(total_offset)):
        # print('mm'+str(n_expression))
        # print(date_dictionary[list_dates_score[n_lt][0]][n_expression])
        try:
            new_word = date_dictionary[list_dates_score[n_lt][0]][n_expression].replace(' ', '_')
            if new_word not in final_output:
                final_output[new_word] = [list_dates_score[n_lt][1], [total_offset[n_expression]]]
            else:
                final_output[new_word][1].append(total_offset[n_expression])
        except:
            return final_output
    return final_output


def text_refactor(new_text, final_score_output, tt_name):
    n_txt = ''
    if tt_name == 'rule_based':
        return new_text
    else:
        tokenize_text = new_text.split()
        for date in final_score_output:
            new_word = date.replace(' ', '_')
            for i in final_score_output[date]:
                offset = final_score_output[date][i][1]
                for n_ofset in offset:
                    tokenize_text[n_ofset] = new_word
            n_txt = " ".join(tokenize_text)
    return n_txt

def text_multi_refactor(new_text, final_score_output, tt_name):
    if tt_name == 'rule_based':
        return new_text
    else:
        tokenize_text = new_text.split()
        for i in final_score_output:
            offset = final_score_output[i][1]
            new_word = i.replace(' ', '_')
            for n_ofset in offset:
                tokenize_text[n_ofset] = new_word
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

