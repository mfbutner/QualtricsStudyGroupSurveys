import pandas as pd
import streamlit as st
from .fetch_responses import fetch_responses


def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    front_col_names = ["RecordedDate", "Team", "RecipientEmail", 
                       "RecipientFirstName", "RecipientLastName"]
    remaining_col_names = [col for col in df.columns if col not in front_col_names]
    return df[front_col_names + remaining_col_names]

def format_df_for_display(original_df: pd.DataFrame) -> pd.DataFrame:
    df = original_df.copy()
    df = df[df.Finished == "True"] # Show only complete ('Finished') responses
    df.drop_duplicates(inplace=True)
    df["RecordedDate"] = df["RecordedDate"].str[:10] # cut out timestamp from display
    cols_to_drop = ["RecipientEmail.1", "Finished"]
    df.drop(columns=cols_to_drop, errors='ignore', inplace=True)
    df.reset_index(drop=True, inplace=True) # Fix indices after dropping rows
    ordered_df = reorder_columns(df)
    return ordered_df

def fetch_qualtrics_response_data(qualtrics, survey_id) -> pd.DataFrame:
    @st.cache_data() # cache dataframe
    def load_data():
        return fetch_responses(qualtrics, survey_id)
    raw_df = load_data()
    return format_df_for_display(raw_df)

def build_streamlit(df: pd.DataFrame):
    st.set_page_config(layout="wide")
    st.title("Qualtrics Study Group Survey Responses")

    teams_options = df["Team"].dropna().astype(str).unique().tolist()
    team_choices = sorted([team for team in teams_options if team])
    team_choices.insert(0, "All teams")

    choice = st.selectbox("Choose a team", options=team_choices, index=0) # autoselect "All teams"

    if choice != "All teams":
        df = df.loc[df["Team"].astype(str) == choice].copy() # .copy() silences a pandas warning
        df.drop(columns="Team", inplace=True) # Remove team name column if already filtering for team
        df.reset_index(drop=True, inplace=True)

    st.dataframe(df)