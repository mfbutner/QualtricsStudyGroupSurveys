import os
from dotenv import load_dotenv
from QualtricsStudyGroupSurveys import QualtricsConnection

load_dotenv()

def build_person_choice(display: str, team_value: str, person_email: str):
    return {
        "Display": display,
        "DisplayLogic": {
            "0": {
                "0": {
                    "LogicType": "EmbeddedField",
                    "LeftOperand": "Team",
                    "Operator": "EqualTo",
                    "RightOperand": str(team_value),
                    "Type": "Expression",
                    "Description": (
                        '<span class="ConjDesc">If</span> '
                        '<span class="LeftOpDesc">Team</span> '
                        '<span class="OpDesc">Is Equal to</span> '
                        f'<span class="RightOpDesc"> {team_value} </span>'
                    )
                },
                "1": {
                    "LogicType": "PanelData",
                    "LeftOperand": "m://Email1",
                    "Operator": "NotEqualTo",
                    "RightOperand": person_email,
                    "Type": "Expression",
                    "Description": (
                        '<span class="ConjDesc">And</span>'
                        '<span class="schema_desc">Contact List</span>'
                        '<span class="select_val_desc LeftOperand_desc">Email</span>'
                        '<span class="select_val_desc Operator_desc">Is Not Equal to</span>'
                        f'<span class="textbox_val_desc RightOperand_desc">{person_email}</span>'
                    ),
                    "Conjuction": "And"
                },
                "Type": "If"
            },
            "Type": "BooleanExpression",
            "inPage": False
        }
    }

WHO_MET_CHOICES = [
    ("Person 1 Team1", "1", "Team1Person1@ucdavis.edu"),
    ("Person 2 Team 1", "1", "Team1Person2@ucdavis.edu"),
    ("Person 3 Team 1", "1", "Team1Person3@ucdavis.edu"),
    ("Person 4 Team 1", "1", "Team1Person4@ucdavis.edu"),
    ("Person 5 Team 1", "1", "Team1Person5@ucdavis.edu"),
    ("Person 1 Team2", "2", "Team2Person1@ucdavis.edu"),
    ("Person 2 Team 2", "2", "Team2Person2@ucdavis.edu"),
    ("Person 3 Team 2", "2", "Team2Person3@ucdavis.edu"),
    ("Person 4 Team 2", "2", "Team2Person4@ucdavis.edu"),
]

def meet_count_question():
    return {
        "QuestionText": "How many times did you meet with your group this week? Report at most your top 10 interactions.",
        "DefaultChoices": False,
        "DataExportTag": "Q1.1",
        "QuestionType": "TE",
        "Selector": "SL",
        "DataVisibility": {"Private": False, "Hidden": False},
        "Configuration": {"QuestionDescriptionOption": "UseText"},
        "QuestionDescription": "How many times did you meet with your group this week? Report at most your top 10 interactions.",
        "Validation": {
            "Settings": {
                "ForceResponse": "ON",
                "ForceResponseType": "ON",
                "Type": "ContentType",
                "MinChars": "1",
                "ContentType": "ValidNumber",
                "ValidDateType": "DateWithFormat",
                "ValidPhoneType": "ValidUSPhone",
                "ValidZipType": "ValidUSZip",
                "ValidNumber": {"Min": "0", "Max": "10", "NumDecimals": "0"}
            }
        },
        "GradingData": [],
        "Language": [],
        "NextChoiceId": 3,
        "NextAnswerId": 1,
        "SearchSource": {"AllowFreeResponse": "false"}
    }

def _display_logic(qid: str, equals_text: str):
    return {
        "Type": "BooleanExpression",
        "inPage": False,
        "0": {
            "Type": "If",
            "0": {
                "LogicType": "Question",
                "QuestionID": qid,
                "QuestionIsInLoop": "no",
                "ChoiceLocator": f"q://{qid}/ChoiceTextEntryValue",
                "Operator": "EqualTo",
                "QuestionIDFromLocator": qid,
                "LeftOperand": f"q://{qid}/ChoiceTextEntryValue",
                "RightOperand": equals_text,
                "Type": "Expression",
                "Description": (
                    f'<span class="ConjDesc">If</span> '
                    f'<span class="QuestionDesc">{qid}</span> '
                    f'<span class="LeftOpDesc">Text Response</span> '
                    f'<span class="OpDesc">Is Equal to</span> '
                    f'<span class="RightOpDesc"> {equals_text} </span>'
                )
            }
        }
    }

