import os
import sys
import pandas as pd
import json
from dotenv import load_dotenv
from jsonschema import validate
from QualtricsStudyGroupSurveys import QualtricsConnection

load_dotenv()

DIRECTORY_ID = os.getenv("Q_DIRECTORY_ID")
MAILING_LIST_ID = os.getenv("Q_MAILING_LIST_ID")
API_TOKEN = os.getenv("Q_API_TOKEN")
DATA_CENTER = os.getenv("Q_DATA_CENTER")

contact_schema = {
    "type": "object",
    "properties": {
        "firstName": {"type": "string"},
        "lastName": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "extRef": {"type": "string"},
        "embeddedData": {
            "type": "object",
            "properties": {
                "Team": {"type": "string"}
            },
            "required": ["Team"]
        }
    },
    "required": ["email"]
}



def is_in_mailing_list(qualtrics: QualtricsConnection, directory_id, mailing_list_id, email) -> bool:
    contacts = qualtrics.get_mailing_list_contacts(directory_id, mailing_list_id)
    for contact in contacts['result']['elements']:
        if contact['email'] == email:
            return True
    return False

def upload_csv_to_mailing_list(qualtrics: QualtricsConnection, directory_id, mailing_list_id, csv_path) -> None:
    dataframe = pd.read_csv(csv_path)
    for row in dataframe.itertuples():
        email = row.Email
        first_name = row.FirstName
        last_name = row.LastName
        contact = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "extRef": str(row.StudentID),
            "embeddedData": {
                "Team": str(row.Team),
                "canvasId": str(row.CanvasId)
            }
        }
        try:
            validate(instance=contact, schema=contact_schema)
        except Exception as e:
            print(f"Insufficient data to create contact for email {email}: {e}")
            continue
        if is_in_mailing_list(qualtrics, directory_id, mailing_list_id, email):
            print(f"User with email {email} already in mailing list, skipping...")
            continue
        response = qualtrics.add_contact_to_mailing_list(directory_id, mailing_list_id, contact)
        response.raise_for_status()

def main():
    qualtrics = QualtricsConnection(DATA_CENTER, API_TOKEN)
    if not sys.argv[1]:
        print("Please provide a path to a csv as a command line argument.")
        sys.exit(1)
    csv_path = sys.argv[1]
    res = upload_csv_to_mailing_list(qualtrics, DIRECTORY_ID, MAILING_LIST_ID, csv_path)

    # new_contact = {
    #     "firstName": "Test",
    #     "lastName": "User",
    #     "email": "nsching@ucdavis.edu",
    #     "extRef": "123456",
    #     "embeddedData": {
    #         "Team": "A"
    #     }
    # }
    # res = add_contact_to_mailing_list(qualtrics, DIRECTORY_ID, MAILING_LIST_ID, new_contact)
    print(json.dumps(res, indent=4))

if __name__ == "__main__":
    main()