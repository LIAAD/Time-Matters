
import datefinder
import numpy as np
import json
import os
from sutime import SUTime
from date_extractor import extract_dates as exDT
import articleDateExtractor
from chronyk import Chronyk
import spacy
import dateparser
from datetime import datetime
from time import mktime
from dateparser.date import DateDataParser
import time
def sutime(message):
    jar_files = os.path.join(os.path.dirname(__file__), 'jars')
    sutime = SUTime(jars=jar_files, mark_time_ranges=True)
    print(json.dumps(sutime.parse(message), sort_keys=True, indent=4))

def dateFind(message):
   dates=[]
   matches = datefinder.find_dates(message,source=True)
   for match in matches:
     dates.append(match)
     print(match)

   npDates=np.array(dates)
  # print(npDates)

def dateExtractor(message):
  date = exDT(message)
  print("date: ",date)


def aarticleDateExtractor(message):
    d = articleDateExtractor.extractArticlePublishedDate("http://edition.cnn.com/2015/11/28/opinions/sutter-cop21-paris-preview-two-degrees/index.html")
    print (d)

def Datepaser(message):
      print(DateDataParser(languages=['en']).get_date_data(u'7 July 1937'))
     
if __name__ == '__main__':
    f = open('text.txt','r')
    message = f.read()
    print(message)
    print('===========================================================================')
    #dateFind(message)
    #sutime(message)
    #dateExtractor(message)
    #aarticleDateExtractor(message)
    #heidelTime(message)
    Datepaser(message)