def verify_time_matters(num_of_keywords, N, n_contextual_window, TH):
    if not isinstance(num_of_keywords, int) or num_of_keywords < 0:
        print('Please specify a valid num_of_keywords'
              'options:\n'
              'n, where n is any integer > 0;')
        return {}

    elif n_contextual_window != 'full_sentence' and not isinstance(n_contextual_window, int) or (isinstance(n_contextual_window, int) and n_contextual_window < 0) :
        print('Please specify a valid n_contextual_window\n'
              'options:\n'
              '     full_sentence;\n'
              '     n, where n is any integer > 0;')
        return {}

    elif N != 'max' and not isinstance(N, int) or isinstance(N, int) and N < 0:
        print('Please specify a valid n context vector size\n'
              'options:\n'
              '     max;\n'
              '     n, where n is any integer > 0;')


        return {}
    elif not isinstance(TH, float) or TH < 0:
        print('Please specify a valid TH threshold\n'
              'options:\n'
              '      n, where n is any float > 0;')
        return {}


def verify_temporal_tagger(tt_name):
    if tt_name != 'py_heideltime' and tt_name != 'rule_based':
        print('Please specify a valid time_tagger_name.\n'
              'options:\n'
              '     py_heideltime;\n'
              '     rule_based')
        return {}


def verify_score_type(score_type, debug_mode, date_granularity):
    date_granularity_options = ['day', 'month', 'year', 'full']
    if date_granularity.lower() not in date_granularity_options:
        print('Please specify a valid date_granularity.\n'
              'options:\n'
              '     full;\n'
              '     year;\n'
              '     month:\n'
              '     day;')
        return {}

    if score_type != 'ByDoc' and score_type != 'BySentence':
        print('Please specify a valid score_type.\n'
              'options:\n'
              '     ByDoc;\n'
              '     BySentence;')
        return {}
    if not isinstance(debug_mode, bool):
        print('Please specify a valid option for debug_mode.\n'
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
