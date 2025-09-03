import pandas as pd
import streamlit as st
from .fetch_responses import fetch_responses


def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    front_col_names = ["RecordedDate", "Team", "RecipientEmail", 
                       "RecipientLastName", "RecipientFirstName"]
    remaining_col_names = [col for col in df.columns if col not in front_col_names]
    return df[front_col_names + remaining_col_names]

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    old_to_new_col_name_map = {"RecipientEmail": "Email", "RecipientFirstName": "First Name",
                                "RecipientLastName": "Last Name", "RecordedDate": "Date"}
    # TODO rename the question id columns for easier reading
    return df.rename(columns = old_to_new_col_name_map)

def format_df_for_display(original_df: pd.DataFrame) -> pd.DataFrame:
    df = original_df.copy()
    df = df[df.Finished == "True"].drop_duplicates(ignore_index=True) # Show only complete responses

    cols_to_drop = ["RecipientEmail.1", "Finished"]
    df = df.drop(columns=cols_to_drop, errors='ignore')

    df = reorder_columns(df)
    df = rename_columns(df)
    return df

def fetch_qualtrics_response_data(qualtrics, survey_id) -> pd.DataFrame:
    @st.cache_data(show_spinner=False) # cache dataframe
    def load_data():
        return fetch_responses(qualtrics, survey_id)
    
    if st.button("Refresh Data"):
        load_data.clear()
        load_data()

    with st.spinner("Loading response data from Qualtrics..."):
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