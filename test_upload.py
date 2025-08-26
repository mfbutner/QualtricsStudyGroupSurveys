import json
import sys
import os
from dotenv import load_dotenv
from QualtricsStudyGroupSurveys import QualtricsConnection

load_dotenv()

DATA_CENTER = os.getenv("Q_DATA_CENTER")
API_TOKEN = os.getenv("Q_API_TOKEN")
SURVEY_ID = os.getenv("Q_TEST_SURVEY_ID")
BUTNER_SURVEY_ID = os.getenv("Q_BUTNER_SURVEY_ID")

def upload_survey_questions(survey_id: str, qualtrics_connection: QualtricsConnection, questions_json: dict):
    endpoint = f"/API/v3/survey-definitions/{survey_id}/questions"
    headers = {}

    response = qualtrics_connection.connection.post(endpoint, headers=headers, json=questions_json)
    # response.raise_for_status()
    return response.json()

sample_question_info = {
    "QuestionText": "Who did you meet with during your meeting?",
    "QuestionType": "MC",
	"Selector": "MAVR",
	"SubSelector": "TX",
    "QuestionDescription": "Who did you meet with during your meeting?",
	"ChoiceOrder": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
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
                        "Conjunction": "And"
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
                        "Conjunction": "And"
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
                        "Conjunction": "And"
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
                        "Conjunction": "And"
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
                        "Conjunction": "And"
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
                        "Conjunction": "And"
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
                        "Conjunction": "And"
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
                        "Conjunction": "And"
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
                        "Conjunction": "And"
                    },
                    "Type": "If"
                },
                "Type": "BooleanExpression",
                "inPage": False
            }
        }
    },
	"Validation": { 
        "Settings": { 
            "ForceResponse": "OFF",
            "Type": "None" 
        }
    },
	"Configuration": {
		"QuestionDescriptionOption": "UseText"
	}
}