def no_meeting_explanation(qid_meet_count: str):
    return {
        "QuestionText": "Please explain why you didn't meet with your group this week.",
        "DefaultChoices": False,
        "DataExportTag": "Q2.1",
        "QuestionType": "TE",
        "Selector": "ESTB",
        "DataVisibility": {"Private": False, "Hidden": False},
        "Configuration": {"QuestionDescriptionOption": "UseText"},
        "QuestionDescription": "Please explain why you didn't meet with your group this week.",
        "Validation": {"Settings": {"ForceResponse": "ON", "ForceResponseType": "ON", "Type": "MinChar", "MinChars": "10"}},
        "GradingData": [],
        "Language": [],
        "NextChoiceId": 4,
        "NextAnswerId": 1,
        "SearchSource": {"AllowFreeResponse": "false"},
        "DisplayLogic": _display_logic(qid_meet_count, "0")
    }

def no_meeting_upload_question(qid_meet_count: str):
    return {
        "QuestionText": (
            "Please upload any supporting screenshots, images, or other files that support why you didn't meet with your group. "
            "For example, if you didn't meet with your group because you reached out to them but no one responded, include those screen shots here.<br><br>"
            "If you need to upload multiple files, you will need to zip them first.&nbsp;<br><br>This question is optional.<br>"
        ),
        "DefaultChoices": False,
        "DataExportTag": "Q2.2",
        "QuestionType": "FileUpload",
        "Selector": "FileUpload",
        "DataVisibility": {"Private": False, "Hidden": False},
        "Configuration": {
            "QuestionDescriptionOption": "UseText",
            "MinSeconds": "0",
            "MaxSeconds": "0",
            "AudioOnly": False,
            "VideoUpload": False
        },
        "QuestionDescription": "Please upload any supporting screenshots, images, or other files that support why you didn't meet...",
        "Validation": {"Settings": {"ForceResponse": "OFF", "Type": "None"}},
        "GradingData": [],
        "Language": [],
        "NextChoiceId": 4,
        "NextAnswerId": 1,
        "ScreenCaptureText": "Capture Screen",
        "DisplayLogic": _display_logic(qid_meet_count, "0")
    }

def who_did_you_meet_with_question():
    choices = {}
    for i, (display, team, email) in enumerate(WHO_MET_CHOICES, start=1):
        choices[str(i)] = build_person_choice(display, team, email)

    return {
        "QuestionText": "Who did you meet with during your ${lm://Field/2} meeting?",
        "DefaultChoices": False,
        "DataExportTag": "Q3.2",
        "QuestionType": "MC",
        "Selector": "MAVR",
        "SubSelector": "TX",
        "DataVisibility": {"Private": False, "Hidden": False},
        "Configuration": {"QuestionDescriptionOption": "UseText"},
        "QuestionDescription": "Who did you meet with during your ${lm://Field/2} meeting?",
        "Choices": choices,
        "ChoiceOrder": list(range(1, len(WHO_MET_CHOICES) + 1)),
        "Validation": {"Settings": {"ForceResponse": "ON", "ForceResponseType": "ON", "Type": "MinChoices", "MinChoices": "1"}},
        "GradingData": [],
        "Language": [],
        "NextChoiceId": len(WHO_MET_CHOICES) + 1,
        "NextAnswerId": 1
    }

def meeting_date_question():
    return {
        "QuestionText": "When was your ${lm://Field/2} meeting?",
        "DefaultChoices": False,
        "DataExportTag": "Q3.1",
        "QuestionType": "MC",
        "Selector": "DL",
        "DataVisibility": {"Private": False, "Hidden": False},
        "Configuration": {"QuestionDescriptionOption": "UseText"},
        "QuestionDescription": "When was your ${lm://Field/2} meeting?",
        "Choices": {
            "1": {"Display": "Date1"},
            "2": {"Display": "Date2"},
            "3": {"Display": "Date3"},
            "4": {"Display": "Click to write Choice 4"}
        },
        "ChoiceOrder": [1, 2, 3, 4],
        "Validation": {"Settings": {"ForceResponse": "ON", "ForceResponseType": "ON", "Type": "None"}},
        "GradingData": [],
        "Language": [],
        "NextChoiceId": 5,
        "NextAnswerId": 1
    }

