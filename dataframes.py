from dictionary import kw_ext
import pandas as pd
import statistics
import operator

# *************************************************
# remove duplicates from words and dates array
def remove_duplicates(string_list):
    return list(dict.fromkeys(string_list))


def dt_frames(dictionary, words_array, dates_array,  window, threshold, max_array_len):
    print("\n")
    print("***************************************************")
    print('*************** DataFrame *************************')
    words_list = remove_duplicates(words_array)
    dates_list = remove_duplicates(dates_array)
    unic_array = words_array + dates_array
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
                px_y, px, py = find_axis_data(dictionary, x_axis, y_axis, window)
                result = dice_calc(px_y, px, py, x_axis, y_axis)
                dt.at[x_axis, y_axis] = result
    print("\n")
    print('*********************************************************************')
    print('************************** Dice Matrix ******************************')
    print(dt.to_string())
    calc_info_simba(dates_list, words_list, dt, threshold, max_array_len)


# **********************************************************************
# find the position and the frequency of words
def find_axis_data(dictionary, x_axis, y_axis, window):
    list_x = dictionary[x_axis]
    list_y = dictionary[y_axis]
    count = 0
    for key in list_x[2]:
        if key in list_y[2]:
            x_offset = list_x[2][key][1]
            y_offset = list_y[2][key][1]
            cc = find_distance_of_words(x_offset, y_offset, window)
            count += cc
    return count, list_x[0], list_y[0]


# **********************************************************
# verifica se na mesma sentence as palavras estão á distancia defenido pela window
def find_distance_of_words(x_offset, y_offset, window):
    for x in x_offset:
        for y in y_offset:
            if -window <= x - y <= window:
                return 1
    return 0


# ******************************************************************************************
# calculation of dice.
def dice_calc(px_y, px, py, x_axis, y_axis):
    if px_y == 0:
        result = 0
    else:
        result = (2*px_y)/(px+py)
    print(x_axis, y_axis,'px=', px, 'py=', py , 'px_y=', px_y, 'result =', result)
    return result


# ******************************************************************************************
# calculation of dice.
def calc_info_simba(dates_array, words_array, dt, thrahold, max_array_len):
    print('***************************************************************************')
    print('*********************** Info simba ****************************************')
    is_vector = {}
    gte_dict = {}

    for dat in dates_array:
        dd_vector = relevant_array(dat, dt, thrahold)
        is_vector[dat] = []
        for wor in words_array:
            if dt.loc[dat,wor] > 0:
                ww_vector = relevant_array(wor, dt, thrahold)
                dates_result, words_result, dates_words_result = find_max_length(dat, wor, dd_vector, ww_vector, dt, max_array_len)
                calc = calc_is(dates_result, words_result, dates_words_result)

                is_vector[dat].append(calc)
        try :
            gte_dict[dat] = statistics.median(is_vector[dat])
        except ValueError:
            pass
    print(is_vector)
    print('\n')
    print('***************************************************************************')
    print('************** GTE: Temporal simularity module ****************************')
    sorted_dict = sorted(gte_dict.items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_dict)


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
    if max_array_length > 0 and (len(date_relevant_array) > max_array_length < len(word_relevant_array)):
        # sin in dates_array
        max_length = max_array_length
        dates_result, words_result = calc_sim_vector(date_relevant_array[:max_length], word_relevant_array[:max_length], dt)
        dates_words_result = sim_word_date_vector(date, word, dates_result, words_result, date_relevant_array[:max_length], word_relevant_array[:max_length],dt)

    elif max_array_length <= 0 and (len(date_relevant_array) >= len(word_relevant_array)):
        max_length = len(word_relevant_array)
        dates_result, words_result = calc_sim_vector(date_relevant_array[:max_length], word_relevant_array[:max_length], dt)
        dates_words_result = sim_word_date_vector(date, word, dates_result, words_result, date_relevant_array[:max_length], word_relevant_array[:max_length],dt)

    else:
        max_length = len(date_relevant_array)
        dates_result, words_result = calc_sim_vector(date_relevant_array[:max_length], word_relevant_array[:max_length], dt)
        dates_words_result = sim_word_date_vector(date, word, dates_result, words_result, date_relevant_array[:max_length], word_relevant_array[:max_length],dt)

    return dates_result, words_result, dates_words_result


# *******************************************************************************************
# calc the sim of dates and word vectors
def calc_sim_vector(date_ultimate_array, word_ultimate_array, dataframe):
    # calc dates sim vector
    date_vector_result = 0
    word_vector_result = 0
    for dt_x in date_ultimate_array:
        for dt_y in date_ultimate_array:
            value = dataframe.loc[dt_x, dt_y]
            date_vector_result += value

    # calc words sim vector
    for word_x in word_ultimate_array:
        for word_y in word_ultimate_array:
            value = dataframe.loc[word_x, word_y]
            word_vector_result += value
    return date_vector_result, word_vector_result


# *******************************************************************************************
# calc the sim of dates with word vectors
def sim_word_date_vector(date, word, date_result, word_result, date_ultimate_array, word_ultimate_array, dataframe):
    date_word_result = 0
    print(date, '=>', date_ultimate_array, 'result= ', date_result)
    print(word, '=>', word_ultimate_array, 'result= ', word_result)
    for dt in date_ultimate_array:
        for word in word_ultimate_array:
            value = dataframe.loc[dt, word]
            date_word_result += value
    print('total= ', date_word_result)
    return date_word_result


# *******************************************************************************************
# calc the similarity of dates with relevant words
def calc_is(dates_result, words_result, dates_words_result):
    if dates_words_result <= 0:
        result = 0
    else:
        result = dates_words_result/(dates_result+words_result-dates_words_result)
    return result

