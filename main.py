from Project.survey import Survey

def main():
    with open("filepath.csv", "r") as survey_config_file:
        survey = make_survey_from_CSV(survey_config_file)

if __name__ == "__main__":
    main()