


import codecs
#text_file = codecs.open('dan.txt', "r+", "utf-8").read()

#inal_score_output = Time_Matters_SingleDoc(text, language="English", date_extractor='py_heideltime', debug_mode=False, context_vector_size='Max', score_by_sentence=False)


#print(Time_Matters_SingleDoc(text, temporal_tagger=['rule_based'], time_matters=[10, 'full_sentence', 'max', 0.05], score_type='multiple', debug_mode=False))
#final_score_output = Time_Matters_SingleDoc(text, temporal_tagger=['py_heideltime'], time_matters_parameters=[10, 10, 'max', 0.05], score_type='single', debug_mode=False)


#print(n_txt)

from Time_Matters_MultipleDocs import Time_Matters_MultipleDocs
text= "2011 Haiti Earthquake Anniversary. As of 2010 (see 1500 photos here), the following major earthquakes "\
    "have been recorded in Haiti. The first great earthquake mentioned in histories of Haiti occurred in "\
    "1564 in what was still the Spanish colony. It destroyed Concepción de la Vega. On January 12, 2010, "\
    "a massive earthquake struck the nation of Haiti, causing catastrophic damage inside and around the "\
    "capital city of Port-au-Prince. On the first anniversary of the earthquake, 12 January 2011, "\
    "Haitian Prime Minister Jean-Max Bellerive said the death toll from the quake in 2010 was more "\
    "than 316,000, raising the figures in 2010 from previous estimates. I immediately flashed back to the afternoon "\
    "of February 11, 1975 when, on my car radio, I first heard the news. Yesterday..."

text2 = '''The earthquake hit at 4:53 PM some 15 miles (25 km) southwest of the Haitian capital of Port-au-Prince. The initial shock registered a magnitude of 7.0 and was soon followed by two aftershocks of magnitudes 5.9 and 5.5. More aftershocks occurred in the following days, including another one of magnitude 5.9 that struck on January 20 at Petit Goâve, a town some 35 miles (55 km) west of Port-au-Prince. Haiti had not been hit by an earthquake of such enormity since the 18th century, the closest in force being a 1984 shock of magnitude 6.9. A magnitude-8.0 earthquake had struck the Dominican Republic in 1946.'''

text3 = '''The collapsed buildings defining the landscape of the disaster area came as a consequence of Haiti’s lack of building codes. Without adequate reinforcement, the buildings disintegrated under the force of the quake, killing or trapping their occupants. In Port-au-Prince the cathedral and the National Palace were both heavily damaged, as were the United Nations headquarters, national penitentiary, and parliament building. The city, already beset by a strained and inadequate infrastructure and still recovering from the two tropical storms and two hurricanes of August–September 2008, was ill-equipped to deal with such a disaster. Other affected areas of the country—faced with comparable weaknesses—were similarly unprepared.'''
text4 = '''2010 Haiti earthquake, large-scale earthquake that occurred January 12, 2010, on the West Indian island of Hispaniola, comprising the countries of Haiti and the Dominican Republic. Most severely affected was Haiti, occupying the western third of the island. An exact death toll proved elusive in the ensuing chaos. The Haitian government’s official count was more than 300,000, but other estimates were considerably smaller. Hundreds of thousands of survivors were displaced.'''
text5 = '''2011 several organizations filed claims against the United Nations asking that it take responsibility for the outbreak, install new water and waste-management systems, and compensate those who fell ill or lost relatives to cholera. In December 2012 the UN, while not acknowledging that its troops had been vectors of the disease, announced that it would fund a program proposed by the governments of Haiti and the Dominican Republic to rid Hispaniola of cholera by instituting new sanitation and vaccination measures. Critics noted, however, that the proposed financial scheme for the project hinged largely on previously promised monies not yet in hand. The UN asserted in February 2013 that it would not receive compensation claims related to the outbreak, citing its convention on privileges and immunities. In October 2013 a U.S.-based group, the Institute for Justice and Democracy in Haiti, filed a lawsuit in New York City against the UN, seeking compensation on behalf of Haitians affected by the epidemic. '''
list_of_docs = ['''Trump was born and raised in the New York City borough of Queens and received an economics degree from the Wharton School. 
He took charge of his family's real estate business in 1971, renamed it The Trump Organization, and expanded it from Queens and Brooklyn into Manhattan. 
born The company built or renovated skyscrapers, hotels, casinos, and golf courses. Trump later started various side ventures, mostly by licensing his name. 
He managed the company until his 2017 inauguration. He co-authored several books, including The Art of the Deal. He owned the Miss Universe and Miss USA beauty 
pageants from 1996 to 2015, and he produced and hosted The Apprentice, a reality television show, from 2003 to 2015. Forbes estimates his net worth to be $3.1 billion.''',

                '''Trump entered the 2016 presidential race as a Republican and defeated sixteen candidates in the primaries. Commentators described his political positions 
as populist, protectionist, and nationalist. He was elected president in a surprise victory over Democratic nominee Hillary Clinton, although he lost the popular vote.
[b] He became the oldest and wealthiest person ever to assume the presidency, and the first without prior military or government service. His election and policies have sparked numerous protests. 
Trump has made many false or misleading statements during his campaign and presidency. The statements have been documented by fact-checkers, and the media have widely 
described the phenomenon as unprecedented in American politics. Many of his comments and actions have been characterized as racially charged or racist.
                ''',
                '''Trump During his presidency, Trump ordered a travel ban on citizens from several Muslim-majority countries, 
citing security concerns; after legal challenges, the Supreme Court upheld the policy's third revision. He enacted a tax cut package for individuals and businesses, 
which also rescinded the individual health insurance mandate and allowed oil drilling in the Arctic Refuge. Trump He appointed Neil Gorsuch and Brett Kavanaugh to the Supreme Court. 
In foreign policy, Trump pursued his America First agenda, withdrawing the U.S. from the Trans-Pacific Partnership trade negotiations, the Paris Agreement on climate change, and the Iran nuclear deal.
 He recognized Jerusalem as the capital of Israel; imposed import tariffs on various goods, triggering a trade war with China; and started negotiations with North Korea seeking denuclearization.''',

                '''When Trump was in college from queens 1964 to 1968, he obtained four student draft deferments.
[18][19] In 1966, he was deemed fit for military service based upon a medical examination and in July 1968, a local draft board classified him as eligible to serve. 
However in October 1968, he was given a medical deferment which resulted in a 1-Y classification: "Unqualified for duty except in the case of a national emergency."
[20] Trump said in July 2015 that his medical deferment was due to his "feet"; he "had a bone spur", but said he could not remember which foot was injured. Trump's presidential 
campaign then stated that Trump had bone spurs in both feet.[21]
                ''']
