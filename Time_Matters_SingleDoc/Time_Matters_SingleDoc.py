from Time_Matters_SingleDoc.InvertedIndex import kw_ext
from Time_Matters_SingleDoc.GetDateScores import dt_frames
import nltk
from langdetect import detect


def Time_Matters_SingleDoc(txt, language, contextual_window_distance=10, threshold=0.05, max_array_len=0, max_keywords=10, analysis_sentence=True,
                ignore_contextual_window_distance=False, heideltime_document_type='news', heideltime_document_creation_time='', heideltime_date_granularity='', debug=False):
    yake_lang = detect(txt)
    inverted_index, words_array, dates_array = kw_ext(yake_lang,language, txt, max_keywords, heideltime_document_type, heideltime_document_creation_time, heideltime_date_granularity)
    relevant_dates, DiceMatrix  = dt_frames(inverted_index, words_array, dates_array, contextual_window_distance, threshold, max_array_len, analysis_sentence,  ignore_contextual_window_distance)

    dates_array_score = []
    for k in range(len(relevant_dates)):
        dates_array_score.append((relevant_dates[k][0], relevant_dates[k][1]))
    final_score_output = get_final_output(inverted_index, dates_array_score)
    if debug:
        return final_score_output, dates_array, words_array, inverted_index, DiceMatrix
    else:
        return final_score_output


def Time_Matters_SingleDoc_PerSentence(txt, language, contextual_window_distance=10, threshold=0.05, max_array_len=0, max_keywords=10,
                           ignore_contextual_window_distance=False, heideltime_document_type='news', heideltime_document_creation_time='', heideltime_date_granularity=''):
    yake_lang = detect(txt)
    sentences = nltk.sent_tokenize(txt)
    final_score_output = []
    for i in range(len(sentences)):
        dictionary, words_array, dates_array = kw_ext(yake_lang, language, sentences[i], max_keywords, heideltime_document_type , heideltime_document_creation_time, heideltime_date_granularity)
        relevant_dates = dt_frames(dictionary, words_array, dates_array, contextual_window_distance, threshold, max_array_len, True, ignore_contextual_window_distance)

        dates_array_score = get_final_output_sentence(dictionary, relevant_dates, i)
        if dates_array_score:
            final_score_output.append(dates_array_score)
        else:
            pass
    return final_score_output, sentences


def get_final_output(dictionary, list_dates_score):
    final_output= []
    for lt in list_dates_score:
        dict_date_info = (dictionary[lt[0]][2])
        total_offset=[]
        for offset in dict_date_info:
            total_offset += dict_date_info[offset][1]

        final_output.append((lt[0],lt[1],total_offset))
    return final_output


def get_final_output_sentence(dictionary, list_dates_score, sentence_index):
    final_output= []
    for lt in list_dates_score:
        dict_date_info = (dictionary[lt[0]][2])
        total_offset=[]
        for offset in dict_date_info:
            total_offset += dict_date_info[offset][1]

        final_output.append((lt[0], [(sentence_index, lt[1], total_offset)]))
    return final_output
