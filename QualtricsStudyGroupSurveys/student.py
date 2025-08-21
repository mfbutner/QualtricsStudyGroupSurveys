from collections import namedtuple

Name = namedtuple("Name", ["last_name", "first_name"])

class Student():
    def __init__(self, last_name:str, first_name:str, email:str, student_ID:str, canvas_ID:str, team:int):
        self._name = Name(last_name, first_name)
        self._email = email
        self._student_ID = student_ID
        self._canvas_ID = canvas_ID
        self._team = team
    
    def __str__(self):
        return f"Student with name ({self._name.last_name}, {self._name.first_name}), email address {self._email}, student ID {self._student_ID}, Canvas ID {self._canvas_ID}, and on team {self._team}"
    
