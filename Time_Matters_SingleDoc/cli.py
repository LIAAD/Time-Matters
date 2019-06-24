from Time_Matters_SingleDoc import Time_Matters_SingleDoc

help_text = '''
 Usage_examples (make sure that the input parameters should be within quotes):
  Default Parameters: Time_Matters_SingleDoc -i "['text', 'August 31st']" -tt "['py_heideltime','English']"
  All the Parameters: Time_Matters_SingleDoc -i "['text', 'August 31st']" -tt "['py_heideltime','English', 'days', 'news', '2019-05-05']" -tm "[10,'none', 'max', 0.05]" -st single -dm False

Options:
  [required]: that is, need to specify one of the two options (text or path).
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  -i, --input LIST                      A list that specifies the type of input: a text or path
                                        Example:
                                                "['text', 'August 31st']" 
                                                "['path', 'text.txt']"



  [not required]
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  -tt, --temporal_tagger LIST           Specifies the temporal tagger (“heideltime”, “rule-based”) and the corresponding parameters.                                              
                                        py_heideltime
                                            parameters:
                                            
                                                temporal_tagger_name
                                                    options:
                                                            "py_heideltime"
                                                language
                                                    options:
                                                            "English";
                                                            "Portuguese";
                                                            "Spanish";
                                                            "Germany";
                                                            "Dutch";
                                                            "Italian";
                                                            "French".
                                                
                                                date_granularity
                                                    options:
                                                            "year" (means that for the date YYYY-MM-DD only the YYYY will be retrieved); 
                                                            "month" (means that for the date YYYY-MM-DD only the YYYY-MM will be retrieved); 
                                                            "day" - (default param. Means that for the date YYYY-MM-DD it will retrieve YYYY-MM-DD).
                                                            
                                                document_type    
                                                    options:
                                                            "News" for news-style documents - default param; 
                                                            "Narrative" for narrative-style documents (e.g., Wikipedia articles); 
                                                            "Colloquial" for English colloquial (e.g., Tweets and SMS);  
                                                            "Scientific" for scientific articles (e.g., clinical trails).
                                                            
                                                document_creation_time            
                                                     Document creation date in the format YYYY-MM-DD. Taken into account when "News" or "Colloquial" 
                                                     texts are specified.
                                                     Example: "2019-05-30".
                                                     
                                            Example:
                                                "['py_heideltime','English', 'days', 'news', '2019-05-05']"
                                                                                          
                                        Rule_Based
                                            parameters:
                                                                                    
                                                temporal_tagger_name
                                                    options:
                                                            "rule_based"

                                                date_granularity
                                                    options:
                                                            "year" (means that for the date YYYY-MM-DD only the YYYY will be retrieved); 
                                                            "month" (means that for the date YYYY-MM-DD only the YYYY-MM will be retrieved); 
                                                            "day" - (default param. Means that for the date YYYY-MM-DD it will retrieve YYYY-MM-DD).                                                        
                                                    
                                            Example:
                                                "['rule_based','days']"    

  [not required]
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  -tm, --time_matters LIST              specifies information about the Time-Matters
                                            the number of YAKE! keywords to extract from the text (num_of_keywords),
                                            information regarding the construction of the vocabulary context vector (N,
                                            TH), and information concerning the scope of search (n_contextual_window)
                                            
                                            Example:
                                                "[num_of_keywords=10, context_window_distance=10, N='max', TH=0.05]"
                                                
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  -st, --score_type TEXT                Specifies the type of score
                                        Options:
                                                "single" Single score per date;
                                                "Multiple" Multiple score depending which sentence that the date appears;


  -dm, --debug_mode BOOLEAN             Return the following data:
                                                "Candidates dates list";
                                                "Relevante words list, extracted by YAKE!";
                                                "Inverted Index"
                                                "Dice Matrix"
                                                "Relevant dates list with the score and offset"
                                                
  

  --help                                Show this message and exit.

'''


def Dates():
    import sys
    arg = []
    for i in range(len(sys.argv)):
        opt = sys.argv[i]
        arg.append(opt)

    def run_time_matters(text):
        time_tagger_arg_list = get_arguments_list_values(arg, '-tt', 'temporal_tagger', [])
        time_matterss_arg_list = get_arguments_list_values(arg, '-tm', 'time_matters', [])
        score_type = get_arguments_values(arg, '-st', '--score_type', 'single')
        debug_mode = get_arguments_values(arg, '-dm', '--debug_mode', False)

        if not debug_mode:
            output = Time_Matters_SingleDoc(text, time_tagger_arg_list, time_matterss_arg_list, score_type, debug_mode)
            print(output)
        else:
            final_score_output, dates_array, words_array, inverted_index, DiceMatrix = Time_Matters_SingleDoc(text, time_tagger_arg_list, time_matterss_arg_list, score_type, debug_mode)

            print('Candidate Dates =' + str(dates_array))
            print('Relevant words =' + str(words_array))
            print('Inverted Index =' + str(inverted_index))
            print('==========================DICE Matrix=======================')
            print(DiceMatrix)
            print('=======================GTE Final score======================')
            print(final_score_output)

    if '--help' in arg:
        print(help_text)
        exit(1)

    # make sure if was input text arugument

    if '-i' in arg or '--input_file' in arg:
        position = verify_argument_pos(arg, '-i', '--input_file')
        str_input_list = arg[position+1]
        import ast
        input_list = ast.literal_eval(str_input_list)
        if input_list[0] == 'path':
            import codecs
            text = codecs.open(input_list[1], "r+", "utf-8").read()
        else:
            text = input_list[1]
        run_time_matters(text)
    else:
        print('Bad arguments [--help]')
        exit(1)


def get_arguments_list_values(arg_list, argument, extense_argument, defaut_value):
    input_list = []
    try:
        try:
            position = arg_list.index(argument)
        except:
            position = arg_list.index(extense_argument)

        if argument in arg_list or extense_argument in arg_list:
            str_input_list = arg_list[position + 1]
            import ast
            input_list = ast.literal_eval(str_input_list)
    except:
        input_list = defaut_value
    return input_list


def get_arguments_values(arg_list, argument, extense_argument, defaut_value):
    value = ''
    try:
        try:
            position = arg_list.index(argument)
        except:
            position = arg_list.index(extense_argument)

        if argument in arg_list or extense_argument in arg_list:
            value = arg_list[position + 1]

    except:
        value = defaut_value
    return value


def verify_argument_pos(arg_list, argument, extense_argument):
    try:
        position = arg_list.index(argument)
    except:
        position = arg_list.index(extense_argument)
    return position


if __name__ == "__main__":
    Dates()
