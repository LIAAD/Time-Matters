text= "2011 Haiti 2010-01-12 Earthquake 2010-01-12 Anniversary. As of 2010 (see 1500 photos here), the following major earthquakes "\
    "have been recorded in Haiti. The first great earthquake mentioned in histories of Haiti occurred in "\
    "1564 in what was still the Spanish colony. It destroyed Concepción de la Vega. On January 12, 2010, "\
    "a massive earthquake struck the nation of Haiti, causing catastrophic damage inside and around the "\
    "capital  city of Port-au-Prince. On the first anniversary of the earthquake, 12 January 2011"\
    "Haitian Prime Minister Jean-Max Bellerive said the death toll from the quake in 2010 was more "\
    "than 316,000, raising the figures in 2010 from previous estimates. I immediately flashed back to the afternoon "\
    "of February 11, 1975 when, on my car radio, I first heard the news. 2010-01-12 Yesterday..."

from Time_Matters_SingleDoc import Time_Matters_SingleDoc
t_file = open('text.txt')
txt = t_file.read()
output = Time_Matters_SingleDoc(txt, temporal_tagger=['py_heideltime'], time_matters=[10, 'full_sentence', 'max'], score_type='BySentence', debug_mode=True)
print(output)

