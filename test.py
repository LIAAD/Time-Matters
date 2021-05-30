import pytest
from Time_Matters_SingleDoc import Time_Matters_SingleDoc
from Time_Matters_MultipleDocs import Time_Matters_MultipleDocs

def test_SingleDocs_ByDoc_PyHeidelteime_DefaultParams_EN():
    text = '''2011 Haiti Earthquake Anniversary. As of 2010 (see 1500 photos here), the following major earthquakes have been recorded in Haiti. The first great earthquake mentioned in histories of Haiti occurred in 1564 in what was still the Spanish colony. It destroyed Concepción de la Vega. On January 12, 2010, a massive earthquake struck the nation of Haiti, causing catastrophic damage inside and around the capital city of Port-au-Prince. On the first anniversary of the earthquake, 12 January 2011, Haitian Prime Minister Jean-Max Bellerive said the death toll from the quake in 2010 was more than 316,000, raising the figures in 2010 from previous estimates. I immediately flashed back to the afternoon of February 11, 1975 when, on my car radio, I first heard the news. Yesterday...'''

    results = Time_Matters_SingleDoc(text)
    #results = Time_Matters_SingleDoc(text, temporal_tagger=['py_heideltime', 'Portuguese', 'full', 'news', '2014-11-02'], time_matters=[1, 30, 'full_sentence', 'max', 0.05])
    print(results)

    Score = results[0]
    assert Score['2011-01-12'][0] == 1
    assert Score['2010'][0] == 0.983
    assert Score['1564'][0] == 0.799
    assert Score['2010-01-12'][0] == 0.743
    assert Score['2011'][0] == 0.568
    assert Score['1975-02-11taf'][0] == 0
    assert Score['1975-02-10'][0] == 0
    assert Score['1975-02-11taf'][1][0] == 'the afternoon of February 11, 1975'

    RelevantKWs = results[2]
    assert RelevantKWs['Haiti'] == 0.03398184332272179
    assert RelevantKWs['Earthquake'] == 0.057956360194986824
    assert RelevantKWs['Anniversary'] == 0.14196117057440455
    assert RelevantKWs['Spanish'] == 0.2508020526438915
    assert RelevantKWs['Vega'] == 0.27659635792739035
    assert RelevantKWs['Concepción'] == 0.2909058641653513
    assert RelevantKWs['Haitian'] == 0.3243134631520642
    assert RelevantKWs['Prime'] == 0.33993156462789687
    assert RelevantKWs['Minister'] == 0.33993156462789687
    assert RelevantKWs['Bellerive'] == 0.33993156462789687

    TextNormalized = results[3]
    assert TextNormalized == "<d>2011</d> <kw>Haiti</kw> <kw>Earthquake</kw> <kw>Anniversary</kw>. As of <d>2010</d> (see 1500 photos here), the following major earthquakes have been recorded in <kw>Haiti</kw>. The first great <kw>earthquake</kw> mentioned in histories of <kw>Haiti</kw> occurred in <d>1564</d> in what was still the <kw>Spanish</kw> colony. It destroyed <kw>Concepción</kw> de la <kw>Vega</kw>. On <d>2010-01-12</d>, a massive <kw>earthquake</kw> struck the nation of <kw>Haiti</kw>, causing catastrophic damage inside and around the capital city of Port-au-Prince. On the first <kw>anniversary</kw> of the <kw>earthquake</kw>, <d>2011-01-12</d>, <kw>Haitian</kw> <kw>Prime</kw> <kw>Minister</kw> Jean-Max <kw>Bellerive</kw> said the death toll from the quake in <d>2010</d> was more than 316,000, raising the figures in <d>2010</d> from previous estimates. I immediately flashed back to <d>1975-02-11TAF</d> when, on my car radio, I first heard the news. <d>1975-02-10</d>..."

    TextTokens = results[4]
    assert len(TextTokens) == 121
    assert TextTokens[109] == '<d>1975-02-11TAF</d>'
    assert TextTokens[120] == '<d>1975-02-10</d>'

    SentencesNormalized = results[5]
    assert SentencesNormalized[2] == 'The first great <kw>earthquake</kw> mentioned in histories of <kw>Haiti</kw> occurred in <d>1564</d> in what was still the <kw>Spanish</kw> colony.'

    SentencesTokens = results[6]
    assert len(SentencesTokens[0]) == 4
    assert len(SentencesTokens[1]) == 16
    assert len(SentencesTokens[2]) == 19
    assert len(SentencesTokens[3]) == 6
    assert len(SentencesTokens[4]) == 23
    assert len(SentencesTokens[5]) == 36
    assert len(SentencesTokens[6]) == 16
    assert len(SentencesTokens[7]) == 1

