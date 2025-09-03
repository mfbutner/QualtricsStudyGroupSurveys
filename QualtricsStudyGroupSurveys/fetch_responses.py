import time
import pandas as pd
from io import BytesIO
from zipfile import ZipFile
from .qualtrics_connection import QualtricsConnection


def poll_export_status(qualtrics: QualtricsConnection, survey_id: str, export_progress_id: str, poll_interval_seconds = 5.0, timeout_duration_seconds = 600):
    timeout_deadline = time.monotonic() + timeout_duration_seconds
    while True:
        result = qualtrics.get_export_status(survey_id, export_progress_id)
        status = result.get("status", "")
        if status == "complete":
            return result.get("fileId", "")
        elif status == "failed":
            raise RuntimeError("Qualtrics results export failed.")
        
        if time.monotonic() >= timeout_deadline:
            raise TimeoutError("Export status polling timed out.")
        
        time.sleep(poll_interval_seconds)


def fetch_responses(qualtrics: QualtricsConnection, survey_id: str) -> pd.DataFrame:
    included_metadata = ["finished", "recipientLastName", 
                         "recipientFirstName", "recipientEmail"]
    export_params = {
        "format": "csv",
        "useLabels": True,
        "breakoutSets": "False",
        "timeZone": "America/Los_Angeles",
        "surveyMetadataIds": included_metadata
    }
    progress_id = qualtrics.start_response_export(survey_id, export_params)
    file_id = poll_export_status(qualtrics, survey_id, progress_id)
    export_bytes = qualtrics.get_export_file(survey_id, file_id)
    zip_bytes = BytesIO(export_bytes)

    with ZipFile(zip_bytes) as f:
        csv_name = f.namelist()[0] # should only have the single results csv in the zip file
        csv_bytes = f.read(csv_name)
        df = pd.read_csv(BytesIO(csv_bytes))
        return df