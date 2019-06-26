
def verify_input_data(temporal_tagger, time_matters):

    tt_name = 'py_heideltime'
    language = 'English'
    document_type = 'news'
    document_creation_time = ''
    date_granularity = ''
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
