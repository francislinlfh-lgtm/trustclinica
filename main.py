
import uuid
from datetime import datetime, date
from typing import List, Optional

import anthropic as _anthropic
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from patient_case import PATIENTS
from evaluator import evaluate_tags, evaluate_with_qa
from state_machine import apply_tags, can_disclose, get_response_mode, PRESSURE_TAGS, get_disclosure_layer
from llm import generate_patient_response
from database import init_db, save_session, load_session
from rubric import score_session
from nonverbal import get_visual_state, get_visual_cue_for_timeline
from model_transcripts import get_model_transcript

import os as _os
load_dotenv(dotenv_path=_os.path.join(_os.path.dirname(__file__), ".env"))

init_db()

REPEATED_PRESSURE_WINDOW    = 3
REPEATED_PRESSURE_THRESHOLD = 2

CLINICAL_DRIFT_WINDOW = 3

CLINICAL_ENGAGEMENT_TAGS = {
    "relevant_clinical_question",
    "red_flag_acknowledged",
    "safe_next_step",
    "appropriate_uncertainty",
    "plain_explanation",
}

def _check_repeated_pressure(
    current_tags: List[str],
    recent_tags: List[List[str]],
) -> bool:
    window = list(recent_tags[-(REPEATED_PRESSURE_WINDOW - 1):]) + [current_tags]
    return sum(
        1 for t in window if any(tag in PRESSURE_TAGS for tag in t)
    ) >= REPEATED_PRESSURE_THRESHOLD

def _check_clinical_drift(
    current_tags: List[str],
    recent_tags: List[List[str]],
    turn_number: int,
) -> bool:
    """
    Return True if the student has gone CLINICAL_DRIFT_WINDOW turns without
    any clinical engagement tags, AND we are past the opening turns.

    Clinical drift only fires after turn 2 — early turns are expected to be
    focused on rapport and agenda-setting.
    """
    if turn_number <= 2:
        return False
    window = list(recent_tags[-(CLINICAL_DRIFT_WINDOW - 1):]) + [current_tags]
    if len(window) < CLINICAL_DRIFT_WINDOW:
        return False
    return not any(
        any(tag in CLINICAL_ENGAGEMENT_TAGS for tag in turn_tags)
        for turn_tags in window
    )

def _select_hint(session: dict) -> str:
    """
    Return a contextual hint for the current session state.

    Hint selection is state-driven, not just sequential:
    - If the student has never used empathy/open questions → hint about emotional acknowledgment
    - If the encounter is strained → hint about communication repair
    - If many turns passed with no confidentiality tag (for adolescent case) → specific hint
    - Otherwise → cycle through the patient's pre-written hints by turn number
    """
    patient    = session["patient"]
    tag_counts = session.get("tag_counts", {})
    encounter_status = session.get("encounter_status", "active")
    turn_number = len(session.get("timeline", []))
    hints       = getattr(patient, "hints", [])

    if not hints:
        return "Consider asking an open-ended question about what concerns the patient most."

    if encounter_status in ("strained", "ruptured"):
        return (
            "The encounter has become strained. Consider acknowledging that the "
            "conversation may have felt difficult, before continuing with clinical questions."
        )

    empathy_count = tag_counts.get("empathy", 0) + tag_counts.get("open_question", 0)
    if empathy_count == 0 and turn_number >= 2:
        return hints[0]

    hint_index = min(turn_number, len(hints) - 1)
    return hints[hint_index]

HIGH_RISK_CASES = {"james"}

class StartRequest(BaseModel):
    patient_id:              str  = "alex"
    participant_id:          str  = ""
    attempt_number:          int  = 1
    learning_mode:           str  = "independent"
    enable_high_risk_cases:  bool = False
    pre_efficacy:            dict = {}
    browser_id:              str  = ""

class SelfEfficacyRequest(BaseModel):
    session_id:   str
    phase:        str
    ratings:      dict
    usability:    int = 0
    usefulness:   int = 0
    qualitative:  dict = {}

