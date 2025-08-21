from Project.survey import Survey
from Project.CSV_reader import CSV_reader

def main():
    survey:Survey
    with open("test.csv", "r") as survey_config_file:
        survey = CSV_reader.make_survey_from_CSV(survey_config_file, "Test-Butner-Survey")
    survey.pushToQualtrics("blah", "de-blah")

if __name__ == "__main__":
    main()