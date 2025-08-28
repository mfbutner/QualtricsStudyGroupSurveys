import humanize

def get_loop_options(looping_condition_question_id):
    static = {str(i): {"2": humanize.ordinal(i)} for i in range(1, 11)}
    return {
        "Locator": f"q://{looping_condition_question_id}/LoopAndMerge/MergeOnNumericResponse?v=10",
        "QID": looping_condition_question_id,
        "ChoiceGroupLocator": f"q://{looping_condition_question_id}/LoopAndMerge/MergeOnNumericResponse",
        "Static": static,
        "Randomization": "None"
    }

def make_default_block(description: str, loop_options = None):
    block = {
        "Description": description,
        "Type": "Standard",
        "SubType": "",
        "BlockElements": [],
        "Options": {
            "BlockLocking": "false",
            "RandomizeQuestions": "false",
            "BlockVisibility": "Expanded"
        }
    }
    
    if loop_options is not None:
         block["Options"]["Looping"] = "Question"
         block["Options"]["LoopingOptions"] = loop_options

    return block

def create_block_and_return_id(qualtrics_connection, survey_id, description: str, loop_options = None) -> str:
    block = make_default_block(description, loop_options)
    response = qualtrics_connection.add_block(survey_id, block)
    return response.get("result", {}).get("BlockID", "")