class TagOverrideRequest(BaseModel):
    session_id:   str
    turn_number:  int
    add_tags:     List[str] = []
    remove_tags:  List[str] = []
    faculty_note: str = ""

class StartResponse(BaseModel):
    session_id:               str
    patient_id:               str
    patient_name:             str
    patient_intro:            str
    initial_state:            dict
    learning_objectives:      List[str]
    communication_challenge:  str
    pre_encounter_principle:  str
    case_description:         str
    student_task:             str
    clinical_task_description: str
    key_clinical_questions:   List[str]
    red_flags:                List[str]

class ChatRequest(BaseModel):
    session_id: str
    message:    str

class ChatResponse(BaseModel):
    patient_reply:     str
    tags_detected:     List[str]
    state:             dict
    disclosure_layer:  int
    encounter_status:  str
    response_mode:     str
    visual_state:      str
    cue_label:         str

class ReportResponse(BaseModel):
    session_id:       str
    patient_id:       str
    created_at:       str
    total_turns:      int
    final_state:      dict
    disclosure_layer: int
    encounter_status: str
    timeline:         List[dict]
    feedback:         dict
    rupture_events:   List[dict] = []
    end_reason:       str = ""

class RubricResponse(BaseModel):
    session_id:            str
    patient_id:            str
    total_turns:           int
    rubric:                dict
    disclosure_layer:      int
    final_encounter_status: str
    framework_note:        str
    validity_caution:      str

class ExportResponse(BaseModel):
    export_version:    str
    generated_at:      str
    session_id:        str
    patient_id:        str
    patient_name:      str
    patient_setting:   str
    created_at:        str
    participant_id:    str
    attempt_number:    int
    learning_mode:     str
    total_turns:       int
    final_state:       dict
    disclosure_layer:  int
    encounter_status:  str
    tag_counts:        dict
    timeline:          List[dict]
    nonverbal_timeline: List[dict]

class HintResponse(BaseModel):
    session_id:  str
    turn_number: int
    hint:        str

class ModelTranscriptResponse(BaseModel):
    case_id:         str
    summary:         str
    key_principles:  List[str]
    turns:           List[dict]
    key_moments:     List[dict]
    after_report:    dict

class CasesResponse(BaseModel):
    cases: List[dict]

app = FastAPI(
    title="Clinical Communication Rehearsal Tool — API",
    description=(
        "Backend for the Text-Based Clinical Communication Rehearsal Tool.\n\n"
        "This tool provides formative, text-based practice with fictional patient encounters. "
        "It is not a validated clinical assessment instrument and does not measure "
        "real patient trust or clinical communication competence.\n\n"
        "**All patient cases are entirely fictional.** Do not enter real patient information.\n\n"
        "**Available cases:** alex, diane, marcus, rosa, james, priya\n\n"
        "**Endpoints:**\n"
        "- POST /start — create a session\n"
        "- POST /chat — send a message\n"
        "- GET /hint/{session_id} — request a contextual hint (guided mode)\n"
        "- GET /report/{session_id} — turn-by-turn report\n"
        "- GET /rubric/{session_id} — 9-domain formative rubric\n"
        "- GET /model_transcript/{case_id} — annotated model transcript\n"
        "- GET /export/{session_id} — full export data\n"
        "- GET /cases — list of available cases with metadata"
    ),
    version="0.5.0",
)

@app.get("/state_config", tags=["Faculty"])
def get_state_config():
    """
    Return the heuristic state machine configuration for faculty transparency.

    This endpoint exposes the state delta weights and key constants.
    These values are heuristic educational parameters, not empirically
    validated measures of patient emotion or trust.
    """
    from state_machine import STATE_DELTAS, MAX_TRUST_GAIN_PER_TURN, MAX_TRUST_LOSS_PER_TURN, REPAIR_MAX_TRUST_GAIN, DIMINISHING_RETURN_TAGS, PRESSURE_TAGS
    return {
        "model_type": "heuristic_educational",
        "disclaimer": (
            "This state machine is a heuristic educational model. "
            "State values are not empirically estimated measures of patient emotion or trust. "
            "They are used to create consistent, inspectable training scenarios and to connect "
            "communication behaviors with simulated patient responses."
        ),
        "state_variables": ["trust", "anxiety", "defensiveness", "shame"],
        "state_variable_range": "0–100 (heuristic, not validated)",
        "tag_deltas": STATE_DELTAS,
        "max_trust_gain_per_turn": MAX_TRUST_GAIN_PER_TURN,
        "max_trust_loss_per_turn": MAX_TRUST_LOSS_PER_TURN,
        "repair_max_trust_gain":   REPAIR_MAX_TRUST_GAIN,
        "diminishing_return_tags": list(DIMINISHING_RETURN_TAGS),
        "pressure_tags":           list(PRESSURE_TAGS),
        "encounter_statuses":      ["active", "strained", "ruptured", "repair_attempted", "partially_repaired", "ended"],
    }


