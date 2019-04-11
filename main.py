
from dictionary import kw_ext
from dataframes import dt_frames


def main(txt, window=5, threshold=0.05, max_array_len=0):
    dictionary, words_array, dates_array = kw_ext(txt)
    dt_frames(dictionary, words_array, dates_array, window, threshold, max_array_len)


if __name__ == '__main__':
    f = open('text.txt', 'r')
    message = f.read()
    print(message)
    print('===========================================================================')
    main(message)
