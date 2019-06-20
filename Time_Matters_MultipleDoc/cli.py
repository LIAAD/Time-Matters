import click
from Time_Matters_MultipleDoc import Time_Matters_MultipleDoc
@click.command()
@click.option("-d", '--dir', help='Directory path that cointain the docs should be surrounded by quotes (e.g., “/test”)', required=False)
@click.option("-l", '--language', help='[required] Language text is required and should be surrounded by quotes “”. Options: English, Portuguese, Spanish, Germany, Dutch, Italian, French (e.g., “English”).', required=True)
@click.option("-cwd", '--context_window_distance', help='max distance between words',default=10, required=False)
@click.option("-th", '--threshold', help='minimum DICE threshold similarity values',default=0.05, required=False)
@click.option("-n", '--max_array_len', help='size of the context vector',default=0 ,required=False)
@click.option("-ky", '--max_keywords', help='max keywords',default=10 ,required=False)
@click.option("-icwd", '--ignore_contextual_window_distance', help='ignore contextual window distance',default=False ,required=False)
@click.option("-dt", '--heideltime_document_type', help='Type of the document text should be surrounded by quotes “”. Options: News, Narrative, Colloquial, Scientific (e.g., “News”).', default='News', required=False)
@click.option("-dct", '--heideltime_document_creation_time', help=' Document creation date in the format YYYY-MM-DD should be surrounded by quotes (e.g., “2019-05-30”). Note that this date will only be taken into account when News or Colloquial texts are specified.', default="", required=False)
@click.option("-dg", '--heideltime_date_granularity', help='Value of granularity should be surrounded by quotes “”. Options: Year, Month, day (e.g., “Year”).', default='', required=False)
@click.option("-de", '--date_extractor', help='Type of the date extractor should be surrounded by quotes “”. Options: py_heideltime, rule_based (e.g., “py_heideltime”).', default='rule_based', required=False)
def Dates(language, context_window_distance, threshold, max_array_len, max_keywords, ignore_contextual_window_distance, dir, heideltime_document_type, heideltime_document_creation_time, heideltime_date_granularity, date_extractor):
    def run_time_matters(text_content):
        output = Time_Matters_MultipleDoc(text_content, language, context_window_distance, threshold, max_array_len,
                                          max_keywords, ignore_contextual_window_distance, heideltime_document_type, heideltime_document_creation_time, heideltime_date_granularity, date_extractor)
        print(output)
    if not dir:
        print('Pelase enter a directory with docs to be analysed')
        exit(1)
    else:
        docs = []
        import glob, codecs
        files = [f for f in glob.glob(dir + "**/*.txt", recursive=True)]
        # print(files)
        for file in files:
            text_file = codecs.open(file, "r", "utf-8")
            contents = text_file.read()
            docs.append(contents)
        print(docs)
        run_time_matters(docs)


if __name__ == "__main__":
    Dates()
