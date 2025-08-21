import pandas
from typing import TextIO
from Project.survey import Survey

class CSV_reader:

    @staticmethod  
    def make_survey_from_CSV(CSV_file:TextIO, survey_name:str): #TODO: make CSV parser based on Prof. Butner's sample CSV
        return Survey(survey_name)