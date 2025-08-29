import pandas as pd
from datetime import datetime, timedelta

def get_date_range(start_date: datetime, end_date: datetime):
    delta = end_date - start_date
    return [start_date + timedelta(days=i) for i in range(delta.days + 1)]

def get_date_choices(start_date: datetime | str, end_date: datetime | str):
    date_format = "%m-%d-%Y"
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, date_format)
    
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, date_format)

    range = get_date_range(start_date, end_date)
    choices = {}
    for i, date in enumerate(range):
        choices[str(i+1)] = {
            "Display": date.strftime("%m-%d-%Y")
        }
    return choices

def build_people_list(csv_path):
    df = pd.read_csv(csv_path)
    people = []
    for row in df.itertuples():
        first_name = row.FirstName
        last_name = row.LastName
        team = str(row.Team)
        email = row.Email
        people.append((first_name, last_name, team, email))
    return people
