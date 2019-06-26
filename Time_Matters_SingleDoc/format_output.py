
def get_final_output(dictionary, list_dates_score, debug_mode, date_dictionary):
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


def get_final_output_rule_based(dictionary, list_dates_score, debug_mode):
    final_output = {}

    for lt in list_dates_score:
        dict_date_info = (dictionary[lt[0]][2])
        total_offset=[]
        for offset in dict_date_info:
            total_offset += dict_date_info[offset][1]
        if not debug_mode:
            final_output[lt[0]] = lt[1]
        else:
            final_output[lt[0]] = [lt[1], total_offset]
    return final_output