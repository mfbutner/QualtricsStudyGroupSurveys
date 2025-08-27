import os
import json
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from QualtricsStudyGroupSurveys import QualtricsConnection

load_dotenv()

def get_date_range(start_date: datetime, end_date: datetime):
    delta = end_date - start_date
    return [start_date + timedelta(days=i) for i in range(delta.days + 1)]

def get_date_choices(start_date: datetime, end_date: datetime):
    range = get_date_range(start_date, end_date)
    choices = {}
    for i, date in enumerate(range):
        choices[str(i+1)] = {
            "Display": date.strftime("%m-%d-%Y")
        }
    return choices

def build_person_choice(first_name: str, last_name: str, team_value: str, email: str):
    name = f"{first_name.strip()} {last_name.strip()}"

    team_info = (
        '<span class="ConjDesc">If</span> '
        '<span class="LeftOpDesc">Team</span> '
        '<span class="OpDesc">Is Equal to</span> '
        f'<span class="RightOpDesc"> {team_value} </span>'
    )
    email_info = (
        '<span class="ConjDesc">And</span>'
        '<span class="schema_desc">Contact List</span>'
        '<span class="select_val_desc LeftOperand_desc">Email</span>'
        '<span class="select_val_desc Operator_desc">Is Not Equal to</span>'
        f'<span class="textbox_val_desc RightOperand_desc">{email}</span>'
    )

    with open("question_templates/build_person_choice.json", "r", encoding="utf-8") as f:
        template_content = json.load(f)

    template_content["Display"] = name
    template_content["DisplayLogic"]["0"]["0"]["RightOperand"] = team_value
    template_content["DisplayLogic"]["0"]["1"]["RightOperand"] = email
    template_content["DisplayLogic"]["0"]["0"]["Description"] = team_info
    template_content["DisplayLogic"]["0"]["1"]["Description"] = email_info

    return template_content

def meet_count_question():
    with open("question_templates/meet_count_question.json", "r", encoding="utf-8") as f:
        template_content = json.load(f)

    return template_content

def no_meeting_explanation():
    with open("question_templates/no_meeting_explanation.json", "r", encoding="utf-8") as f:
        template_content = json.load(f)

    return template_content

def no_meeting_upload_question():
    with open("question_templates/no_meeting_upload_question.json", "r", encoding="utf-8") as f:
        template_content = json.load(f)

    return template_content

def who_did_you_meet_with_question(people):
    choices = {}
    for i, (first, last, team, email) in enumerate(people, start=1):
        choices[str(i)] = build_person_choice(first, last, team, email)

    with open("question_templates/who_did_you_meet_with_question.json", "r", encoding="utf-8") as f:
        template_content = json.load(f)

    template_content["Choices"] = choices
    template_content["ChoiceOrder"] = list(range(1, len(choices) + 1))
    template_content["NextChoiceId"] = len(choices) + 1

    return template_content

def meeting_date_question(start_date: datetime, end_date: datetime):
    dates = get_date_choices(start_date, end_date)

    with open("question_templates/meeting_date_question.json", "r", encoding="utf-8") as f:
        base = json.load(f)

    base["Choices"] = dates
    base["ChoiceOrder"] = list(range(1, len(dates)+1))
    base["NextChoiceId"] = len(dates) + 1

    return base

def meeting_activities_question():
    with open("question_templates/meeting_activities_question.json", "r", encoding="utf-8") as f:
        template_content = json.load(f)

    return template_content

def meeting_duration_question():
    with open("question_templates/meeting_duration_question.json", "r", encoding="utf-8") as f:
        template_content = json.load(f)

    return template_content

def who_did_you_not_meet_with_question(people):
    choices = {}
    for i, (first, last, team, email) in enumerate(people, start=1):
        choices[str(i)] = build_person_choice(first, last, team, email)
    choices[str(len(choices)+1)] = {
        "Display": "I met with everyone in my group",
        "ExclusiveAnswer": True
    }    
    
    with open("question_templates/who_did_you_not_meet_with_question.json", "r", encoding="utf-8") as f:
        template_content = json.load(f)  

    template_content["Choices"] = choices
    template_content["ChoiceOrder"] = list(range(1, len(choices) + 1))
    template_content["NextChoiceId"] = len(choices) + 1

    return template_content

def build_people_list(csv_path):
    df = pd.read_csv(csv_path)
    people = []
    for row in df.itertuples():
        first_name = row.FirstName
        last_name = row.LastName
        team = str(row.Team)
        email = row.Email
        people.append((first_name, last_name, team, email))
    return people

def generate_survey(qualtrics_connection: QualtricsConnection, survey_id, start_date, end_date, people) -> None:
    qualtrics_connection.add_question(survey_id, meet_count_question())
    qualtrics_connection.add_question(survey_id, no_meeting_explanation())
    # qualtrics_connection.add_question(survey_id, no_meeting_upload_question())
    qualtrics_connection.add_question(survey_id, who_did_you_meet_with_question(people))
    qualtrics_connection.add_question(survey_id, meeting_date_question(start_date, end_date))
    qualtrics_connection.add_question(survey_id, meeting_activities_question())
    qualtrics_connection.add_question(survey_id, meeting_duration_question())
    qualtrics_connection.add_question(survey_id, who_did_you_not_meet_with_question(people))
    print("Added all questions")



if __name__ == "__main__":
    start = "08-27-2027"
    end = "09-02-2027"
    date_format = "%m-%d-%Y"
    start_date = datetime.strptime(start, date_format)
    end_date = datetime.strptime(end, date_format)
    people = build_people_list("data/ExampleContacts.csv")
    qualtrics = QualtricsConnection(os.getenv("Q_DATA_CENTER"), os.getenv("Q_API_TOKEN"))
    generate_survey(qualtrics, os.getenv("Q_TEST_SURVEY_ID"), start_date, end_date, people)
