import pandas as pd
import streamlit as st
from .fetch_responses import fetch_responses


def row_by_interaction(df: pd.DataFrame):
    """Make each row its own interaction"""

    named_cols = ["Email", "Last_Name", "First_Name"]
    variable_cols = ["Date_of_Meeting", "Activities", "Other_Activity"]
    headers = named_cols + variable_cols + [f"Duration_With_{i + 1}" for i in range(9)]

    new_df = pd.DataFrame(columns=headers)
    for _, row in df.iterrows():
        for meeting in range(int((row["Times_Met"]))):
            interaction_data_cols = named_cols + [f"{col}_{meeting + 1}" for col in variable_cols]
            interaction_data_cols += [f"Duration_With_{i + 1}_{meeting + 1}" for i in range(9)]
            new_df.loc[len(new_df)] = [row[header] for header in interaction_data_cols]
            
            row_index = len(new_df) - 1
            for i in range(9):
                col = f"Duration_With_{i+1}"

                if new_df[col].dtype != "string":
                    new_df[col] = new_df[col].astype("string")

                team_member = row.get(f"TeamMember{i + 1}", "")
                team_member = "" if pd.isna(team_member) else str(team_member)

                duration = new_df.loc[row_index, col]
                duration = "" if pd.isna(duration) else str(duration)

                new_df.loc[row_index, col] = f"{team_member}, {duration}"

    return new_df

def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:

    front_col_names = ["RecipientEmail", "Team", 
                       "RecipientLastName", "RecipientFirstName"]
    remaining_col_names = [col for col in df.columns if col not in front_col_names]
    return df[front_col_names + remaining_col_names]

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    old_to_new_col_name_map = {"RecipientEmail": "Email",
                               "RecipientLastName": "Last_Name",
                               "RecipientFirstName": "First_Name",
                               "Q1.1": "Times_Met",
                               "Q2.1": "Reason_For_Not_Meeting",
                               "Q2.2": "Evidence_For_Not_Meeting",
                               "Q2.2_Name": "File_Name",
                               "Q2.2_Size": "File_Size",
                               "Q2.2_Type": "File_Type",
                               "Q4.1": "Didn't_Meet_With"
                               }
    for i in range(10):
        old_to_new_col_name_map[f"{i + 1}_Q3.1"] = f"Date_of_Meeting_{i + 1}"
        old_to_new_col_name_map[f"{i + 1}_Q3.2"] = f"Activities_{i + 1}"
        old_to_new_col_name_map[f"{i + 1}_Q3.2_8_TEXT"] = f"Other_Activity_{i + 1}"
        for j in range(9):
            old_to_new_col_name_map[f"{i + 1}_Q3.3_{j + 1}"] = f"Duration_With_{j + 1}_{i + 1}"

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
                    "__js_StartDate", "Q2.2_Id"]
    df = df.drop(columns=cols_to_drop, errors='ignore')

    df = reorder_columns(df)
    df = rename_columns(df)
    return df

def format_df_for_no_meetings(original_df: pd.DataFrame) -> pd.DataFrame:
    meet_count = pd.to_numeric(original_df["Times_Met"]).fillna(0)
    new_df = original_df.loc[meet_count == 0].reset_index(drop=True).copy()
    col_names = ["Email", "Team", "Last_Name", "First_Name", 
                 "Reason_For_Not_Meeting", "File_Name",
                 "File_Size", "File_Type"]
    return new_df[col_names]

def format_df_for_interactions(original_df: pd.DataFrame) -> pd.DataFrame:
        meet_count = pd.to_numeric(original_df["Times_Met"]).fillna(0)
        new_df = original_df.loc[meet_count > 0].copy()
        new_df = row_by_interaction(new_df)
        return new_df

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

    meeting_number_choice = st.selectbox(
        "Filter for number of meetings", 
        options=["1+", "0"], 
        index=0) # defaults to '1+' meetings
    
    if meeting_number_choice == "0":
        no_meeting_df = format_df_for_no_meetings(df)
        st.dataframe(no_meeting_df)
        return 

    teams_options = sorted(df["Team"].dropna().astype(str).unique().tolist())
    if not teams_options:
        st.info("No teams found")
        return
    
    for team in teams_options:
        team_df = df.loc[df["Team"].astype(str) == team].copy()
        interactions_df = format_df_for_interactions(team_df)

        label = f"Team {team}: {len(interactions_df)} interaction(s)"
        with st.expander(label, expanded=False):
            st.dataframe(interactions_df)