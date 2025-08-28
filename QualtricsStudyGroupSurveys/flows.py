
def embedded_data_flow(flow_id: str) -> dict:
    return {
        "Type": "EmbeddedData",
        "FlowID": flow_id,
        "EmbeddedData": [
            {
                "Description": "Team",
                "Type": "Recipient",
                "Field": "Team",
                "VariableType": "String",
                "DataVisibility": [],
                "AnalyzeText": False,
            },
            {
                "Description": "RecipientEmail",
                "Type": "Recipient",
                "Field": "RecipientEmail",
                "VariableType": "String",
                "DataVisibility": [],
                "AnalyzeText": False,
            },
        ],
    }

def standard_flow(flow_id: str, block_id: str) -> dict:
    return {
        "Type": "Standard",
        "ID": block_id,
        "FlowID": flow_id,
        "Autofill": []
    }

def build_branch_logic(meet_count_question_id: str) -> dict:
    locator = f"q://{meet_count_question_id}/ChoiceTextEntryValue"
    return {
        "0": {
            "0": {
                "LogicType": "Question",
                "QuestionID": meet_count_question_id,
                "QuestionIsInLoop": "no",
                "ChoiceLocator": locator,
                "Operator": "EqualTo",
                "QuestionIDFromLocator": meet_count_question_id,
                "LeftOperand": locator,
                "RightOperand": "0",
                "IgnoreCase": 1,
                "Type": "Expression",
            },
            "Type": "If",
        },
        "Type": "BooleanExpression",
    }

def build_all_flows(meet_count_question_id: str, met_with_group_block_id: str, no_meeting_block_id: str, meeting_details_block_id: str, who_not_meet_block_id: str,):
    embedded_data = embedded_data_flow("FL_2")
    met_with_group = standard_flow("FL_3", met_with_group_block_id)

    branch_logic = build_branch_logic(meet_count_question_id)
    branch_flow  = [
        standard_flow("FL_4", no_meeting_block_id),
        {
            "Type": "EndSurvey",
            "FlowID": "FL_5"
        },
    ]
    branch = {
        "Type": "Branch",
        "FlowID": "FL_6",
        "Description": "No-meeting path",
        "BranchLogic": branch_logic,
        "Flow": branch_flow,
    }

    meeting_details = standard_flow("FL_7", meeting_details_block_id)
    who_not_meet = standard_flow("FL_8", who_not_meet_block_id)

    flow_list = [embedded_data, met_with_group, branch, meeting_details, who_not_meet]

    count = 1 + len(flow_list) + len(branch_flow) # 1 is from root which we add in return statement

    return {
        "Type": "Root",
        "FlowID": "FL_1",
        "Flow": flow_list,
        "Properties": {"Count": count},
    }
