import json
import sys
import os
from dotenv import load_dotenv
from QualtricsStudyGroupSurveys import QualtricsConnection, OathInformation
from QualtricsStudyGroupSurveys import generate_survey, build_people_list, get_date_choices

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


def test_create_question(qualtrics_connection: QualtricsConnection):
    survey_id = 'SV_8qA5Z7zoSCI3PKK'
    endpoint = f'/API/v3/survey-definitions/{survey_id}/questions'
    headers = {
        "Content-Type": "application/json"
    }

    question = {
        "QuestionText": "Who did you meet with during your meeting?",
        "DefaultChoices": False,
        "DataExportTag": "Q3.2",
        "QuestionID": "QID1",
        "QuestionType": "MC",
        "Selector": "MAVR",
        "SubSelector": "TX",
        "DataVisibility": {
            "Private": False,
            "Hidden": False
        },
        "Configuration": {
            "QuestionDescriptionOption": "UseText"
        },
        "QuestionDescription": "Who did you meet with during your meeting?",
        "Choices": {
            "1": {
                "Display": "Person 1 Team1",
                "DisplayLogic": {
                    "0": {
                        "0": {
                            "LogicType": "EmbeddedField",
                            "LeftOperand": "Team",
                            "Operator": "EqualTo",
                            "RightOperand": "1",
                            "Type": "Expression",
                            "Description": "<span class=\"ConjDesc\">If</span> <span class=\"LeftOpDesc\">Team</span> <span class=\"OpDesc\">Is Equal to</span> <span class=\"RightOpDesc\"> 1 </span>"
                        },
                        "1": {
                            "LogicType": "PanelData",
                            "LeftOperand": "m://Email1",
                            "Operator": "NotEqualTo",
                            "RightOperand": "Team1Person1@ucdavis.edu",
                            "Type": "Expression",
                            "Description": "<span class=\"ConjDesc\">And</span><span class=\"schema_desc\">Contact List</span><span class=\"select_val_desc LeftOperand_desc\">Email</span><span class=\"select_val_desc Operator_desc\">Is Not Equal to</span><span class=\"textbox_val_desc RightOperand_desc\">Team1Person1@ucdavis.edu</span>",
                            "Conjuction": "And"
                        },
                        "Type": "If"
                    },
                    "Type": "BooleanExpression",
                    "inPage": False
                }
            },
            "2": {
                "Display": "Person 2 Team 1",
                "DisplayLogic": {
                    "0": {
                        "0": {
                            "LogicType": "EmbeddedField",
                            "LeftOperand": "Team",
                            "Operator": "EqualTo",
                            "RightOperand": "1",
                            "Type": "Expression",
                            "Description": "<span class=\"ConjDesc\">If</span> <span class=\"LeftOpDesc\">Team</span> <span class=\"OpDesc\">Is Equal to</span> <span class=\"RightOpDesc\"> 1 </span>"
                        },
                        "1": {
                            "LogicType": "PanelData",
                            "LeftOperand": "m://Email1",
                            "Operator": "NotEqualTo",
                            "RightOperand": "Team1Person2@ucdavis.edu",
                            "Type": "Expression",
                            "Description": "<span class=\"ConjDesc\">And</span><span class=\"schema_desc\">Contact List</span><span class=\"select_val_desc LeftOperand_desc\">Email</span><span class=\"select_val_desc Operator_desc\">Is Not Equal to</span><span class=\"textbox_val_desc RightOperand_desc\">Team1Person2@ucdavis.edu</span>",
                            "Conjuction": "And"
                        },
                        "Type": "If"
                    },
                    "Type": "BooleanExpression",
                    "inPage": False
                }
            },
            "3": {
                "Display": "Person 3 Team 1",
                "DisplayLogic": {
                    "0": {
                        "0": {
                            "LogicType": "EmbeddedField",
                            "LeftOperand": "Team",
                            "Operator": "EqualTo",
                            "RightOperand": "1",
                            "Type": "Expression",
                            "Description": "<span class=\"ConjDesc\">If</span> <span class=\"LeftOpDesc\">Team</span> <span class=\"OpDesc\">Is Equal to</span> <span class=\"RightOpDesc\"> 1 </span>"
                        },
                        "1": {
                            "LogicType": "PanelData",
                            "LeftOperand": "m://Email1",
                            "Operator": "NotEqualTo",
                            "RightOperand": "Team1Person3@ucdavis.edu",
                            "Type": "Expression",
                            "Description": "<span class=\"ConjDesc\">And</span><span class=\"schema_desc\">Contact List</span><span class=\"select_val_desc LeftOperand_desc\">Email</span><span class=\"select_val_desc Operator_desc\">Is Not Equal to</span><span class=\"textbox_val_desc RightOperand_desc\">Team1Person3@ucdavis.edu</span>",
                            "Conjuction": "And"
                        },
                        "Type": "If"
                    },
                    "Type": "BooleanExpression",
                    "inPage": False
                }
            },
            "4": {
                "Display": "Person 4 Team 1",
                "DisplayLogic": {
                    "0": {
                        "0": {
                            "LogicType": "EmbeddedField",
                            "LeftOperand": "Team",
                            "Operator": "EqualTo",
                            "RightOperand": "1",
                            "Type": "Expression",
                            "Description": "<span class=\"ConjDesc\">If</span> <span class=\"LeftOpDesc\">Team</span> <span class=\"OpDesc\">Is Equal to</span> <span class=\"RightOpDesc\"> 1 </span>"
                        },
                        "1": {
                            "LogicType": "PanelData",
                            "LeftOperand": "m://Email1",
                            "Operator": "NotEqualTo",
                            "RightOperand": "Team1Person4@ucdavis.edu",
                            "Type": "Expression",
                            "Description": "<span class=\"ConjDesc\">And</span><span class=\"schema_desc\">Contact List</span><span class=\"select_val_desc LeftOperand_desc\">Email</span><span class=\"select_val_desc Operator_desc\">Is Not Equal to</span><span class=\"textbox_val_desc RightOperand_desc\">Team1Person4@ucdavis.edu</span>",
                            "Conjuction": "And"
                        },
                        "Type": "If"
                    },
                    "Type": "BooleanExpression",
                    "inPage": False
                }
            },
            "5": {
                "Display": "Person 5 Team 1",
                "DisplayLogic": {
                    "0": {
                        "0": {
                            "LogicType": "EmbeddedField",
                            "LeftOperand": "Team",
                            "Operator": "EqualTo",
                            "RightOperand": "1",
                            "Type": "Expression",
                            "Description": "<span class=\"ConjDesc\">If</span> <span class=\"LeftOpDesc\">Team</span> <span class=\"OpDesc\">Is Equal to</span> <span class=\"RightOpDesc\"> 1 </span>"
                        },
                        "1": {
                            "LogicType": "PanelData",
                            "LeftOperand": "m://Email1",
                            "Operator": "NotEqualTo",
                            "RightOperand": "Team1Person5@ucdavis.edu",
                            "Type": "Expression",
                            "Description": "<span class=\"ConjDesc\">And</span><span class=\"schema_desc\">Contact List</span><span class=\"select_val_desc LeftOperand_desc\">Email</span><span class=\"select_val_desc Operator_desc\">Is Not Equal to</span><span class=\"textbox_val_desc RightOperand_desc\">Team1Person5@ucdavis.edu</span>",
                            "Conjuction": "And"
                        },
                        "Type": "If"
                    },
                    "Type": "BooleanExpression",
                    "inPage": False
                }
            },
            "6": {
                "Display": "Person 1 Team2",
                "DisplayLogic": {
                    "0": {
                        "0": {
                            "LogicType": "EmbeddedField",
                            "LeftOperand": "Team",
                            "Operator": "EqualTo",
                            "RightOperand": "2",
                            "Type": "Expression",
                            "Description": "<span class=\"ConjDesc\">If</span> <span class=\"LeftOpDesc\">Team</span> <span class=\"OpDesc\">Is Equal to</span> <span class=\"RightOpDesc\"> 2 </span>"
                        },
                        "1": {
                            "LogicType": "PanelData",
                            "LeftOperand": "m://Email1",
                            "Operator": "NotEqualTo",
                            "RightOperand": "Team2Person1@ucdavis.edu",
                            "Type": "Expression",
                            "Description": "<span class=\"ConjDesc\">And</span><span class=\"schema_desc\">Contact List</span><span class=\"select_val_desc LeftOperand_desc\">Email</span><span class=\"select_val_desc Operator_desc\">Is Not Equal to</span><span class=\"textbox_val_desc RightOperand_desc\">Team2Person1@ucdavis.edu</span>",
                            "Conjuction": "And"
                        },
                        "Type": "If"
                    },
                    "Type": "BooleanExpression",
                    "inPage": False
                }
            },
            "7": {
                "Display": "Person 2 Team 2",
                "DisplayLogic": {
                    "0": {
                        "0": {
                            "LogicType": "EmbeddedField",
                            "LeftOperand": "Team",
                            "Operator": "EqualTo",
                            "RightOperand": "2",
                            "Type": "Expression",
                            "Description": "<span class=\"ConjDesc\">If</span> <span class=\"LeftOpDesc\">Team</span> <span class=\"OpDesc\">Is Equal to</span> <span class=\"RightOpDesc\"> 2 </span>"
                        },
                        "1": {
                            "LogicType": "PanelData",
                            "LeftOperand": "m://Email1",
                            "Operator": "NotEqualTo",
                            "RightOperand": "Team2Person2@ucdavis.edu",
                            "Type": "Expression",
                            "Description": "<span class=\"ConjDesc\">And</span><span class=\"schema_desc\">Contact List</span><span class=\"select_val_desc LeftOperand_desc\">Email</span><span class=\"select_val_desc Operator_desc\">Is Not Equal to</span><span class=\"textbox_val_desc RightOperand_desc\">Team2Person2@ucdavis.edu</span>",
                            "Conjuction": "And"
                        },
                        "Type": "If"
                    },
                    "Type": "BooleanExpression",
                    "inPage": False
                }
            },
            "8": {
                "Display": "Person 3 Team 2",
                "DisplayLogic": {
                    "0": {
                        "0": {
                            "LogicType": "EmbeddedField",
                            "LeftOperand": "Team",
                            "Operator": "EqualTo",
                            "RightOperand": "2",
                            "Type": "Expression",
                            "Description": "<span class=\"ConjDesc\">If</span> <span class=\"LeftOpDesc\">Team</span> <span class=\"OpDesc\">Is Equal to</span> <span class=\"RightOpDesc\"> 2 </span>"
                        },
                        "1": {
                            "LogicType": "PanelData",
                            "LeftOperand": "m://Email1",
                            "Operator": "NotEqualTo",
                            "RightOperand": "Team2Person3@ucdavis.edu",
                            "Type": "Expression",
                            "Description": "<span class=\"ConjDesc\">And</span><span class=\"schema_desc\">Contact List</span><span class=\"select_val_desc LeftOperand_desc\">Email</span><span class=\"select_val_desc Operator_desc\">Is Not Equal to</span><span class=\"textbox_val_desc RightOperand_desc\">Team2Person3@ucdavis.edu</span>",
                            "Conjuction": "And"
                        },
                        "Type": "If"
                    },
                    "Type": "BooleanExpression",
                    "inPage": False
                }
            },
            "9": {
                "Display": "Person 4 Team 2",
                "DisplayLogic": {
                    "0": {
                        "0": {
                            "LogicType": "EmbeddedField",
                            "LeftOperand": "Team",
                            "Operator": "EqualTo",
                            "RightOperand": "2",
                            "Type": "Expression",
                            "Description": "<span class=\"ConjDesc\">If</span> <span class=\"LeftOpDesc\">Team</span> <span class=\"OpDesc\">Is Equal to</span> <span class=\"RightOpDesc\"> 2 </span>"
                        },
                        "1": {
                            "LogicType": "PanelData",
                            "LeftOperand": "m://Email1",
                            "Operator": "NotEqualTo",
                            "RightOperand": "Team2Person4@ucdavis.edu",
                            "Type": "Expression",
                            "Description": "<span class=\"ConjDesc\">And</span><span class=\"schema_desc\">Contact List</span><span class=\"select_val_desc LeftOperand_desc\">Email</span><span class=\"select_val_desc Operator_desc\">Is Not Equal to</span><span class=\"textbox_val_desc RightOperand_desc\">Team2Person4@ucdavis.edu</span>",
                            "Conjuction": "And"
                        },
                        "Type": "If"
                    },
                    "Type": "BooleanExpression",
                    "inPage": False
                }
            }
        },
        "ChoiceOrder": [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9
        ],
        "Validation": {
            "Settings": {
                "ForceResponse": "ON",
                "ForceResponseType": "ON",
                "Type": "MinChoices",
                "MinChoices": "1"
            }
        },
        "GradingData": [],
        "Language": [],
        "NextChoiceId": 10,
        "NextAnswerId": 1,
        "QuestionText_Unsafe": "Who did you meet with during your meeting?"
    },

    response = qualtrics_connection.connection.post(endpoint, headers=headers, json=question)
    with open(r'C:\Users\mfbut\PycharmProjects\QualtricsStudyGroupSurveys\dummy.json', 'w') as dummy_file:
        json.dump(response.json(), dummy_file)


if __name__ == '__main__':
    start = "08-27-2027"
    end = "09-02-2027"
    csv_path = "data/ExampleContacts.csv"

    date_choices = get_date_choices(start, end)
    people = build_people_list(csv_path)
    qualtrics = QualtricsConnection(os.getenv("Q_DATA_CENTER"), os.getenv("Q_API_TOKEN"))

    generate_survey(qualtrics, os.getenv("Q_TEST_SURVEY_ID"), date_choices, people)

    print("Done")