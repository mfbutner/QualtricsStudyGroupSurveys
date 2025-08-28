import os
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from .qualtrics_connection import QualtricsConnection

from .questions import (
    meet_count_question,
    no_meeting_explanation,
    no_meeting_upload_question,
    who_did_you_meet_with_question,
    meeting_date_question,
    meeting_activities_question,
    meeting_duration_question,
    who_did_you_not_meet_with_question
)
from .blocks import create_block_and_return_id, get_loop_options

load_dotenv()


def get_date_range(start_date: datetime, end_date: datetime):
    delta = end_date - start_date
    return [start_date + timedelta(days=i) for i in range(delta.days + 1)]

def get_date_choices(start_date: datetime | str, end_date: datetime | str):
    date_format = "%m-%d-%Y"
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, date_format)
    
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, date_format)

    range = get_date_range(start_date, end_date)
    choices = {}
    for i, date in enumerate(range):
        choices[str(i+1)] = {
            "Display": date.strftime("%m-%d-%Y")
        }
    return choices

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


def generate_survey(qualtrics_connection: QualtricsConnection, survey_id, date_choices, people) -> None:
    met_with_group_block_id = create_block_and_return_id(qualtrics_connection, survey_id, "Met with group?")
    meet_count_question_response = qualtrics_connection.add_question(survey_id, met_with_group_block_id, meet_count_question())
    meet_count_question_id = meet_count_question_response.get("result", {}).get("QuestionID", "")

    no_meeting_block_id = create_block_and_return_id(qualtrics_connection, survey_id, "Explanation for why you didn't meet")
    qualtrics_connection.add_question(survey_id, no_meeting_block_id, no_meeting_explanation(meet_count_question_id))
    # qualtrics_connection.add_question(survey_id, no_meeting_block_id, no_meeting_upload_question(meet_count_question_id))
    
    meeting_details_loop_options = get_loop_options(meet_count_question_id)
    meeting_details_block_id = create_block_and_return_id(qualtrics_connection, survey_id, "Meeting details", meeting_details_loop_options)
    qualtrics_connection.add_question(survey_id, meeting_details_block_id, who_did_you_meet_with_question(people))
    qualtrics_connection.add_question(survey_id, meeting_details_block_id, meeting_date_question(date_choices))
    qualtrics_connection.add_question(survey_id, meeting_details_block_id, meeting_activities_question())
    qualtrics_connection.add_question(survey_id, meeting_details_block_id, meeting_duration_question())
    
    who_did_you_not_meet_block_id = create_block_and_return_id(qualtrics_connection, survey_id, "Who didn't you meet with?")
    qualtrics_connection.add_question(survey_id, who_did_you_not_meet_block_id, who_did_you_not_meet_with_question(people))


if __name__ == "__main__":
    start = "08-27-2027"
    end = "09-02-2027"
    date_choices = get_date_choices(start, end)
    people = build_people_list("data/ExampleContacts.csv")
    qualtrics = QualtricsConnection(os.getenv("Q_DATA_CENTER"), os.getenv("Q_API_TOKEN"))
    generate_survey(qualtrics, os.getenv("Q_TEST_SURVEY_ID"), date_choices, people)
