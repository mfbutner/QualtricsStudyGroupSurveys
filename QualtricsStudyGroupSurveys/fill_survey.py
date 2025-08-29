import json
from QualtricsStudyGroupSurveys import QualtricsConnection


def fill_question_template(question: dict):
    return question

def fill_survey(qualtrics, survey_id, date_choices, people) -> None:
    response = qualtrics.get_questions(survey_id)
    questions_list = response.get("elements", [])

    for question in questions_list:
        with open("data/fill_survey_output.txt", "a") as f:
            f.write(json.dumps(question, indent=4))

        question_id = question.get("QuestionID")
        patched_question = fill_question_template(question)
        qualtrics.update_question(survey_id, question_id, patched_question)
