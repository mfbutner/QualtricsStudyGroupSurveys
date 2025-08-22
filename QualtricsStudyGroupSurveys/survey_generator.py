from typing import List
from .student import Student
from .survey import Survey
from .question import Multiple_Choice, Text_Entry, File_Upload, Selector
from .validation import Validation, Validation_Type
from .mc_choice import Choice

class Survey_Generator:
    @staticmethod
    def generate_survey_from_students(students:List[Student], dates:List[int], survey_name:str) -> Survey: # TODO: different datatype for dates. Probably datetime.
        survey = Survey(survey_name)
        survey.addQuestion(Text_Entry("Q1.1", "How many times did you meet with your group this week? Report at most your top 10 interactions.",
                           Validation(True, Validation_Type.VALIDNUMBER, {"maxDecimals":0, "maximum":10.0, "minimum":0.0}), Selector.SL))
        survey.addQuestion(Text_Entry("Q2.1", "Please explain why you didn't meet with your group this week.", 
                           Validation(True, Validation_Type.MINCHAR, {"minChars":10}), Selector.ESTB))
        survey.addQuestion(File_Upload("Q2.2", "Please upload any supporting screenshots, images, or other files that support why you didn't meet" \
                                       "with your group. For example, if you didn't meet with your group because you reached out to them but no one" \
                                       "responded, include those screen shots here.<br><br>If you need to upload multiple files, you will need to" \
                                       "zip them first. <br><br>This question is optional.<br>", Validation(False)))
        q3_1 = Multiple_Choice("Q1.3", "When was your ${lm://Field/2} meeting?", Validation(True), Selector.DL, False)
        for date in dates:
            q3_1.addChoice(Choice(f"Date{date}", f"Date{date}"))
        q3_1.addChoice(Choice("Click to write Choice 4", "Click to write Choice 4"))
        survey.addQuestion(q3_1)
        return survey
