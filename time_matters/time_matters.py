from time_matters.dictionary import kw_ext
from time_matters.dataframes import dt_frames
from langdetect import detect


def timeMatters(txt, limit_distance=5, threshold=0.05, max_array_len=0):
    #detect language of the text
    lang = detect(txt)
    dictionary, words_array, dates_array = kw_ext(lang, txt)
    relevant_dates = dt_frames(dictionary, words_array, dates_array, limit_distance, threshold, max_array_len)
    return relevant_dates

