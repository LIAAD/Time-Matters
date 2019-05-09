import pandas as pd
import statistics
import operator


# *************************************************
# remove duplicates from words and dates array
def remove_duplicates(string_list):
    return list(dict.fromkeys(string_list))


def dt_frames(dictionary, words_array, dates_array, limit_distance, threshold, max_array_len, analisys_sentence, ignore_contextual_window_distance):
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
                px_y, px, py = find_axis_data(dictionary, x_axis, y_axis, limit_distance, analisys_sentence, ignore_contextual_window_distance)
                result = dice_calc(px_y, px, py, x_axis, y_axis)
                dt.at[x_axis, y_axis] = result
    print("\n")
    print('*********************************************************************')
    print('************************** Dice Matrix ******************************')
    print(dt.to_string())
    sorted_dict = calc_info_simba(dates_list, words_list, dt, threshold, max_array_len)
    return sorted_dict


# **********************************************************************
# find the position and the frequency of words
def find_axis_data(dictionary, x_axis, y_axis, limit_distance, analisys_sentence, ignore_contextual_window_distance):
    list_x = dictionary[x_axis]
    list_y = dictionary[y_axis]
    count = 0
    x_offset = []
    y_offset = []
    if analisys_sentence:
        for key in list_x[2]:
            if key in list_y[2]:
                x_offset = list_x[2][key][1]
                y_offset = list_y[2][key][1]
                if ignore_contextual_window_distance:
                    count += 1
                else:
                    cc = find_distance_of_words(x_offset, y_offset, limit_distance)
                    count += cc
    else:
        for key_x in list_x[2]:
            x_offset += list_x[2][key_x][1]

        for key_y in list_y[2]:
            y_offset += list_y[2][key_y][1]
        # print('x_offset ', x_offset)
        # print('y_offset ', y_offset)
        cc = find_distance_of_words(x_offset, y_offset, limit_distance)
        count += cc
    return count, list_x[1], list_y[1]


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
    # print(x_axis, y_axis, 'px=', px, 'py=', py, 'px_y=', px_y, 'result =', result)
    return result


# ******************************************************************************************
# calculation of dice.
def calc_info_simba(dates_array, words_array, dt, thrahold, max_array_len):
    # print('***************************************************************************')
    # print('*********************** Info simba ****************************************')
    is_vector = {}
    gte_dict = {}

    for dat in dates_array:
        dd_vector = relevant_array(dat, dt, thrahold)
        is_vector[dat] = []
        for wor in words_array:
            if dt.loc[dat, wor] > thrahold:
                ww_vector = relevant_array(wor, dt, thrahold)
                info_simba_result = find_max_length(dat, wor, dd_vector, ww_vector, dt, max_array_len)
                is_vector[dat].append(info_simba_result)
        try:
            if is_vector[dat] != []:
                gte_dict[dat] = statistics.median(is_vector[dat])
            else:
                gte_dict[dat] = 0
        except ValueError:
            pass
    #print(is_vector)
    print('\n')
    print('***************************************************************************')
    print('************** GTE: Temporal simularity module ****************************')
    sorted_dict = sorted(gte_dict.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_dict


# *******************************************************************************************
# calc the som of dice for the same vector.
def relevant_array(word, dt, thrahold):
    vector_sim = []
    a = dt.sort_values(by=[word], ascending=False)
    ar1 = a[word] > thrahold
    result = 0
    # Get ndArray of all column names
    index_names = a[ar1].index.values

    for nm in index_names:
        if nm != word:
            vector_sim.append(nm)
    return vector_sim


# *******************************************************
# discover the max length to calculate the sim of vector
def find_max_length(date, word, date_relevant_array, word_relevant_array, dt, max_array_length):
    if max_array_length > 0 and (len(date_relevant_array) >= max_array_length <= len(word_relevant_array)):
        # sin in dates_array
        max_length = max_array_length
        result = calc_sim_vector(word, date, date_relevant_array[:max_length], word_relevant_array[:max_length], dt)

    elif max_array_length <= 0 and (len(date_relevant_array) >= len(word_relevant_array)):
        max_length = len(word_relevant_array)
        result = calc_sim_vector(word, date, date_relevant_array[:max_length], word_relevant_array[:max_length], dt)

    else:
        if len(date_relevant_array) < len(word_relevant_array):
            max_length = len(date_relevant_array)
            result = calc_sim_vector(word, date, date_relevant_array[:max_length],word_relevant_array[:max_length], dt)

        else:
            max_length = len(word_relevant_array)
            result = calc_sim_vector(word, date, date_relevant_array[:max_length], word_relevant_array[:max_length], dt)

    return result


# *******************************************************************************************
# calc the sim of dates and word vectors
def calc_sim_vector(word, date, date_ultimate_array, word_ultimate_array, dataframe):
    # calc dates sim vector
    date_vector_result = []
    word_vector_result = []

    for dt_x in date_ultimate_array:
        value = dataframe.loc[date, dt_x]
        date_vector_result.append(value)

    # calc words sim vector
    for word_x in word_ultimate_array:
        value = dataframe.loc[word, word_x]
        word_vector_result.append(value)

    result = sim_calc(word, date, word_vector_result, date_vector_result)
    return result


def sim_calc(word, date, word_vector_result, date_vector_result):
    # sim for dates array
    sim_date_date = sum([x * y for x in date_vector_result for y in date_vector_result])
    # sim for words array
    sim_word_word = sum([x * y for x in word_vector_result for y in word_vector_result])
    # sim for date word array
    sim_date_word = sum([x * y for x in date_vector_result for y in word_vector_result])

    #print(word, '=>', word_vector_result, 'Result= ', sim_word_word)
    #print(date, '=>', date_vector_result, 'Result= ', sim_date_date)
    #print('result= ', sim_date_word)

    if sim_date_word <= 0:
        result = 0
    else:
        result = sim_date_word / (sim_date_date + sim_word_word - sim_date_word)
     # print(result)
    return result

