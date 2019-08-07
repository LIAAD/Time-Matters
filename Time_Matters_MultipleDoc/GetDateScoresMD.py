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
            px_y, px, py = find_axis_data(inverted_index[Term1], inverted_index[Term2], n_contextual_window, score_type)

            result = DICE(px_y, px, py)
            dataframe.at[Term1, Term2] = result
            dataframe.at[Term2, Term1] = result

    dice_exec_time = (time.time() - dice_start_time)
    pd.set_option('display.max_columns', 1000)

    if score_type == 'ByDocSentence':
        gte_start_time = time.time()
        gte_dict = main_info_simba_ByDocSentence(dates_list, words_list, dataframe, TH, N, inverted_index, n_contextual_window)
        gte_exec_time = (time.time() - gte_start_time)
        return gte_dict, dataframe, dice_exec_time, gte_exec_time
    elif score_type == 'ByCorpus':
        gte_start_time = time.time()
        gte_dict = main_info_simba_ByCorpus(dates_list, words_list, dataframe, TH, N)
        gte_exec_time = (time.time() - gte_start_time)
        return gte_dict, dataframe, dice_exec_time, gte_exec_time
    elif score_type == 'ByDoc':
        gte_start_time = time.time()
        gte_dict = main_info_simba_ByDoc(dates_list, words_list, dataframe, TH, N, inverted_index, n_contextual_window)
        gte_exec_time = (time.time() - gte_start_time)
        return gte_dict, dataframe, dice_exec_time, gte_exec_time


# **********************************************************************
# find the position and the frequency of words
def find_axis_data(x_axis, y_axis, n_contextual_window, score_type):

    if score_type == 'ByCorpus':
       pxy, px, py = ByCorpus_find_data(x_axis, y_axis)
    elif score_type == 'ByDoc':
        pxy, px, py = ByDoc_find_data(x_axis, y_axis, n_contextual_window)
    else:
        pxy, px, py = ByDocSentence_find_data(x_axis, y_axis, n_contextual_window)
    return pxy, px, py


def ByCorpus_find_data(x_axis, y_axis):
    count = 0
    for key in x_axis[2]:
        if key in y_axis[2]:
            count += 1

    return count, x_axis[0], y_axis[0]


def ByDoc_find_data(x_axis, y_axis, doc_n_contextual_window):
    count = 0
    sf_x_count = 0
    sf_y_count = 0
    for key in x_axis[2]:
        if key in y_axis[2]:
            if doc_n_contextual_window == 'full_sentence':
                count += 1
                sf_x_count += x_axis[0]
                sf_y_count += y_axis[0]
            else:
                for sentence_key in x_axis[2][key][2][2]:
                    if sentence_key in y_axis[2][key][2][2]:
                        sf_x_count += x_axis[2][key][2][0]
                        sf_y_count += y_axis[2][key][2][0]
                        x_offset = x_axis[2][key][2][2][sentence_key][1]
                        y_offset = y_axis[2][key][2][2][sentence_key][1]
                        # distance value (0 = words does not appears together between n_contextual_window) (1 = words appears together between n_contextual_window)
                        distance_value = distance_of_terms(x_offset, y_offset, doc_n_contextual_window)
                        count += distance_value

    return count, sf_x_count, sf_y_count


def ByDocSentence_find_data(x_axis, y_axis, doc_n_contextual_window):
    count = 0
    sf_x_count = 0
    sf_y_count = 0
    for key in x_axis[2]:
        if key in y_axis[2]:

            for sentence_key in x_axis[2][key][2][2]:
                if sentence_key in y_axis[2][key][2][2]:
                    sf_x_count += x_axis[2][key][2][0]
                    sf_y_count += y_axis[2][key][2][0]
                    if doc_n_contextual_window == 'full_sentence':
                        count += 1
                    else:
                        x_offset = x_axis[2][key][2][2][sentence_key][1]
                        y_offset = y_axis[2][key][2][2][sentence_key][1]
                        # distance value (0 = words does not appears together between n_contextual_window) (1 = words appears together between n_contextual_window)
                        distance_value = distance_of_terms(x_offset, y_offset, doc_n_contextual_window)
                        count += distance_value

    return count, sf_x_count, sf_y_count


