import struct
import zlib
import base64
import math
import json
import csv
import io
import os
import sys
import time
import uuid
import subprocess
from datetime import datetime

import streamlit as st
import requests

from nonverbal import get_patient_svg, VISUAL_STATE_DATA, CUE_PANEL_LIMITATION, CUE_REFLECTION_NOTE, get_cue_panel_data
import sheets_logger

API_URL = "http://localhost:8000"

TOOL_LIMITATION = (
    "TrustMed uses typed interactions and simplified visual cue representations. "
    "It therefore cannot reproduce the central difficulty of live clinical communication: "
    "responding in real time under emotional, interpersonal, and time pressure while "
    "interpreting tone, silence, interruptions, facial expression, posture, and body language. "
    "The tool is best understood as a rehearsal and reflection environment for communication "
    "reasoning, cue recognition, and safe explanation — not as a substitute for standardized "
    "patient encounters, OSCEs, bedside teaching, or faculty-observed role play."
)

CLINICAL_FRAMING = (
    "This tool does not assess diagnostic accuracy. It provides formative feedback on how "
    "learners communicate while gathering clinically relevant information, recognizing safety "
    "issues, explaining uncertainty, and proposing safe next steps in fictional cases."
)

RUBRIC_LIMITATION = (
    "The rubric is formative and model-generated. It has not been psychometrically validated "
    "and should not be used for formal assessment without faculty review, inter-rater reliability "
    "testing, and comparison with human evaluator ratings."
)

CUE_LIMITATION = CUE_PANEL_LIMITATION

STATE_MODEL_NOTE = (
    "The patient-state model is heuristic. Trust, anxiety, defensiveness, and shame values "
    "are not measurements of real patient emotion. They are educational parameters used to "
    "create consistent simulated responses."
)

FULL_LIMITATIONS = f"""**Text format.** {TOOL_LIMITATION}

**Patient-state model.** {STATE_MODEL_NOTE}

**Rubric.** {RUBRIC_LIMITATION}

**Visual cue panel.** {CUE_LIMITATION}"""

SELF_EFFICACY_CAUTION = (
    "These self-efficacy ratings are exploratory and should not be interpreted as proof of "
    "learning without a controlled study."
)

HIGH_RISK_CASES = {"james"}

SELF_EFFICACY_ITEMS = [
    "I feel confident responding to patient distrust.",
    "I feel confident asking sensitive questions respectfully.",
    "I feel confident explaining uncertainty to a patient.",
    "I feel confident balancing empathy with clinical information gathering.",
    "I feel confident recognizing emotional or visual cues during a clinical encounter.",
]

