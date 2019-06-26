import pandas as pd
import statistics
import operator
from itertools import product

# *************************************************
# remove duplicates from words and dates array
def remove_duplicates(string_list):
    return list(dict.fromkeys(string_list))


def dt_frames(inverted_index, words_array, dates_array, n_contextual_window, TH, N, score_type):
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
                px_y, px, py = find_axis_data(inverted_index, x_axis, y_axis, n_contextual_window)
                result = dice_calc(px_y, px, py, x_axis, y_axis)
                dt.at[x_axis, y_axis] = result

    #print("\n")
    #print('*********************************************************************')
    #print('************************** Dice Matrix ******************************')
    #print(dt.to_string())
    #print('\n')
    if score_type.lower() == 'multiple':
       date_sentence_score =  calc_info_simba_per_sentence(dates_list, dt, TH, N, inverted_index, n_contextual_window)
       return date_sentence_score, dt
    else:
        sorted_dict = calc_info_simba(dates_list, dt, TH, N)
        return sorted_dict, dt


# **********************************************************************
# find the position and the frequency of words
def find_axis_data(inverted_index, x_axis, y_axis, n_contextual_window ):
    list_x = inverted_index[x_axis]
    list_y = inverted_index[y_axis]
    count = 0
    for key in list_x[2]:
        if key in list_y[2]:
            x_offset = list_x[2][key][1]
            y_offset = list_y[2][key][1]
            if n_contextual_window == 'full_sentence':
                count += 1
            else:
                cc = find_distance_of_words(x_offset, y_offset, n_contextual_window)
                count += cc
    return count, list_x[0], list_y[0]


