from Time_Matters_SingleDoc import Time_Matters_SingleDoc
from Time_Matters_SingleDoc.validate_input import *

help_text = '''
 Usage_examples (make sure that the input parameters should be within quotes):
  Default Parameters: Time_Matters_SingleDoc -i "['text', 'August 31st']" -tt "['py_heideltime','English']"
  All the Parameters: Time_Matters_SingleDoc -i "['text', 'August 31st']" -tt "['py_heideltime','English', 'days', 'news', '2019-05-05']" -tm "[10,'none', 'max', 0.05]" -st single -dm "False"

Options:
 [required]: either specify a text or an input_file path.
  ----------------------------------------------------------------------------------------------------------------------------------
  -i, --input               A list that specifies the type of input: a text or a file path
                            Example:
                                    "['text', 'August 31st']"
                                    "['path', 'c:\\text.txt']"



 [not required]
 ----------------------------------------------------------------------------------------------------------------------------------
  -tt, --temporal_tagger   Specifies the temporal tagger and the corresponding parameters.
                           Default: "py_heideltime"
			   Options:
			   	    "py_heideltime"
				    "rule_based"
				 
			   py_heideltime (parameters):
			   ____________________________
			   - temporal_tagger_name
			     Options:
				     "py_heideltime"

			   - language
			     Default: "English"
			     Options:
			   	      "English";
				      "Portuguese";
				      "Spanish";
				      "Germany";
				      "Dutch";
				      "Italian";
				      "French".

		          - date_granularity
			    Default: "full"
			    Options:
			           "full": means that all types of granularity will be retrieved, from the coarsest to the 
					   finest-granularity.
			           "day": means that for the date YYYY-MM-DD-HH:MM:SS it will retrieve YYYY-MM-DD;
				   "month": means that for the date YYYY-MM-DD-HH:MM:SS only the YYYY-MM will be retrieved;
				   "year": means that for the date YYYY-MM-DD-HH:MM:SS only the YYYY will be retrieved;

			  - document_type
			    Default: "News"
			    Options:
			  	    "News": for news-style documents - default param;
				    "Narrative": for narrative-style documents (e.g., Wikipedia articles);
				    "Colloquial": for English colloquial (e.g., Tweets and SMS);
				    "Scientific": for scientific articles (e.g., clinical trails).

			  - document_creation_time
			    Document creation date in the format YYYY-MM-DD. Taken into account when "News" or "Colloquial" texts
		            are specified.
		            Example: "2019-05-30".

			  - Example: "['py_heideltime','English', 'full', 'news', '2019-05-05']"	 

		          
			  Rule_Based (parameters):
		          ____________________________
			  - temporal_tagger_name
			    Options:
			  	    "rule_based"

			  - date_granularity
			    Default: "full"
			    Options:
			           "full": means that all types of granularity will be retrieved, from the coarsest to the 
					   finest-granularity.
			           "day": means that for the date YYYY-MM-DD-HH:MM:SS it will retrieve YYYY-MM-DD;
				   "month": means that for the date YYYY-MM-DD-HH:MM:SS only the YYYY-MM will be retrieved;
				   "year": means that for the date YYYY-MM-DD-HH:MM:SS only the YYYY will be retrieved;

			  - Example: "['rule_based','full']"

 [not required]
 ----------------------------------------------------------------------------------------------------------------------------------
  -tm, --time_matters     Specifies information about Time-Matters, namely:
			  - num_of_keywords: number of YAKE! keywords to extract from the text
			    Default: 10
			    Options:
				    any integer > 0

		          - n_contextual_window: defines the search space where co-occurrences between terms may be counted.
			    Default: "full_sentence"
			    Options:
                                    "full_sentence": the system will look for co-occurrences between terms that occur within the search 
				                    space of a sentence;
			            n: where n is any value > 0, that is, the system will look for co-occurrences between terms that 
				       occur within a window of n terms;
				       
		          - N: N-size context vector for InfoSimba vectors
			    Default: "max"
			    Options: 
			            "max": where "max" is given by the maximum number of terms eligible to be part of the vector
				    any integer > 0
				    
			  - TH: all the terms with a DICE similarity > TH threshold are eligible to the context vector of InfoSimba
			    Default: 0.05
			    Options: 
				    any integer > 0


			  - Example: "[10, 'full_sentence', 'max', 0.05]"

 [not required]
 ----------------------------------------------------------------------------------------------------------------------------------
  -st, --score_type       Specifies the type of score for the temporal expression found in the text
  			  Default: "single"
                          Options:
                                  "ByDoc": returns a single score regardless the temporal expression occurs in different sentences;
                                  "BySentence": returns multiple scores (one for each sentence where it occurs)
			  - Example: "[10, 'full_sentence', 'max', 0.05]"
 [not required]
 ----------------------------------------------------------------------------------------------------------------------------------
  -dm, --debug_mode      Returns detailed information about the results
  	                 Default: False
			 Options:
			          False: when set to False debug mode is not activated
				  True: activates debug mode. In that case it returns 
                                        "Text";
					"NormalizedText"
					"Score"
					"CandidateDates"
					"NormalizedCandidateDates"
					"RelevantKWs"
					"InvertedIndex"
					"Dice_Matrix

  --help                 Show this message and exit.

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
        score_type = get_arguments_values(arg, '-st', '--score_type', 'ByDoc')
        debug_mode = get_arguments_values(arg, '-dm', '--debug_mode', 'False')

        if debug_mode == 'False':
            output = Time_Matters_SingleDoc(text, time_tagger_arg_list, time_matterss_arg_list, score_type,
                                            str2bool(debug_mode))
            if output != {}:
                print('=========================== GTE Final score ===================================' + '\n')
                print(output)
            else:
                print('{}')

        elif debug_mode == 'True':
            try:
                if time_tagger_arg_list[0] == 'rule_based':
                    rule_based_output(text, time_tagger_arg_list, time_matterss_arg_list, score_type,
                                      str2bool(debug_mode))
                else:
                    py_heideltime_output(text, time_tagger_arg_list, time_matterss_arg_list, score_type,
                                         str2bool(debug_mode))
            except:
                py_heideltime_output(text, time_tagger_arg_list, time_matterss_arg_list, score_type,
                                     str2bool(debug_mode))
        else:
            print('Please specify a valid option for debug_mode.\n'
                  'options:\n'
                  '     True;\n'
                  '     False;')
            return {}

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

def str2bool(v):
  return v in ("True")

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


def rule_based_output(text, time_tagger_arg_list, time_matterss_arg_list, score_type, debug_mode):
    try:
        NormalizedText, final_score_output, candidate_dates_list, words_array, inverted_index, DiceMatrix, execution_time_list = Time_Matters_SingleDoc(
            text, time_tagger_arg_list, time_matterss_arg_list, score_type, debug_mode)

        print('=========================== Normalized Text ====================================\n')
        print(NormalizedText)
        print('\n')
        print('=========================== GTE Final score ====================================\n')
        print(str(final_score_output) + '\n')
        print('=========================== Candidate dates Dictionary =========================\n')
        print(str(candidate_dates_list) + '\n')
        print('=========================== Relevant Keywords ==================================\n')
        print(str(words_array) + '\n')
        print('=========================== Inverted Index =====================================\n')
        print(str(inverted_index) + '\n')
        print('========================== DICE Matrix =========================================\n')
        print(DiceMatrix, '\n')
        print('============================= Execution time list  =============================\n')
        print(execution_time_list)
    except ValueError:
        print('{}')

def py_heideltime_output(text, time_tagger_arg_list, time_matterss_arg_list, score_type, debug_mode):
    try:
        n_txt, NormalizedText, final_score_output, candidate_dates_dictionary, normalized_candidate_date_dictionary, words_array, inverted_index, DiceMatrix, execution_time_list = Time_Matters_SingleDoc(
            text, time_tagger_arg_list, time_matterss_arg_list, score_type, debug_mode)

        print('=========================== Original Text ======================================\n')
        print(n_txt)
        print('\n')
        print('=========================== Normalized Text ====================================\n')
        print(NormalizedText)
        print('\n')
        print('=========================== GTE Final score ====================================\n')
        print(str(final_score_output) + '\n')
        print('=========================== Candidate dates Dictionary =========================\n')
        print(str(candidate_dates_dictionary) + '\n')
        print('=========================== Normalized Candidate dates Dictionary ==============\n')
        print(str(normalized_candidate_date_dictionary) + '\n')
        print('=========================== Relevant Keywords ==================================\n')
        print(str(words_array) + '\n')
        print('=========================== Inverted Index =====================================\n')
        print(str(inverted_index) + '\n')
        print('========================== DICE Matrix =========================================\n')
        print(DiceMatrix, '\n')
        print('============================= Execution time list  =============================\n')
        print(execution_time_list)
    except ValueError:
        print('{}')

if __name__ == "__main__":
    Dates()
