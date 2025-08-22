
if __name__ == '__main__':
    # first command line argument is the datacenter: https://iad1.qualtrics.com/
    # if two command line parameters are entered, then the second is assumed to be your API token
    # if 3 or 4 command line parameters are entered then
    # - sys.argv[2] is your oath client id
    # - sys.argv[3] is your oath client secret
    # - optionally, sys.argv[4] can be your scope, if not entered it will default to manage:all
    import sys
    import json
    from QualtricsStudyGroupSurveys import QualtricsConnection
    from QualtricsStudyGroupSurveys import OathInformation
    from QualtricsStudyGroupSurveys.CSV_reader import CSV_reader
    from QualtricsStudyGroupSurveys.survey_generator import Survey_Generator

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

    # print(qualtrics.who_am_i())
    surveys = qualtrics.list_surveys()
    # print(surveys)
    my_servey = surveys['elements'][0] if surveys['elements'][0]['name'] == 'Test-Butner-Survey' else surveys['elements'][1]
    # print(qualtrics.get_survey(my_servey['id']))
    questions = (qualtrics.get_questions(my_servey['id']))
    print(json.dumps(questions, indent=2))
    # students = CSV_reader.parse_CSV_for_students("ExampleContacts.csv")
    # activities = [f"Activity {i}" for i in range(1,4)]
    # survey = Survey_Generator.generate_survey_from_students(students, [1,2,3], activities, [5, 10, 20, "More than 20"], my_servey['name'])
    # survey.pushToQualtrics(qualtrics)
    # print(json.dumps(survey.generate_json(), indent=2)) # indent for pretty-print
