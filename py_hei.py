from py_heideltime import py_heideltime

tex = '''
over 55 years Thurs August 31st - News today  2005-02-02 over 55 years that they are beginning to evacuate 2009/2010 the London children tomorrow. Percy is a billeting officer. I can't see that they will be much safer here.
'''

from yake import KeywordExtractor

from yake.highlight import TextHighlighter

simple_kwextractor = KeywordExtractor(lan="en", n=3, dedupLim=0.9, dedupFunc='seqm', windowsSize=1, top=20)
keywords = simple_kwextractor.extract_keywords(tex)

th = TextHighlighter(max_ngram_size=3)
print(th.highlight(tex, keywords))