# **********************************************************
# verify if a distance between words are according n_contextual_window
def distance_of_terms(x_offset, y_offset, n_contextual_window):
    if any(1 for x  in x_offset for y in y_offset if abs(x - y) <= n_contextual_window) == True:
        value = 1
    else:
        value = 0
    return value


# ******************************************************************************************
# calculation of dice.
def DICE(px_y, px, py):
    try:
        result = (2 * px_y) / (px + py)
    except:
        result = 0
    return result


# ******************************************************************************************
# calculation of info simba.
def main_info_simba_ByCorpus(dates_list, words_list, dataframe, TH, N):
    is_dictionary = {}
    gte_dictionary = {}
    dataframe_dictionary = dataframe.to_dict()

    for date in dates_list:
        is_dictionary[date] = []

        for word in words_list:
            if dataframe.loc[date, word] > TH and word not in dates_list:

                ContextVector_date = Create_ContextualVectorByCorpus(date, dataframe, TH)
                ContextVector_word = Create_ContextualVectorByCorpus(word, dataframe, TH)
                maxLen = max_length(len(ContextVector_date), len(ContextVector_word), N)
                result = InfoSimba(ContextVector_date[:maxLen], ContextVector_word[:maxLen], dataframe_dictionary)

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
    return sorted_gte_dict


# calculation of info simba per Doc .
def main_info_simba_ByDoc(dates_list, words_list, dataframe, TH, N, inverted_index, n_contextual_window):
    gte_dict = {}
    dataframe_dictionary = dataframe.to_dict()
    for date in dates_list:
        gte_dict[date] = {}
        index_array = Doc_index(inverted_index[date][2].keys())
        for index in index_array:
            info_simba_array = []
            for word in words_list:
                    if dataframe.loc[date, word] > TH and word not in dates_list:
                        ContextVector_date = Create_ContextVectorByDoc(date, dataframe, TH, inverted_index, index, n_contextual_window)
                        ContextVector_word = Create_ContextVectorByDoc(word, dataframe, TH, inverted_index, index, n_contextual_window)
                        maxLen = max_length(len(ContextVector_date), len(ContextVector_word), N)
                        result = InfoSimba(ContextVector_date[:maxLen], ContextVector_word[:maxLen], dataframe_dictionary)
                        if result != 0:
                            info_simba_array.append(result)
                    try:
                        rounded_result = round_up(statistics.median(info_simba_array), decimals=3)
                        gte_dict[date][index] = [rounded_result]
                    except:
                        gte_dict[date][index] = [0]

    return gte_dict


# calculation of info simba per Doc .
def main_info_simba_ByDocSentence(dates_list, word_list, dataframe, TH, N, inverted_index, n_contextual_window):
    gte_dict = {}
    dataframe_dictionary = dataframe.to_dict()
    for date in dates_list:
        gte_dict[date] = {}
        index_array = Doc_index(inverted_index[date][2].keys())

        for doc_index in index_array:
            gte_dict[date][doc_index] = {}
            sentence_index_array = Doc_index(inverted_index[date][2][doc_index][2][2].keys())
            for sentence_index in sentence_index_array:
                info_simba_array = []

                for word in word_list:
                    if word not in dates_list and dataframe.loc[date, word] > TH:
                        ContextVector_date = Create_ContextVectorByDocSentence(date, dataframe, TH, inverted_index, doc_index, sentence_index, n_contextual_window)

                        ContextVector_word = Create_ContextVectorByDocSentence(word, dataframe, TH, inverted_index, doc_index, sentence_index, n_contextual_window)

                        maxLen = max_length(len(ContextVector_date), len(ContextVector_word), N)
                        result = InfoSimba(ContextVector_date[:maxLen], ContextVector_word[:maxLen], dataframe_dictionary)

                        if result != 0:
                            info_simba_array.append(result)
                try:
                    rounded_result = round_up(statistics.median(info_simba_array), decimals=3)
                    gte_dict[date][doc_index][sentence_index] = [rounded_result]

                except:
                    gte_dict[date][doc_index][sentence_index] = [0]
    return gte_dict