def meeting_activities_question():
    return {
        "QuestionText": "What did you do during your ${lm://Field/2} meeting?",
        "DefaultChoices": False,
        "DataExportTag": "Q3.3",
        "QuestionType": "MC",
        "Selector": "MAVR",
        "SubSelector": "TX",
        "DataVisibility": {"Private": False, "Hidden": False},
        "Configuration": {"QuestionDescriptionOption": "UseText"},
        "QuestionDescription": "What did you do during your ${lm://Field/2} meeting?",
        "Choices": {
            "1": {"Display": "Activity 1"},
            "2": {"Display": "Activity 2"},
            "3": {"Display": "Activity 3"}
        },
        "ChoiceOrder": [1, 2, 3],
        "Validation": {"Settings": {"ForceResponse": "ON", "ForceResponseType": "ON", "Type": "MinChoices", "MinChoices": "1"}},
        "GradingData": [],
        "Language": [],
        "NextChoiceId": 4,
        "NextAnswerId": 1
    }

def meeting_duration_question():
    return {
        "QuestionText": "How long did your&nbsp;${lm://Field/2} meeting last?",
        "DataExportTag": "Q3.4",
        "QuestionType": "MC",
        "Selector": "SAVR",
        "SubSelector": "TX",
        "DataVisibility": {"Private": False, "Hidden": False},
        "Configuration": {"QuestionDescriptionOption": "UseText"},
        "QuestionDescription": "How long did your ${lm://Field/2} meeting last?",
        "Choices": {
            "1": {"Display": "5 minutes"},
            "2": {"Display": "10 minutes"},
            "3": {"Display": "20 minutes"},
            "4": {"Display": "More than 20 minutes"}
        },
        "ChoiceOrder": [1, 2, 3, 4],
        "Validation": {"Settings": {"ForceResponse": "ON", "ForceResponseType": "ON", "Type": "None"}},
        "Language": [],
        "NextChoiceId": 5,
        "NextAnswerId": 1
    }

def who_did_you_not_meet_with_question():
    choices = {str(i): {"Display": f"Person {i}"} for i in range(1, 10)}
    choices["10"] = {"Display": "I met with everyone in my group", "ExclusiveAnswer": True}
    return {
        "QuestionText": "Who did you NOT meet with this week?",
        "DefaultChoices": False,
        "DataExportTag": "Q4.1",
        "QuestionType": "MC",
        "Selector": "MAVR",
        "SubSelector": "TX",
        "DataVisibility": {"Private": False, "Hidden": False},
        "Configuration": {"QuestionDescriptionOption": "UseText"},
        "QuestionDescription": "Who did you NOT meet with this week?",
        "Choices": choices,
        "ChoiceOrder": list(range(1, 11)),
        "Validation": {"Settings": {"ForceResponse": "ON", "ForceResponseType": "ON", "Type": "MinChoices", "MinChoices": "1"}},
        "GradingData": [],
        "Language": [],
        "NextChoiceId": 11,
        "NextAnswerId": 1
    }

def generate_survey(qualtrics_connection: QualtricsConnection, survey_id) -> None:
    meet_count = meet_count_question()
    resp = qualtrics_connection.add_question(survey_id, meet_count)
    qid_meet_count = resp['result']['QuestionID']

    #qualtrics_connection.add_question(survey_id, no_meeting_explanation(qid_meet_count))
    #qualtrics_connection.add_question(survey_id, no_meeting_upload_question(qid_meet_count))

    qualtrics_connection.add_question(survey_id, who_did_you_meet_with_question())
    qualtrics_connection.add_question(survey_id, meeting_date_question())
    qualtrics_connection.add_question(survey_id, meeting_activities_question())
    qualtrics_connection.add_question(survey_id, meeting_duration_question())

    qualtrics_connection.add_question(survey_id, who_did_you_not_meet_with_question())

if __name__ == "__main__":

    qualtrics = QualtricsConnection(os.getenv("Q_DATA_CENTER"), os.getenv("Q_API_TOKEN"))
    generate_survey(qualtrics, os.getenv("Q_TEST_SURVEY_ID"))
    print("Done")
