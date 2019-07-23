import pandas as pd
import statistics
import operator
import time


# *************************************************
# remove duplicates from words and dates array
def remove_duplicates(string_list):
    return list(dict.fromkeys(string_list))

def round_up(n, decimals=0):
    import math
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def GetDataScores(inverted_index, words_array, dates_array, n_contextual_window, TH, N, score_type):
    words_list = remove_duplicates(words_array)
    dates_list = remove_duplicates(dates_array)

    unic_array = words_list + dates_list
    clean_unic_array = remove_duplicates(unic_array)

    dice_start_time = time.time()
    # dataframe
    dataframe = pd.DataFrame(index=clean_unic_array, columns=clean_unic_array)
    # run all words off array's
    for i in range(0, len(clean_unic_array)):
        Term1 = clean_unic_array[i]
        dataframe.at[Term1, Term1] = 1
        for j in range(i+1, len(clean_unic_array)):
            Term2 = clean_unic_array[j]
            px_y, px, py = find_axis_data(inverted_index[Term1], inverted_index[Term2], n_contextual_window)
            result = DICE(px_y, px, py, Term1, Term2)
            dataframe.at[Term1, Term2] = result
            dataframe.at[Term2, Term1] = result

    dice_exec_time = (time.time() - dice_start_time)
    #print("\n")
    #print('*********************************************************************')
    #print('************************** Dice Matrix ******************************')
    print(dataframe.to_string())
    #print('\n')
    if score_type == 'BySentence':
        gte_start_time = time.time()
        gte_dict = main_info_simba_BySentence(dates_list, words_list, dataframe, TH, N, inverted_index, n_contextual_window)
        gte_exec_time = (time.time() - gte_start_time)
        return gte_dict, dataframe, dice_exec_time, gte_exec_time
    else:
        gte_start_time = time.time()
        gte_dict = main_info_simba_ByDoc(dates_list, words_list, dataframe, TH, N)
        gte_exec_time = (time.time() - gte_start_time)
        return gte_dict, dataframe, dice_exec_time, gte_exec_time


# **********************************************************************
# find the position and the frequency of words
def find_axis_data(x_axis, y_axis, doc_n_contextual_window):
    count = 0
    for key in x_axis[2]:
        if key in y_axis[2]:
            if doc_n_contextual_window == 'full_document':
                count += 1
            else:
                x_offset = x_axis[2][key][1]
                y_offset = y_axis[2][key][1]
                # distance value (0 = words does not appears together between n_contextual_window) (1 = words appears together between n_contextual_window)
                distance_value = distance_of_terms(x_offset, y_offset, doc_n_contextual_window)
                count += distance_value
    return count, x_axis[0], y_axis[0]


# **********************************************************
# verify if a distance between words are according n_contextual_window
def distance_of_terms(x_offset, y_offset, n_contextual_window):
    if any(1 for x   in x_offset for y in y_offset if abs(x - y) < n_contextual_window) == True:
        value = 1
    else:
        value = 0
    return value


# ******************************************************************************************
# calculation of dice.
def DICE(px_y, px, py, x_axis, y_axis):
    try:
        result = (2 * px_y) / (px + py)
    except:
        result = 0
    #print(x_axis, y_axis, 'p('+x_axis+')=', px, 'p('+y_axis+')=', py, 'px_y=', px_y, 'result =', result)
    return result


