import nltk
import string
def word_tokenizer(text):

    k = nltk.word_tokenize(text)
    # removed the punctuation in text

    tokens_filtered = [token.lower() for token in k if token not in string.punctuation]
    return tokens_filtered

def test_trans(s):
    import string
    return s.translate(str.maketrans('', '', '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'))

def sentence_tokenizer(text):
    # usage of nltk to tokenize the text by sentences
    sentences = nltk.sent_tokenize(text)
    return sentences


def remove_special_characters(ss):
    import re
    # insert spaces between special characters to isolate them
    special_char_pattern = re.compile(r'([{.(-)!}])')
    text = special_char_pattern.sub(" \\1 ", ss)

    # remove special chars
    pattern = r'[^a-zA-z0-9\s]-'
    text = re.sub(pattern, '', text)

    return text
if __name__ == '__main__':

    file = open('dan.txt')
    text = '''
    The Carnation Revolution (Portuguese: Revolução dos Cravos), also known as 2019-04-25 (Portuguese: 25 de 
    Abril), was initially a 1974-04-25 military coup in Lisbon which overthrew the authoritarian Estado Novo regime.
    1974 [1] The revolution 1974 began as a coup organised by the Armed Forces Movement 
    (Portuguese: Movimento das Forças Armadas, MFA), composed of military officers who opposed the regime, but it was 
    soon coupled with an 2000 unanticipated, popular civil resistance campaign. 1974 The revolution led to the 2019-FA of the Estado 
    Novo, P48Y  of authoritarian 20-02-2000 2004-01-30 rule in Portugal, and Portugal's withdrawal from its African colonies 2000
    '''
    #strip_text = test_trans(text)
    #print(strip_text)

    print(test_trans(text))
    texttt = file.read()
    sentence_array = sentence_tokenizer(text)

    aray = ['1974', '2019-FA ', '2004-2011', '1690-1698']

    dates = {}
    for dt in aray:
        last_pos = 0
        totalfreq = 0
        search_str = dt
        dates[dt] = [0,0,{}]
        for n in range(len(sentence_array)):
            #strip_text = test_trans(sentence_array[n]).split()
            strip_text = test_trans(sentence_array[n]).split()
            print(strip_text)
            for i, w in enumerate(strip_text):
                if w.lower() == search_str:
                    if n not in dates[dt][2]:
                        pos =i+last_pos
                        dates[dt][2][n] = [0, [pos]]

                    else:
                        pos = i + last_pos

                        dates[dt][2][n][1].append(pos)
            try:
                ct = len(dates[dt][2][n][1])
                totalfreq += ct
                dates[dt][2][n][0] = ct

            except:
                pass
            last_pos += len(strip_text)
        dates[dt][0] = len(dates[dt][2])
        dates[dt][1] = totalfreq
    print(dates)
    print('\n')

import time
start_time = time.time()

tests = ['500', '1000', '2000', '4000', '6000','8000', '10000', '12000', '15000']
for test in tests:
    file = open('dan'+str(test)+'.txt')
    text = file.read()
    sutime_start_time = time.time()
    output = Time_Matters_SingleDoc(text, temporal_tagger=['sutime'], time_matters_parameters=[10, 'none', 'max', 0.05], score_type='single', debug_mode=False)
    print(output)
    print("---sutime wrapper %s seconds ---" % (time.time() - sutime_start_time))

    py_heideltime_start_time = time.time()
    output_py = Time_Matters_SingleDoc(text, temporal_tagger=['py_heideltime'], time_matters_parameters=[10, 'none', 'max', 0.05], score_type='single', debug_mode=False)
    print(output_py)
    print("---py_heideltime %s seconds ---" % (time.time() - py_heideltime_start_time))

