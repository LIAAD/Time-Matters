from Time_Matters_SingleDoc.InvertedIndex import kw_ext
from Time_Matters_SingleDoc.GetDateScores import dt_frames
import nltk

def Time_Matters_MultipleDoc(listof_docs, language, contextual_window_distance=10, threshold=0.05, max_array_len=0, max_keywords=10,
                           ignore_contextual_window_distance=False, heideltime_document_type='news', heideltime_document_creation_time='', heideltime_date_granularity=''):
    final_score_output = []
    for i in range(len(listof_docs)):
        dictionary, words_array, dates_array = kw_ext(language, listof_docs[i], max_keywords, heideltime_document_type , heideltime_document_creation_time, heideltime_date_granularity)
        relevant_dates = dt_frames(dictionary, words_array, dates_array, contextual_window_distance, threshold, max_array_len, True, ignore_contextual_window_distance)

        dates_array_score = get_final_output_doc(dictionary, relevant_dates, i)
        if dates_array_score:
            final_score_output.append(dates_array_score)
        else:
            pass
    return final_score_output


def get_final_output_doc(dictionary, list_dates_score, sentence_index):
    final_output = []
    for lt in list_dates_score:
        dict_date_info = (dictionary[lt[0]][2])
        total_offset=[]
        for offset in dict_date_info:
            total_offset += dict_date_info[offset][1]

        final_output.append((lt[0], [(sentence_index, lt[1], total_offset)]))
    return final_output

if __name__ == '__main__':
    list_of_docs = ['''The Carnation Revolution (Portuguese: Revolução dos Cravos), also known as the 25th of April (Portuguese: 25 de Abril), was initially a 25 April 1974 military coup in Lisbon which overthrew the authoritarian Estado Novo regime.[1] The revolution began as a coup organised by the Armed Forces Movement (Portuguese: Movimento das Forças Armadas, MFA), composed of military officers who opposed the regime, but it was soon coupled with an unanticipated, popular civil resistance campaign. The revolution led to the fall of the Estado Novo, the end of 48 years of authoritarian rule in Portugal, and Portugal's withdrawal from its African colonies.''',
                    '''Thurs August 31st - News today that they are beginning to evacuate the London children tomorrow. Percy is a billeting officer. I can't see that they will be much safer here.''']

    print(Time_Matters_MultipleDoc(list_of_docs, language="English"))

