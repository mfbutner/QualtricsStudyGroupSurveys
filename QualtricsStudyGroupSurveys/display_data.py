import pandas as pd
import streamlit as st
from .fetch_responses import fetch_responses


def row_by_interaction(df: pd.DataFrame):
    """Make each row its own interaction"""
    return df

def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    front_col_names = ["RecipientEmail", "Team", 
                       "RecipientLastName", "RecipientFirstName"]
    remaining_col_names = [col for col in df.columns if col not in front_col_names]
    return df[front_col_names + remaining_col_names]

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    old_to_new_col_name_map = {"RecipientEmail": "Email",
                               "RecipientFirstName": "First Name",
                               "RecipientLastName": "Last Name"}
    # TODO rename the question id columns for easier reading
    return df.rename(columns = old_to_new_col_name_map)

def insert_people_names(original_df: pd.DataFrame) -> pd.DataFrame:
    df = original_df.copy()
    question_cols = [col for col in df.columns if col.endswith("_Q3.2")]

    def piped_text_to_embedded_data(piped_text: str) -> str:
        piped_text = str(piped_text)
        removed_piped_text_notation = piped_text.strip().rstrip("}").lstrip("${e:/Field}")
        return removed_piped_text_notation.replace("%20"," ")

    for col in question_cols:
        out_col = []
        for index, entry in df[col].items():
            if not isinstance(entry, str) or not entry.strip():
                out_col.append(entry)
                continue

            piped_text_parts = entry.split(",")
            embedded_data_parts = [piped_text_to_embedded_data(part) for part in piped_text_parts]
            
            entry_with_embedded_data = []
            for team_member in embedded_data_parts:
                person_name = df.at[index, team_member]
                entry_with_embedded_data.append(person_name)
            df.at[index, col] = ", ".join(entry_with_embedded_data)

    return df

def populate_dates(original_df: pd.DataFrame) -> pd.DataFrame:
    """Converts 'Date1' -> actual date"""
    df = original_df.copy()
    start_date = pd.to_datetime(df["__js_StartDate"])
    for date_column in [col for col in df.columns if col.endswith("_Q3.1")]:
        df.loc[:, date_column] = df[date_column].astype("string").str.strip().str[-1]
        days_from_start = pd.to_numeric(df[date_column], errors="coerce") - 1
        days_difference = pd.to_timedelta(days_from_start, unit="D")
        df[date_column] = (start_date + days_difference).dt.strftime("%m-%d-%Y")
    return df

def format_df_for_display(original_df: pd.DataFrame) -> pd.DataFrame:
    df = original_df.copy()
    df = df[df.Finished == "True"].drop_duplicates(ignore_index=True) # Show only complete responses

    df = populate_dates(df)
    # df = insert_people_names(df)

    cols_to_drop = ["RecipientEmail.1", "Finished", "CanvasId", "StudentID", 
                    "__js_StartDate"]
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
    team_choices.insert(0, "All")
    
    team_choice = st.selectbox("Choose a team", options=team_choices, index=0) # autoselect "All teams"

    if team_choice != "All":
        df = df.loc[df["Team"].astype(str) == team_choice].copy() # .copy() silences a pandas warning
        df.drop(columns="Team", inplace=True) # Remove team name column if already filtering for team
        df.reset_index(drop=True, inplace=True)

    meeting_number_choice = st.selectbox("Filter for number of meetings", options=["All", "0", "1+"], index=0)
    meet_count = pd.to_numeric(df["Q1.1"]).fillna(0)

    if meeting_number_choice == "0":
        df = df.loc[meet_count == 0].copy()
    elif meeting_number_choice == "1+":
        df = df.loc[meet_count != 0].copy()
        df = row_by_interaction(df)

    st.dataframe(df)