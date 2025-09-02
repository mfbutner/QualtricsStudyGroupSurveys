import sys
import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from QualtricsStudyGroupSurveys import QualtricsConnection, OathInformation
from QualtricsStudyGroupSurveys.fetch_responses import fetch_responses


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

def fetch_df() -> pd.DataFrame:
    load_dotenv()
    
    qualtrics = QualtricsConnection(os.getenv("Q_DATA_CENTER"), os.getenv("Q_API_TOKEN"))
    return fetch_responses(qualtrics, os.getenv("Q_TEST_SURVEY_ID"))

def format_df_for_display(original_df: pd.DataFrame) -> pd.DataFrame:
    df = original_df.copy()
    df = df[df.Finished == '1'] # Show only complete responses
    df.drop_duplicates(inplace=True)
    df["RecordedDate"] = df["RecordedDate"].str[:10]
    cols_to_drop = ["StartDate", "EndDate", "Status", "IPAddress", 
                    "Progress", "Duration (in seconds)", "ResponseId",
                    "LocationLatitude", "LocationLongitude", "DistributionChannel",
                    "UserLanguage", "Finished", "RecipientEmail.1", "ExternalReference"]
    df.drop(columns=cols_to_drop, errors='ignore', inplace=True)

    df.reset_index(drop=True, inplace=True) # Fix indices after dropping rows
    return df

def make_streamlit(df: pd.DataFrame):
    st.title("Qualtrics Study Group Survey Responses")
    st.dataframe(df)

if __name__ == '__main__':
    df = fetch_df()
    formatted_df = format_df_for_display(df)
    make_streamlit(formatted_df)