# **********************************************************
# verifica se na mesma sentence as palavras estão á distancia defenido pela limit_distance
def find_distance_of_words(x_offset, y_offset, n_contextual_window):
    value = 0

    for x, y in product(range(len(x_offset)), range(len(y_offset))):
        try:
            if -n_contextual_window <= x_offset[x] - y_offset[y] <= n_contextual_window:
                return 1
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
def calc_info_simba(dates_array, dt, TH, N):
    #print('***************************************************************************')
    #print('*********************** Info simba ****************************************')
    is_vector = {}
    gte_dict = {}
    for dat in dates_array:
        dd_vector = relevant_array(dat, dt, TH)
        x = len(dd_vector)
        max_val_allowed = get_max_len(x, N)

        is_vector[dat] = []

        for wor in dd_vector[:max_val_allowed]:
            if dt.loc[dat, wor] > TH and dat != wor:
                ww_vector = relevant_array(wor, dt, TH)
                info_simba_result = find_max_length(dat, wor, dd_vector, ww_vector, dt, max_val_allowed)
                is_vector[dat].append(float('%.3f' % info_simba_result))
        if is_vector[dat] != []:
            gte_dict[dat] = statistics.median(is_vector[dat])
        else:
            gte_dict[dat] = 0
        #print(is_vector)
        #sprint(gte_dict)
        #print('\n')
        #print('***************************************************************************')
        #print('************** GTE: Temporal simularity module ****************************')
    sorted_dict = sorted(gte_dict.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_dict


def get_max_len(len_array, N):
    if N == 'max':
        return len_array
    else:
        return N


# ******************************************************************************************
# calculation of info simba per sentence .
def calc_info_simba_per_sentence(dates_array, dt, TH, N, inverted_index, n_contextual_window):
    dict_result = []

    for dat in dates_array:
        dd_vector = relevant_array(dat, dt, TH)
        #print(dat + ' original relevant array ' + str(dd_vector))
        index_array = sentence_index(dat, inverted_index)
        dict_result.append((dat, []))
        for index in index_array:
            info_simba_array = []
            #print('sentence '+str(index))
            relevant_date_array_by_sentence = define_vector_by_sentence(inverted_index, dd_vector, index, dat, n_contextual_window)
            for wor in relevant_date_array_by_sentence:
                relevant_word_array_by_sentence = define_word_vector_by_sentence(wor, inverted_index, index, dt,
                                                                                 TH, dat, n_contextual_window)
                info_simba_result = find_max_length(dat, wor, relevant_date_array_by_sentence, relevant_word_array_by_sentence,
                                             dt, N)
                info_simba_array.append(info_simba_result)
            for i in range(len(dict_result)):
                if dict_result[i][0] == dat:
                    try:
                        dict_result[i][1].append((index, float("%.3f" % statistics.median(info_simba_array))))
                    except:
                        dict_result[i][1].append((index, 0))
    return dict_result


# *******************************************************************************************
# calc the som of dice for the same vector.
def relevant_array(word, dt, TH):
    vector_sim = []
    a = dt.sort_values(by=[word], ascending=False)

    ar1 = a[word] > TH

    # Get ndArray of all column names
    index_names = a[ar1].index.values

    for nm in index_names:
        if nm != word:
            vector_sim.append(nm)
    return vector_sim


# *******************************************************
# discover the max length to calculate the sim of vector
def find_max_length(date, word, date_relevant_array, word_relevant_array, dt, N):
    if N == 'max':
        if len(date_relevant_array) < len(word_relevant_array):
            max_length = len(date_relevant_array)
            result = calc_sim_vector(word, date, date_relevant_array[:max_length], word_relevant_array[:max_length], dt)
            return result

        else:
            max_length = len(word_relevant_array)
            result = calc_sim_vector(word, date, date_relevant_array[:max_length], word_relevant_array[:max_length], dt)
            return result
    else:

        if N > 0 and (len(date_relevant_array) >= N <= len(word_relevant_array)):
            # sin in dates_array
            max_length = int(N)
            result = calc_sim_vector(word, date, date_relevant_array[:max_length], word_relevant_array[:max_length], dt)
            return result

        elif N <= 0 and (len(date_relevant_array) >= len(word_relevant_array)):
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


def get_ocorrency(date_offset, word, word_offset, n_contextual_window):
    for d, w in product(date_offset, word_offset):
        if -n_contextual_window <= d - w <= n_contextual_window:
            return word
        else:
            pass
    return ''


def define_word_vector_by_sentence(word, inverted_index, index, dataframe, TH, date, n_contextual_window):
    ww_vector = relevant_array(word, dataframe, TH)
    #print(word + ' original relevant array ' + str(ww_vector))
    relevant_word_array_by_sentence = define_vector_by_sentence(inverted_index, ww_vector, index, date, n_contextual_window)
    return relevant_word_array_by_sentence


# *******************************************************************************************
# calc the sim of dates and word vectors
def calc_sim_vector(word, date, date_ultimate_array, word_ultimate_array, dataframe):
    # calc dates sim vector
    date_vector_result = 0
    word_vector_result = 0
    # calc date sim context vector
    for dt_x, dt_y in product(date_ultimate_array, date_ultimate_array):
        value = dataframe.loc[dt_x, dt_y]
        date_vector_result += value

    # calc words sim context vector
    for word_x, word_y in product(word_ultimate_array, word_ultimate_array):
        value = dataframe.loc[word_x, word_y]
        word_vector_result += value


    date_word_vector_result =  sim_word_date_vector(word, date, date_vector_result, word_vector_result, date_ultimate_array, word_ultimate_array, dataframe)
    result = sim_calc(date_vector_result, word_vector_result , date_word_vector_result)
    return result


# *******************************************************************************************
# calc the sim of dates with word vectors
def sim_word_date_vector(word, date, date_result, word_result, date_ultimate_array, word_ultimate_array, dataframe):
    date_word_result = 0
    #print(date, '=>', date_ultimate_array, 'result= ', date_result)
    #print(word, '=>', word_ultimate_array, 'result= ', word_result)
    for dt , word in product(date_ultimate_array, word_ultimate_array):
        value = dataframe.loc[dt, word]
        date_word_result += value
    #print('('+date+', '+word+')'+' result' , date_word_result)
    return date_word_result


# ***************************************************************************************
# calc of GTE
def sim_calc(date_vector_result, word_vector_result , date_word_vector_result ):

    if date_word_vector_result <= 0:
        result = 0
    else:
        try:
            result = date_word_vector_result / (date_vector_result + word_vector_result - date_word_vector_result)
        except:
            result = 0
    #print(result)
    #print('\n')
    return result

