text= "2011 Haiti knowlage Earthquake Anniversary. 2002 2006 As of 2010 (see 1500 photos here), the following major earthquakes "\
    "have been recorded in Haiti. The first great earthquake mentioned in histories of Haiti occurred in "\
    "1564 in what was now still the Spanish colony. It destroyed Concepción de la Vega. On January 12, 2010, "\
    "a massive earthquake struck the nation of Haiti, causing catastrophic damage inside and around the "\
    "capital city of Port-au-Prince. On the first anniversary of the earthquake, 12 January 2011, "\
    "Haitian Prime Minister Jean-Max Bellerive said the death toll from the quake in 2010 was more "\
    "than 316,000, raising the figures in 2010 from previous estimates. I immediately flashed back to the afternoon "\
    "of February 11, 1975 when, on  my car radio, I first heard the news. Yesterday..."


t_file = open('dan.txt').read()
len(t_file.split(' '))

t2_file = open('boston.txt').read()
len(t2_file.split(' '))

t3_file = open('bp.txt').read()
len(t3_file.split(' '))

from py_rule_based import py_rule_based
result1 = py_rule_based(t_file)
print(result1[-1]['rule_based_processing'])
result2 = py_rule_based(t2_file)
print(result2[-1]['rule_based_processing'])
result3 = py_rule_based(t3_file)
print(result3[-1]['rule_based_processing'])
print('\n')
from py_heideltime import py_heideltime
result1_heidel = py_heideltime(t_file)
print(result1_heidel[-1]['heideltime_processing'])
result2_heidel = py_heideltime(t2_file)
print(result2_heidel[-1]['heideltime_processing'])
result3_heidel = py_heideltime(t3_file)
print(result3_heidel[-1]['heideltime_processing'])


import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

objects = ((len(t2_file.split(' ')), len(t3_file.split(' ')), len(t_file.split(' '))))
y_pos = np.arange(len(objects))
performance = [result2_heidel[-1]['heideltime_processing'], result3_heidel[-1]['heideltime_processing'], result1_heidel[-1]['heideltime_processing']]

plt.bar(y_pos, performance, align='center', alpha=0.5, color='b')
plt.xticks(y_pos, objects)
plt.ylabel('Tempo(s)')
plt.title('py_heideltime tempo de processamento por token')

plt.show()