def test_SingleDocs_ByDoc_PyHeidelteime_OtherParams_EN():
    text = '''2011 Haiti Earthquake Anniversary. As of 2010 (see 1500 photos here), the following major earthquakes have been recorded in Haiti. The first great earthquake mentioned in histories of Haiti occurred in 1564 in what was still the Spanish colony. It destroyed Concepción de la Vega. On January 12, 2010, a massive earthquake struck the nation of Haiti, causing catastrophic damage inside and around the capital city of Port-au-Prince. On the first anniversary of the earthquake, 12 January 2011, Haitian Prime Minister Jean-Max Bellerive said the death toll from the quake in 2010 was more than 316,000, raising the figures in 2010 from previous estimates. I immediately flashed back to the afternoon of February 11, 1975 when, on my car radio, I first heard the news. Yesterday...'''
    results = Time_Matters_SingleDoc(text, temporal_tagger=['py_heideltime', 'English', 'year', 'news', '2009-01-01'])
    print(results)
    Score = results[0]
    dict_Score = {'2011': [0.981, ['2011', '12 January 2011']],
                 '2010': [0.98, ['2010', 'January 12, 2010', '2010', '2010']],
                 '1564': [0.856, ['1564']],
                 '1975': [0, ['the afternoon of February 11, 1975']],
                 '2008': [0, ['Yesterday']]}

    assert Score == dict_Score

def test_SingleDocs_ByDoc_PyHeidelteime_OtherParams1_EN():
    text = '''2011 Haiti Earthquake Anniversary. As of 2010 (see 1500 photos here), the following major earthquakes have been recorded in Haiti. The first great earthquake mentioned in histories of Haiti occurred in 1564 in what was still the Spanish colony. It destroyed Concepción de la Vega. On January 12, 2010, a massive earthquake struck the nation of Haiti, causing catastrophic damage inside and around the capital city of Port-au-Prince. On the first anniversary of the earthquake, 12 January 2011, Haitian Prime Minister Jean-Max Bellerive said the death toll from the quake in 2010 was more than 316,000, raising the figures in 2010 from previous estimates. I immediately flashed back to the afternoon of February 11, 1975 when, on my car radio, I first heard the news. Yesterday...'''
    results = Time_Matters_SingleDoc(text, time_matters=[3, 20, 'full_sentence', 'max', 0.05])
    print(results)
    Score = results[0]
    dict_Score = {'2011': [1.0, ['2011']],
                 '2011-01-12': [1.0, ['12 January 2011']],
                 '1564': [0.838, ['1564']],
                 '2010-01-12': [0.706, ['January 12, 2010']],
                 '2010': [0.67, ['2010', '2010', '2010']],
                 '1975-02-11taf': [0, ['the afternoon of February 11, 1975']],
                 '1975-02-10': [0, ['Yesterday']]}

    assert Score == dict_Score

def test_SingleDocs_ByDoc_RuleBased_DefaultParams_EN():
    text = '''2011 Haiti Earthquake Anniversary. As of 2010 (see 1500 photos here), the following major earthquakes have been recorded in Haiti. The first great earthquake mentioned in histories of Haiti occurred in 1564 in what was still the Spanish colony. It destroyed Concepción de la Vega. On January 12, 2010, a massive earthquake struck the nation of Haiti, causing catastrophic damage inside and around the capital city of Port-au-Prince. On the first anniversary of the earthquake, 12 January 2011, Haitian Prime Minister Jean-Max Bellerive said the death toll from the quake in 2010 was more than 316,000, raising the figures in 2010 from previous estimates. I immediately flashed back to the afternoon of February 11, 1975 when, on my car radio, I first heard the news. Yesterday...'''
    results = Time_Matters_SingleDoc(text, temporal_tagger=['rule_based'])
    print(results)
    Score = results[0]
    dict_Score = {'2011': [0.981, ['2011', '2011']],
                 '2010': [0.892, ['2010', '2010', '2010', '2010']],
                 '1564': [0.856, ['1564']],
                 '1500': [0.853, ['1500']],
                 '1975': [0, ['1975']]}

    assert Score == dict_Score

