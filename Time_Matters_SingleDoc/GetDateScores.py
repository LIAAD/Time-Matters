import pandas as pd
import statistics
import operator
from itertools import product
import time


# *************************************************
# remove duplicates from words and dates array
def remove_duplicates(string_list):
    return list(dict.fromkeys(string_list))


def dt_frames(inverted_index, words_array, dates_array, n_contextual_window, TH, N, score_type):
    words_list = remove_duplicates(words_array)
    dates_list = remove_duplicates(dates_array)

    unic_array = words_list + dates_list
    clean_unic_array = remove_duplicates(unic_array)

    dice_start_time = time.time()
    # dataframe
    dt = pd.DataFrame(index=clean_unic_array, columns=clean_unic_array)
    # run all words off array's
    for i in range(0, len(clean_unic_array)):
        Term1 = clean_unic_array[i]
        dt.at[Term1, Term1] = 1
        for j in range(i+1, len(clean_unic_array)):
            Term2 = clean_unic_array[j]
            px_y, px, py = find_axis_data(inverted_index[Term1], inverted_index[Term2], n_contextual_window)
            result = dice_calc(px_y, px, py, Term1, Term2)
            dt.at[Term1, Term2] = result
            dt.at[Term2, Term1] = result

    dice_exec_time = (time.time() - dice_start_time)
    #print("\n")
    #print('*********************************************************************')
    #print('************************** Dice Matrix ******************************')
    #print(dt.to_string())
    #print('\n')
    if score_type == 'BySentence':
        gte_start_time = time.time()
        date_sentence_score = calc_info_simba_per_sentence(dates_list, dt, TH, N, inverted_index, n_contextual_window)
        gte_exec_time = (time.time() - gte_start_time)
        return date_sentence_score, dt, dice_exec_time, gte_exec_time
    else:
        gte_start_time = time.time()
        sorted_dict = calc_info_simba(dates_list, dt, TH, N, words_list)
        gte_exec_time = (time.time() - gte_start_time)
        return sorted_dict, dt, dice_exec_time, gte_exec_time


# **********************************************************************
# find the position and the frequency of words
def find_axis_data(x_axis, y_axis, n_contextual_window ):
    count = 0
    for key in x_axis[2]:
        if key in y_axis[2]:
            if n_contextual_window == 'full_sentence':
                count += 1
            else:
                x_offset = x_axis[2][key][1]
                y_offset = y_axis[2][key][1]
                # distance value (0 = words does not appears together between n_contextual_window) (1 = words appears together between n_contextual_window)
                distance_value = find_distance_of_words(x_offset, y_offset, n_contextual_window)
                x_axis += distance_value
    return count, x_axis[0], y_axis[0]


# **********************************************************
# verify if a distance between words are according n_contextual_window
def find_distance_of_words(x_offset, y_offset, n_contextual_window):
    if any(1 for x in x_offset for y in y_offset if abs(x - y) < n_contextual_window) == True:
        value = 1
    else:
        value = 0
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
def calc_info_simba(dates_array, dt, TH, N, words_list):
    #print('***************************************************************************')
    #print('*********************** Info simba ****************************************')
    is_vector = {}
    gte_dict = {}
    for dat in dates_array:
        dd_vector = relevant_array(dat, dt, TH, dates_array)
        #print(dat)
        #print(dd_vector)
        x = len(dd_vector)
        max_val_allowed = get_max_len(x, N)

        is_vector[dat] = []

        for wor in dd_vector[:max_val_allowed]:
            if dt.loc[dat, wor] > TH and dat != wor:
                ww_vector = relevant_array(wor, dt, TH, dates_array)
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
    #sorted_dict = sorted(gte_dict.items(), key=lambda kv: kv[1])
    return sorted_dict


def get_max_len(len_array, N):
    if N == 'max':
        return len_array
    elif isinstance(N, int):
        return N
    else:
        print('The value of N are not valid\n'
              'options:\n'
              '     max;\n'
              '     number(integer);')
        return exit(1)


# calculation of info simba per sentence .
def calc_info_simba_per_sentence(dates_array, dt, TH, N, inverted_index, n_contextual_window):
    dict_result = {}

    for dat in dates_array:
        dd_vector = relevant_array(dat, dt, TH, dates_array)
        #print(dat)
        #print(dat + ' original relevant array ' + str(dd_vector))
        index_array = sentence_index(dat, inverted_index)
        dict_result[dat] = {}
        for index in index_array:
            info_simba_array = []
            #print('sentence '+str(index))
            relevant_date_array_by_sentence = define_vector_by_sentence(inverted_index, dd_vector, index, dat, n_contextual_window)
            for wor in relevant_date_array_by_sentence:
                relevant_word_array_by_sentence = define_word_vector_by_sentence(wor, inverted_index, index, dt,
                                                                                 TH, dat, n_contextual_window, dates_array)
                info_simba_result = find_max_length(dat, wor, relevant_date_array_by_sentence, relevant_word_array_by_sentence,
                                             dt, N)
                info_simba_array.append(info_simba_result)
            for i in range(len(dict_result)):
                    try:
                        dict_result[dat][index] = [float("%.3f" % statistics.median(info_simba_array))]
                    except:
                        dict_result[dat][index] = [0]
    return dict_result