@app.post("/self_efficacy", tags=["Pilot"])
def save_self_efficacy(request: SelfEfficacyRequest):
    """Store pre or post self-efficacy ratings for a session."""
    session = load_session(request.session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session '{request.session_id}' not found.")

    if request.phase == "pre":
        session["pre_efficacy"] = {
            "ratings":   request.ratings,
            "recorded_at": datetime.utcnow().isoformat(),
        }
    elif request.phase == "post":
        session["post_efficacy"] = {
            "ratings":    request.ratings,
            "usability":  request.usability,
            "usefulness": request.usefulness,
            "qualitative": request.qualitative,
            "recorded_at": datetime.utcnow().isoformat(),
        }
    else:
        raise HTTPException(status_code=400, detail="phase must be 'pre' or 'post'.")

    save_session(request.session_id, session)
    return {"status": "saved", "phase": request.phase}


@app.post("/faculty/tag_override", tags=["Faculty"])
def faculty_tag_override(request: TagOverrideRequest):
    """
    Allow faculty to add, remove, or annotate evaluator tags for a specific turn.
    Only available in faculty review mode.

    Changes are stored alongside the original tags for comparison.
    The original model-generated rubric is not changed — a faculty-adjusted
    rubric can be requested by calling /rubric/{session_id}?use_overrides=true.
    """
    from evaluator import VALID_TAGS
    session = load_session(request.session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session '{request.session_id}' not found.")

    if session.get("learning_mode") != "faculty":
        raise HTTPException(status_code=403, detail="Tag overrides are only available in Faculty Review Mode.")

    timeline = session.get("timeline", [])
    turn_idx = request.turn_number - 1
    if turn_idx < 0 or turn_idx >= len(timeline):
        raise HTTPException(status_code=400, detail=f"Turn {request.turn_number} not found.")

    for tag in request.add_tags + request.remove_tags:
        if tag not in VALID_TAGS:
            raise HTTPException(status_code=400, detail=f"Unknown tag: {tag}")

    overrides = session.get("faculty_qa_overrides", {})
    overrides[str(request.turn_number)] = {
        "add_tags":    request.add_tags,
        "remove_tags": request.remove_tags,
        "faculty_note": request.faculty_note,
        "recorded_at": datetime.utcnow().isoformat(),
    }
    session["faculty_qa_overrides"] = overrides
    save_session(request.session_id, session)
    return {"status": "saved", "turn": request.turn_number}


@app.get("/benchmark", tags=["Faculty"])
def run_benchmark():
    """
    Run the evaluator against the built-in benchmark set.

    Returns expected tags, detected tags, missed tags, extra tags,
    and a rough agreement rate for each test case.

    Evaluator QA supports transparency and calibration;
    it does not establish evaluator validity.
    """
    try:
        from benchmark import BENCHMARK_CASES
    except ImportError:
        raise HTTPException(status_code=503, detail="benchmark.py not found.")

    results = []
    total   = 0
    agreed  = 0

    for case in BENCHMARK_CASES:
        msg      = case["message"]
        expected = set(case["expected_tags"])
        detected = set(evaluate_tags(msg))
        missed   = expected - detected
        extra    = detected - expected
        overlap  = expected & detected
        case_agreement = len(overlap) / max(len(expected | detected), 1)

        total  += 1
        agreed += case_agreement

        results.append({
            "id":            case.get("id", total),
            "label":         case.get("label", ""),
            "message":       msg,
            "expected_tags": sorted(expected),
            "detected_tags": sorted(detected),
            "missed_tags":   sorted(missed),
            "extra_tags":    sorted(extra),
            "agreement":     round(case_agreement, 2),
        })

    overall_agreement = round(agreed / total, 3) if total > 0 else 0

    return {
        "disclaimer": (
            "Evaluator QA supports transparency and calibration; "
            "it does not establish evaluator validity."
        ),
        "total_cases":        total,
        "overall_agreement":  overall_agreement,
        "results":            results,
    }


@app.get("/cases", response_model=CasesResponse, tags=["Cases"])
def list_cases() -> CasesResponse:
    """Return metadata for all available patient cases."""
    cases = []
    for pid, patient in PATIENTS.items():
        cases.append({
            "id":                     patient.id,
            "case_id":                getattr(patient, "case_id", ""),
            "name":                   patient.name,
            "age":                    patient.age,
            "setting":                getattr(patient, "setting", ""),
            "chief_concern":          patient.chief_complaint,
            "difficulty":             getattr(patient, "communication_difficulty", "Intermediate"),
            "health_literacy":        getattr(patient, "health_literacy", "Moderate"),
            "trust_barrier":          getattr(patient, "trust_barrier", ""),
            "case_description":       getattr(patient, "case_description", ""),
            "communication_challenge": getattr(patient, "communication_challenge", ""),
            "learning_objectives":    getattr(patient, "learning_objectives", []),
        })
    return CasesResponse(cases=cases)

MAX_SESSIONS_PER_DAY    = int(_os.getenv("MAX_SESSIONS_PER_DAY", "30"))
MAX_PER_BROWSER_PER_DAY = int(_os.getenv("MAX_PER_BROWSER_PER_DAY", "10"))
MAX_TURNS_PER_SESSION   = int(_os.getenv("MAX_TURNS_PER_SESSION", "10"))

_daily_session_counts: dict = {}
_browser_day_counts:   dict = {}


def _today() -> str:
    return date.today().isoformat()


@app.post("/start", response_model=StartResponse, tags=["Simulation"])
def start_session(request: StartRequest = StartRequest()) -> StartResponse:
    """Create a new rehearsal session with a chosen patient case."""
    patient = PATIENTS.get(request.patient_id)
    if patient is None:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown patient_id '{request.patient_id}'. Available: {list(PATIENTS.keys())}",
        )

    valid_modes = {"guided", "independent", "faculty"}
    if request.learning_mode not in valid_modes:
        raise HTTPException(status_code=400, detail=f"learning_mode must be one of: {valid_modes}")

    if patient.id in HIGH_RISK_CASES and not request.enable_high_risk_cases:
        raise HTTPException(
            status_code=403,
            detail=(
                f"Case '{patient.id}' involves advanced clinical content including suicidal ideation. "
                "Set enable_high_risk_cases=true to proceed. "
                "Faculty review is recommended before using this case in a pilot."
            ),
        )

    today = _today()
    if _daily_session_counts.get(today, 0) >= MAX_SESSIONS_PER_DAY:
        raise HTTPException(
            status_code=429,
            detail=(
                "This tool has reached its daily testing capacity. Please check back tomorrow — "
                "and thanks for helping test it."
            ),
        )
    bid = (request.browser_id or "").strip()
    if bid and _browser_day_counts.get((today, bid), 0) >= MAX_PER_BROWSER_PER_DAY:
        raise HTTPException(
            status_code=429,
            detail=(
                f"You've reached the limit of {MAX_PER_BROWSER_PER_DAY} practice sessions per day "
                "from this browser. Please come back tomorrow."
            ),
        )

    session_id    = str(uuid.uuid4())
    initial_state = patient.initial_state.copy()

    session_data = {
        "session_id":              session_id,
        "patient_id":              patient.id,
        "patient":                 patient,
        "state":                   initial_state,
        "timeline":                [],
        "created_at":              datetime.utcnow().isoformat(),
        "conversation_history":    [
            {"role": "user",      "content": "(The consultation begins. You enter the room.)"},
            {"role": "assistant", "content": patient.intro_message},
        ],
        "tag_counts":              {},
        "recent_tags":             [],
        "encounter_status":        "active",
        "nonverbal_timeline":      [],
        "participant_id":          request.participant_id,
        "attempt_number":          request.attempt_number,
        "learning_mode":           request.learning_mode,
        "disclosure_layer":        1,
        "rupture_events":          [],
        "pre_efficacy":            request.pre_efficacy,
        "post_efficacy":           {},
        "faculty_qa_overrides":    {},
    }

    save_session(session_id, session_data)

    _daily_session_counts[today] = _daily_session_counts.get(today, 0) + 1
    if bid:
        _browser_day_counts[(today, bid)] = _browser_day_counts.get((today, bid), 0) + 1

    return StartResponse(
        session_id=session_id,
        patient_id=patient.id,
        patient_name=patient.name,
        patient_intro=patient.intro_message,
        initial_state=initial_state.to_dict(),
        learning_objectives=getattr(patient, "learning_objectives", []),
        communication_challenge=getattr(patient, "communication_challenge", ""),
        pre_encounter_principle=getattr(patient, "pre_encounter_principle", ""),
        case_description=getattr(patient, "case_description", ""),
        student_task=getattr(patient, "student_task", ""),
        clinical_task_description=getattr(patient, "clinical_task_description", ""),
        key_clinical_questions=getattr(patient, "key_clinical_questions", []),
        red_flags=getattr(patient, "red_flags", []),
    )

@app.post("/chat", response_model=ChatResponse, tags=["Simulation"])
def chat(request: ChatRequest) -> ChatResponse:
    """Send a message to the simulated patient and receive a response."""
    session = load_session(request.session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session '{request.session_id}' not found.")

    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    real_data_keywords = ["date of birth", "social security", "dob:", "ssn:", "mrn:"]
    if any(kw in request.message.lower() for kw in real_data_keywords):
        raise HTTPException(
            status_code=400,
            detail=(
                "Your message appears to contain real patient-identifying information. "
                "This tool uses fictional cases only. Do not enter real patient data."
            ),
        )

    patient          = session["patient"]
    old_state        = session["state"].copy()
    encounter_status = session.get("encounter_status", "active")
    recent_tags      = session.get("recent_tags", [])

    learning_mode = session.get("learning_mode", "independent")
    if learning_mode == "faculty":
        eval_result = evaluate_with_qa(request.message)
        tags    = eval_result["tags"]
        qa_data = eval_result["qa"]
    else:
        tags    = evaluate_tags(request.message)
        qa_data = {}

    if _check_repeated_pressure(tags, recent_tags):
        if "repeated_pressure" not in tags:
            tags = list(tags) + ["repeated_pressure"]
            qa_data["repeated_pressure"] = {"source": "injected", "rule_matched": None, "rationale": "Injected by backend: pressure pattern detected across multiple turns."}

    turn_number_so_far = len(session.get("timeline", []))
    if _check_clinical_drift(tags, recent_tags, turn_number_so_far):
        if "clinical_drift" not in tags:
            tags = list(tags) + ["clinical_drift"]
            qa_data["clinical_drift"] = {"source": "injected", "rule_matched": None, "rationale": "Injected by backend: no clinical engagement detected in last 3 turns."}

    new_state, new_encounter_status, rupture_occurred = apply_tags(
        state=old_state,
        tags=tags,
        recent_tags=recent_tags,
        encounter_status=encounter_status,
    )

    if rupture_occurred:
        rupture_events = session.get("rupture_events", [])
        rupture_events.append({
            "turn":             turn_number_so_far + 1,
            "trigger_tags":     [t for t in tags if t in {"critical_boundary_violation", "repeated_pressure", "judgmental_tone", "coercive_pressure", "accusatory_question"}],
            "status_at_rupture": new_encounter_status,
            "trust_at_rupture": new_state.trust,
        })
        session["rupture_events"] = rupture_events
    session["state"]            = new_state
    session["encounter_status"] = new_encounter_status

    if new_encounter_status == "ended" and not session.get("end_reason"):
        if "critical_boundary_violation" in tags:
            session["end_reason"] = (
                "The encounter ended because a critical professional boundary was crossed "
                "(for example, a threat or an inappropriate personal comment). In a real "
                "clinical setting this would end the interaction and require escalation."
            )
        elif new_state.trust <= 15:
            session["end_reason"] = (
                "The encounter ended because the patient's trust fell to the point of "
                "disengagement. Repeated pressure or dismissiveness without a genuine repair "
                "attempt can cause a simulated patient to withdraw."
            )
        else:
            session["end_reason"] = (
                "The encounter ended. Review the visual cue timeline to see how the "
                "patient's state changed across the conversation."
            )

    layer = get_disclosure_layer(new_state.trust, patient.disclosure_threshold)
    session["disclosure_layer"] = layer

    mode = get_response_mode(new_state, patient.disclosure_threshold, new_encounter_status)

    visual_state = get_visual_state(
        trust=new_state.trust,
        anxiety=new_state.anxiety,
        defensiveness=new_state.defensiveness,
        shame=new_state.shame,
        encounter_status=new_encounter_status,
        recent_tags=recent_tags + [tags],
    )

    session["conversation_history"].append({"role": "user", "content": request.message})

    try:
        patient_reply = generate_patient_response(
            patient=patient,
            state=new_state,
            conversation_history=session["conversation_history"],
            disclosure_layer=layer,
            response_mode=mode,
            encounter_status=new_encounter_status,
        )
    except _anthropic.BadRequestError as e:
        detail = str(e)
        if "credit balance" in detail.lower():
            raise HTTPException(status_code=503, detail="Anthropic API error: insufficient credits.")
        raise HTTPException(status_code=503, detail=f"Anthropic API error: {detail}")
    except _anthropic.APIError as e:
        raise HTTPException(status_code=503, detail=f"Anthropic API error: {e}")

    session["conversation_history"].append({"role": "assistant", "content": patient_reply})
    session["recent_tags"] = (recent_tags + [tags])[-REPEATED_PRESSURE_WINDOW:]

    if new_encounter_status != "ended" and (len(session["timeline"]) + 1) >= MAX_TURNS_PER_SESSION:
        new_encounter_status = "ended"
        session["encounter_status"] = "ended"
        if not session.get("end_reason"):
            session["end_reason"] = (
                f"This session reached its limit of {MAX_TURNS_PER_SESSION} messages. "
                "Ending here so you can review your feedback."
            )

    tag_counts = session.get("tag_counts", {})
    for tag in tags:
        tag_counts[tag] = tag_counts.get(tag, 0) + 1
    session["tag_counts"] = tag_counts

    turn_number = len(session["timeline"]) + 1

    cue_record = get_visual_cue_for_timeline(visual_state, tags, turn_number)

    nonverbal_timeline = session.get("nonverbal_timeline", [])
    nonverbal_timeline.append(cue_record)
    session["nonverbal_timeline"] = nonverbal_timeline

    session["timeline"].append({
        "turn":             turn_number,
        "student_message":  request.message,
        "patient_reply":    patient_reply,
        "tags_detected":    tags,
        "state_before":     old_state.to_dict(),
        "state_after":      new_state.to_dict(),
        "state_delta":      {k: new_state.to_dict()[k] - old_state.to_dict()[k] for k in new_state.to_dict()},
        "disclosure_layer": layer,
        "encounter_status": new_encounter_status,
        "response_mode":    mode,
        "visual_state":     visual_state,
        "cue_label":        cue_record["cue_label"],
        "evaluator_qa":     qa_data,
        "rupture_occurred": rupture_occurred,
    })

    save_session(request.session_id, session)

    return ChatResponse(
        patient_reply=patient_reply,
        tags_detected=tags,
        state=new_state.to_dict(),
        disclosure_layer=layer,
        encounter_status=new_encounter_status,
        response_mode=mode,
        visual_state=visual_state,
        cue_label=cue_record["cue_label"],
    )

@app.get("/hint/{session_id}", response_model=HintResponse, tags=["Simulation"])
def get_hint(session_id: str) -> HintResponse:
    """
    Return a contextual hint for the current session state.

    Hints are available in guided practice mode. They scaffold communication
    reasoning without giving away the answer.
    """
    session = load_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")

    hint        = _select_hint(session)
    turn_number = len(session.get("timeline", []))

    return HintResponse(
        session_id=session_id,
        turn_number=turn_number,
        hint=hint,
    )

@app.get("/model_transcript/{case_id}", response_model=ModelTranscriptResponse, tags=["Learning"])
def model_transcript(case_id: str) -> ModelTranscriptResponse:
    """
    Return the annotated model transcript for a case.

    Model transcripts are pre-written by the tool developers (not generated
    by the LLM on demand) to ensure pedagogical consistency.
    They show what strong communication looks like in the same case
    the student just practiced.
    """
    if case_id not in PATIENTS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown case_id '{case_id}'. Available: {list(PATIENTS.keys())}",
        )

    mt = get_model_transcript(case_id)
    if mt is None:
        raise HTTPException(
            status_code=404,
            detail=f"No model transcript available for case '{case_id}'.",
        )

    return ModelTranscriptResponse(
        case_id=case_id,
        summary=mt.get("summary", ""),
        key_principles=mt.get("key_principles", []),
        turns=mt.get("turns", []),
        key_moments=mt.get("key_moments", []),
        after_report=mt.get("after_report", {}),
    )

@app.get("/report/{session_id}", response_model=ReportResponse, tags=["Evaluation"])
def get_report(session_id: str) -> ReportResponse:
    """Turn-by-turn session report. See /rubric for the full formative rubric."""
    session = load_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")

    timeline   = session["timeline"]
    final_state = session["state"]
    patient     = session["patient"]
    tag_counts  = session.get("tag_counts", {})
    layer       = session.get("disclosure_layer", 1)

    if not tag_counts and timeline:
        for turn in timeline:
            for tag in turn.get("tags_detected", []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

    feedback_lines = []
    if timeline:
        initial_trust = timeline[0]["state_before"]["trust"]
        trust_delta   = final_state.trust - initial_trust
        if trust_delta > 20:
            feedback_lines.append(f"Trust increased by {trust_delta} points across the encounter.")
        elif trust_delta > 0:
            feedback_lines.append(f"Trust improved slightly ({trust_delta:+d} pts).")
        elif trust_delta < -10:
            feedback_lines.append(f"Trust dropped by {abs(trust_delta)} points.")

    layer_label = {
        1: "Patient concerns remained largely unexplored.",
        2: "Patient expressed surface emotional concern.",
        3: "Patient shared contextual background.",
        4: "Patient partially indicated a deeper concern.",
        5: "Patient fully disclosed hidden concern.",
    }.get(layer, "")
    if layer_label:
        feedback_lines.append(layer_label)

    return ReportResponse(
        session_id=session_id,
        patient_id=patient.id,
        created_at=session["created_at"],
        total_turns=len(timeline),
        final_state=final_state.to_dict(),
        disclosure_layer=layer,
        encounter_status=session.get("encounter_status", "active"),
        timeline=timeline,
        feedback={"tag_counts": tag_counts, "summary": feedback_lines},
        rupture_events=session.get("rupture_events", []),
        end_reason=session.get("end_reason", ""),
    )

@app.get("/rubric/{session_id}", response_model=RubricResponse, tags=["Evaluation"])
def get_rubric(session_id: str) -> RubricResponse:
    """
    Generate a 9-domain formative rubric evaluation for a completed session.

    Calls Claude Sonnet to holistically score the full transcript.
    May take 15-25 seconds. Results are not cached server-side.

    DISCLAIMER: Rubric scores are model-generated formative feedback.
    They are not validated clinical assessment measures.
    The rubric domains are derived from established communication frameworks
    but have not been validated as an assessment instrument.
    """
    from rubric import RUBRIC_FRAMEWORK_NOTE, RUBRIC_VALIDITY_CAUTION

    session = load_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")

    patient  = session["patient"]
    timeline = session["timeline"]

    if not timeline:
        raise HTTPException(
            status_code=400,
            detail="No conversation turns recorded. Complete at least one exchange before requesting rubric evaluation.",
        )

    tag_counts        = session.get("tag_counts", {})
    nonverbal_timeline = session.get("nonverbal_timeline", [])
    layer             = session.get("disclosure_layer", 1)

    rubric_result = score_session(
        conversation_history=session["conversation_history"],
        patient_name=patient.name,
        patient_age=patient.age,
        setting=getattr(patient, "setting", "Primary Care"),
        chief_concern=patient.chief_complaint,
        trust_barrier=getattr(patient, "trust_barrier", ""),
        health_literacy=getattr(patient, "health_literacy", "Moderate"),
        tag_counts=tag_counts,
        nonverbal_timeline=nonverbal_timeline,
        key_clinical_questions=getattr(patient, "key_clinical_questions", []),
        red_flags=getattr(patient, "red_flags", []),
    )

    if rubric_result is None:
        raise HTTPException(
            status_code=503,
            detail="Rubric scoring failed. This may be due to API unavailability or an insufficient conversation length.",
        )

    return RubricResponse(
        session_id=session_id,
        patient_id=patient.id,
        total_turns=len(timeline),
        rubric=rubric_result,
        disclosure_layer=layer,
        final_encounter_status=session.get("encounter_status", "active"),
        framework_note=RUBRIC_FRAMEWORK_NOTE,
        validity_caution=RUBRIC_VALIDITY_CAUTION,
    )

@app.get("/export/{session_id}", response_model=ExportResponse, tags=["Export"])
def export_session(session_id: str) -> ExportResponse:
    """
    Export complete session data for research or quality improvement.

    PRIVACY NOTE: Do not include real patient-identifying information in session messages.
    Use fictional or de-identified content only.

    NOTE: Rubric scores are not included in this export.
    Call /rubric/{session_id} separately and combine client-side if needed.
    """
    session = load_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")

    patient    = session["patient"]
    timeline   = session["timeline"]
    final_state = session["state"]

    pre_eff  = session.get("pre_efficacy", {})
    post_eff = session.get("post_efficacy", {})

    pre_ratings  = pre_eff.get("ratings", {})
    post_ratings = post_eff.get("ratings", {})
    change_scores = {
        k: post_ratings[k] - pre_ratings[k]
        for k in pre_ratings
        if k in post_ratings and isinstance(pre_ratings[k], (int, float)) and isinstance(post_ratings[k], (int, float))
    }

    return {
        "export_version":         "3.0",
        "export_disclaimer":      (
            "Generated by a formative educational rehearsal tool. "
            "Rubric scores are model-generated and not validated. "
            "All patient data is fictional. "
            "Self-efficacy ratings are exploratory and should not be interpreted "
            "as proof of learning without a controlled study."
        ),
        "generated_at":           datetime.utcnow().isoformat(),
        "session_id":             session_id,
        "patient_id":             patient.id,
        "patient_name":           patient.name,
        "patient_setting":        getattr(patient, "setting", ""),
        "created_at":             session["created_at"],
        "participant_id":         session.get("participant_id", ""),
        "attempt_number":         session.get("attempt_number", 1),
        "learning_mode":          session.get("learning_mode", "independent"),
        "total_turns":            len(timeline),
        "final_state":            final_state.to_dict(),
        "disclosure_layer":       session.get("disclosure_layer", 1),
        "encounter_status":       session.get("encounter_status", "active"),
        "rupture_events":         session.get("rupture_events", []),
        "tag_counts":             session.get("tag_counts", {}),
        "timeline":               timeline,
        "nonverbal_timeline":     session.get("nonverbal_timeline", []),
        "pre_efficacy":           pre_eff,
        "post_efficacy":          post_eff,
        "self_efficacy_change":   change_scores,
        "faculty_qa_overrides":   session.get("faculty_qa_overrides", {}),
    }
