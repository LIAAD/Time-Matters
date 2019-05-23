from time_matters.InvertedIndex import kw_ext
from time_matters.GetDateScores import dt_frames
from langdetect import detect
import nltk


def timeMatters(txt, contextual_window_distance=10, threshold=0.05, max_array_len=0, max_keywords=10, analysis_sentence=True, ignore_contextual_window_distance=False, heideltime_document_type='news', heideltime_document_creation_time=''):
    #detect language of the text
    lang = detect(txt)
    dictionary, words_array, dates_array = kw_ext(lang, txt, max_keywords, heideltime_document_type, heideltime_document_creation_time)
    relevant_dates = dt_frames(dictionary, words_array, dates_array, contextual_window_distance, threshold, max_array_len, analysis_sentence,  ignore_contextual_window_distance)

    dates_array_score = []
    for k in range(len(relevant_dates)):
        dates_array_score.append({'Date': relevant_dates[k][0], 'Score': relevant_dates[k][1]})
    return dates_array_score


def timeMattersPerSentence(txt, contextual_window_distance=10, threshold=0.05, max_array_len=0, max_keywords=10, ignore_contextual_window_distance=False, heideltime_document_type='news', heideltime_document_creation_time=''):
    #detect language of the text
    sentences = nltk.sent_tokenize(txt)
    dates_array_score = []
    lang = detect(txt)
    for i in range(len(sentences)):
        dictionary, words_array, dates_array = kw_ext(lang, sentences[i], max_keywords, heideltime_document_type , heideltime_document_creation_time)
        relevant_dates = dt_frames(dictionary, words_array, dates_array, contextual_window_distance, threshold, max_array_len, True, ignore_contextual_window_distance)
        dates_array_score.append({'sentence'+str(i+1): {}})
        for k in range(len(relevant_dates)):
            dates_array_score[i]['sentence'+str(i+1)][k] = ({'Date': relevant_dates[k][0], 'Score': relevant_dates[k][1]})
    return dates_array_score
