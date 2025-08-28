import json

def build_person_choice(first_name: str, last_name: str, team_value: str, email: str):
    name = f"{first_name.strip()} {last_name.strip()}"

    team_info = (
        '<span class="ConjDesc">If</span> '
        '<span class="LeftOpDesc">Team</span> '
        '<span class="OpDesc">Is Equal to</span> '
        f'<span class="RightOpDesc"> {team_value} </span>'
    )
    email_info = (
        '<span class="ConjDesc">And</span>'
        '<span class="schema_desc">Contact List</span>'
        '<span class="select_val_desc LeftOperand_desc">Email</span>'
        '<span class="select_val_desc Operator_desc">Is Not Equal to</span>'
        f'<span class="textbox_val_desc RightOperand_desc">{email}</span>'
    )

    with open("question_templates/build_person_choice.json", "r", encoding="utf-8") as f:
        template_content = json.load(f)

    template_content["Display"] = name
    template_content["DisplayLogic"]["0"]["0"]["RightOperand"] = team_value
    template_content["DisplayLogic"]["0"]["1"]["RightOperand"] = email
    template_content["DisplayLogic"]["0"]["0"]["Description"] = team_info
    template_content["DisplayLogic"]["0"]["1"]["Description"] = email_info

    return template_content

def meet_count_question():
    with open("question_templates/meet_count_question.json", "r", encoding="utf-8") as f:
        template_content = json.load(f)

    return template_content

def no_meeting_explanation(meet_count_question_id):
    locator = f"q://{meet_count_question_id}/ChoiceTextEntryValue"
    with open("question_templates/no_meeting_explanation.json", "r", encoding="utf-8") as f:
        template_content = json.load(f)

    template_content["DisplayLogic"]["0"]["0"]["QuestionID"] = meet_count_question_id
    template_content["DisplayLogic"]["0"]["0"]["ChoiceLocator"] = locator
    template_content["DisplayLogic"]["0"]["0"]["QuestionIDFromLocator"] = meet_count_question_id
    template_content["DisplayLogic"]["0"]["0"]["LeftOperand"] = locator

    return template_content

def no_meeting_upload_question(meet_count_question_id):
    locator = f"q://{meet_count_question_id}/ChoiceTextEntryValue"
    with open("question_templates/no_meeting_upload_question.json", "r", encoding="utf-8") as f:
        template_content = json.load(f)

    template_content["DisplayLogic"]["0"]["0"]["QuestionID"] = meet_count_question_id
    template_content["DisplayLogic"]["0"]["0"]["ChoiceLocator"] = locator
    template_content["DisplayLogic"]["0"]["0"]["QuestionIDFromLocator"] = meet_count_question_id
    template_content["DisplayLogic"]["0"]["0"]["LeftOperand"] = locator

    return template_content

def who_did_you_meet_with_question(people):
    choices = {}
    for i, (first, last, team, email) in enumerate(people, start=1):
        choices[str(i)] = build_person_choice(first, last, team, email)

    with open("question_templates/who_did_you_meet_with_question.json", "r", encoding="utf-8") as f:
        template_content = json.load(f)

    template_content["Choices"] = choices
    template_content["ChoiceOrder"] = list(range(1, len(choices) + 1))
    template_content["NextChoiceId"] = len(choices) + 1

    return template_content

def meeting_date_question(date_choices):
    with open("question_templates/meeting_date_question.json", "r", encoding="utf-8") as f:
        base = json.load(f)

    base["Choices"] = date_choices
    base["ChoiceOrder"] = list(range(1, len(date_choices)+1))
    base["NextChoiceId"] = len(date_choices) + 1

    return base

def meeting_activities_question():
    with open("question_templates/meeting_activities_question.json", "r", encoding="utf-8") as f:
        template_content = json.load(f)

    return template_content

def meeting_duration_question():
    with open("question_templates/meeting_duration_question.json", "r", encoding="utf-8") as f:
        template_content = json.load(f)

    return template_content

def who_did_you_not_meet_with_question(people):
    choices = {}
    for i, (first, last, team, email) in enumerate(people, start=1):
        choices[str(i)] = build_person_choice(first, last, team, email)
    choices[str(len(choices)+1)] = {
        "Display": "I met with everyone in my group",
        "ExclusiveAnswer": True
    }    
    
    with open("question_templates/who_did_you_not_meet_with_question.json", "r", encoding="utf-8") as f:
        template_content = json.load(f)  

    template_content["Choices"] = choices
    template_content["ChoiceOrder"] = list(range(1, len(choices) + 1))
    template_content["NextChoiceId"] = len(choices) + 1

    return template_content
