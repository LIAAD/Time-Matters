from time_matters.dictionary import kw_ext
from time_matters.dataframes import dt_frames
from langdetect import detect

def timeMatters(txt, window=5, threshold=0.05, max_array_len=0):
    lang = detect(txt)
    dictionary, words_array, dates_array = kw_ext(lang, txt)
    dt_frames(dictionary, words_array, dates_array, window, threshold, max_array_len)