# ******************************************************************************************
# calculation of info simba.
def main_info_simba_ByDoc(dates_list, words_list, dataframe, TH, N):
    is_dictionary = {}
    gte_dictionary = {}
    for date in dates_list:
        is_dictionary[date] = []
        #ContextVector_date = Create_ContextualVector(date, dataframe, TH)

        for word in words_list:
            if dataframe.loc[date, word] > TH and word not in dates_list:
                word_ContextVector = Create_ContextualVector(word, dataframe, TH)
                date_context_vector = Create_ContextualVector(date, dataframe, TH)
                maxLen = max_length(len(date_context_vector), len(word_ContextVector), N)
                #date_context_vector, word_ContextVector = Create_ContextVector(date, word, dataframe, TH, N, score_type, Inverted_Index, False, n_contextual_window)
                result = InfoSimba(date_context_vector[:maxLen], word_ContextVector[:maxLen], dataframe)
                is_dictionary[date].append(result)

        if is_dictionary[date] != []:
            rounded_result = round_up(statistics.median(is_dictionary[date]), decimals=3)
            gte_dictionary[date] = rounded_result
        else:
            gte_dictionary[date] = 0

    sorted_gt = sorted(gte_dictionary.items(), key=operator.itemgetter(1), reverse=True)


    sorted_gte_dict = {}
    for i in sorted_gt:
        sorted_gte_dict[i[0]] = i[1]
    print(sorted_gte_dict)
    return sorted_gte_dict


# calculation of info simba per sentence .
def main_info_simba_BySentence(dates_list, words_list, dataframe, TH, N, inverted_index, n_contextual_window):
    gte_dict = {}

    for date in dates_list:
        gte_dict[date] = {}
        index_array = sentence_index(date, inverted_index)
        for index in index_array:
            info_simba_array = []
            ContextVector_date = Create_ContextVector_ByDoc(date, dataframe, TH, inverted_index, index,
                                                                 n_contextual_window)

            for word in ContextVector_date:
                if word not in dates_list:

                    ContextVector_word = Create_ContextVector_ByDoc(word, dataframe, TH, inverted_index, index, n_contextual_window)

                    maxLen = max_length(len(ContextVector_date), len(ContextVector_word), N)
                    result = InfoSimba(ContextVector_date[:maxLen], ContextVector_word[:maxLen], dataframe)
                    if result != 0:
                        info_simba_array.append(result)
            try:
                rounded_result = round_up(statistics.median(info_simba_array), decimals=3)
                gte_dict[date][index] = [rounded_result]
            except:
                gte_dict[date][index] = [0]

    return gte_dict


# ****************************************************************************************************
# define a array with sentence index for words and dates. according inverted index
def sentence_index(date, inverted_index):
    sentence_key = inverted_index[date][2].keys()
    sentence_index_array = []
    for n_sentence in sentence_key:
        sentence_index_array.append(n_sentence)
    return sentence_index_array


def max_length(lenX, lenY, N):
    if N == "max":
        N = 9999999
    maxLength = min(lenX, lenY, N)
    return maxLength


def Create_ContextualVector(term, DF, TH):
    DF_Filtered = DF[term][DF[term]>TH].sort_values(ascending=False)
    contextVector = [x for x in DF_Filtered.index.tolist() if x != term]
    return contextVector


def Create_ContextVector_ByDoc(term, DF, TH, Inverted_Index, Index, n_contextual_window):
    DF_Filtered = DF[term][DF[term] > TH].sort_values(ascending=False)
    contextVector = []
    for x in DF_Filtered.index.tolist():

        try:
            offset_x = Inverted_Index[x][2][Index]
            offset_y = Inverted_Index[term][2][Index]
            if n_contextual_window != 'full_document':
                if x != term and distance_of_terms(offset_x[1], offset_y[1], n_contextual_window):
                    contextVector.append(x)
            elif x != term:
                contextVector.append(x)
        except:
            pass
    return contextVector


# *******************************************************************************************
# calc Info simba
def InfoSimba(ContextVector_X, ContextVector_Y, DF):
    Sum_XY = sum([DF.loc[x, y] for x in ContextVector_X for y in ContextVector_Y])
    #print(f"sum_XY = {Sum_XY}")

    Sum_XX = sum([DF.loc[x, y] for x in ContextVector_X for y in ContextVector_X])
    #print(f"sum_XX = {Sum_XX}")

    Sum_YY = sum([DF.loc[x, y] for x in ContextVector_Y for y in ContextVector_Y])
    #print(f"sum_YY = {Sum_YY}")

    try:
        result = Sum_XY / (Sum_XX + Sum_YY - Sum_XY)
        #print(f"result = {result}")
        return result
    except:
        return 0