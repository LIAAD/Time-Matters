from dictionary import kw_ext
from dataframes import dt_frames


def time_matters(txt, window=5, threshold=0.05, max_array_len=0):
    dictionary, words_array, dates_array = kw_ext(txt)
    dt_frames(dictionary, words_array, dates_array, window, threshold, max_array_len)

