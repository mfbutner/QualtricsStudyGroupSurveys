from Project.survey import Survey
from Project.CSV_reader import CSV_reader

def main():
    survey:Survey
    with open("filepath.csv", "r") as survey_config_file:
        survey = CSV_reader.make_survey_from_CSV(survey_config_file)
    survey.pushToQualtrics()

if __name__ == "__main__":
    main()