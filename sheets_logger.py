"""Optional Google Sheets logging for pilot data collection.

If a Google service account and a SHEET_ID are provided (via Streamlit secrets
or environment variables), each completed session appends a row to the sheet.
If they are not configured, every function here is a silent no-op so the app
runs normally without it.

Configure via Streamlit secrets:

    SHEET_ID = "the-spreadsheet-id-from-its-url"

    [gcp_service_account]
    type = "service_account"
    project_id = "..."
    private_key_id = "..."
    private_key = "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n"
    client_email = "...@....iam.gserviceaccount.com"
    client_id = "..."
    auth_uri = "https://accounts.google.com/o/oauth2/auth"
    token_uri = "https://oauth2.googleapis.com/token"
    auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
    client_x509_cert_url = "..."
"""

import os
import json
import time
from datetime import datetime
from typing import Optional

import streamlit as st

DOMAIN_IDS = [
    "opening_agenda_setting",
    "patient_centered_inquiry",
    "recognition_of_emotion",
    "empathy_validation",
    "patient_perspective",
    "clinical_information_gathering",
    "clarity_plain_language",
    "shared_decision_making",
    "safety_professionalism",
    "cue_recognition",
]

COLUMNS = (
    [
        "logged_at", "record_type", "session_id", "participant_id", "case_id",
        "attempt_number", "learning_mode",
        "total_turns", "encounter_status", "final_trust", "rupture_count", "end_reason",
        "rubric_mean",
    ]
    + [f"d_{d}" for d in DOMAIN_IDS]
    + [f"pre_se_{i}" for i in range(1, 6)]
    + [f"post_se_{i}" for i in range(1, 6)]
    + ["usability", "usefulness",
       "reflection_q1", "reflection_q2", "reflection_q3", "qualitative_comment",
       "transcript"]
)

WORKSHEET_NAME = "sessions"


def _creds_info() -> Optional[dict]:
    try:
        if "gcp_service_account" in st.secrets:
            return dict(st.secrets["gcp_service_account"])
    except Exception:
        pass
    raw = os.environ.get("GCP_SERVICE_ACCOUNT")
    if raw:
        try:
            return json.loads(raw)
        except Exception:
            return None
    return None


def _sheet_id() -> Optional[str]:
    try:
        if "SHEET_ID" in st.secrets:
            return str(st.secrets["SHEET_ID"])
    except Exception:
        pass
    return os.environ.get("SHEET_ID")


def is_configured() -> bool:
    return _creds_info() is not None and bool(_sheet_id())


@st.cache_resource(show_spinner=False)
def _get_worksheet():
    info = _creds_info()
    sid = _sheet_id()
    if not info or not sid:
        return None
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_info(info, scopes=scopes)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(sid)
        try:
            ws = sheet.worksheet(WORKSHEET_NAME)
        except Exception:
            ws = sheet.add_worksheet(title=WORKSHEET_NAME, rows=2000, cols=len(COLUMNS) + 5)
        if not ws.row_values(1):
            ws.append_row(COLUMNS, value_input_option="USER_ENTERED")
        return ws
    except Exception:
        return None


def _stringify(value) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def log_record(record: dict) -> bool:
    """Append one row built from COLUMNS. Returns True on success, never raises.

    Retries once after a short pause, since the most common failure is a
    transient Google Sheets API rate-limit rather than a permanent error.
    """
    ws = _get_worksheet()
    if ws is None:
        return False
    full = {**record, "logged_at": datetime.utcnow().isoformat()}
    row = [_stringify(full.get(col, "")) for col in COLUMNS]
    for attempt in range(2):
        try:
            ws.append_row(row, value_input_option="USER_ENTERED")
            return True
        except Exception:
            if attempt == 0:
                time.sleep(1.5)
                continue
            return False
    return False