# ***********************************************************************************
# calc the som of dice for the same vector.
def relevant_array(word, dt, TH, dates_list):
    sorted_vector = dt.sort_values(by=[word], ascending=False)

    filter_low_dice_score = sorted_vector[word] > TH

    # Get ndArray of all column names
    index_names = sorted_vector[filter_low_dice_score].index.values
    vector_sim = [w for w in index_names if w != word and w not in dates_list]

    return vector_sim


# *******************************************************
# discover the max length to calculate the sim of vector
def find_max_length(date, word, date_relevant_array, word_relevant_array, dt, N):
    if N == 'max':
        if len(date_relevant_array) < len(word_relevant_array):
            max_length = len(date_relevant_array)
            result = IS(date_relevant_array[:max_length], word_relevant_array[:max_length], dt)
            return result

        else:
            max_length = len(word_relevant_array)
            result = IS(date_relevant_array[:max_length], word_relevant_array[:max_length], dt)
            return result
    else:

        if N > 0 and (len(date_relevant_array) >= N <= len(word_relevant_array)):
            # sin in dates_array
            max_length = int(N)
            result = IS(date_relevant_array[:max_length], word_relevant_array[:max_length], dt)
            return result

        elif N <= 0 and (len(date_relevant_array) >= len(word_relevant_array)):
            max_length = len(word_relevant_array)
            result = IS(date_relevant_array[:max_length], word_relevant_array[:max_length], dt)
            return result
        else:
            if len(date_relevant_array) < len(word_relevant_array):
                max_length = len(date_relevant_array)
                result = IS(date_relevant_array[:max_length], word_relevant_array[:max_length],
                                         dt)
                return result

            else:
                max_length = len(word_relevant_array)
                result = IS(date_relevant_array[:max_length], word_relevant_array[:max_length],
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


def define_vector_by_sentence(inverted_index, all_sentences_context_vector, index, date, n_contextual_window):
    relevant_array_by_sentence = []
    #print(date+' '+str(inverted_index[date][2][index][1]))
    #print('\n')
    date_offset = inverted_index[date][2][index][1]
    for word in all_sentences_context_vector:
        word_sim = inverted_index[word][2].keys()
        for n_sentence_word in word_sim:
            if index == n_sentence_word and n_contextual_window == 'full_sentence':
                relevant_array_by_sentence.append(word)
            elif index == n_sentence_word and n_contextual_window != 'full_sentence':
                #print(word+' '+str(inverted_index[word][2][index][1]))
                word_offset = inverted_index[word][2][index][1]
                verified_word = get_ocorrency(date_offset, word, word_offset ,n_contextual_window)
                if verified_word != '':
                    relevant_array_by_sentence.append(verified_word)

    #print('\n')
    return relevant_array_by_sentence


def get_ocorrency(y_offset, word, x_offset, n_contextual_window):
    if any(1 for x in x_offset for y in y_offset if abs(x - y) < n_contextual_window) == True:
        return word
    else:
        pass
    return ''


def define_word_vector_by_sentence(word, inverted_index, index, dataframe, TH, date, n_contextual_window, dates_list):
    ww_vector = relevant_array(word, dataframe, TH, dates_list)
    #print(word + ' original relevant array ' + str(ww_vector))
    relevant_word_array_by_sentence = define_vector_by_sentence(inverted_index, ww_vector, index, date, n_contextual_window)
    return relevant_word_array_by_sentence


# *******************************************************************************************
# calc Info simba
def IS(ContextVector_X, ContextVector_Y, dataframe):

    Sum_YY = sum([dataframe.loc[x, y] for x in ContextVector_Y for y in ContextVector_Y])

    Sum_XY = sum([dataframe.loc[x, y] for x in ContextVector_X for y in ContextVector_Y])

    Sum_XX = sum([dataframe.loc[x, y] for x in ContextVector_X for y in ContextVector_X])
    try:
        result = Sum_XY / (Sum_XX + Sum_YY - Sum_XY)
        return result
    except:
        return 0
