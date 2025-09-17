from collections import namedtuple
from typing import Dict
from itertools import combinations
from copy import deepcopy
import unittest

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
    
    def get_name(self) -> Name:
        return self._name

    def get_name_first_last(self) -> str:
        return f"{self._name.first_name} {self._name.last_name}"

class Interaction:
    def __init__(self, reporter:Student, date:str, durations:Dict[Name, int]):
        self._reporter = reporter
        self._date = date
        self._durations = durations
        
    # Returns true if the interactions match, except maybe that one student recorded lower numbers than the other due to leaving early
    def perfect_match(self, other): 
        if self._date != other._date:
            return False
        
        my_full_durations = deepcopy(self._durations)
        their_full_durations = deepcopy(other._durations)

        my_duration = max(list(my_full_durations.values()))
        their_duration = max(list(their_full_durations.values()))

        # If the other student recorded a larger number for me than I did for myself (or me for them), that's a discrepancy
        if my_duration < other._durations[self._reporter.get_name()]:
            return False
        
        if their_duration < self._durations[other._reporter.get_name()]:
            return False

        
        # We assume that students stayed only as long as the longest interaction that they recorded
        my_full_durations[self._reporter.get_name()] = my_duration
        their_full_durations[other._reporter.get_name()] = their_duration

        for name in my_full_durations.keys(): # If a student left early, then it's okay that they recored lower numbers for everyone
            if my_full_durations[name] > their_full_durations[name] and their_full_durations[name] != their_duration:
                return False
            if my_full_durations[name] < their_full_durations[name] and my_full_durations[name] != my_duration:
                return False

        return True

