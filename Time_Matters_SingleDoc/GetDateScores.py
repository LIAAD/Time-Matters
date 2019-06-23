import pandas as pd
import statistics
import operator
import time


# *************************************************
# remove duplicates from words and dates array
def remove_duplicates(string_list):
    return list(dict.fromkeys(string_list))


def dt_frames(inverted_index, words_array, dates_array, contextual_window_distance, threshold_sim_value, context_vector_size, score_type):
    words_list = remove_duplicates(words_array)
    dates_list = remove_duplicates(dates_array)

    unic_array = words_list + dates_list
    clean_unic_array = remove_duplicates(unic_array)
    # dataframe
    dt = pd.DataFrame(index=clean_unic_array, columns=clean_unic_array)
    # run all words off array's
    for x_axis in clean_unic_array:
        for y_axis in clean_unic_array:
            if x_axis == y_axis:
                # set 1 on dataframe in words that are the same in 2 axis
                dt.at[x_axis, y_axis] = 1
            else:
                px_y, px, py = find_axis_data(inverted_index, x_axis, y_axis, contextual_window_distance, score_type)
                result = dice_calc(px_y, px, py, x_axis, y_axis)
                dt.at[x_axis, y_axis] = result

    #print("\n")
    #print('*********************************************************************')
    #print('************************** Dice Matrix ******************************')
    #print(dt.to_string())
    if score_type.lower() == 'multiple':
       date_sentence_score =  calc_info_simba_per_sentence(dates_list, dt, threshold_sim_value, context_vector_size, inverted_index)
       return date_sentence_score, dt
    else:
        sorted_dict = calc_info_simba(dates_list, words_list, dt, threshold_sim_value, context_vector_size)
        return sorted_dict, dt


# **********************************************************************
# find the position and the frequency of words
def find_axis_data(inverted_index, x_axis, y_axis, contextual_window_distance, score_by_sentence):
    list_x = inverted_index[x_axis]
    list_y = inverted_index[y_axis]
    count = 0
    for key in list_x[2]:
        if key in list_y[2]:
            x_offset = list_x[2][key][1]
            y_offset = list_y[2][key][1]
            if contextual_window_distance == 'none':
                count += 1
            else:
                cc = find_distance_of_words(x_offset, y_offset, contextual_window_distance)
                count += cc
    return count, list_x[0], list_y[0]


# **********************************************************
# verifica se na mesma sentence as palavras estão á distancia defenido pela limit_distance
def find_distance_of_words(x_offset, y_offset, limit_distance):
    value = 0
    for x in range(len(x_offset)):
        for y in range(len(y_offset)):
            if len(x_offset) > len(y_offset):
                try:
                    if -limit_distance <= x_offset[x] - y_offset[value] <= limit_distance:
                        value += 1
                    pass
                except:
                    return value
            else:
                try:
                    if -limit_distance <= x_offset[value] - y_offset[y] <= limit_distance:
                        value += 1
                    pass
                except:
                    return value

    return value


# ******************************************************************************************
# calculation of dice.
def dice_calc(px_y, px, py, x_axis, y_axis):
    try:
        result = (2 * px_y) / (px + py)
    except:
        result = 0
    #print(x_axis, y_axis, 'p('+x_axis+')=', px, 'p('+y_axis+')=', py, 'px_y=', px_y, 'result =', result)
    return result


