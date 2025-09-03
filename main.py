import sys
from QualtricsStudyGroupSurveys import QualtricsConnection, OathInformation
from QualtricsStudyGroupSurveys.display_data import fetch_qualtrics_response_data, build_streamlit


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
    response_data = fetch_qualtrics_response_data(qualtrics, survey_id)
    build_streamlit(response_data)

if __name__ == '__main__':
    # main()
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    qualtrics = QualtricsConnection(os.getenv("Q_DATA_CENTER"), os.getenv("Q_API_TOKEN"))
    response_data = fetch_qualtrics_response_data(qualtrics, os.getenv("Q_TEST_SURVEY_ID"))
    build_streamlit(response_data)
