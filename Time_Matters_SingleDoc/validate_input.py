def verify_time_matters(num_of_keywords, N, n_contextual_window, TH):
    if not isinstance(num_of_keywords, int) or num_of_keywords < 0:
        print('Please specify a valid num_of_keywords\n'
              'options:\n'
              '     n, where n is any integer > 0;')
        return {}

    elif (n_contextual_window != 'full_sentence' and not isinstance(n_contextual_window, int)) or (isinstance(n_contextual_window, int) and n_contextual_window < 0) :
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


def verify_temporal_tagger(tt_name, language, document_type, date_granularity, document_creation_time):
    tt_options = ['py_heideltime', 'rule_based']
    if tt_name not in tt_options:
        print('Please specify a valid time_tagger_name.\n'
              'options:\n'
              '     py_heideltime;\n'
              '     rule_based;')
        return {}
    document_type_list = ['news', 'narrative', 'colloquial', 'scientific']
    list_lang = ['english', 'portuguese', 'spanish', 'germany', 'dutch', 'italian', 'french']
    date_granularity_options = ['day', 'month', 'year', 'full']
    import re
    try:
        match = re.findall('^\d{4}[-]\d{2}[-]\d{2}$', document_creation_time)
    except:
        match = []
    if not isinstance(language, str) and language not in list_lang or language.lower() not in list_lang:
        print('Please specify a valid language.\n'
              'Options:\n'
              '      English;\n'
              '      Portuguese;\n'
              '      Spanish;\n'
              '      Germany;\n'
              '      Dutch;\n'
              '      Italian;\n'
              '      French.')
        return {}
    elif date_granularity not in date_granularity_options:
        print('Please specify a valid date_granularity.\n'
              'options:\n'
              '     full;\n'
              '     year;\n'
              '     month;\n'
              '     day;')
        return {}
    elif not isinstance(document_type, str) and document_type not in document_type_list or document_type.lower() not in document_type_list:
        print('Please specify a valid document_type.\n'
              'options:\n'
              '     news;\n'
              '     narrative;\n'
              '     colloquial;\n'
              '     scientific;')
        return {}
    elif not isinstance(document_type, str) and document_type not in document_type_list or document_type.lower() not in document_type_list:
        print('Please specify a valid document_type.\n'
              'options:\n'
              '     news;\n'
              '     narrative;\n'
              '     colloquial;\n'
              '     scientific;')
        return {}
    elif match == [] and document_creation_time !='yyyy-mm-dd':
        print('Please specify a date in the following format: YYYY-MM-DD.')
        return {}


def verify_score_type(score_type, debug_mode):
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
        if temporal_tagger[0] == 'py_heideltime':
            language = temporal_tagger[1]
            date_granularity = temporal_tagger[2]
            document_type = temporal_tagger[3]
            document_creation_time = temporal_tagger[4]
        elif temporal_tagger[0] == 'rule_based':
            tt_name = temporal_tagger[0]
            date_granularity = temporal_tagger[1]
        else:
            tt_name = 1
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