question_info = {
    "QuestionText": "Who did you meet with during your meeting?",
    "DefaultChoices": False,
    "DataExportTag": "Q3.2",
    "QuestionID": "QID20",
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
                        "LeftOperand": "m://Email",
                        "Operator": "NotEqualTo",
                        "RightOperand": "Team1Person1@ucdavis.edu",
                        "Type": "Expression",
                        "Description": "<span class=\"ConjDesc\">And</span><span class=\"schema_desc\">Contact List</span><span class=\"select_val_desc LeftOperand_desc\">Email</span><span class=\"select_val_desc Operator_desc\">Is Not Equal to</span><span class=\"textbox_val_desc RightOperand_desc\">Team1Person1@ucdavis.edu</span>",
                        "Conjunction": "And"
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
                        "LeftOperand": "m://Email",
                        "Operator": "NotEqualTo",
                        "RightOperand": "Team1Person2@ucdavis.edu",
                        "Type": "Expression",
                        "Description": "<span class=\"ConjDesc\">And</span><span class=\"schema_desc\">Contact List</span><span class=\"select_val_desc LeftOperand_desc\">Email</span><span class=\"select_val_desc Operator_desc\">Is Not Equal to</span><span class=\"textbox_val_desc RightOperand_desc\">Team1Person2@ucdavis.edu</span>",
                        "Conjunction": "And"
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
                        "LeftOperand": "m://Email",
                        "Operator": "NotEqualTo",
                        "RightOperand": "Team1Person3@ucdavis.edu",
                        "Type": "Expression",
                        "Description": "<span class=\"ConjDesc\">And</span><span class=\"schema_desc\">Contact List</span><span class=\"select_val_desc LeftOperand_desc\">Email</span><span class=\"select_val_desc Operator_desc\">Is Not Equal to</span><span class=\"textbox_val_desc RightOperand_desc\">Team1Person3@ucdavis.edu</span>",
                        "Conjunction": "And"
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
                        "LeftOperand": "m://Email",
                        "Operator": "NotEqualTo",
                        "RightOperand": "Team1Person4@ucdavis.edu",
                        "Type": "Expression",
                        "Description": "<span class=\"ConjDesc\">And</span><span class=\"schema_desc\">Contact List</span><span class=\"select_val_desc LeftOperand_desc\">Email</span><span class=\"select_val_desc Operator_desc\">Is Not Equal to</span><span class=\"textbox_val_desc RightOperand_desc\">Team1Person4@ucdavis.edu</span>",
                        "Conjunction": "And"
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
                        "LeftOperand": "m://Email",
                        "Operator": "NotEqualTo",
                        "RightOperand": "Team1Person5@ucdavis.edu",
                        "Type": "Expression",
                        "Description": "<span class=\"ConjDesc\">And</span><span class=\"schema_desc\">Contact List</span><span class=\"select_val_desc LeftOperand_desc\">Email</span><span class=\"select_val_desc Operator_desc\">Is Not Equal to</span><span class=\"textbox_val_desc RightOperand_desc\">Team1Person5@ucdavis.edu</span>",
                        "Conjunction": "And"
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
                        "LeftOperand": "m://Email",
                        "Operator": "NotEqualTo",
                        "RightOperand": "Team2Person1@ucdavis.edu",
                        "Type": "Expression",
                        "Description": "<span class=\"ConjDesc\">And</span><span class=\"schema_desc\">Contact List</span><span class=\"select_val_desc LeftOperand_desc\">Email</span><span class=\"select_val_desc Operator_desc\">Is Not Equal to</span><span class=\"textbox_val_desc RightOperand_desc\">Team2Person1@ucdavis.edu</span>",
                        "Conjunction": "And"
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
                        "LeftOperand": "m://Email",
                        "Operator": "NotEqualTo",
                        "RightOperand": "Team2Person2@ucdavis.edu",
                        "Type": "Expression",
                        "Description": "<span class=\"ConjDesc\">And</span><span class=\"schema_desc\">Contact List</span><span class=\"select_val_desc LeftOperand_desc\">Email</span><span class=\"select_val_desc Operator_desc\">Is Not Equal to</span><span class=\"textbox_val_desc RightOperand_desc\">Team2Person2@ucdavis.edu</span>",
                        "Conjunction": "And"
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
                        "LeftOperand": "m://Email",
                        "Operator": "NotEqualTo",
                        "RightOperand": "Team2Person3@ucdavis.edu",
                        "Type": "Expression",
                        "Description": "<span class=\"ConjDesc\">And</span><span class=\"schema_desc\">Contact List</span><span class=\"select_val_desc LeftOperand_desc\">Email</span><span class=\"select_val_desc Operator_desc\">Is Not Equal to</span><span class=\"textbox_val_desc RightOperand_desc\">Team2Person3@ucdavis.edu</span>",
                        "Conjunction": "And"
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
                        "LeftOperand": "m://Email",
                        "Operator": "NotEqualTo",
                        "RightOperand": "Team2Person4@ucdavis.edu",
                        "Type": "Expression",
                        "Description": "<span class=\"ConjDesc\">And</span><span class=\"schema_desc\">Contact List</span><span class=\"select_val_desc LeftOperand_desc\">Email</span><span class=\"select_val_desc Operator_desc\">Is Not Equal to</span><span class=\"textbox_val_desc RightOperand_desc\">Team2Person4@ucdavis.edu</span>",
                        "Conjunction": "And"
                    },
                    "Type": "If"
                },
                "Type": "BooleanExpression",
                "inPage": False
            }
        }
    },
    "ChoiceOrder": [1,2,3,4,5,6,7,8,9],
    "Validation": {
        "Settings": {
            "ForceResponse": "ON",
            "ForceResponseType": "ON",
            "Type": "MinChoices",
            "MinChoices": "1"
        }
    },
    "Language": [],
    "GradingData": [],
    "NextChoiceId": 10,
    "NextAnswerId": 1,
    "QuestionText_Unsafe": "Who did you meet with during your meeting?"
}


if __name__ == "__main__":
    qualtrics = QualtricsConnection(DATA_CENTER, API_TOKEN)
    res = upload_survey_questions(SURVEY_ID, qualtrics, sample_question_info)
    # res = qualtrics.download_all_survey_attributes(BUTNER_SURVEY_ID, r'PATH_TO_DOWNLOAD_SURVEY_INFO_TO', create_dir_if_missing=True, create_parents=True)
    print(json.dumps(res, indent=4))