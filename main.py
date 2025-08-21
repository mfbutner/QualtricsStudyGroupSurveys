from QualtricsStudyGroupSurveys.survey import Survey
from QualtricsStudyGroupSurveys.CSV_reader import CSV_reader

if __name__ == '__main__':
    # first command line argument is the datacenter: https://iad1.qualtrics.com/
    # if two command line parameters are entered, then the second is assumed to be your API token
    # if 3 or 4 command line parameters are entered then
    # - sys.argv[2] is your oath client id
    # - sys.argv[3] is your oath client secret
    # - optionally, sys.argv[4] can be your scope, if not entered it will default to manage:all
    import sys
    from QualtricsStudyGroupSurveys import QualtricsConnection
    from QualtricsStudyGroupSurveys import OathInformation
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

    print(qualtrics.who_am_i())
    print(qualtrics.list_surveys())
    # print(qualtrics.get_survey('ENTER SURVEY ID HERE if using this'))

    survey:Survey
    with open("test.csv", "r") as survey_config_file:
        survey = CSV_reader.make_survey_from_CSV(survey_config_file, "Test-Butner-Survey")
    survey.pushToQualtrics("blah", "de-blah")