st.set_page_config(
    page_title="Clinical Communication Rehearsal Tool",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_data
def _cppn_bg() -> str:
    W, H = 300, 90

    def fwd(x, y):
        r = math.sqrt(x * x + y * y)
        h1 = math.sin(5.0 * x + 2.0 * y)
        h2 = math.tanh(2.5 * x - 1.5 * y + 1.2 * r)
        h3 = math.sin(3.0 * y + 2.5 * x + 0.8 * r)
        h4 = math.cos(4.5 * x - 1.0 * y + 0.5 * r)
        h5 = math.tanh(0.6 * h1 + 0.8 * h2 - 0.4 * h3 + 0.5 * h4)
        h6 = math.sin(1.1 * h1 - 0.7 * h2 + 1.3 * h3 + 0.6 * h4)
        h7 = math.cos(-0.5 * h1 + 1.2 * h2 + 0.9 * h3 - 0.8 * h4)
        r_out = math.tanh(0.15 * h5 + 0.12 * h6 - 0.25 * h7)
        g_out = math.tanh(0.25 * h5 - 0.35 * h6 + 0.18 * h7)
        b_out = math.tanh(0.75 * h5 + 0.55 * h6 + 0.38 * h7)
        rv = int((r_out + 1) / 2 * 35 + 5)
        gv = int((g_out + 1) / 2 * 55 + 20)
        bv = int((b_out + 1) / 2 * 100 + 70)
        return rv, gv, bv

    def chunk(tag, data):
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    try:
        ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
        raw = bytearray()
        for row in range(H):
            raw.append(0)
            for col in range(W):
                x = (col / W) * 2 - 1
                y = (row / H) * 2 - 1
                rv, gv, bv = fwd(x, y)
                raw.extend([rv, gv, bv])
        idat = chunk(b"IDAT", zlib.compress(bytes(raw), 6))
        iend = chunk(b"IEND", b"")
        png = b"\x89PNG\r\n\x1a\n" + ihdr + idat + iend
        return "data:image/png;base64," + base64.b64encode(png).decode()
    except Exception:
        return ""


def inject_css() -> None:
    bg = _cppn_bg()
    if bg:
        bg_css = (
            f"linear-gradient(rgba(10,35,68,0.60), rgba(10,35,68,0.84)), "
            f"url('{bg}') no-repeat center / cover, #0d2d54"
        )
    else:
        bg_css = "#0d2d54"

    st.markdown(f"""
<style>
html, body {{
    font-family: "Times New Roman", Times, serif !important;
    color: #1c2b3a;
}}
[data-testid="stApp"],
[data-testid="stMain"],
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"] {{
    font-family: "Times New Roman", Times, serif !important;
}}
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] td,
[data-testid="stMarkdownContainer"] th,
[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] em,
[data-testid="stMarkdownContainer"] a,
[data-testid="stChatMessageContent"],
[data-testid="stChatMessageContent"] p,
[data-testid="stText"],
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] p,
[data-testid="stExpander"] li,
[data-testid="stExpander"] td,
[data-testid="stExpander"] th,
[data-testid="stMetricLabel"],
[data-testid="stMetricValue"],
[data-testid="stSelectbox"] label,
[data-testid="stTextInput"] label,
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] label,
[data-testid="stTextArea"] textarea,
[data-testid="stRadio"] label,
[data-testid="stCheckbox"] label,
[data-testid="stChatInput"] textarea,
[data-testid="stSlider"] label,
[data-testid="stSlider"] p,
.stButton > button,
label, input[type="text"], input[type="number"], textarea, select,
p, h1, h2, h3, h4, h5, h6 {{
    font-family: "Times New Roman", Times, serif !important;
}}
[data-testid="stIconMaterial"],
span[class*="material-symbols"],
span[class*="material-icons"],
[class*="material-symbols-"],
[class*="material-icons-"] {{
    font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
}}
[data-testid="stHeader"] {{ background-color: #0d2d54 !important; border-bottom: none !important; }}
[data-testid="stHeader"] button, [data-testid="stHeader"] a, [data-testid="stHeader"] span {{ color: white !important; }}
[data-testid="stHeader"] button svg, [data-testid="stHeader"] a svg, [data-testid="stHeader"] span svg {{
    filter: brightness(0) invert(1) !important;
}}
[data-testid="stApp"], [data-testid="stMain"] {{ background: #f4f6f9 !important; }}
section.main > div.block-container {{
    background: #f4f6f9 !important;
    padding-top: 0 !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 100% !important;
}}
[data-testid="stSidebar"] > div:first-child {{ background: #0d2d54 !important; padding-top: 1.5rem !important; }}
[data-testid="stSidebar"] * {{ color: #d6e4f0 !important; }}
.stButton > button {{
    background: #1a4480 !important; color: #ffffff !important;
    border: none !important; border-radius: 4px !important;
    font-weight: 600 !important; font-size: 0.88rem !important;
    padding: 9px 20px !important; transition: background 0.15s ease !important;
}}
.stButton > button * {{ color: #ffffff !important; background: transparent !important; }}
.stButton > button:hover {{ background: #003872 !important; }}
.stSelectbox > div > div, .stTextInput > div > div, .stTextArea > div > div {{
    background: #ffffff !important; border: 1px solid #c8d0da !important; border-radius: 4px !important;
}}
[data-testid="stBottom"], [data-testid="stBottom"] > div,
[data-testid="stChatInput"], [data-testid="stChatInput"] > div {{
    background: #ffffff !important; border-top: 1px solid #dee2e8 !important;
}}
[data-testid="stChatInput"] textarea {{ background: #ffffff !important; color: #1c2b3a !important; }}
[data-testid="stChatMessageContent"] {{ font-size: 0.91rem; line-height: 1.65; }}
[data-testid="stMetricValue"] {{ color: #1a4480 !important; font-weight: 700 !important; font-size: 1.4rem !important; }}
[data-testid="stMetricLabel"] {{ color: #5a6775 !important; font-size: 0.68rem !important; text-transform: uppercase !important; letter-spacing: 0.8px !important; }}
[data-testid="stExpander"] {{ border: 1px solid #dee2e8 !important; border-radius: 4px !important; background: #ffffff !important; }}
[data-testid="stExpander"] summary {{ font-weight: 600 !important; font-size: 0.9rem !important; }}
.score-badge {{
    background: #f0f4f8;
    color: #1c2b3a;
    font-weight: 600;
    border-radius: 3px;
    padding: 2px 10px;
    font-size: 0.85rem;
    border: 1px solid #d1d9e0;
}}
.card {{ background:#ffffff;border:1px solid #dde2e8;border-radius:6px;padding:20px 24px;margin-bottom:14px;box-shadow:0 1px 3px rgba(0,0,0,0.04); }}
.card-header {{ font-size:0.65rem;font-weight:700;color:#6a7787;text-transform:uppercase;letter-spacing:1.2px;margin-bottom:6px; }}
.card-title {{ font-size:1.05rem;font-weight:700;color:#1a3f6f;margin-bottom:4px; }}
.page-band {{
    background: {bg_css};
    color: #ffffff;
    padding: 26px 28px 20px 28px;
    margin: -0.5rem -2rem 20px -2rem;
    border-bottom: 3px solid rgba(255,255,255,0.12);
}}
.page-band h1 {{
    font-size: 2.4rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 6px 0;
    letter-spacing: -0.5px;
    text-shadow: 0 1px 4px rgba(0,0,0,0.35);
    line-height: 1.15;
}}
.page-band p {{
    font-size: 0.87rem;
    color: rgba(255,255,255,0.72);
    margin: 0;
}}
.notice-box   {{ background:#fffbeb;border:1px solid #e0cfa0;border-left:4px solid #b08030;border-radius:4px;padding:12px 16px;font-size:0.85rem;margin-bottom:14px; }}
.info-box     {{ background:#f0f7ff;border:1px solid #c8ddf4;border-left:4px solid #3b6ea8;border-radius:4px;padding:12px 16px;font-size:0.85rem;margin-bottom:14px; }}
.limit-box    {{ background:#f8fafc;border:1px solid #cbd5e1;border-left:4px solid #94a3b8;border-radius:4px;padding:12px 16px;font-size:0.82rem;color:#475569;margin-bottom:14px; }}
.principle-box {{ background:#f0f7ff;border:1px solid #bfdbfe;border-left:4px solid #2563eb;border-radius:4px;padding:14px 18px;font-size:0.92rem;font-style:italic;margin-bottom:16px; }}
.hint-box     {{ background:#fefce8;border:1px solid #e5d060;border-left:4px solid #a07020;border-radius:4px;padding:12px 16px;font-size:0.87rem;margin-bottom:14px; }}
.annotation-box {{ background:#f4fbf5;border:1px solid #b8dfc0;border-left:4px solid #2e7d52;border-radius:4px;padding:11px 15px;font-size:0.85rem;margin-top:8px; }}
.safety-note  {{ background:#f8fafc;border:1px solid #cbd5e1;border-left:4px solid #64748b;border-radius:4px;padding:10px 14px;margin:6px 0;font-size:0.85rem; }}
.clinical-task-box {{ background:#f4f8ff;border:1px solid #c0d4f0;border-left:4px solid #1a4480;border-radius:4px;padding:14px 18px;font-size:0.88rem;margin-bottom:14px; }}
.integration-box {{ background:#f4f8f4;border:1px solid #b8d8c0;border-left:4px solid #2e6d44;border-radius:4px;padding:14px 18px;font-size:0.88rem;margin-bottom:14px; }}
.badge-intro     {{ background:#e8f0e8;color:#2e5a2e;padding:2px 10px;border-radius:12px;font-size:0.70rem;font-weight:600; }}
.badge-inter     {{ background:#e8eef8;color:#1e3a6a;padding:2px 10px;border-radius:12px;font-size:0.70rem;font-weight:600; }}
.badge-advanced  {{ background:#f0e8f0;color:#5a1e5a;padding:2px 10px;border-radius:12px;font-size:0.70rem;font-weight:600; }}
.badge-guided    {{ background:#e8f0e8;color:#2e5a2e;padding:2px 10px;border-radius:12px;font-size:0.70rem;font-weight:600; }}
.badge-independent {{ background:#e8eef8;color:#1e3a6a;padding:2px 10px;border-radius:12px;font-size:0.70rem;font-weight:600; }}
.badge-faculty   {{ background:#ede9fe;color:#4c1d95;padding:2px 10px;border-radius:12px;font-size:0.70rem;font-weight:600; }}
.status-label {{ background:#e8eef8;color:#1e3a6a;padding:2px 10px;border-radius:12px;font-size:0.75rem;font-weight:600; }}
.cue-panel {{ background:#ffffff;border:1px solid #e2e8f0;border-radius:6px;padding:12px 14px;margin-bottom:10px;font-size:0.82rem; }}
.cue-label-text {{ font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:4px;color:#475569; }}
.model-student {{ background:#f0f6ff;border-left:3px solid #2563eb;padding:10px 14px;border-radius:4px;margin-bottom:6px;font-size:0.88rem; }}
.model-patient  {{ background:#f4fbf5;border-left:3px solid #16a34a;padding:10px 14px;border-radius:4px;margin-bottom:6px;font-size:0.88rem; }}
.section-divider {{ border:none;border-top:1px solid #e2e8f0;margin:20px 0; }}
.step-strip {{ display:flex;flex-wrap:wrap;gap:6px;margin:0 0 14px 0;align-items:center; }}
.step-pill {{ font-size:0.72rem;padding:3px 11px;border-radius:12px;font-weight:600;white-space:nowrap; }}
.step-done   {{ background:#dbe7d8;color:#2e5a2e; }}
.step-active {{ background:#1a4480;color:#ffffff; }}
.step-todo   {{ background:#eef1f5;color:#9aa6b4; }}
</style>
""", unsafe_allow_html=True)


CASE_CATALOG = [
    {
        "id": "alex", "case_id": "TC-001", "name": "Alex Chen", "age": 16,
        "setting": "Adolescent Medicine Clinic",
        "chief_concern": "Lower abdominal pain",
        "difficulty": "Intermediate", "health_literacy": "Moderate",
        "trust_barrier": "Fear of parental disclosure; shame about sexual health history",
        "communication_challenge": "Adolescent confidentiality and sensitive topic timing",
        "description": (
            "A 16-year-old presents with lower abdominal pain and is visibly evasive. "
            "Her parents are waiting outside."
        ),
    },
    {
        "id": "diane", "case_id": "TC-002", "name": "Diane Flores", "age": 28,
        "setting": "University Health Center",
        "chief_concern": "Fatigue, weight loss, dizziness",
        "difficulty": "Advanced", "health_literacy": "High",
        "trust_barrier": "Deep shame; fear of judgment; strong minimization",
        "communication_challenge": "Non-judgmental inquiry with a high-shame patient",
        "description": (
            "A 28-year-old doctoral student attributes physical symptoms to academic stress. "
            "She is concealing a significant behavioral health concern."
        ),
    },
    {
        "id": "marcus", "case_id": "TC-003", "name": "Marcus Webb", "age": 52,
        "setting": "Internal Medicine — Primary Care",
        "chief_concern": "Recurrent chest tightness",
        "difficulty": "Intermediate", "health_literacy": "Moderate",
        "trust_barrier": "Prior ER dismissal; anticipates being dismissed again",
        "communication_challenge": "Validating prior negative experience; adherence inquiry",
        "description": (
            "A 52-year-old presents after feeling dismissed at a prior emergency visit. "
            "He has quietly stopped a prescribed medication."
        ),
    },
    {
        "id": "rosa", "case_id": "TC-004", "name": "Rosa Gutierrez", "age": 67,
        "setting": "Community Health Center",
        "chief_concern": "Dizziness and imbalance",
        "difficulty": "Introductory", "health_literacy": "Low",
        "trust_barrier": "Shame about medication confusion; financial barrier; language barrier",
        "communication_challenge": "Plain language; non-judgmental adherence and cost inquiry",
        "description": (
            "A 67-year-old with hypertension says she takes her medications, "
            "but pharmacy records suggest otherwise."
        ),
    },
    {
        "id": "james", "case_id": "TC-005", "name": "James Okafor", "age": 34,
        "setting": "Primary Care — Routine Visit",
        "chief_concern": "Low mood and sleep difficulty",
        "difficulty": "Advanced", "health_literacy": "High",
        "trust_barrier": "Passive suicidal ideation; stigma; prior dismissal; cost concerns",
        "communication_challenge": "Safety assessment, mental health inquiry, stigma, minimization",
        "description": (
            "A 34-year-old teacher minimizes persistent low mood. He carries "
            "passive suicidal ideation he has disclosed to no one."
        ),
    },
    {
        "id": "priya", "case_id": "TC-006", "name": "Priya Sharma", "age": 45,
        "setting": "Primary Care — Return Visit",
        "chief_concern": "Persistent breast lump, previously dismissed",
        "difficulty": "Intermediate", "health_literacy": "High",
        "trust_barrier": "Prior dismissal without imaging; reluctance to appear difficult",
        "communication_challenge": "Avoiding false reassurance; acknowledging prior care",
        "description": (
            "A 45-year-old returns with a breast lump called benign eight months ago "
            "without imaging."
        ),
    },
]

SCORE_LABELS = {1: "Absent / Harmful", 2: "Weak / Generic", 3: "Adequate", 4: "Strong", 5: "Excellent"}
INJECTION_KEYWORDS = [
    "ignore previous", "disregard instructions", "system prompt", "you are now",
    "act as", "forget your role", "new instructions", "override",
]


def navigate_to(page: str) -> None:
    st.session_state.page = page
    st.rerun()


STEP_FLOW = [
    ("Welcome", "landing"),
    ("Setup & Case", "setup"),
    ("Case Brief", "case_brief"),
    ("Encounter", "simulation"),
    ("Report", "report"),
]

_SESSION_KEYS_TO_CLEAR = [
    "session_id", "case_id", "messages", "ended", "start_data",
    "rubric_result", "model_transcript_data", "previous_session_id",
    "previous_rubric", "attempt_number", "visual_state", "disclosure_layer",
    "encounter_status", "hint_shown", "current_hint", "high_risk_acknowledged",
    "enable_high_risk", "pre_efficacy", "framework_note", "validity_caution",
]


def _reset_all_session() -> None:
    for key in _SESSION_KEYS_TO_CLEAR:
        st.session_state.pop(key, None)


def render_header(title: str, subtitle: str = "", step_page: str = None, show_restart: bool = True) -> None:
    sub_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(f"""
<div class="page-band">
  <h1>{title}</h1>
  {sub_html}
</div>
""", unsafe_allow_html=True)

    step_idx = next((i for i, (lbl, pg) in enumerate(STEP_FLOW) if pg == step_page), None)
    if step_idx is None and not show_restart:
        return

    col_steps, col_restart = st.columns([6, 1])
    with col_steps:
        if step_idx is not None:
            pills = []
            for i, (lbl, pg) in enumerate(STEP_FLOW):
                cls = "step-done" if i < step_idx else ("step-active" if i == step_idx else "step-todo")
                pills.append(f'<span class="step-pill {cls}">{i + 1}. {lbl}</span>')
            st.markdown('<div class="step-strip">' + "".join(pills) + "</div>", unsafe_allow_html=True)
    with col_restart:
        if show_restart:
            if st.button("↺ Restart", key="restart_btn", help="Clear this session and start over"):
                _reset_all_session()
                navigate_to("landing")


def api(endpoint: str, method: str = "GET", payload: dict = None, timeout: int = 60):
    try:
        url = f"{API_URL}{endpoint}"
        r = requests.post(url, json=payload, timeout=timeout) if method == "POST" else requests.get(url, timeout=timeout)
        if r.status_code == 200:
            return r.json()
        try:
            detail = r.json().get("detail", "")
        except Exception:
            detail = ""
        if r.status_code == 429:
            st.warning(detail or "This tool is at capacity right now. Please try again later.")
        else:
            st.error(f"API error ({r.status_code}): {detail or 'Unknown error'}")
        return None
    except requests.ConnectionError:
        st.error("Cannot connect to the simulation backend (localhost:8000). Is the FastAPI server running?")
        return None
    except requests.Timeout:
        st.error("The request timed out. Rubric scoring may take up to 30 seconds — please try again.")
        return None


def score_label(score: int) -> str:
    return SCORE_LABELS.get(int(score), "")


def difficulty_badge(level: str) -> str:
    m = {"Introductory": "intro", "Intermediate": "inter", "Advanced": "advanced"}
    return f'<span class="badge-{m.get(level, "inter")}">{level}</span>'


def mode_badge(mode: str) -> str:
    return f'<span class="badge-{mode}">{mode.capitalize()} Practice</span>'


def status_label_html(status: str) -> str:
    labels = {"active": "Active", "strained": "Strained", "ruptured": "Ruptured", "ended": "Ended"}
    return f'<span class="status-label">{labels.get(status, status.capitalize())}</span>'


def _message_safe(msg: str) -> bool:
    ml = msg.lower()
    return not any(kw in ml for kw in INJECTION_KEYWORDS)


def _reset_for_retry() -> None:
    st.session_state["previous_session_id"] = st.session_state.get("session_id", "")
    st.session_state["previous_rubric"]     = st.session_state.get("rubric_result")
    st.session_state["attempt_number"]      = st.session_state.get("attempt_number", 1) + 1
    for key in ["start_data", "messages", "rubric_result", "model_transcript_data"]:
        st.session_state.pop(key, None)
    st.session_state["ended"]            = False
    st.session_state["visual_state"]     = "guarded"
    st.session_state["disclosure_layer"] = 1
    st.session_state["encounter_status"] = "active"


def page_landing() -> None:
    render_header(
        "Clinical Communication Rehearsal Tool",
        "Practice a tough patient conversation and get instant, private feedback",
        step_page="landing",
        show_restart=False,
    )

    col_main, col_side = st.columns([3, 2])

    with col_main:
        st.markdown("#### What this is")
        st.markdown(
            "You play the **clinician**. You'll type back and forth with a **simulated patient** "
            "who has a concern they're unsure about sharing. Try to build enough trust to understand "
            "what's going on, ask the questions that matter, and explain the next steps clearly.\n\n"
            "At the end you get a **feedback report** on how you balanced warmth, clinical focus, and "
            "clear explanation. **No medical background needed** — anyone can try it."
        )
        st.markdown(
            '<div class="info-box"><strong>What to expect:</strong> about 5–10 minutes, '
            'up to ~10 messages in one conversation, then your feedback report. No sign-up.</div>',
            unsafe_allow_html=True,
        )

    with col_side:
        st.markdown("#### Cases you can pick")
        for c in CASE_CATALOG:
            st.markdown(
                f"**{c['case_id']}: {c['name']}, {c['age']}** &nbsp;&nbsp;"
                f"{difficulty_badge(c['difficulty'])}  \n"
                f"<small style='color:#5a6775;'>{c['chief_concern']} — {c['setting']}</small>",
                unsafe_allow_html=True,
            )

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    st.markdown("#### Before you start")
    st.markdown(
        '<div class="limit-box">'
        '• All patient cases are <strong>fictional</strong> — please don\'t type any real personal or medical details.<br/>'
        '• Feedback is <strong>AI-generated and formative</strong>: a practice aid for communication, not a real assessment and not medical advice.<br/>'
        '• This is an early tool being tested. <strong>The whole conversation you type, plus your ratings, are saved anonymously</strong> to help improve it.'
        '</div>',
        unsafe_allow_html=True,
    )

    agreed = st.checkbox("I understand — let's start.")
    if st.button("Begin", disabled=not agreed):
        navigate_to("setup")


def page_setup() -> None:
    render_header(
        "Session Setup and Case Selection",
        "Configure your session, then choose a fictional patient case",
        step_page="setup",
    )

    col_form, col_info = st.columns([2, 2])

    with col_form:
        st.markdown("#### Participant Identifier")
        participant_id = st.text_input(
            "Participant ID (optional)",
            value=st.session_state.get("participant_id", ""),
            placeholder="optional — initials or a nickname",
        )
        st.markdown("#### Your Background")
        training_level = st.selectbox(
            "Your background (optional)",
            ["Prefer not to say", "Not in healthcare", "Health student", "Clinician / health professional", "Educator / faculty"],
        )
        st.markdown("#### Practice Mode")
        mode_options = {
            "Guided Practice": "guided",
            "Independent Practice": "independent",
            "Faculty Review": "faculty",
        }
        mode_label = st.radio("Select mode", list(mode_options.keys()), index=1)
        learning_mode = mode_options[mode_label]

    with col_info:
        st.markdown("#### Mode Descriptions")
        st.markdown("""
**Guided Practice**
Hints and cue interpretations shown during the conversation. Good if you'd like more support.

**Independent Practice**
No hints; you get the full feedback report at the end. Recommended.

**Faculty Review**
Shows the behind-the-scenes scoring and internals — for reviewers and educators.
""")
        st.markdown(
            '<div class="info-box"><strong>Faculty Review unlocks:</strong> case learning '
            'objectives, trust barrier and red flags, the per-turn Evaluator QA panel, the '
            'state-machine transparency table, the evaluator benchmark, and the faculty '
            'rationale page.</div>',
            unsafe_allow_html=True,
        )

    pre_ratings = {}
    with st.expander("Pre-session self-efficacy (optional — for pilot data)", expanded=False):
        st.markdown(
            f'<div class="info-box">'
            f'Rate your confidence before this session (1 = Not at all confident, 5 = Very confident). '
            f'Optional — leave at the midpoint to skip.<br/>'
            f'<small>{SELF_EFFICACY_CAUTION}</small>'
            f'</div>',
            unsafe_allow_html=True,
        )
        for i, item in enumerate(SELF_EFFICACY_ITEMS):
            pre_ratings[f"se_{i+1}"] = st.slider(
                item,
                min_value=1, max_value=5,
                value=st.session_state.get(f"pre_se_{i+1}", 3),
                key=f"pre_se_slider_{i}",
            )
            st.session_state[f"pre_se_{i+1}"] = pre_ratings[f"se_{i+1}"]

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    st.markdown(
        f"#### Choose a Case &nbsp; <span style='font-size:0.8rem;font-weight:400;color:#5a6775;'>Mode: {mode_badge(learning_mode)}</span>",
        unsafe_allow_html=True,
    )

    def _commit_setup() -> None:
        st.session_state["participant_id"] = participant_id
        st.session_state["training_level"] = training_level
        st.session_state["learning_mode"]  = learning_mode
        st.session_state["pre_efficacy"]   = pre_ratings

    for c in CASE_CATALOG:
        hr_tag = ' &nbsp; <span class="badge-advanced">High-risk — faculty approval</span>' if c["id"] in HIGH_RISK_CASES else ""
        st.markdown(f"""
<div class="card">
  <div class="card-header">{c['case_id']} &nbsp;|&nbsp; {c['setting']}</div>
  <div class="card-title">{c['name']}, {c['age']} &nbsp; {difficulty_badge(c['difficulty'])}{hr_tag} &nbsp; <small style="font-weight:400;font-size:0.78rem;color:#5a6775;">Health literacy: {c['health_literacy']}</small></div>
  <div style="font-size:0.88rem;color:#334155;margin-bottom:4px;"><strong>Chief concern:</strong> {c['chief_concern']}</div>
  <div style="font-size:0.85rem;color:#475569;margin-bottom:4px;">{c['description']}</div>
  <div style="font-size:0.82rem;color:#64748b;"><strong>Communication challenge:</strong> {c['communication_challenge']}</div>
</div>
""", unsafe_allow_html=True)
        if st.button(f"Select {c['name']} ({c['case_id']})", key=f"sel_{c['id']}"):
            _commit_setup()
            st.session_state["case_id"] = c["id"]
            navigate_to("case_brief")


def page_case_brief() -> None:
    case_id = st.session_state.get("case_id", "alex")
    case    = next((c for c in CASE_CATALOG if c["id"] == case_id), CASE_CATALOG[0])
    mode    = st.session_state.get("learning_mode", "independent")
    is_high_risk = case_id in HIGH_RISK_CASES

    if is_high_risk and not st.session_state.get("high_risk_acknowledged"):
        render_header("High-Risk Case: Faculty Approval Required", "TC-005 — James Okafor", step_page="case_brief")
        st.markdown(f"""
<div class="notice-box">
<strong>⚠ TC-005 is a high-risk case.</strong><br/><br/>
This case involves a patient with passive suicidal ideation who has disclosed this to no one.
It is intended for advanced learners in contexts where a faculty member is present or available.
<br/><br/>
<strong>This case is not appropriate for unsupervised introductory use.</strong>
It requires familiarity with safe-messaging guidelines and mental health inquiry in primary care.
</div>
""", unsafe_allow_html=True)
        approved = st.checkbox(
            "I am a faculty member or advanced learner and I confirm this case is appropriate for this context.",
            key="high_risk_approve_cb",
        )
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Cancel — Choose a Different Case"):
                navigate_to("setup")
        with col2:
            if st.button("Proceed to Case Brief", disabled=not approved):
                st.session_state["high_risk_acknowledged"] = True
                st.session_state["enable_high_risk"] = True
                st.rerun()
        return

    if "start_data" not in st.session_state or st.session_state.get("start_data", {}).get("patient_id") != case_id:
        attempt_number       = st.session_state.get("attempt_number", 1)
        enable_high_risk     = st.session_state.get("enable_high_risk", False)
        pre_efficacy         = st.session_state.get("pre_efficacy", {})
        data = api("/start", "POST", {
            "patient_id":              case_id,
            "participant_id":          st.session_state.get("participant_id", ""),
            "attempt_number":          attempt_number,
            "learning_mode":           mode,
            "enable_high_risk_cases":  enable_high_risk,
            "pre_efficacy":            pre_efficacy,
            "browser_id":              st.session_state.get("browser_id", ""),
        })
        if data:
            st.session_state["start_data"]       = data
            st.session_state["session_id"]       = data["session_id"]
            st.session_state["messages"]         = []
            st.session_state["ended"]            = False
            st.session_state["visual_state"]     = "guarded"
            st.session_state["disclosure_layer"] = 1
            st.session_state["encounter_status"] = "active"
        else:
            render_header(f"Case Brief: {case['name']}, {case['age']}", case["case_id"], step_page="case_brief")
            st.info("This session could not be started (see the message above). If a daily limit was reached, please try again tomorrow.")
            if st.button("Back to Cases"):
                navigate_to("setup")
            return

    data = st.session_state.get("start_data", {})

    render_header(
        f"Case Brief: {case['name']}, {case['age']}",
        f"{case['case_id']} &nbsp;|&nbsp; {case['setting']} &nbsp;|&nbsp; {difficulty_badge(case['difficulty'])}",
        step_page="case_brief",
    )

    col_brief, col_sidebar = st.columns([3, 2])

    with col_brief:
        st.markdown("#### Case Description")
        st.markdown(data.get("case_description") or case["description"])

        st.markdown("#### Your Task")
        st.markdown(data.get("student_task") or "_No task description available._")

        st.markdown("#### Communication Challenge")
        challenge = data.get("communication_challenge") or case.get("communication_challenge", "")
        if challenge:
            st.markdown(f'<div class="notice-box">{challenge}</div>', unsafe_allow_html=True)

        st.markdown("#### Key Principle")
        principle = data.get("pre_encounter_principle", "")
        if principle:
            st.markdown(f'<div class="principle-box">{principle}</div>', unsafe_allow_html=True)

        clinical_task = data.get("clinical_task_description", "")
        key_qs        = data.get("key_clinical_questions", [])
        red_flags     = data.get("red_flags", [])

        st.markdown("#### Clinical Task")
        if clinical_task:
            st.markdown(f'<div class="clinical-task-box">{clinical_task}</div>', unsafe_allow_html=True)
        if key_qs:
            st.markdown("**Clinical history areas that matter in this case:**")
            for q in key_qs:
                st.markdown(f"- {q}")

        if mode == "faculty" and red_flags:
            with st.expander("Faculty View: Red Flags and Trust Barrier"):
                st.markdown("**Red flags to recognize:**")
                for r in red_flags:
                    st.markdown(f"- {r}")
                st.markdown(f"**Trust barrier:** {case['trust_barrier']}")
                st.markdown(f"**Health literacy:** {case['health_literacy']}")

    with col_sidebar:
        st.markdown("#### Learning Objectives")
        for obj in data.get("learning_objectives", []):
            st.markdown(f"- {obj}")

        st.markdown("#### Patient Profile")
        st.markdown(f"""
- **Name:** {case['name']}, {case['age']} years old
- **Setting:** {case['setting']}
- **Chief concern:** {case['chief_concern']}
- **Mode:** {mode_badge(mode)}
""", unsafe_allow_html=True)

        st.markdown(f'<div class="limit-box"><strong>Reminder.</strong> {CLINICAL_FRAMING}</div>', unsafe_allow_html=True)

    st.markdown("")
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Back to Cases"):
            navigate_to("setup")
    with col2:
        if st.button("Begin Encounter"):
            navigate_to("simulation")


def page_simulation() -> None:
    case_id    = st.session_state.get("case_id", "alex")
    session_id = st.session_state.get("session_id", "")
    mode       = st.session_state.get("learning_mode", "independent")
    ended      = st.session_state.get("ended", False)
    case       = next((c for c in CASE_CATALOG if c["id"] == case_id), CASE_CATALOG[0])

    visual_state     = st.session_state.get("visual_state", "guarded")
    encounter_status = st.session_state.get("encounter_status", "active")
    messages         = st.session_state.get("messages", [])
    start_data       = st.session_state.get("start_data", {})
    patient_name     = start_data.get("patient_name", case["name"])
    patient_intro    = start_data.get("patient_intro", "")
    student_turns    = sum(1 for m in messages if m.get("role") == "student")

    render_header(
        f"Encounter: {patient_name}, {case['age']}",
        f"{case['case_id']} &nbsp;|&nbsp; {case['setting']} &nbsp;|&nbsp; {mode_badge(mode)}",
        step_page="simulation",
    )

    if "hint_shown" not in st.session_state:
        st.session_state["hint_shown"] = False
    if "current_hint" not in st.session_state:
        st.session_state["current_hint"] = ""

    col_panel, col_chat = st.columns([2, 3])

    with col_panel:
        svg = get_patient_svg(visual_state, case_id, width=150)
        st.markdown(svg, unsafe_allow_html=True)

        cue_data = get_cue_panel_data(visual_state, mode)

        affect    = cue_data.get("affect_display", "")
        gaze      = cue_data.get("gaze_direction", "")
        posture   = cue_data.get("posture", "")
        resp_sty  = cue_data.get("response_style", "")
        latency   = cue_data.get("latency_marker", "")
        openness  = cue_data.get("openness_level", "")
        ambig     = cue_data.get("ambiguous_note", "")
        interp    = cue_data.get("possible_student_interpretation", "")
        ped_note  = cue_data.get("pedagogical_note", "")

        cue_rows = []
        if affect:    cue_rows.append(("Affect", affect))
        if gaze:      cue_rows.append(("Gaze", gaze))
        if posture:   cue_rows.append(("Posture", posture))
        if resp_sty:  cue_rows.append(("Response style", resp_sty))
        if latency:   cue_rows.append(("Latency", latency))
        if openness:  cue_rows.append(("Openness", openness))

        if cue_rows:
            rows_html = "".join(
                f'<div style="display:flex;gap:8px;margin-bottom:3px;">'
                f'<span style="font-size:0.68rem;font-weight:700;color:#64748b;min-width:96px;text-transform:uppercase;">{label}</span>'
                f'<span style="font-size:0.82rem;color:#1c2b3a;">{value}</span>'
                f'</div>'
                for label, value in cue_rows
            )
            st.markdown(f"""
<div class="cue-panel">
<div class="cue-label-text">Visual Cue Support Panel</div>
{rows_html}
</div>
""", unsafe_allow_html=True)

        if ambig:
            st.markdown(f'<div class="hint-box" style="font-size:0.80rem;"><strong>Note on ambiguity:</strong> {ambig}</div>', unsafe_allow_html=True)

        if interp and mode in ("guided", "faculty"):
            st.markdown(f'<div class="annotation-box"><strong>Possible interpretation:</strong> {interp}</div>', unsafe_allow_html=True)

        if ped_note:
            if mode == "guided":
                st.markdown(f'<div class="hint-box"><strong>Cue Interpretation</strong><br/>{ped_note}</div>', unsafe_allow_html=True)
            elif mode == "faculty":
                with st.expander("Pedagogical note (faculty)"):
                    st.markdown(ped_note)
            else:
                with st.expander("Cue reflection note"):
                    st.markdown(ped_note)

        if mode == "faculty":
            state_data = VISUAL_STATE_DATA.get(visual_state, {})
            with st.expander("Internal state values (faculty)"):
                rpt = api(f"/report/{session_id}")
                if rpt:
                    fs = rpt.get("final_state", {})
                    st.markdown(
                        f"Trust: **{fs.get('trust', '?')}** &nbsp;|&nbsp; "
                        f"Anxiety: **{fs.get('anxiety', '?')}** &nbsp;|&nbsp; "
                        f"Defensiveness: **{fs.get('defensiveness', '?')}** &nbsp;|&nbsp; "
                        f"Shame: **{fs.get('shame', '?')}**"
                    )
                st.caption("These are heuristic parameters, not measurements of real emotion.")

        st.markdown(f'<div style="font-size:0.72rem;color:#64748b;font-style:italic;margin-top:6px;">{CUE_REFLECTION_NOTE}</div>', unsafe_allow_html=True)

        st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
        st.markdown(f"""
<div style="font-size:0.78rem;color:#5a6775;line-height:1.8;">
<strong>{patient_name}</strong> &nbsp;|&nbsp; {case['age']} yrs<br/>
{case['setting']}<br/>
Turn: <strong>{student_turns}</strong> &nbsp;|&nbsp; Encounter: {status_label_html(encounter_status)}
</div>
""", unsafe_allow_html=True)

        if mode == "guided" and not ended:
            st.markdown("")
            if st.button("Request Hint", key="btn_hint"):
                hint_data = api(f"/hint/{session_id}")
                if hint_data:
                    st.session_state["current_hint"] = hint_data.get("hint", "")
                    st.session_state["hint_shown"]   = True
            if st.session_state.get("hint_shown") and st.session_state.get("current_hint"):
                st.markdown(f'<div class="hint-box"><strong>Hint</strong><br/>{st.session_state["current_hint"]}</div>', unsafe_allow_html=True)

        st.markdown("")
        st.markdown(f'<div class="limit-box" style="font-size:0.74rem;">{CUE_LIMITATION}</div>', unsafe_allow_html=True)

    with col_chat:
        if encounter_status == "ruptured" and not ended:
            st.markdown(
                '<div class="notice-box"><strong>The relationship is ruptured.</strong> '
                'Continued pressure, dismissiveness, or jargon may end the encounter. A genuine '
                'repair — naming what went wrong and inviting the patient back in — may help '
                'recover it.</div>',
                unsafe_allow_html=True,
            )

        if not messages and patient_intro:
            with st.chat_message("assistant", avatar=":material/person:"):
                st.markdown(f"**{patient_name}:** {patient_intro}")

        for msg in messages:
            if msg["role"] == "student":
                with st.chat_message("user"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("assistant", avatar=":material/person:"):
                    st.markdown(f"**{patient_name}:** {msg['content']}")

        if ended:
            st.markdown('<div class="info-box"><strong>Encounter ended.</strong> Click below to view your formative feedback.</div>', unsafe_allow_html=True)
            if st.button("View Formative Report", use_container_width=True):
                navigate_to("report")
        else:
            col_end, _ = st.columns([1, 3])
            with col_end:
                if st.button("End Encounter"):
                    st.session_state["ended"] = True
                    st.rerun()

            user_input = st.chat_input("Your response to the patient...")
            if user_input:
                user_input = user_input.strip()
                if not user_input:
                    st.warning("Please enter a response.")
                elif not _message_safe(user_input):
                    st.error("Your message contains text that appears to attempt to modify the simulation's behavior.")
                else:
                    st.session_state["hint_shown"]   = False
                    st.session_state["current_hint"] = ""

                    with st.chat_message("user"):
                        st.markdown(user_input)

                    with st.spinner(f"Waiting for {patient_name}..."):
                        result = api("/chat", "POST", {"session_id": session_id, "message": user_input})

                    if result:
                        patient_reply    = result["patient_reply"]
                        new_visual_state = result.get("visual_state", "guarded")
                        new_layer        = result.get("disclosure_layer", 1)
                        new_status       = result.get("encounter_status", "active")

                        st.session_state["visual_state"]     = new_visual_state
                        st.session_state["disclosure_layer"] = new_layer
                        st.session_state["encounter_status"] = new_status

                        messages.append({"role": "student", "content": user_input})
                        messages.append({"role": "patient", "content": patient_reply})
                        st.session_state["messages"] = messages

                        if new_status == "ended":
                            st.session_state["ended"] = True

                        with st.chat_message("assistant", avatar=":material/person:"):
                            st.markdown(f"**{patient_name}:** {patient_reply}")

                        st.rerun()


def _render_3_profile_report(rubric_result: dict, mode: str) -> None:
    PROFILE_DOMAIN_MAP = {
        "Relationship and Emotion": [
            "recognition_of_emotion",
            "empathy_validation",
            "patient_perspective",
            "cue_recognition",
        ],
        "Clinical Focus and Safety": [
            "patient_centered_inquiry",
            "clinical_information_gathering",
            "safety_professionalism",
        ],
        "Explanation and Shared Planning": [
            "opening_agenda_setting",
            "clarity_plain_language",
            "shared_decision_making",
        ],
    }

    all_domains = {d.get("id", ""): d for d in rubric_result.get("domains", [])}

    profile_labels = list(PROFILE_DOMAIN_MAP.keys())
    profile_cols   = st.columns(len(profile_labels))

    for col, profile_name in zip(profile_cols, profile_labels):
        domain_ids   = PROFILE_DOMAIN_MAP[profile_name]
        domain_items = [all_domains[did] for did in domain_ids if did in all_domains]
        if not domain_items:
            continue

        scores      = [d.get("score", 1) for d in domain_items]
        avg         = round(sum(scores) / len(scores), 1)
        best_domain = max(domain_items, key=lambda d: d.get("score", 1))
        worst_domain = min(domain_items, key=lambda d: d.get("score", 1))

        best_alt  = best_domain.get("stronger_alternative", "")
        worst_alt = worst_domain.get("stronger_alternative", "")

        with col:
            st.markdown(f"""
<div class="card">
<div class="card-header">{profile_name}</div>
<div class="card-title" style="font-size:1.3rem;">{avg} / 5</div>
<div style="font-size:0.84rem;color:#334155;margin-top:8px;">
<strong>Strength:</strong> {best_domain.get('name','')}<br/>
<span style="color:#2e7d52;font-size:0.82rem;">{best_domain.get('score_explanation','')[:160]}</span>
</div>
<div style="font-size:0.84rem;color:#334155;margin-top:8px;">
<strong>Priority improvement:</strong> {worst_domain.get('name','')}<br/>
<span style="color:#7d2e2e;font-size:0.82rem;">{worst_domain.get('improvement','')[:160]}</span>
</div>
</div>
""", unsafe_allow_html=True)
            if worst_alt:
                st.markdown(f'<div class="annotation-box" style="font-size:0.82rem;"><strong>Example revision:</strong><br/>"{worst_alt}"</div>', unsafe_allow_html=True)


def _render_faculty_qa_panel(timeline: list, session_id: str) -> None:
    st.markdown("### Evaluator QA Panel (Faculty)")
    st.markdown("""
<div class="limit-box">
Evaluator QA shows per-turn tag sources (rule-based vs. LLM-based) and rationale. This panel
supports faculty calibration and does not establish evaluator validity. Source: <em>rule_based</em>
= matched a fixed phrase; <em>llm_based</em> = LLM classification only;
<em>rule_based+llm_based</em> = matched both.
</div>
""", unsafe_allow_html=True)

    source_colors = {
        "rule_based":         "#e0f0e0",
        "llm_based":          "#e0eaff",
        "rule_based+llm_based": "#fff3cd",
        "injected":           "#f0e0ff",
    }

    for turn_data in timeline:
        turn    = turn_data.get("turn", "?")
        s_msg   = turn_data.get("student_message", "")
        tags    = turn_data.get("tags_detected", [])
        qa_data = turn_data.get("evaluator_qa", {})

        with st.expander(f"Turn {turn} — {len(tags)} tag(s)", expanded=False):
            st.markdown(f"**Student:** _{s_msg[:250]}_")

            if qa_data:
                for tag in sorted(qa_data.keys()):
                    qa    = qa_data[tag]
                    src   = qa.get("source", "unknown")
                    rule  = qa.get("rule_matched", "")
                    rat   = qa.get("rationale", "")
                    color = source_colors.get(src, "#f0f4f8")
                    src_label = src.replace("_", " ").title()
                    st.markdown(f"""
<div style="background:{color};border-radius:4px;padding:7px 12px;margin-bottom:5px;font-size:0.82rem;">
<strong>{tag.replace('_',' ')}</strong>
&nbsp;<span style="font-size:0.70rem;color:#475569;background:#ffffff;padding:1px 7px;border-radius:10px;border:1px solid #cbd5e1;">{src_label}</span>
{"<br/><span style='color:#475569;'>Matched phrase: <em>" + rule + "</em></span>" if rule else ""}
{"<br/>" + rat if rat else ""}
</div>
""", unsafe_allow_html=True)
            elif tags:
                for t in tags:
                    st.markdown(f"- `{t}`")
            else:
                st.markdown("_No tags detected._")

            st.markdown("**Faculty override:**")
            add_tags_str = st.text_input(
                "Add tags (comma-separated)",
                key=f"qa_add_{turn}",
                placeholder="e.g. empathy, open_question",
            )
            remove_tags_str = st.text_input(
                "Remove tags (comma-separated)",
                key=f"qa_remove_{turn}",
                placeholder="e.g. rushed_sensitive_question",
            )
            faculty_note_text = st.text_input(
                "Faculty note (optional)",
                key=f"qa_note_{turn}",
            )
            if st.button("Apply Override", key=f"qa_override_btn_{turn}"):
                payload = {
                    "session_id":   session_id,
                    "turn_number":  turn,
                    "add_tags":     [t.strip() for t in add_tags_str.split(",") if t.strip()],
                    "remove_tags":  [t.strip() for t in remove_tags_str.split(",") if t.strip()],
                    "faculty_note": faculty_note_text,
                }
                result = api("/faculty/tag_override", "POST", payload)
                if result:
                    st.success("Override applied.")


def _render_state_transparency_panel(session_id: str) -> None:
    st.markdown("### State Machine Transparency (Faculty)")
    st.markdown("""
<div class="limit-box">
The patient-state model is heuristic. Trust, anxiety, defensiveness, and shame are educational
parameters, not measurements of real patient emotion. Tag weights are approximate and have not
been calibrated against standardized patient observers.
</div>
""", unsafe_allow_html=True)
    sc = api("/state_config")
    if sc:
        disclaimer = sc.get("heuristic_disclaimer", "")
        if disclaimer:
            st.markdown(f'<div class="notice-box">{disclaimer}</div>', unsafe_allow_html=True)
        state_deltas = sc.get("state_deltas", {})
        if state_deltas:
            rows = []
            for tag, deltas in sorted(state_deltas.items()):
                rows.append(
                    f"| `{tag}` | "
                    + " | ".join(
                        f"{'+' if v>0 else ''}{v}" for v in [
                            deltas.get("trust", 0),
                            deltas.get("anxiety", 0),
                            deltas.get("defensiveness", 0),
                            deltas.get("shame", 0),
                        ]
                    )
                    + " |"
                )
            st.markdown("| Tag | Trust | Anxiety | Defensiveness | Shame |")
            st.markdown("|-----|-------|---------|---------------|-------|")
            for row in rows:
                st.markdown(row)


def _render_rubric_detail(rubric_result: dict) -> None:
    st.markdown("### Formative Rubric — 10 Domains")

    try:
        from rubric import get_overall_score
        avg_score = get_overall_score(rubric_result)
        st.markdown(f"Mean score across all domains: **{avg_score}/5.0**")
    except Exception:
        pass

    for d in rubric_result.get("domains", []):
        score = d.get("score", 1)
        sl    = score_label(score)
        fwk   = ""
        try:
            from rubric import RUBRIC_DOMAINS
            fwk_data = next((rd for rd in RUBRIC_DOMAINS if rd["id"] == d.get("id")), None)
            if fwk_data:
                fwk = fwk_data.get("framework", "")
        except Exception:
            pass

        with st.expander(f"{d.get('name', d.get('id', 'Domain'))}  —  {score}/5  ({sl})", expanded=(score <= 2)):
            st.markdown(f'<span class="score-badge">{score}/5 — {sl}</span>', unsafe_allow_html=True)
            if fwk:
                st.caption(f"Framework basis: {fwk}")
            st.markdown(f"**Assessment:** {d.get('score_explanation', '')}")
            evidence = d.get("evidence", "")
            if evidence and evidence != "Not observed in transcript":
                st.markdown(f"**Evidence:** _{evidence}_")
            else:
                st.markdown("_No direct evidence observed._")
            st.markdown(f"**Improvement target:** {d.get('improvement', '')}")
            alt = d.get("stronger_alternative", "")
            if alt:
                st.markdown(f'<div class="annotation-box"><strong>Stronger alternative:</strong><br/>"{alt}"</div>', unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

    missed_clinical  = rubric_result.get("missed_clinical_info", [])
    missed_emotional = rubric_result.get("missed_emotional_concerns", [])
    col_mc, col_me = st.columns(2)
    with col_mc:
        st.markdown("### Missed Clinical Information")
        for m in missed_clinical:
            if m:
                st.markdown(f"- {m}")
        if not missed_clinical:
            st.markdown("_None identified._")
    with col_me:
        st.markdown("### Missed Emotional Concerns")
        for m in missed_emotional:
            if m:
                st.markdown(f"- {m}")
        if not missed_emotional:
            st.markdown("_None identified._")

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

    integrated_ex = rubric_result.get("integrated_improvement_example", "")
    if integrated_ex:
        st.markdown("### Integrated Response Example")
        st.markdown("An example combining emotional acknowledgment with a relevant clinical question:")
        st.markdown(f'<div class="annotation-box" style="font-size:0.92rem;">{integrated_ex}</div>', unsafe_allow_html=True)
        st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

    missed_opp = rubric_result.get("missed_opportunities", [])
    if missed_opp:
        st.markdown("### Other Missed Opportunities")
        for m in missed_opp:
            if m:
                st.markdown(f"- {m}")
        st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)


def _rubric_domain_scores(rubric_result: dict) -> dict:
    out = {}
    for d in (rubric_result or {}).get("domains", []):
        did = d.get("id", "")
        if did:
            out[f"d_{did}"] = d.get("score", "")
    return out


def _format_transcript(report: dict) -> str:
    lines = []
    intro = st.session_state.get("start_data", {}).get("patient_intro", "")
    if intro:
        lines.append(f"[0] Patient (opening): {intro.strip()}")
    for t in report.get("timeline", []):
        turn = t.get("turn", "?")
        student = (t.get("student_message") or "").strip()
        patient = (t.get("patient_reply") or "").strip()
        lines.append(f"[{turn}] Student: {student}")
        if patient:
            lines.append(f"    Patient: {patient}")
    return "\n".join(lines)[:40000]


def _log_session_summary(report: dict, rubric_result: dict, mode: str) -> None:
    if not (rubric_result and sheets_logger.is_configured()):
        return
    session_id = st.session_state.get("session_id", "")
    flag = f"_logged_summary_{session_id}"
    if st.session_state.get(flag):
        return
    final_state = report.get("final_state", {})
    try:
        from rubric import get_overall_score
        mean = get_overall_score(rubric_result)
    except Exception:
        mean = ""
    pre = st.session_state.get("pre_efficacy", {}) or {}
    record = {
        "record_type":      "session_summary",
        "session_id":       session_id,
        "participant_id":   st.session_state.get("participant_id", ""),
        "case_id":          st.session_state.get("case_id", ""),
        "attempt_number":   st.session_state.get("attempt_number", 1),
        "learning_mode":    mode,
        "total_turns":      report.get("total_turns", 0),
        "encounter_status": report.get("encounter_status", ""),
        "final_trust":      final_state.get("trust", ""),
        "rupture_count":    len(report.get("rupture_events", [])),
        "end_reason":       report.get("end_reason", ""),
        "rubric_mean":      mean,
    }
    record.update({f"pre_se_{i}": pre.get(f"se_{i}", "") for i in range(1, 6)})
    record.update(_rubric_domain_scores(rubric_result))
    record["transcript"] = _format_transcript(report)
    if sheets_logger.log_record(record):
        st.session_state[flag] = True


def page_report() -> None:
    case_id      = st.session_state.get("case_id", "alex")
    session_id   = st.session_state.get("session_id", "")
    case         = next((c for c in CASE_CATALOG if c["id"] == case_id), CASE_CATALOG[0])
    start_data   = st.session_state.get("start_data", {})
    patient_name = start_data.get("patient_name", case["name"])
    mode         = st.session_state.get("learning_mode", "independent")

    render_header(
        f"Formative Report: {case['case_id']} — {patient_name}",
        "Formative feedback only. Not a validated assessment instrument.",
        step_page="report",
    )

    report = api(f"/report/{session_id}")
    if not report:
        st.error("Could not load report data.")
        return

    final_state      = report.get("final_state", {})
    total_turns      = report.get("total_turns", 0)
    encounter_status = report.get("encounter_status", "active")
    timeline         = report.get("timeline", [])
    rupture_events   = report.get("rupture_events", [])
    end_reason       = report.get("end_reason", "")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Turns", total_turns)
    with col2:
        st.metric("Encounter", encounter_status.capitalize())
    with col3:
        st.metric("Final Trust", f"{final_state.get('trust', 0)}/100")
    with col4:
        st.metric("Rupture Events", len(rupture_events))

    if encounter_status == "ended" and end_reason:
        st.markdown(f'<div class="notice-box"><strong>Why the encounter ended.</strong> {end_reason}</div>', unsafe_allow_html=True)

    if rupture_events:
        st.markdown('<div class="notice-box"><strong>Rupture events:</strong> One or more ruptures were recorded. See the visual cue timeline for details.</div>', unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    st.markdown(f'<div class="clinical-task-box"><strong>Clinical framing.</strong> {CLINICAL_FRAMING}</div>', unsafe_allow_html=True)

    rubric_result = st.session_state.get("rubric_result")
    if rubric_result is None:
        st.info("Your encounter summary is shown above. Generating the formative rubric now — this usually takes 20–30 seconds.")
        with st.spinner("Scoring communication across the rubric domains..."):
            rubric_response = api(f"/rubric/{session_id}", timeout=90)
        if rubric_response:
            rubric_result = rubric_response.get("rubric")
            st.session_state["rubric_result"]    = rubric_result
            st.session_state["framework_note"]   = rubric_response.get("framework_note", "")
            st.session_state["validity_caution"] = rubric_response.get("validity_caution", "")

    if rubric_result:
        _log_session_summary(report, rubric_result, mode)
        if mode == "faculty" and st.session_state.get(f"_logged_summary_{session_id}"):
            st.caption("Pilot logging: this session was recorded to the Google Sheet.")

        st.markdown(f"""
<div class="limit-box">
<strong>Framework basis:</strong> {st.session_state.get('framework_note', '')}
&nbsp;&nbsp;<strong>Validity caution:</strong> {st.session_state.get('validity_caution', RUBRIC_LIMITATION)}
</div>
""", unsafe_allow_html=True)

        st.markdown("### Communication Profile")
        _render_3_profile_report(rubric_result, mode)

        overall = rubric_result.get("overall_profile", "")
        if overall:
            st.markdown(f'<div class="card"><div class="card-header">Overall Profile</div>{overall}</div>', unsafe_allow_html=True)

        st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
        show_detail = st.toggle(
            "Show full rubric detail (10 domains, missed items, and example revisions)",
            value=False,
            help="The three-profile summary above is the headline feedback. Expand for the full breakdown.",
        )
        if show_detail:
            _render_rubric_detail(rubric_result)

        st.markdown("### Safety and Professionalism Notes")
        safety_flags = rubric_result.get("safety_flags", [])
        if safety_flags:
            for flag in safety_flags:
                st.markdown(f'<div class="safety-note">{flag}</div>', unsafe_allow_html=True)
        else:
            st.markdown("_No safety or professionalism concerns flagged._")

    else:
        st.warning("Rubric scoring was unavailable.")

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    st.markdown("### Visual Cue Timeline")
    st.markdown(f'<div class="limit-box">{CUE_LIMITATION}</div>', unsafe_allow_html=True)

    if timeline:
        for turn_data in timeline:
            turn  = turn_data.get("turn", "?")
            vs    = turn_data.get("visual_state", "guarded")
            cl    = turn_data.get("cue_label", "")
            s_msg = turn_data.get("student_message", "")
            tags  = turn_data.get("tags_detected", [])
            sdata = VISUAL_STATE_DATA.get(vs, {})
            ped   = sdata.get("pedagogical_note", "")
            cue_d = sdata.get("cue_description", "")
            ruptured_flag = turn_data.get("rupture_occurred", False)

            header = f"Turn {turn} — {cl}"
            if ruptured_flag:
                header += " ⚠ Rupture"

            with st.expander(header, expanded=False):
                st.markdown(f"**Student:** _{s_msg[:200]}{'...' if len(s_msg) > 200 else ''}_")
                if tags:
                    st.markdown(f"**Behaviors detected:** {', '.join(t.replace('_', ' ') for t in tags)}")
                if cue_d:
                    st.markdown(f"**Patient cue support:** {cue_d}")
                if ped:
                    st.markdown(f'<div class="hint-box"><strong>Communication lesson:</strong><br/>{ped}</div>', unsafe_allow_html=True)
                if ruptured_flag:
                    st.markdown('<div class="notice-box"><strong>Rupture recorded on this turn.</strong> This event is stored in the session even if the relationship partially recovered.</div>', unsafe_allow_html=True)
    else:
        st.markdown("_No turns recorded._")

    if mode == "faculty" and timeline:
        st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
        _render_faculty_qa_panel(timeline, session_id)
        st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
        _render_state_transparency_panel(session_id)

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    st.markdown("### Tool Limitations")
    st.markdown(f"""
<div class="limit-box">
<strong>Text format.</strong> {TOOL_LIMITATION}
<br/><br/>
<strong>Patient-state model.</strong> {STATE_MODEL_NOTE}
<br/><br/>
<strong>Rubric.</strong> {RUBRIC_LIMITATION}
<br/><br/>
<strong>Visual cue panel.</strong> {CUE_LIMITATION}
</div>
""", unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        if st.button("View Model Transcript", use_container_width=True):
            navigate_to("model_transcript")
    with col_b:
        if st.button("Retry This Case", use_container_width=True):
            _reset_for_retry()
            navigate_to("case_brief")
    with col_c:
        if st.button("Reflection and Export", use_container_width=True):
            navigate_to("reflection")
    with col_d:
        if mode == "faculty":
            if st.button("Faculty Rationale", use_container_width=True):
                navigate_to("faculty_rationale")


def page_model_transcript() -> None:
    case_id = st.session_state.get("case_id", "alex")
    case    = next((c for c in CASE_CATALOG if c["id"] == case_id), CASE_CATALOG[0])

    if "model_transcript_data" not in st.session_state:
        with st.spinner("Loading model transcript..."):
            mt_data = api(f"/model_transcript/{case_id}")
        if mt_data:
            st.session_state["model_transcript_data"] = mt_data

    mt = st.session_state.get("model_transcript_data")

    render_header(
        f"Model Transcript: {case['name']}, {case['age']}",
        f"{case['case_id']} — Annotated example of integrated clinical communication",
    )

    if not mt:
        st.error("Model transcript unavailable.")
        if st.button("Back to Report"):
            navigate_to("report")
        return

    st.markdown("""
<div class="limit-box">
<strong>About model transcripts:</strong> These are pre-written examples that illustrate
strong integrated communication — attending to both the patient's emotional state and
the clinical information needed. They are not generated by the language model on demand.
Annotations explain the reasoning behind each choice.
</div>
""", unsafe_allow_html=True)

    st.markdown(f"**Summary:** {mt.get('summary', '')}")

    key_principles = mt.get("key_principles", [])
    if key_principles:
        st.markdown("#### Key Principles Demonstrated")
        for p in key_principles:
            st.markdown(f"- {p}")

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    st.markdown("#### Model Transcript")

    patient_name = st.session_state.get("start_data", {}).get("patient_name", case["name"])

    for turn_data in mt.get("turns", []):
        turn        = turn_data.get("turn", "?")
        student_msg = turn_data.get("student", "")
        patient_msg = turn_data.get("patient", "")
        annotation  = turn_data.get("annotation", "")
        tags        = turn_data.get("tags_demonstrated", [])

        st.markdown(f"**Turn {turn}**")
        st.markdown(f"""
<div class="model-student"><strong>Student (model):</strong><br/>{student_msg}</div>
<div class="model-patient"><strong>{patient_name}:</strong><br/>{patient_msg}</div>
""", unsafe_allow_html=True)
        if annotation:
            st.markdown(f'<div class="annotation-box"><strong>Annotation:</strong> {annotation}</div>', unsafe_allow_html=True)
        if tags:
            st.caption(f"Behaviors demonstrated: {', '.join(t.replace('_', ' ') for t in tags)}")
        st.markdown("")

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

    after = mt.get("after_report", {})
    if after:
        st.markdown("#### How to Use This for Your Next Attempt")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**What the model did**")
            st.markdown(after.get("what_model_did", ""))
        with col2:
            st.markdown("**Common mistakes to avoid**")
            st.markdown(after.get("common_mistakes", ""))
        with col3:
            st.markdown("**Your next attempt goal**")
            st.markdown(f'<div class="principle-box">{after.get("next_attempt_goal", "")}</div>', unsafe_allow_html=True)

    st.markdown("")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Back to Report"):
            navigate_to("report")
    with col2:
        if st.button("Retry This Case"):
            _reset_for_retry()
            navigate_to("case_brief")
    with col3:
        if st.button("Reflection and Export"):
            navigate_to("reflection")


def page_reflection() -> None:
    case_id       = st.session_state.get("case_id", "alex")
    session_id    = st.session_state.get("session_id", "")
    case          = next((c for c in CASE_CATALOG if c["id"] == case_id), CASE_CATALOG[0])
    rubric_result = st.session_state.get("rubric_result")
    mode          = st.session_state.get("learning_mode", "independent")

    render_header(
        f"Reflection: {case['case_id']} — {case['name']}",
        "Formative reflection, post-session ratings, and export",
    )

    st.markdown("### Reflection Questions")
    st.markdown('<div class="info-box">Reflection is most useful when answered before looking at the model transcript. Write honestly — this is for your own learning.</div>', unsafe_allow_html=True)

    reflection_prompts = rubric_result.get("reflection_prompts", []) if rubric_result else []
    default_prompts = [
        "What was the most difficult moment in this encounter, and what made it difficult?",
        "Was there a moment where you had to choose between addressing the patient's emotional state and asking a clinical question? What did you do, and would you do it differently?",
        "What visual or emotional cue did you noticed in the patient's responses, and how did it change what you said next? If you did not adjust, what would you do differently now?",
    ]
    prompts     = reflection_prompts if reflection_prompts else default_prompts
    reflections = {}
    for i, prompt in enumerate(prompts):
        st.markdown(f"**{i + 1}.** {prompt}")
        reflections[f"q{i+1}"] = st.text_area(
            f"Response to question {i+1}",
            label_visibility="collapsed",
            key=f"reflection_{i}",
            height=100,
        )

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    st.markdown("### Post-Session Self-Efficacy (Pilot)")
    st.markdown(
        f'<div class="info-box">'
        f'Rate your confidence now, after this session (1 = Not at all confident, 5 = Very confident).<br/>'
        f'<small>{SELF_EFFICACY_CAUTION}</small>'
        f'</div>',
        unsafe_allow_html=True,
    )
    post_ratings = {}
    for i, item in enumerate(SELF_EFFICACY_ITEMS):
        post_ratings[f"se_{i+1}"] = st.slider(
            item,
            min_value=1, max_value=5,
            value=st.session_state.get(f"post_se_{i+1}", 3),
            key=f"post_se_slider_{i}",
        )
        st.session_state[f"post_se_{i+1}"] = post_ratings[f"se_{i+1}"]

    pre_ratings = st.session_state.get("pre_efficacy", {})
    if pre_ratings and post_ratings:
        deltas = {
            k: post_ratings.get(k, 3) - pre_ratings.get(k, 3)
            for k in post_ratings
        }
        non_zero = [(k, v) for k, v in deltas.items() if v != 0]
        if non_zero:
            st.markdown("**Self-efficacy change (pre → post):**")
            for k, v in non_zero:
                idx    = int(k.split("_")[1]) - 1
                label  = SELF_EFFICACY_ITEMS[idx]
                sign   = "+" if v > 0 else ""
                st.markdown(f"- {label}: **{sign}{v}**")

    usability_rating  = st.slider("Overall tool usability (1–5)", 1, 5, 3, key="usability_rating")
    usefulness_rating = st.slider("Educational usefulness (1–5)", 1, 5, 3, key="usefulness_rating")
    qualitative_text  = st.text_area("Any other comments about the tool (optional)", key="qualitative_comment", height=80)

    if st.button("Submit Post-Session Ratings"):
        payload = {
            "session_id": session_id,
            "phase":      "post",
            "ratings":    post_ratings,
            "usability":  usability_rating,
            "usefulness": usefulness_rating,
            "qualitative": {"comment": qualitative_text},
        }
        result = api("/self_efficacy", "POST", payload)
        if result:
            st.success("Post-session ratings submitted.")
        if pre_ratings:
            pre_payload = {
                "session_id": session_id,
                "phase":      "pre",
                "ratings":    pre_ratings,
            }
            api("/self_efficacy", "POST", pre_payload)

        if sheets_logger.is_configured():
            post_record = {
                "record_type":        "post_feedback",
                "session_id":         session_id,
                "participant_id":     st.session_state.get("participant_id", ""),
                "case_id":            case_id,
                "learning_mode":      mode,
                "usability":          usability_rating,
                "usefulness":         usefulness_rating,
                "reflection_q1":      reflections.get("q1", ""),
                "reflection_q2":      reflections.get("q2", ""),
                "reflection_q3":      reflections.get("q3", ""),
                "qualitative_comment": qualitative_text,
            }
            post_record.update({f"post_se_{i}": post_ratings.get(f"se_{i}", "") for i in range(1, 6)})
            post_record.update({f"pre_se_{i}": pre_ratings.get(f"se_{i}", "") for i in range(1, 6)})
            if sheets_logger.log_record(post_record):
                st.caption("Your pilot responses were recorded.")

    prev_rubric = st.session_state.get("previous_rubric")
    if prev_rubric and rubric_result:
        st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
        st.markdown("### Attempt Comparison")
        st.markdown('<div class="info-box">Scores are model-generated and may vary slightly between runs.</div>', unsafe_allow_html=True)

        prev_domains = {d["id"]: d["score"] for d in prev_rubric.get("domains", [])}
        curr_domains = {d["id"]: d["score"] for d in rubric_result.get("domains", [])}

        st.markdown("| Domain | Attempt 1 | Attempt 2 | Change |")
        st.markdown("|--------|-----------|-----------|--------|")
        for d in rubric_result.get("domains", []):
            did    = d.get("id", "")
            dname  = d.get("name", did)
            prev_s = prev_domains.get(did, "—")
            curr_s = curr_domains.get(did, "—")
            if isinstance(prev_s, int) and isinstance(curr_s, int):
                delta  = curr_s - prev_s
                change = f"+{delta}" if delta > 0 else str(delta) if delta < 0 else "—"
            else:
                change = "—"
            st.markdown(f"| {dname} | {prev_s} | {curr_s} | {change} |")

    if mode == "faculty":
        st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
        st.markdown("### Evaluator Benchmark (Faculty)")
        st.markdown("""
<div class="limit-box">
Benchmark results reflect agreement between the evaluator and 20 pre-written test cases.
This is a calibration check, not a validation study. Agreement rates between 70-85% are
expected given the ambiguity inherent in clinical communication classification.
</div>
""", unsafe_allow_html=True)
        if st.button("Run Evaluator Benchmark"):
            with st.spinner("Running 20 benchmark cases..."):
                bm_result = api("/benchmark")
            if bm_result:
                overall = bm_result.get("overall_agreement_rate", 0)
                st.metric("Overall Agreement Rate", f"{overall:.0%}")
                cases = bm_result.get("cases", [])
                if cases:
                    st.markdown("| # | Label | Expected | Detected | Missed | Extra | Agreement |")
                    st.markdown("|---|-------|----------|----------|--------|-------|-----------|")
                    for c in cases:
                        expected = ", ".join(c.get("expected_tags", []))
                        detected = ", ".join(c.get("detected_tags", []))
                        missed   = ", ".join(c.get("missed_tags", []))
                        extra    = ", ".join(c.get("extra_tags", []))
                        agree    = f"{c.get('agreement_rate', 0):.0%}"
                        st.markdown(f"| {c.get('id','?')} | {c.get('label','')[:40]} | {expected[:30]} | {detected[:30]} | {missed[:30]} | {extra[:30]} | {agree} |")

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    st.markdown("### Export")
    st.markdown('<div class="limit-box">Export includes session transcript, tag counts, rubric scores, reflection responses, and self-efficacy data. No real patient data should be included.</div>', unsafe_allow_html=True)

    col_json, col_csv = st.columns(2)
    with col_json:
        json_data = _build_json_export(session_id, reflections, post_ratings)
        if json_data:
            st.download_button(
                "Download Session Data (JSON)",
                data=json.dumps(json_data, indent=2),
                file_name=f"trustmed_{case_id}_{session_id[:8]}.json",
                mime="application/json",
                use_container_width=True,
            )
    with col_csv:
        csv_data = _build_csv_export(session_id, reflections)
        if csv_data:
            st.download_button(
                "Download Rubric Summary (CSV)",
                data=csv_data,
                file_name=f"trustmed_rubric_{case_id}_{session_id[:8]}.csv",
                mime="text/csv",
                use_container_width=True,
            )

    st.markdown("")
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("Back to Report"):
            navigate_to("report")
    with col2:
        if mode == "faculty":
            if st.button("Faculty Rationale"):
                navigate_to("faculty_rationale")
    with col3:
        if st.button("New Case / Return to Setup"):
            _reset_all_session()
            navigate_to("setup")


def _build_json_export(session_id: str, reflections: dict, post_ratings: dict = None) -> dict:
    export_data = api(f"/export/{session_id}", timeout=30) or {}
    pre_ratings = st.session_state.get("pre_efficacy", {})
    deltas = {}
    if pre_ratings and post_ratings:
        deltas = {k: (post_ratings.get(k, 3) - pre_ratings.get(k, 3)) for k in post_ratings}
    return {
        "export_version": "3.0",
        "export_disclaimer": (
            "Generated by a formative educational rehearsal tool. "
            "Rubric scores are model-generated and not validated. "
            "All patient data is fictional."
        ),
        "session":                export_data,
        "rubric":                 st.session_state.get("rubric_result"),
        "reflection_responses":   reflections,
        "pre_efficacy":           pre_ratings,
        "post_efficacy":          post_ratings or {},
        "self_efficacy_change":   deltas,
        "exported_at":            datetime.utcnow().isoformat(),
    }


def _build_csv_export(session_id: str, reflections: dict) -> str:
    rubric_result = st.session_state.get("rubric_result")
    if not rubric_result:
        return ""
    output         = io.StringIO()
    writer         = csv.writer(output)
    case_id        = st.session_state.get("case_id", "")
    attempt_number = st.session_state.get("attempt_number", 1)
    writer.writerow(["session_id", "case_id", "attempt_number", "domain_id", "domain_name", "score", "score_label", "improvement"])
    for d in rubric_result.get("domains", []):
        writer.writerow([
            session_id, case_id, attempt_number,
            d.get("id", ""), d.get("name", ""),
            d.get("score", ""), score_label(d.get("score", 1)),
            d.get("improvement", ""),
        ])
    return output.getvalue()


def page_faculty_rationale() -> None:
    render_header(
        "Faculty Rationale",
        "Design justification, limitations, and pilot guidance for instructors",
    )

    SECTIONS = [
        (
            "Purpose",
            """TrustMed is a formative rehearsal environment for clinical communication. It is not an
assessment instrument, a replacement for standardized patients, or a source of validated
competency data. Its purpose is to give learners a low-stakes space to rehearse integrated
communication — attending simultaneously to patient emotion and clinical information
gathering — and to receive structured formative feedback with instructional annotations.""",
        ),
        (
            "What it trains",
            """The tool trains three integrated skill areas:

1. **Relationship and emotion** — Empathy, trust-building, recognizing and responding to
emotional cues, managing distress and shame, avoiding dismissive or premature reassurance.

2. **Clinical focus and safety** — Asking focused and relevant history questions, recognizing
red flags, navigating sensitive topics appropriately, avoiding unsafe closure.

3. **Explanation and shared planning** — Plain language, communicating uncertainty honestly,
proposing safe next steps, supporting patient autonomy and decision-making.

These are taught as an integrated system, not as isolated competencies.""",
        ),
        (
            "What it does not claim",
            f"""The tool does not:
- Measure clinical competence or diagnostic reasoning
- Validate communication proficiency
- Reproduce the difficulty of live patient interaction
- Generate reliable scores for formal assessment

{RUBRIC_LIMITATION}

{STATE_MODEL_NOTE}""",
        ),
        (
            "Educational design",
            """Each case is designed around a specific trust barrier and communication challenge. Cases
progress from introductory (TC-001 Rosa Gutierrez — plain language and adherence) through
intermediate (TC-001 Alex Chen, TC-003 Marcus Webb, TC-006 Priya Sharma) to advanced
(TC-002 Diane Flores, TC-005 James Okafor). TC-005 is gated and requires faculty approval.

Practice modes:
- **Guided** — Cue interpretation shown directly; hints available; suitable for early learners.
- **Independent** — No mid-encounter guidance; full formative report on completion; default mode.
- **Faculty Review** — Exposes learning objectives, trust barrier, red flags, evaluator QA panel,
and state machine transparency panel; intended for instructor preview and faculty-led debriefs.""",
        ),
        (
            "Rubric basis",
            """The 10-domain rubric is structured around established clinical communication frameworks
including the Calgary-Cambridge Guide, the Four Habits Model, and safe-messaging principles
for sensitive topics. Domains are grouped into three profiles: Relationship and Emotion,
Clinical Focus and Safety, and Explanation and Shared Planning.

Rubric scores are generated by a large language model (Claude) and are formative only. They
have not been tested for inter-rater reliability against human evaluators. Before using scores
in any formal educational context, faculty should:

1. Review sample transcripts and rubric outputs independently
2. Conduct a small inter-rater reliability check with a clinical communication educator
3. Treat scores as prompts for discussion, not as proficiency determinations""",
        ),
        (
            "Heuristic state model",
            f"""{STATE_MODEL_NOTE}

The patient-state parameters (trust, anxiety, defensiveness, shame) are updated by a heuristic
tag-weight system. Each communication behavior tag applies fixed deltas. The Faculty Review
mode exposes the state delta table via the State Machine Transparency panel in the report view.

Tag detection uses a two-layer system: (1) rule-based phrase matching and (2) LLM-based
classification. The Evaluator QA panel in Faculty Review mode shows per-tag source labels
(rule_based, llm_based, or rule_based+llm_based) and LLM rationale for each turn.

The benchmark endpoint runs 20 pre-written test cases and reports agreement rates. Expected
overall agreement is 70–85%, limited by inherent classification ambiguity.""",
        ),
        (
            "Data collected",
            """Session data includes: an optional self-entered participant code, case ID, attempt
number, the full conversation transcript, detected communication tags, rubric scores, pre/post
self-efficacy ratings, rupture events, usability/usefulness ratings, and free-text reflections.

No real patient data is collected and all cases are fictional. When Google Sheets logging is
configured, each session appends rows to a private spreadsheet the researcher controls —
including the scores, ratings, and the full conversation transcript, with no identifiers unless
a participant voluntarily types one. Participants may also export their own session as JSON/CSV.""",
        ),
        (
            "Suggested pilot use",
            """Recommended pilot design:
1. Assign two cases at different difficulty levels (e.g., TC-004 + TC-001 or TC-003)
2. Collect pre- and post-session self-efficacy ratings via the tool
3. Export session JSON for aggregate tag and rubric analysis
4. Conduct a 20-minute faculty-led debrief using the model transcript and Evaluator QA panel
5. Compare rubric scores with a 5-minute independent faculty rating of the same transcript

Pilot data should be used to calibrate the tool, not to demonstrate learning gains, without
a controlled design.""",
        ),
        (
            "Limitations",
            FULL_LIMITATIONS,
        ),
        (
            "Recommended next validation steps",
            """For reviewer-defensible use:

1. **Face validity** — Expert review of rubric domains by ≥2 clinical communication educators
2. **Content validity** — Review of case scenarios by ≥1 practicing clinician per specialty
3. **Inter-rater reliability** — Compare rubric scores on 20 transcripts against human rater scores
4. **Benchmark calibration** — Report evaluator benchmark results publicly per evaluator version
5. **Pilot study** — Compare pre/post self-efficacy with matched control group
6. **Concurrent validity (longer term)** — Correlate rubric scores with OSCE performance
7. **Safe-messaging review** — TC-005 should be reviewed by a mental health clinician before
   deployment beyond faculty-supervised settings""",
        ),
    ]

    for title, content in SECTIONS:
        with st.expander(title, expanded=(title == "Limitations")):
            st.markdown(content)

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    mode = st.session_state.get("learning_mode", "faculty")
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Back to Report"):
            navigate_to("report")
    with col2:
        if st.button("Return to Setup"):
            navigate_to("setup")


PAGES = {
    "landing":           page_landing,
    "setup":             page_setup,
    "case_brief":        page_case_brief,
    "simulation":        page_simulation,
    "report":            page_report,
    "model_transcript":  page_model_transcript,
    "reflection":        page_reflection,
    "faculty_rationale": page_faculty_rationale,
}


def _get_secret(key: str):
    val = os.environ.get(key)
    if val:
        return val
    try:
        if key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return None


def _bridge_secrets_to_env() -> None:
    for key in ("ANTHROPIC_API_KEY", "APP_PASSWORD", "CLAUDE_MODEL",
                "MAX_SESSIONS_PER_DAY", "MAX_PER_BROWSER_PER_DAY", "MAX_TURNS_PER_SESSION"):
        val = _get_secret(key)
        if val and not os.environ.get(key):
            os.environ[key] = val


def _backend_healthy() -> bool:
    try:
        return requests.get(f"{API_URL}/docs", timeout=2).status_code == 200
    except requests.RequestException:
        return False


@st.cache_resource(show_spinner=False)
def _ensure_backend() -> bool:
    if _backend_healthy():
        return True
    try:
        subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            env=os.environ.copy(),
        )
    except Exception:
        return False
    for _ in range(60):
        if _backend_healthy():
            return True
        time.sleep(0.5)
    return False


def _ensure_browser_id() -> str:
    bid = st.session_state.get("browser_id")
    if not bid:
        bid = uuid.uuid4().hex[:16]
        st.session_state["browser_id"] = bid
    return bid


def main() -> None:
    inject_css()
    _bridge_secrets_to_env()
    _ensure_browser_id()
    with st.spinner("Starting the simulation backend..."):
        backend_up = _ensure_backend()
    if not backend_up:
        st.error("The simulation backend did not start. Please reload the page in a moment.")
        return
    if "page" not in st.session_state:
        st.session_state["page"] = "landing"
    PAGES.get(st.session_state["page"], page_landing)()


if __name__ == "__main__":
    main()
