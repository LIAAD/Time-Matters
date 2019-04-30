#from time_matters.InvertedIndex import kw_ext
#from time_matters.GetDateScores import dt_frames
from langdetect import detect
from InvertedIndex import kw_ext
from GetDateScores import dt_frames
import nltk


def timeMatters(txt, contextual_window_distance=10, threshold=0.05, max_array_len=0, max_keywords=10, analysis_sentence=True):
    #detect language of the text
    lang = detect(txt)
    dictionary, words_array, dates_array = kw_ext(lang, txt, max_keywords)
    relevant_dates = dt_frames(dictionary, words_array, dates_array, contextual_window_distance, threshold, max_array_len, analysis_sentence)

    output = []
    for k in range(len(relevant_dates)):
        output.append({'Date': relevant_dates[k][0], 'Score': relevant_dates[k][1]})
    return output


def timeMattersPerSentence(txt, contextual_window_distance=10, threshold=0.05, max_array_len=0, max_keywords=10, analysis_sentence=True):
    #detect language of the text
    sentences = nltk.sent_tokenize(text)
    output = []
    lang = detect(text)
    for i in range(len(sentences)):
        dictionary, words_array, dates_array = kw_ext(lang, sentences[i], max_keywords)
        relevant_dates = dt_frames(dictionary, words_array, dates_array, contextual_window_distance, threshold, max_array_len, analysis_sentence)
        string = "sentence " + str(i + 1)
        for k in range(len(relevant_dates)):
            output.append({'Sentence '+str(i+1): {'Date': relevant_dates[k][0], 'Score': relevant_dates[k][1]}})
    return output


if __name__ == '__main__':
    text = '''
In 2005, Lev Grossman of Lev Time called Martin "the American Tolkien", and in 2011, he was included on the annual Time Lev 100 list of the most influential people in the world.
Born in 1948, fantasy writer George R. R. Martin Lev grew up in Bayonne, New Jersey. He developed a love for writing early on. His first novel, Dying of the Light, debuted in 1977. Iam out of time in 1977.
    '''
    # output = timeMatters(text, analysis_sentence=False, contextual_window_distance=10)
    output = timeMattersPerSentence(text, contextual_window_distance=5, analysis_sentence=True, max_array_len=3)
    print(output)