import time
from zipfile import ZipFile
from io import BytesIO
from .qualtrics_connection import QualtricsConnection


def poll_export_status(qualtrics: QualtricsConnection, survey_id: str, export_progress_id: str, poll_interval_seconds = 5.0, timeout_seconds = 600):
    timeout = time.monotonic() + timeout_seconds
    while True:
        result = qualtrics.get_export_status(survey_id, export_progress_id)
        status = result.get("status", "")
        if status == "complete":
            return result.get("fileId", "")
        elif status == "failed":
            raise RuntimeError("Export failed")
        
        if time.monotonic >= timeout:
            raise TimeoutError("Export status polling timed out.")
        
        time.sleep(poll_interval_seconds)


def fetch_responses(qualtrics: QualtricsConnection, survey_id: str, export_path: str):
    progress_id = qualtrics.start_response_export(survey_id)
    file_id = poll_export_status(qualtrics, survey_id, progress_id)
    export_bytes = qualtrics.get_export_file(survey_id, file_id)
    zip_bytes = BytesIO(export_bytes)

    with ZipFile(zip_bytes) as f:
        csv_name = f.namelist()[0]
        data = f.read(csv_name)
        with open(export_path, "wb") as f:
            f.write(data)