# ****************************************************************************************************
# define a array with sentence index for words and dates. according inverted index
def Doc_index(sentence_key):
    sentence_index_array = []
    for n_sentence in sentence_key:
        sentence_index_array.append(n_sentence)
    return list(sentence_index_array)


def max_length(lenX, lenY, N):
    if N == "max":
        N = 9999999
    maxLength = min(lenX, lenY, N)
    return maxLength


def Create_ContextualVectorByCorpus(term, DF, TH):

    DF_Filtered = DF[term][DF[term] > TH].sort_values(ascending=False).index.tolist()
    contextVector = [x for x in DF_Filtered if x != term]

    return contextVector


def Create_ContextVectorByDoc(term, DF, TH, inverted_index, index, n_contextual_window):
    DF_Filtered = DF[term][DF[term] > TH].sort_values(ascending=False).index.tolist()
    contextVector = []
    if n_contextual_window != 'full_sentence':
        try:
            for x in DF_Filtered:
                offset_x = inverted_index[x][2][index][1]
                offset_y = inverted_index[term][2][index][1]
                if x != term and distance_of_terms(offset_x, offset_y, n_contextual_window ):
                    contextVector.append(x)
        except:
            pass

        try:
            for i in contextVector:
                term_offset_a = inverted_index[i][2][index][1]
                for k in contextVector[contextVector.index(i)::]:
                    term_offset_b = inverted_index[k][2][index][1]
                    if n_contextual_window != 'full_sentence':
                        if not distance_of_terms(term_offset_a, term_offset_b, n_contextual_window):
                            contextVector.remove(k)
        except:
            pass
    else:
        try:
            contextVector = [x for x in DF_Filtered if x != term and index in inverted_index[term][2] and index in inverted_index[x][2]]
        except:
            pass
    return contextVector


def Create_ContextVectorByDocSentence(term, DF, TH, Inverted_Index, Index, sentence_index, n_contextual_window):
    DF_Filtered = DF[term][DF[term] > TH].sort_values(ascending=False).index.tolist()
    contextVector = []
    for x in DF_Filtered:
        try:
            if n_contextual_window != 'full_sentence':
                offset_x = Inverted_Index[x][2][Index][2][2][sentence_index][1]
                offset_y = Inverted_Index[term][2][Index][2][2][sentence_index][1]
                if x != term and distance_of_terms(offset_x, offset_y, n_contextual_window):
                    contextVector.append(x)
            elif x != term:
                contextVector.append(x)
        except:
            pass
    if n_contextual_window != 'full_sentence':
        try:
            for i in contextVector:
                term_offset_a = Inverted_Index[i][2][Index][2][2][sentence_index][1]
                for k in contextVector[contextVector.index(i)::]:
                    term_offset_b = Inverted_Index[k][2][Index][2][2][sentence_index][1]
                    if not distance_of_terms(term_offset_a, term_offset_b, n_contextual_window):
                        contextVector.remove(k)
        except:
            pass
    return contextVector


# *******************************************************************************************
# calc Info simba
def InfoSimba(ContextVector_X, ContextVector_Y, DF):

    Sum_XY = sum([DF[x][y] for x in ContextVector_X for y in ContextVector_Y])

    Sum_XX = sum([DF[x][y] for x in ContextVector_X for y in ContextVector_X])

    Sum_YY = sum([DF[x][y] for x in ContextVector_Y for y in ContextVector_Y])
    try:
        result = Sum_XY / (Sum_XX + Sum_YY - Sum_XY)
        return result
    except:
        return 0


def get_offset(inverted_index, term, index):
    offset_list = []
    for x in inverted_index[term][2][index][1]:
        offset_list += inverted_index[term][2][x][1]
    return offset_list