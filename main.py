import sys
import os
from dotenv import load_dotenv
from QualtricsStudyGroupSurveys import (
    QualtricsConnection, 
    OathInformation,
    fill_survey)
from QualtricsStudyGroupSurveys.helpers import get_date_choices, build_people_list

load_dotenv()

def main():
    # first command line argument is the datacenter: https://iad1.qualtrics.com/
    # if two command line parameters are entered, then the second is assumed to be your API token
    # if 3 or 4 command line parameters are entered then
    # - sys.argv[2] is your oath client id
    # - sys.argv[3] is your oath client secret
    # - optionally, sys.argv[4] can be your scope, if not entered it will default to manage:all

    match sys.argv:
        case [_, data_center, api_token]:
            qualtrics = QualtricsConnection(data_center, api_token)
        case [_, data_center, client_id, client_secret, scope]:
            oath = OathInformation(client_id, client_secret, scope)
            qualtrics = QualtricsConnection(data_center, oath)
        case [_, data_center, client_id, client_secret]:
            oath = OathInformation(client_id, client_secret)
            qualtrics = QualtricsConnection(data_center, oath)
        case _:
            print('Incorrect number of command line arguments entered')
            exit(1)

    survey_id = 'SURVEY_ID'
    dir_path = r'PATH_TO_DOWNLOAD_SURVEY_INFO_TO'
    qualtrics.download_all_survey_attributes(survey_id,
                                             dir_path)


if __name__ == '__main__':
    start = "08-27-2027"
    end = "09-02-2027"
    csv_path = "data/ExampleContacts.csv"

    date_choices = get_date_choices(start, end)
    people = build_people_list(csv_path)
    qualtrics = QualtricsConnection(os.getenv("Q_DATA_CENTER"), os.getenv("Q_API_TOKEN"))

    fill_survey(qualtrics, os.getenv("Q_TEST_SURVEY_ID"), date_choices, people)

    print("Done")