t_file = open('dan.txt').read()
list_of_docs2 = ['''I born at Portugal 2003 2003. played Juventus Born and raised on the Portuguese island of Madeira, Ronaldo was diagnosed with a racing heart at age 15. He underwent an operation to treat his condition, before signing with Champions Manchester United team at age 18 in 2003. 1992''',
                '''As a child, Born Ronaldo played for amateur team Andorinha from 1992 to 1995,[14] where his father was the kit man,[15] ronaldo and later 2003 spent two years with Nacional. Portugal''',
                '''2000 Ronaldo made played his official debut for Juventus in their opening Serie A match on 18 August, a 3–2 away win over Chievo.[289] On 16 September, his fourth appearance for Juventus, he scored his first goal.''']

list_of_docs3 = ['''Manchester United Football Club is a professional football club based in Old Trafford, Greater Manchester, England, that competes in the Premier League, the top flight of English football. Nicknamed "the Red Devils", the club was founded as Newton Heath LYR Football Club in 1878, changed its name to Manchester United in 1902 and moved to its current stadium, Old Trafford, in 1910. Manchester United have won more trophies than any other club in English football,[5][6] with a record 20 League titles, 12 FA Cups, 5 League Cups and a record 21 FA Community Shields. United have also won 3 UEFA Champions Leagues, 1 UEFA Europa League, 1 UEFA Cup Winners' Cup, 1 UEFA Super Cup, 1 Intercontinental Cup and 1 FIFA Club World Cup. In 1998–99, the club became the first in the history of English football to achieve the continental European treble.[7] By winning the UEFA Europa League in 2016–17, they became one of five clubs to have won all three main UEFA club competitions. ''',
'''Manchester United was the highest-earning football club in the world for 2016–17, with an annual revenue of €676.3 million,[11] and the world's 2002–03 most valuable football club in 2018, valued at £3.1 billion.[12] As of June 2015, it is the world's most valuable football brand, estimated to be worth $1.2 billion.[13][14] After being floated on the London Stock Exchange in 1991, the club was purchased by Malcolm Glazer in May 2005 in a deal valuing the club at almost £800 million, after which the company was taken private again, before going public once more in August 2012, when they made an initial public offering on the New York Stock Exchange. Manchester United is one of the most widely supported football clubs in the world,[15][16] and has rivalries with Liverpool, Manchester City, Arsenal and Leeds United. Portugal.''',
'''Manchester United won the 1878 league again in the 1999–2000 and 2000–01 seasons. The team finished third in 2001–02, before regaining the title in 2002–03.[54] They won the 2003 FA Cup, beating Millwall 3–0 in the final at the Millennium Stadium in Cardiff to lift the trophy for a record 11th time''']
list_of_docs4 = [text,  text2, text3, text4, text5]

import os
path = 'text_dir'
ListOfDocs = []
for file in os.listdir (path) :
    with open(os.path.join(path, file),'r') as f:
        txt = f.read()
        ListOfDocs.append(txt)
#for i in range(1, 15):
Score = Time_Matters_MultipleDocs(ListOfDocs, temporal_tagger=['rule_based'], time_matters=[1, 10], score_type='ByDocSentence', debug_mode=True)
#results = Time_Matters_MultipleDocs(ListOfDocs, temporal_tagger=['rule_based'])
print(Score[0])
print('\n')
#print(inverted_index,'\n')
import pandas as pd
pd.set_option('display.max_rows',10000)
print(Score[-1])

#print(ExecTimeDictionary)
#print(TextNormalized)
#print(Score)
#print(all_docs_TempExpressions)
#print(gte_dictionary)
# {'TotalTime': 0.11967992782592773, 'rule_based_processing': 0.0, 'rule_based_text_normalization': 0.0, 'keyword_text_normalization': 0.004988193511962891, 'YAKE': 0.10272526741027832, 'InvertedIndex': 0.006979942321777344, 'DICE_Matrix': 0.003989458084106445, 'GTE': 0.0009970664978027344}