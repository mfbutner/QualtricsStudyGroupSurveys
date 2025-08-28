from QualtricsStudyGroupSurveys import QualtricsConnection
from QualtricsStudyGroupSurveys import OathInformation
from QualtricsStudyGroupSurveys.CSV_reader import CSV_reader
from QualtricsStudyGroupSurveys.survey_generator import Survey_Generator
from argparse import ArgumentParser, Namespace
from parse_env import load_from_env_file


def main():
    # first command line argument is the datacenter: https://iad1.qualtrics.com/
    # if two command line parameters are entered, then the second is assumed to be your API token
    # if 3 or 4 command line parameters are entered then
    # - sys.argv[2] is your oath client id
    # - sys.argv[3] is your oath client secret
    # - optionally, sys.argv[4] can be your scope, if not entered it will default to manage:all

    parser = ArgumentParser
    parser.add_argument(
        "datacenter",
        nargs="?",
        default="https://iad1.qualtrics.com/",
        help="Qualtrics datacenter URL (e.g., https://iad1.qualtrics.com/)",
    )
    parser.add_argument("api_token", nargs="?", help="API token for authentication")
    parser.add_argument("client_id", nargs="?", help="OAuth client ID")
    parser.add_argument("client_secret", nargs="?", help="OAuth client secret")
    parser.add_argument(
        "scope",
        nargs="?",
        default="manage:all",
        help="OAuth scope (default: manage:all)",
    )

    parser.add_argument("-h", action=help)
    parser.add_argument("-e", "--use-env", default=".env")

    args: Namespace = parser.parse_args()

    # Process Arguments
    if args.use_env:
        env_creds = load_from_env_file(args.use_env)
        datacenter = args.datacenter
        if not datacenter:
            raise parser.error(
                "Datacenter must be supplied as argument or via environment file"
            )
        if env_creds["api_token"]:
            connection = QualtricsConnection(
                datacenter, api_token=env_creds["api_token"]
            )
        elif env_creds["client_id"] and env_creds["client_secret"]:
            if env_creds["scope"]:
                oath = OathInformation(
                    client_id=env_creds["client_id"],
                    client_secret=env_creds["client_secret"],
                    scope=env_creds["scope"],
                )
            else:
                connection = QualtricsConnection(
                    datacenter,
                    oath=OathInformation(
                        client_id=args.client_id, client_secret=args.client_secret
                    ),
                )
        else:
            raise parser.error(
                "No valid set of credentials provided. Must provide either api token or both client id and client secret."
            )
    else:
        datacenter = args.datacenter
        if args.client_id and args.client_secret:
            oath = OathInformation(
                client_id=args.client_id, client_secret=args.client_secret
            )
            connection = QualtricsConnection(datacenter, oath)
        else:
            connection = QualtricsConnection(datacenter, api_token=args.api_token)

    surveys = connection.list_surveys()
    my_survey = (
        surveys["elements"][0]
        if surveys["elements"][0]["name"] == "Test-Butner-Survey"
        else surveys["elements"][1]
    )
    students = CSV_reader.parse_CSV_for_students("MyExampleContacts.csv")
    activities = [f"Activity {i}" for i in range(1, 4)]
    survey = Survey_Generator.generate_survey_from_students(
        students,
        [1, 2, 3],
        activities,
        [str(5), str(10), str(20), "More than 20"],
        my_survey["name"],
        my_survey["id"],
        connection,
    )
    survey.push_flows_to_qualtrics()
    # print(json.dumps(survey.generate_json(), indent=2)) # indent for pretty-print


if __name__ == "__main__":
    main()
