from dictionary import  kw_ext
import pandas as pd
import statistics

def dt_frames(dictionary, words_array, dates_array):
    print("\n")
    print("***************************************************")
    print('*************** DataFrame *************************')
    unic_array = words_array + dates_array
    dt = pd.DataFrame(index=unic_array, columns=unic_array)
    for x_axis in unic_array:
        for y_axis in unic_array:
            if x_axis == y_axis:
               dt.at[x_axis, y_axis] = 1
            else:
                x_total_freq, x_total_offset = find_axis_data(dictionary, x_axis)
                y_total_freq, y_total_offset = find_axis_data(dictionary, y_axis)
                result = dice_calc(x_total_freq, x_total_offset, y_total_freq, y_total_offset, x_axis, y_axis)
                dt.at[x_axis, y_axis] = result
    print("\n")
    print('*********************************************************************')
    print('************************** Dice Matrix ******************************')
    print(dt)
    calc_info_simba(dates_array, words_array, dictionary, dt, unic_array)


def find_axis_data(dictionary, axis):
    list = dictionary[axis]
    all_pos = []
    for key in list[2]:
        all_pos += list[2][key][1]
    return list[1], all_pos

def dice_calc(x_total_freq, x_total_offset, y_total_freq, y_total_offset, x_axis, y_axis):

    px = x_total_freq
    py = y_total_freq

    cont = 0
    for x in x_total_offset:
        for y in y_total_offset:
            if x - y <= 5 and x - y >= -5:
                cont += 1
    px_y = cont
    result = (2*px_y)/(px+py)
    print(x_axis, y_axis,'px=', px, 'py=', py , 'px_y=', px_y, 'result =',result)
    return result


def  calc_info_simba(dates_array, words_array, dictionary, dt, unic_array):
    print('***************************************************************************')
    print('*********************** Info simba ****************************************')
    #print(dt.loc[words_array,dates_array])
    is_vector = {}
    gte_dict = {}
    for dat in dates_array:
        dd, dd_vector = som_same_vec(dat, dt)
        is_vector[dat] = []
        for wor in words_array:
            ww, ww_vector = som_same_vec(wor, dt)
            calc = som_dif_vec(dat, wor, dd_vector, ww_vector, dd, ww, dt)
            is_vector[dat].append(calc)
        gte_dict[dat] = statistics.median(is_vector[dat])
        print(is_vector)
    print('\n')
    print('***************************************************************************')
    print('************** GTE: Temporal simularity module ****************************')
    print(gte_dict)

def som_same_vec(word, dt):
    vector_sim = []
    ar1 = dt[word] > 0.5
    result = 0
    # Get ndArray of all column names
    index_names = dt[ar1].index.values
    for nm in index_names:
        if nm != word:
            vector_sim.append(nm)

    for x in vector_sim:
        for xi in vector_sim:
            rowData = dt.loc[x, xi]
            result += rowData
            #print(x, xi, result)

    #print(vector_sim)
    return result, vector_sim


def som_dif_vec(date, word, dd_vector, ww_vector, dd, ww, dt):
    result = 0
    print(date, '->', dd_vector, 'D= ', dd)
    print(word, '->', ww_vector, 'W= ', ww)
    for d in dd_vector:
        for w in ww_vector:
            rowData = dt.loc[d, w]
            result += rowData
            #print(d, w, result)
    #print(result)

    is_calc = result/(dd+ww-result)
    print(is_calc)
    print('\n')
    return is_calc


if __name__ == '__main__':
    f = open('text.txt', 'r')
    message = f.read()
    print(message)
    print('===========================================================================')
    dictionary, words_array, dates_array = kw_ext(message)
    dt_frames(dictionary, words_array, dates_array)
