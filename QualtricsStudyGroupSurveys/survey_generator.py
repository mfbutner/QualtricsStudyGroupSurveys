from typing import List
from .student import Student
from .survey import Survey
from .question import Multiple_Choice, Text_Entry, File_Upload, Selector
from .survey_validate import Optional_Response, Required_MAVR, Required_SAVR_DL, Min_Chars, Number_In_Range
from .display_logic import Display_My_Team, Display_Only_If_Response_Matches
from .mc_choice import Choice

class Survey_Generator:
    @staticmethod
    def generate_survey_from_students(students:List[Student], dates:List[int], activities:List[str], durations:List[str], survey_name:str, survey_id:str) -> Survey: # TODO: different datatype for dates. Probably datetime.
        survey = Survey(survey_name, survey_id)
        survey.addQuestion(Text_Entry("Q1.1", "How many times did you meet with your group this week? Report at most your top 10 interactions.",
                           Number_In_Range(0,10), Selector.SL, None))
        survey.addQuestion(Text_Entry("Q2.1", "Please explain why you didn't meet with your group this week.", Min_Chars(10), Selector.ESTB,
                           Display_Only_If_Response_Matches("QID1")))
        survey.addQuestion(File_Upload("Q2.2", "Please upload any supporting screenshots, images, or other files that support why you didn't meet" \
                                       "with your group. For example, if you didn't meet with your group because you reached out to them but no one" \
                                       "responded, include those screen shots here.<br><br>If you need to upload multiple files, you will need to" \
                                       "zip them first. <br><br>This question is optional.<br>", Optional_Response(), Display_Only_If_Response_Matches("QID1")))
        
        q3_1 = Multiple_Choice("Q3.1", "When was your ${lm://Field/2} meeting?", Required_SAVR_DL(), Selector.DL, False, [])
        for date in dates:
            q3_1.addChoice(Choice(f"Date{date}", f"Date{date}", False, None))
        q3_1.addChoice(Choice("Click to write Choice 4", "Click to write Choice 4", False, None))
        survey.addQuestion(q3_1)

        q3_2 = Multiple_Choice("Q3.2", "Who did you meet with during your ${lm://Field/2} meeting?", Required_MAVR(), Selector.MAVR, True, [])
        for student in students:
            q3_2.addChoice(Choice(student.get_name_first_last(), student.get_name_first_last(), False, Display_My_Team(student)))
        survey.addQuestion(q3_2)

        q3_3 = Multiple_Choice("Q3.3", "What did you do during your ${lm://Field/2} meeting?", Required_MAVR(), Selector.MAVR, True, [])
        for activity in activities:
            q3_3.addChoice(Choice(activity, activity, False, None))
        survey.addQuestion(q3_3)

        q3_4 = Multiple_Choice("Q3.4", "How long did your ${lm://Field/2} meeting last?", Required_SAVR_DL(), Selector.SAVR, True, [])
        for duration in durations:
            q3_4.addChoice(Choice(f"{duration} minutes", f"{duration} minutes", False, None))
        survey.addQuestion(q3_4)

        q3_5 = Multiple_Choice("Q4.1", "Who did you NOT meet with this week?", Required_MAVR(), Selector.MAVR, True, [])
        for student in students:
            q3_5.addChoice(Choice(student.get_name_first_last(), student.get_name_first_last(), False, Display_My_Team(student)))
        q3_5.addChoice(Choice("I met with everyone in my group", "I met with everyone in my group", True, None))
        survey.addQuestion(q3_5)       

        return survey