def test_SingleDocs_BySentence_PyHeidelteime_DefaultParams_EN():
    text = '''2011 Haiti Earthquake Anniversary. As of 2010 (see 1500 photos here), the following major earthquakes have been recorded in Haiti. The first great earthquake mentioned in histories of Haiti occurred in 1564 in what was still the Spanish colony. It destroyed Concepción de la Vega. On January 12, 2010, a massive earthquake struck the nation of Haiti, causing catastrophic damage inside and around the capital city of Port-au-Prince. On the first anniversary of the earthquake, 12 January 2011, Haitian Prime Minister Jean-Max Bellerive said the death toll from the quake in 2010 was more than 316,000, raising the figures in 2010 from previous estimates. I immediately flashed back to the afternoon of February 11, 1975 when, on my car radio, I first heard the news. Yesterday...'''
    results = Time_Matters_SingleDoc(text, score_type='BySentence')
    print(results)
    Score = results[0]
    dict_Score = {'2011-01-12': {5: [1.0, ['12 January 2011']]},
                 '2010': {1: [0.2, ['2010']], 5: [0.983, ['2010', '2010']]},
                 '2011': {0: [0.831, ['2011']]},
                 '1564': {2: [0.828, ['1564']]},
                 '2010-01-12': {4: [0.68, ['January 12, 2010']]},
                 '1975-02-11taf': {6: [0, ['the afternoon of February 11, 1975']]},
                 '1975-02-10': {7: [0, ['Yesterday']]}}

    assert Score == dict_Score

def test_MultipleDocs_ByCorpus_PyHeidelteime_DefaultParams_EN():
    import os
    path = 'data/MultiDocTexts'
    ListOfDocs = []
    for file in os.listdir(path):
        with open(os.path.join(path, file), 'r') as f:
            txt = f.read()
            ListOfDocs.append(txt)

    results = Time_Matters_MultipleDocs(ListOfDocs, temporal_tagger=['py_heideltime', 'English', 'year', 'news', '2013-04-15'])
    print(results)
    assert(results[0]['2012'][0] == 0.657)
    assert (results[0]['2013'][0] == 0.555)
    assert (results[0]['2014'][0] == 0.488)
    assert (results[0]['2001'][0] == 0.509)
    assert (results[0]['1897'][0] == 0.509)
    assert (results[0]['2010'][0] == 0.459)
    assert (results[0]['2011'][0] == 0.459)
    assert (results[0]['1907'][0] == 0.359)
    assert (results[0]['1958'][0] == 0.359)
    assert (results[0]['1909'][0] == 0.359)
    assert (results[0]['2004'][0] == 0.423)
    assert (results[0]['2016'][0] == 0.249)
    assert (results[0]['2017'][0] == 0.249)
    assert (results[0]['1993'][0] == 0.41)
    assert (results[0]['1995'][0] == 0.41)
    assert (results[0]['2015'][0] == 0.41)
    assert (results[0]['2002'][0] == 0.41)
    assert (results[0]['1994'][0] == 0.332)
    assert (results[0]['1986'][0] == 0.248)
    assert (results[0]['2009'][0] == 0.248)
    assert (results[0]['2006'][0] == 0.248)
    assert (results[0]['1996'][0] == 0.248)

if __name__ == '__main__':
    test_SingleDocs_ByDoc_PyHeidelteime_DefaultParams_EN()
    test_SingleDocs_ByDoc_PyHeidelteime_OtherParams_EN()
    test_SingleDocs_ByDoc_PyHeidelteime_OtherParams1_EN()
    test_SingleDocs_ByDoc_RuleBased_DefaultParams_EN()
    test_SingleDocs_BySentence_PyHeidelteime_DefaultParams_EN()
    #test_MultipleDocs_ByCorpus_PyHeidelteime_DefaultParams_EN()