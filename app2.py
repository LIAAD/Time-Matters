text= '90 years "ages 16 to 90 years. 2011 this is knowlege Haiti 2010-01-12 Earthquake 2010-01-12 Anniversary. As of 2010 (see 1500 photos here), the following major earthquakes '\
    "have nowly been recorded in Haiti. (2000), The first great earthquake mentioned in histories of Haiti occurred in "\
    "1564 in what was still the Spanish colony. It destroyed Concepción de la Vega. On January 12, 2010, "\
    "a massive earthquake struck the nation of Haiti, causing catastrophic damage inside and around the "\
    "capital  city of Port-au-Prince. On the first anniversary of the earthquake, 12 January 2011, "\
    "Haitian Prime Minister Jean-Max Bellerive said the death toll from the quake in 2010 was more "\
    "than 316,000, raising the figures in 2010 from previous estimates. I immediately flashed back to the afternoon "\
    "of February 11, 1975 when, on my car radio, I first heard the news. 2010-01-12 Yesterday..."

from Time_Matters_SingleDoc import Time_Matters_SingleDoc


t_file = open('text.txt')
txt = t_file.read()
#n_txt, NormalizedText, final_score_output, candidate_dates_dictionary, normalized_candidate_date_dictionary, words_array, inverted_index, DiceMatrix, execution_time_list = Time_Matters_SingleDoc(txt, temporal_tagger=['py_heideltime'], time_matters=[10, 'full_sentence', 'max'], score_type='ByDoc', debug_mode=False)

Time_Matters_SingleDoc(txt, temporal_tagger=['rule_based'], time_matters=[10,   'full_sentence', 'max'], score_type='BySentence', debug_mode=True)


#print(n_txt)
#print('\n')
#print(NormalizedText)
#print(final_score_output)
#print(candidate_dates_dictionary)
#print(normalized_candidate_date_dictionary)
#print(words_array)
#print(inverted_index)
#print(DiceMatrix)
#print(execution_time_list)



# {'2011': {0: [0.846, [0]]}, '2010-01-12': {0: [0.805, [2, 4]], 7: [0, [118]]}, 'January_12,_2010': {4: [0.8, [48]]}, '2010': {1: [0.0, [8]], 5: [0.943, [89, 98]]}, '1564': {2: [0.836, [33]]}, '12_January_2011': {5: [0.943, [75]]}, 'the_afternoon_of_February_11,_1975': {6: [0, [107]]}, 'Yesterday': {7: [0, [119]]}}
