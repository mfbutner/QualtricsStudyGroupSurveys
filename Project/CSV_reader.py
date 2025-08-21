import pandas
from typing import TextIO
from survey import Survey

class CSV_reader:

    @staticmethod  
    def make_survey_from_CSV(CSV_file:TextIO):
        return Survey("Test Survey")