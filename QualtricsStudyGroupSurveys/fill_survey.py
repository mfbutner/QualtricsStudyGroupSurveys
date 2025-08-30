import json
from jinja2 import Environment
from .qualtrics_connection import QualtricsConnection

def TEMP_WRITE_QUESTION_TO_FILE(question):
    # TODO delete this guy
    with open("data/fill_survey_output.txt", "a") as f:
        f.write(json.dumps(question, indent=4))

def fill_question_template(question: dict):
    return question

def object_needs_update(question, environment):
    for val in question.values():
        if isinstance(val, str) and "{{" in val and "}}" in val:
            return True
        if isinstance(val, list):
            for item in val:
                if isinstance(item, str) and "{{" in item and "}}" in item:
                    return True
        if isinstance(val, dict):
            if object_needs_update(val, environment):
                return True
        return False
    
    

def fill_survey(qualtrics_connection, survey_id, date_choices, people):
    environment = Environment()
    response = qualtrics_connection.get_questions(survey_id)
    questions_list = response.get("elements", [])

    for question in questions_list:
        TEMP_WRITE_QUESTION_TO_FILE(question)
        if object_needs_update(question, environment):
            question_id = question.get("QuestionID")
            patched_question = fill_question_template(question)
            qualtrics_connection.update_question(survey_id, question_id, patched_question)
