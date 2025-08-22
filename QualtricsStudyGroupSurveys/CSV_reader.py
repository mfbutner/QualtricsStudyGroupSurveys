import pandas as pd
from typing import List
from .survey import Survey
from .student import Student
from .question import *
from .validation import *

class CSV_reader:
    def __init__(self, CSV_file_path:str):
        self._file_path = CSV_file_path

    def make_survey_from_CSV(self, survey_name:str) -> Survey: #TODO: make CSV parser based on Prof. Butner's sample CSV
        students = self._parse()
        survey = Survey(survey_name)
        # survey.addQuestion(Multiple_Choice("test name", "test description", Validation(False)))
        return survey
    
    def _parse(self) -> List[Student]:
        data_frame = pd.read_csv(self._file_path)
        students = []
        for row in data_frame.itertuples():
            students.append(Student(row.LastName, row.FirstName, row.Email, row.StudentID, row.CanvasId, int(row.Team)))

        return students