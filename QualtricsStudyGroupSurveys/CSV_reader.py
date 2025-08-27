import pandas as pd
from typing import List
from .student import Student

class CSV_reader:
    @staticmethod
    def parse_CSV_for_students(CSV_file_path:str) -> List[Student]:
        data_frame = pd.read_csv(CSV_file_path)
        students = []
        for row in data_frame.itertuples():
            students.append(Student(row.LastName, row.FirstName, row.Email, row.StudentID, row.CanvasId, int(row.Team)))

        return students