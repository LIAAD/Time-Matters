def verify_time_matters(num_of_keywords, N, n_contextual_window, TH):
    if not isinstance(num_of_keywords, int):
        print('You must specify a number of relevant keywords to consider (e.g., 10).')
        return {}

    elif n_contextual_window != 'full_sentence' and not isinstance(n_contextual_window, int):
        print('The value of n_contextual_window is not valid\n'
              'options:\n'
              '     full_sentence;\n'
              '     full_document;\n'
              '     number(integer);')
        return {}

    elif N != 'max' and not isinstance(N, int):
        print('The value of N are not valid\n'
              'options:\n'
              '     max;\n'
              '     number(integer);')

        return {}
    elif not isinstance(TH, float):
        print('The value of TH is not valid\n'
              'options:\n'
              '     number(float);')
        return {}


def verify_score_type(score_type, debug_mode):
    if score_type != 'ByDoc' and score_type != 'BySentence':
        print('You must select a valid score_type.\n'
              'options:\n'
              '     ByDoc;\n'
              '     BySentence;')
        return {}
    if isinstance(debug_mode, bool):
        print('You must select a valid option for debug_mode.\n'
              'options:\n'
              '     True;\n'
              '     False;')
        return {}


def verify_input_data(temporal_tagger, time_matters):
    tt_name = 'py_heideltime'
    language = 'English'
    document_type = 'news'
    document_creation_time = 'yyyy-mm-dd'
    date_granularity = 'full'
    # Verify the values for temporal Tagger parameters.
    try:
        tt_name = temporal_tagger[0].lower()
        if tt_name == 'py_heideltime':
            language = temporal_tagger[1]
            date_granularity = temporal_tagger[2].lower()
            document_type = temporal_tagger[3]
            document_creation_time = temporal_tagger[4]
        elif tt_name == 'rule_based':
            date_granularity = temporal_tagger[1].lower()
    except:
        pass
    num_of_keywords = 10
    n_contextual_window = 'full_sentence'
    N = 'max'
    TH = 0.05
    try:
        num_of_keywords = time_matters[0]
        n_contextual_window = time_matters[1]
        N = time_matters[2]
        TH = time_matters[3]
    except:
        pass
    return tt_name, language, document_type, document_creation_time, date_granularity, \
           num_of_keywords, N, TH, n_contextual_window