# ******************************************************************************************
# calculation of info simba.
def calc_info_simba(dates_array, words_array, dt, threshold_sim_value, context_vector_size):
    #print('***************************************************************************')
    #print('*********************** Info simba ****************************************')
    is_vector = {}
    gte_dict = {}
    for dat in dates_array:
        dd_vector = relevant_array(dat, dt, threshold_sim_value)
        x = len(dd_vector)
        max_val_allowed = get_max_len(x, context_vector_size)

        is_vector[dat] = []

        for wor in dd_vector[:max_val_allowed]:
            if dt.loc[dat, wor] > threshold_sim_value and dat != wor:
                ww_vector = relevant_array(wor, dt, threshold_sim_value)
                info_simba_result = find_max_length(dat, wor, dd_vector, ww_vector, dt, max_val_allowed)
                is_vector[dat].append(float('%.3f' % info_simba_result))
        if is_vector[dat] != []:
            gte_dict[dat] = statistics.median(is_vector[dat])
        else:
            gte_dict[dat] = 0
        #print(is_vector)
        #print('\n')
        #print('***************************************************************************')
        #print('************** GTE: Temporal simularity module ****************************')
    sorted_dict = sorted(gte_dict.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_dict


def get_max_len(len_array, context_vector_size):
    if context_vector_size == 'max':
        return len_array
    else:
        return context_vector_size


# ******************************************************************************************
# calculation of info simba per sentence .
def calc_info_simba_per_sentence(dates_array, dt, threshold_sim_value, context_vector_size, inverted_index):
    dict_result = []

    for dat in dates_array:
        dd_vector = relevant_array(dat, dt, threshold_sim_value)
        #print(dat + ' original relevant array ' + str(dd_vector))
        index_array = sentence_index(dat, inverted_index)
        dict_result.append((dat, []))
        for index in index_array:
            info_simba_array = []
         #   print('sentence '+str(index))
            relevant_date_array_by_sentence = define_vector_by_sentence(inverted_index, dd_vector, index)
            for wor in relevant_date_array_by_sentence:
                relevant_word_array_by_sentence = define_word_vector_by_sentence(wor, inverted_index, index, dt,
                                                                                 threshold_sim_value)
                info_simba_result = find_max_length(dat, wor, relevant_date_array_by_sentence, relevant_word_array_by_sentence,
                                             dt, context_vector_size)
                info_simba_array.append(info_simba_result)
            for i in range(len(dict_result)):
                if dict_result[i][0] == dat:
                    try:
                        dict_result[i][1].append((index, float("%.3f" % statistics.median(info_simba_array))))
                    except:
                        dict_result[i][1].append((index, 0))
            #print(dict_result)
          #  print('\n')
    return dict_result


# *******************************************************************************************
# calc the som of dice for the same vector.
def relevant_array(word, dt, threshold_sim_value):
    vector_sim = []
    a = dt.sort_values(by=[word], ascending=False)

    ar1 = a[word] > threshold_sim_value

    # Get ndArray of all column names
    index_names = a[ar1].index.values

    for nm in index_names:
        if nm != word:
            vector_sim.append(nm)
    return vector_sim


# *******************************************************
# discover the max length to calculate the sim of vector
def find_max_length(date, word, date_relevant_array, word_relevant_array, dt, context_vector_size):
    if context_vector_size == 'max':
        if len(date_relevant_array) < len(word_relevant_array):
            max_length = len(date_relevant_array)
            result = calc_sim_vector(word, date, date_relevant_array[:max_length], word_relevant_array[:max_length], dt)
            return result

        else:
            max_length = len(word_relevant_array)
            result = calc_sim_vector(word, date, date_relevant_array[:max_length], word_relevant_array[:max_length], dt)
            return result
    else:

        if context_vector_size > 0 and (len(date_relevant_array) >= context_vector_size <= len(word_relevant_array)):
            # sin in dates_array
            max_length = int(context_vector_size)
            result = calc_sim_vector(word, date, date_relevant_array[:max_length], word_relevant_array[:max_length], dt)
            return result

        elif context_vector_size <= 0 and (len(date_relevant_array) >= len(word_relevant_array)):
            max_length = len(word_relevant_array)
            result = calc_sim_vector(word, date, date_relevant_array[:max_length], word_relevant_array[:max_length], dt)
            return result
        else:
            if len(date_relevant_array) < len(word_relevant_array):
                max_length = len(date_relevant_array)
                result = calc_sim_vector(word, date, date_relevant_array[:max_length], word_relevant_array[:max_length],
                                         dt)
                return result

            else:
                max_length = len(word_relevant_array)
                result = calc_sim_vector(word, date, date_relevant_array[:max_length], word_relevant_array[:max_length],
                                         dt)
                return result


# ****************************************************************************************************
# define a array with sentence index for words and dates. according inverted index
def sentence_index(date, inverted_index):
    sentence_key = inverted_index[date][2].keys()
    sentence_index_array = []
    for n_sentence in sentence_key:
        sentence_index_array.append(n_sentence)
    return sentence_index_array


def define_vector_by_sentence(inverted_index, all_sentences_context_vector, index):
    relevant_array_by_sentence = []
    for n in all_sentences_context_vector:
        word_sim = inverted_index[n][2].keys()
        for n_sentence_word in word_sim:
            if index == n_sentence_word:
                relevant_array_by_sentence.append(n)
    return relevant_array_by_sentence


def define_word_vector_by_sentence(word, inverted_index, index, dataframe, threshold_sim_value):
    ww_vector = relevant_array(word, dataframe, threshold_sim_value)
    #print(word + ' original relevant array ' + str(ww_vector))
    relevant_word_array_by_sentence = define_vector_by_sentence(inverted_index, ww_vector, index)
    return relevant_word_array_by_sentence


# *******************************************************************************************
# calc the sim of dates and word vectors
def calc_sim_vector(word, date, date_ultimate_array, word_ultimate_array, dataframe):
    # calc dates sim vector
    date_vector_result = []
    word_vector_result = []

    #print(date + ' ' + str(date_ultimate_array))
    for dt_x in date_ultimate_array:
        value = dataframe.loc[date, dt_x]
        date_vector_result.append(value)

    #print(date_vector_result)
    # calc words sim vector
    for word_x in word_ultimate_array:
        value = dataframe.loc[word, word_x]
        word_vector_result.append(value)

    #print(word + ' ' + str(word_ultimate_array))
    #print(word_vector_result)
    result = sim_calc(word_vector_result, date_vector_result)
    return result


# ***************************************************************************************
# calc of info-simba
def sim_calc(word_vector_result, date_vector_result):
    # sim for dates array
    sim_date_date = sum([x * y for x in date_vector_result for y in date_vector_result])
    # sim for words array
    sim_word_word = sum([x * y for x in word_vector_result for y in word_vector_result])
    # sim for date word array
    sim_date_word = sum([x * y for x in date_vector_result for y in word_vector_result])

    if sim_date_word <= 0:
        result = 0
    else:
        result = sim_date_word / (sim_date_date + sim_word_word - sim_date_word)
    #print(result)
    #print('\n')
    return result