class Test_Interactions(unittest.TestCase):
    student_A = Student("Student", "A", "email_A", "0", "0", "2")
    student_B = Student("Student", "B", "email_B", "1", "1", "2")
    student_C = Student("Student", "C", "email_C", "2", "2", "2")
    student_D = Student("Student", "D", "email_D", "3", "3", "2")

    def test_identical_interactions(self):
        interaction_0 = Interaction(self.student_A, "today", {
            self.student_B.get_name(): 20,
            self.student_C.get_name(): 20,
            self.student_D.get_name(): 20
        })
        interaction_1 = Interaction(self.student_B, "today", {
            self.student_A.get_name(): 20,
            self.student_C.get_name(): 20,
            self.student_D.get_name(): 20
        })
        self.assertTrue(interaction_0.perfect_match(interaction_1))
        self.assertTrue(interaction_1.perfect_match(interaction_0))


    def test_leave_early_match(self):
        interaction_0 = Interaction(self.student_A, "today", {
            self.student_B.get_name(): 10,
            self.student_C.get_name(): 20,
            self.student_D.get_name(): 20
        })
        interaction_1 = Interaction(self.student_B, "today", {
            self.student_A.get_name(): 10,
            self.student_C.get_name(): 10,
            self.student_D.get_name(): 10
        })
        self.assertTrue(interaction_0.perfect_match(interaction_1))
        self.assertTrue(interaction_1.perfect_match(interaction_0))
    

    def test_leave_early_match_2(self):
        interaction_0 = Interaction(self.student_A, "today", {
            self.student_B.get_name(): 20,
            self.student_C.get_name(): 10,
            self.student_D.get_name(): 10
        })
        interaction_1 = Interaction(self.student_B, "today", {
            self.student_A.get_name(): 20,
            self.student_C.get_name(): 10,
            self.student_D.get_name(): 10
        })

        self.assertTrue(interaction_0.perfect_match(interaction_1))
        self.assertTrue(interaction_1.perfect_match(interaction_0))


    def test_discrepancy_1(self):
        interaction_0 = Interaction(self.student_B, "today", {
            self.student_A.get_name(): 20,
            self.student_C.get_name(): 20,
            self.student_D.get_name(): 20
        })
        interaction_1 = Interaction(self.student_C, "today", {
            self.student_A.get_name(): 10,
            self.student_B.get_name(): 20,
            self.student_D.get_name(): 20
        })

        self.assertFalse(interaction_0.perfect_match(interaction_1))
        self.assertFalse(interaction_1.perfect_match(interaction_0))


    def test_discrepancy_2(self):
        interaction_0 = Interaction(self.student_A, "today", {
            self.student_B.get_name(): 10,
            self.student_C.get_name(): 10,
            self.student_D.get_name(): 10
        })
        interaction_1 = Interaction(self.student_B, "today", {
            self.student_A.get_name(): 20,
            self.student_C.get_name(): 10,
            self.student_D.get_name(): 10
        })

        self.assertFalse(interaction_0.perfect_match(interaction_1))
        self.assertFalse(interaction_1.perfect_match(interaction_0))
    

    def test_discrepancy_3(self):
        interaction_0 = Interaction(self.student_A, "today", {
            self.student_B.get_name(): 10,
            self.student_C.get_name(): 20,
            self.student_D.get_name(): 10
        })
        interaction_1 = Interaction(self.student_B, "today", {
            self.student_A.get_name(): 10,
            self.student_C.get_name(): 20,
            self.student_D.get_name(): 10
        })

        self.assertFalse(interaction_0.perfect_match(interaction_1))
        self.assertFalse(interaction_1.perfect_match(interaction_0))


    def test_full_interaction_match_identical(self):
        interaction_0 = Interaction(self.student_A, "today", {
            self.student_B.get_name(): 20,
            self.student_C.get_name(): 20,
            self.student_D.get_name(): 20
        })
        interaction_1 = Interaction(self.student_B, "today", {
            self.student_A.get_name(): 20,
            self.student_C.get_name(): 20,
            self.student_D.get_name(): 20
        })
        interaction_2 = Interaction(self.student_C, "today", {
            self.student_A.get_name(): 20,
            self.student_B.get_name(): 20,
            self.student_D.get_name(): 20
        })
        interaction_3 = Interaction(self.student_D, "today", {
            self.student_A.get_name(): 20,
            self.student_B.get_name(): 20,
            self.student_C.get_name(): 20
        })

        match_test_interactions = [interaction_0, interaction_1, interaction_2, interaction_3]
        for combination in list(combinations(match_test_interactions, 2)):
            self.assertTrue(combination[0].perfect_match(combination[1]))
            self.assertTrue(combination[1].perfect_match(combination[0]))
    

    def test_full_interaction_match_leave_early(self):
        interaction_0 = Interaction(self.student_A, "today", {
            self.student_B.get_name(): 20,
            self.student_C.get_name(): 10,
            self.student_D.get_name(): 10
        })
        interaction_1 = Interaction(self.student_B, "today", {
            self.student_A.get_name(): 20,
            self.student_C.get_name(): 10,
            self.student_D.get_name(): 10
        })
        interaction_2 = Interaction(self.student_C, "today", {
            self.student_A.get_name(): 10,
            self.student_B.get_name(): 10,
            self.student_D.get_name(): 10
        })
        interaction_3 = Interaction(self.student_D, "today", {
            self.student_A.get_name(): 10,
            self.student_B.get_name(): 10,
            self.student_C.get_name(): 10
        })

        match_test_interactions = [interaction_0, interaction_1, interaction_2, interaction_3]
        for combination in list(combinations(match_test_interactions, 2)):
            self.assertTrue(combination[0].perfect_match(combination[1]))
            self.assertTrue(combination[1].perfect_match(combination[0]))

    
    def test_full_interaction_discrepancy(self):
        interaction_0 = Interaction(self.student_A, "today", {
            self.student_B.get_name(): 20,
            self.student_C.get_name(): 20,
            self.student_D.get_name(): 20
        })
        interaction_1 = Interaction(self.student_B, "today", {
            self.student_A.get_name(): 10,
            self.student_C.get_name(): 20,
            self.student_D.get_name(): 20
        })
        interaction_2 = Interaction(self.student_C, "today", {
            self.student_A.get_name(): 10,
            self.student_B.get_name(): 20,
            self.student_D.get_name(): 20
        })
        interaction_3 = Interaction(self.student_D, "today", {
            self.student_A.get_name(): 10,
            self.student_B.get_name(): 20,
            self.student_C.get_name(): 20
        })

        self.assertTrue(interaction_1.perfect_match(interaction_2))
        self.assertTrue(interaction_2.perfect_match(interaction_1))

        self.assertTrue(interaction_2.perfect_match(interaction_3))
        self.assertTrue(interaction_3.perfect_match(interaction_2))

        self.assertFalse(interaction_0.perfect_match(interaction_1))
        self.assertFalse(interaction_1.perfect_match(interaction_0))

        self.assertFalse(interaction_0.perfect_match(interaction_2))
        self.assertFalse(interaction_2.perfect_match(interaction_0))

        self.assertFalse(interaction_0.perfect_match(interaction_3))
        self.assertFalse(interaction_3.perfect_match(interaction_0))

          
    
if __name__ == "__main__":
    unittest.main()