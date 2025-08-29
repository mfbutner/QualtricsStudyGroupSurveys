import os
import json
from dotenv import load_dotenv
from QualtricsStudyGroupSurveys import QualtricsConnection

load_dotenv()

def fill_question_template(question: dict):
    pass

def fill_survey(qualtrics, survey_id: str) -> None:
    response = qualtrics.get_questions(survey_id)
    questions_list = response.get("elements", [])

    for question in questions_list:
        question_id = question.get("QuestionID")
        patched_question = fill_question_template(question)
        qualtrics.update_question(survey_id, question_id, patched_question)

if __name__ == "__main__":
    qualtrics = QualtricsConnection(os.getenv("Q_DATA_CENTER"), os.getenv("Q_API_TOKEN"))
    fill_survey(qualtrics, os.getenv("Q_TEST_SURVEY_ID"))