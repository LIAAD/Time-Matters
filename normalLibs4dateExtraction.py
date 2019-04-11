
import datefinder
import numpy as np
import json
import os
from date_extractor import extract_dates as exDT
from dateparser.date import DateDataParser
import re
import datetime

def dateFind(message):
   dates=[]
   matches = datefinder.find_dates(message,source=True)
   for match in matches:
     dates.append(match)
     print(match)
   npDates=np.array(dates)
   print(npDates)

def dateExtractor(message):
  date = exDT(message)
  print("date: ",date)


def Datepaser(message):
      print(DateDataParser(languages=['en']).get_date_data('between 1900 and 2017'))


def find_with_re(message):
    from date_extractor import extract_date
    text = message
    date, precision = extract_date(text, return_precision=True)
    print(date)
if __name__ == '__main__':
    f = open('text.txt', 'r')
    message = f.read()
    print(message)
    print('===========================================================================')
    #dateFind(message)
    #sutime(message)
    #dateExtractor(message)
    #aarticleDateExtractor(message)
    #heidelTime(message)
    Datepaser(message)
    #find_with_re(message)