from collections import namedtuple
from typing import Dict
from itertools import combinations
from copy import deepcopy

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
    
    # def perfect_match(self, other) -> bool: # This only returns true if every field is exactly identical, and no one left early
    #     if self._date != other._date:
    #         return False
        
    #     # We match interaction times from the data the other student recorded
    #     my_duration = other._durations[self._reporter.get_name()]
    #     their_duration = self._durations[other._reporter.get_name()]
    
    #     # For this method, we require that all times are identical
    #     if my_duration != their_duration:
    #         return False

    #     self._durations[self._reporter.get_name()] = my_duration
    #     other._durations[other._reporter.get_name()] = their_duration

    #     return self._durations == other._durations
    
    def leave_early_match(self, other): # Returns true if the interactions match, except maybe that one student recorded lower numbers than the other due to leaving early
        if self._date != other._date:
            return False
        
        my_full_durations = deepcopy(self._durations)
        their_full_durations = deepcopy(other._durations)

        my_duration = max(list(my_full_durations.values()))
        their_duration = max(list(their_full_durations.values()))
        
        # We assume that students stayed only as long as the longest interaction that they recorded
        my_full_durations[self._reporter.get_name()] = my_duration
        their_full_durations[other._reporter.get_name()] = their_duration

        for name in my_full_durations.keys(): # If a student left early, then it's okay that they recored lower numbers for everyone
            if my_full_durations[name] != their_full_durations[name]:
                if my_full_durations[name] > their_full_durations[name] and their_full_durations[name] != their_duration:
                    return False
                if my_full_durations[name] < their_full_durations[name] and my_full_durations[name] != my_duration:
                    return False

        return True
    
    
if __name__ == "__main__":
    student_A = Student("Student", "A", "email_A", "0", "0", "2")
    student_B = Student("Student", "B", "email_B", "1", "1", "2")
    student_C = Student("Student", "C", "email_C", "2", "2", "2")
    student_D = Student("Student", "D", "email_D", "3", "3", "2")

    interaction_0 = Interaction(student_A, "today", {
        student_B.get_name(): 20,
        student_C.get_name(): 20,
        student_D.get_name(): 20
    })
    interaction_1 = Interaction(student_B, "today", {
        student_A.get_name(): 20,
        student_C.get_name(): 20,
        student_D.get_name(): 20
    })

    print("First match:")
    print(interaction_0.leave_early_match(interaction_1))
    print(interaction_1.leave_early_match(interaction_0))

    interaction_2 = Interaction(student_A, "today", {
        student_B.get_name(): 10,
        student_C.get_name(): 20,
        student_D.get_name(): 20
    })
    interaction_3 = Interaction(student_B, "today", {
        student_A.get_name(): 10,
        student_C.get_name(): 10,
        student_D.get_name(): 10
    })

    print("Second match:")
    print(interaction_2.leave_early_match(interaction_3))
    print(interaction_3.leave_early_match(interaction_2))

    interaction_4 = Interaction(student_B, "today", {
        student_A.get_name(): 20,
        student_C.get_name(): 20,
        student_D.get_name(): 20
    })
    interaction_5 = Interaction(student_C, "today", {
        student_A.get_name(): 10,
        student_B.get_name(): 20,
        student_D.get_name(): 20
    })

    print("Third match:")
    print(interaction_4.leave_early_match(interaction_5))
    print(interaction_5.leave_early_match(interaction_4))
    print()


    # Full interaction test (expect match)

    interaction_6 = Interaction(student_A, "today", {
        student_B.get_name(): 20,
        student_C.get_name(): 20,
        student_D.get_name(): 20
    })
    interaction_7 = Interaction(student_B, "today", {
        student_A.get_name(): 20,
        student_C.get_name(): 20,
        student_D.get_name(): 20
    })
    interaction_8 = Interaction(student_C, "today", {
        student_A.get_name(): 20,
        student_B.get_name(): 20,
        student_D.get_name(): 20
    })
    interaction_9 = Interaction(student_D, "today", {
        student_A.get_name(): 20,
        student_B.get_name(): 20,
        student_C.get_name(): 20
    })

    print("Full test (expect match):")
    match_test_interactions = [interaction_6, interaction_7, interaction_8, interaction_9]
    for combination in list(combinations(match_test_interactions, 2)):
        if (not combination[0].leave_early_match(combination[1])) or (not combination[1].leave_early_match(combination[0])):
            print(f"Failure! {combination[0]} does not equal {combination[1]}")
    
    print("If no errors, then success!")
    print()


    interaction_10 = Interaction(student_A, "today", {
        student_B.get_name(): 20,
        student_C.get_name(): 20,
        student_D.get_name(): 20
    })
    interaction_11 = Interaction(student_B, "today", {
        student_A.get_name(): 10,
        student_C.get_name(): 20,
        student_D.get_name(): 20
    })
    interaction_12 = Interaction(student_C, "today", {
        student_A.get_name(): 10,
        student_B.get_name(): 20,
        student_D.get_name(): 20
    })
    interaction_13 = Interaction(student_D, "today", {
        student_A.get_name(): 10,
        student_B.get_name(): 20,
        student_C.get_name(): 20
    })

    print("Full test:")
    print("Expect match:")
    if (not interaction_11.leave_early_match(interaction_12)) or (not interaction_12.leave_early_match(interaction_11)):
            print(f"Failure! {interaction_11} does not equal {interaction_12}")
    print("Expect match:")
    if (not interaction_12.leave_early_match(interaction_13)) or (not interaction_13.leave_early_match(interaction_12)):
            print(f"Failure! {interaction_12} does not equal {interaction_13}")
    
    print("Expect failure:")
    if (not interaction_10.leave_early_match(interaction_11)) or (not interaction_11.leave_early_match(interaction_10)):
            print(f"Failure! {interaction_10} does not equal {interaction_11}")
    
    print("Expect failure:")
    if (not interaction_10.leave_early_match(interaction_12)) or (not interaction_12.leave_early_match(interaction_10)):
            print(f"Failure! {interaction_10} does not equal {interaction_12}")
    
    print("Expect failure:")
    if (not interaction_10.leave_early_match(interaction_13)) or (not interaction_13.leave_early_match(interaction_10)):
            print(f"Failure! {interaction_10} does not equal {interaction_13}")








    
