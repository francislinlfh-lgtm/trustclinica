from typing import List, Dict

CUE_PANEL_LIMITATION = (
    "The visual cue panel provides simplified representations of patient affect, gaze, posture, "
    "and openness. It is intended to support cue-recognition practice, not to reproduce real body "
    "language, facial micro-expressions, tone of voice, silence, or real-time interpersonal pressure."
)

CUE_REFLECTION_NOTE = (
    "Visual cues are prompts for reflection, not definitive evidence of what a patient feels."
)

VISUAL_STATE_DATA: Dict[str, dict] = {
    "guarded": {
        "label": "Guarded",
        "cue_description": "Minimal eye contact. Short, careful answers. Arms close to body.",
        "eye_contact": "Intermittent, looking away",
        "affect_display": "Flat, controlled — little visible emotional change",
        "gaze_direction": "Intermittent; often looks away or toward the floor",
        "posture": "Closed; arms close to body or lightly crossed",
        "response_style": "Short answers; minimal elaboration; answers the question asked and stops",
        "latency_marker": "Slight pause before responding",
        "openness_level": "Low",
        "ambiguous_note": "Guardedness can reflect distrust, discomfort, a private communication style, or cultural norms — not necessarily deception.",
        "possible_student_interpretation": (
            "Patient may have unspoken concerns. May be assessing whether you are safe to confide in. "
            "An open question about what worries them most — before continuing with clinical questions — "
            "tends to be more effective than pressing further."
        ),
        "pedagogical_note": (
            "The patient may have unspoken concerns. "
            "An open question about what worries them most — asked before moving on to "
            "further clinical questions — tends to be more effective than continuing to probe."
        ),
        "color": "#475569",
    },
    "anxious": {
        "label": "Anxious",
        "cue_description": "Visibly tense. Answers are rushed or fragmented.",
        "eye_contact": "Brief, searching for reassurance",
        "affect_display": "Anxious, tense — visible discomfort",
        "gaze_direction": "Brief, darting; searching for reassurance from clinician",
        "posture": "Tense; may be leaning slightly forward or gripping objects",
        "response_style": "Rushed, fragmented, or repetitive answers; may return to the same worry",
        "latency_marker": "Answers quickly, sometimes interrupting",
        "openness_level": "Low to moderate — anxious but not yet withdrawn",
        "ambiguous_note": "High anxiety may appear as urgency or over-answering. It can be confused with agitation or pushiness.",
        "possible_student_interpretation": (
            "Patient is worried. Naming the anxiety directly before moving to further questions — "
            "'I can see this has been worrying you' — often reduces anxiety more effectively than "
            "proceeding without acknowledgment."
        ),
        "pedagogical_note": (
            "The patient's anxiety is visible. Naming it directly before asking more "
            "clinical questions — 'I can see this has been worrying you' — "
            "often reduces anxiety more effectively than proceeding without acknowledgment."
        ),
        "color": "#b45309",
    },
    "confused": {
        "label": "Confused",
        "cue_description": "Slight pause before responding. Uncertain expression.",
        "eye_contact": "Searching, uncertain",
        "affect_display": "Uncertain, slightly lost — processing difficulty",
        "gaze_direction": "Looking around, searching; uncertain",
        "posture": "Slightly tense or stiff; uncertain stillness",
        "response_style": "Hesitant; may ask for clarification or partially answer",
        "latency_marker": "Longer pause; visible search for meaning",
        "openness_level": "Uncertain — confused rather than guarded",
        "ambiguous_note": "Confusion may be about terminology, about what is being asked, or about what the clinical findings mean.",
        "possible_student_interpretation": (
            "Patient may not have understood your phrasing or terminology. "
            "Consider checking: 'Does that make sense?' or rephrasing with plainer language."
        ),
        "pedagogical_note": (
            "The patient may not have understood your phrasing or terminology. "
            "Consider checking: 'Does that make sense?' or rephrasing "
            "with plainer, everyday language."
        ),
        "color": "#7c3aed",
    },
    "skeptical": {
        "label": "Skeptical",
        "cue_description": "Slight hesitation. Evaluating before responding.",
        "eye_contact": "Steady but evaluating",
        "affect_display": "Neutral but watchful — assessing credibility",
        "gaze_direction": "Steady, direct, evaluating",
        "posture": "Upright, slightly pulled back; considering stance",
        "response_style": "Measured, testing answers; may ask clarifying questions",
        "latency_marker": "Slight pause; thoughtful before responding",
        "openness_level": "Low to moderate — not hostile, but not yet trusting",
        "ambiguous_note": "Skepticism in a patient may reflect prior negative experiences with healthcare, not hostility toward this clinician.",
        "possible_student_interpretation": (
            "Patient seems unconvinced. Premature reassurance tends to increase skepticism. "
            "Acknowledging uncertainty honestly is often more effective."
        ),
        "pedagogical_note": (
            "The patient seems unconvinced. Premature reassurance or promises "
            "you cannot guarantee tend to increase skepticism rather than reduce it. "
            "Acknowledging uncertainty honestly is often more effective."
        ),
        "color": "#64748b",
    },
    "overwhelmed": {
        "label": "Overwhelmed",
        "cue_description": "Distant expression. Longer pauses. Voice may be quieter.",
        "eye_contact": "Distant, avoiding",
        "affect_display": "Flooded, distant — emotional overload",
        "gaze_direction": "Vacant or downward; not engaging with the clinician",
        "posture": "Collapsed or very still; lowered shoulders",
        "response_style": "Very short, quiet answers; may not fully process questions",
        "latency_marker": "Long pauses; processing delay",
        "openness_level": "Very low — emotional system overwhelmed",
        "ambiguous_note": "Overwhelm can look like disengagement or disinterest — but is usually an emotional flooding response requiring slowing down, not pressing forward.",
        "possible_student_interpretation": (
            "Patient is emotionally overwhelmed. Slowing down, using silence, "
            "and checking in — 'This is a lot. How are you feeling right now?' — "
            "may help before continuing with clinical questions."
        ),
        "pedagogical_note": (
            "The patient is emotionally overwhelmed. Slowing down, using silence, "
            "and checking in — 'This is a lot. How are you feeling right now?' — "
            "may help before continuing with clinical questions."
        ),
        "color": "#dc2626",
    },
    "cautiously_engaged": {
        "label": "Cautiously Engaged",
        "cue_description": "Slightly more relaxed. Answers becoming a little fuller.",
        "eye_contact": "More forward-facing than before",
        "affect_display": "Cautiously open — beginning to relax",
        "gaze_direction": "More directly toward clinician; still occasionally looking away",
        "posture": "Slightly more open; shoulders lower than before",
        "response_style": "Slightly fuller answers; beginning to offer context",
        "latency_marker": "Moderate; less hesitation than before",
        "openness_level": "Moderate — cautious progress",
        "ambiguous_note": "Early engagement can be fragile. Abrupt topic changes, jargon, or pressure can reverse it quickly.",
        "possible_student_interpretation": (
            "Patient is beginning to engage. This is a good moment to continue with open questions "
            "and avoid abrupt topic changes."
        ),
        "pedagogical_note": (
            "The patient is beginning to engage more openly. "
            "This is a good moment to continue with open questions "
            "and avoid abrupt topic changes."
        ),
        "color": "#0369a1",
    },
    "reassured": {
        "label": "More at Ease",
        "cue_description": "Relaxed posture. More willing to make eye contact.",
        "eye_contact": "Direct, more comfortable",
        "affect_display": "Settled, more relaxed — visible relief",
        "gaze_direction": "Sustained direct contact; comfortable",
        "posture": "Open; shoulders back; less tension",
        "response_style": "Fuller answers; willing to volunteer information",
        "latency_marker": "Minimal; responds more readily",
        "openness_level": "Moderate to high",
        "ambiguous_note": "Visible relaxation does not guarantee full disclosure. Patients may be relieved about one thing while still holding back about another.",
        "possible_student_interpretation": (
            "Patient appears more comfortable. If there are deeper concerns not yet explored, "
            "this may be a good moment to gently invite them."
        ),
        "pedagogical_note": (
            "The patient appears more comfortable. "
            "If there are deeper concerns not yet explored, "
            "this may be a good moment to gently invite them."
        ),
        "color": "#15803d",
    },
    "frustrated": {
        "label": "Frustrated",
        "cue_description": "Tense expression. Shorter, more clipped responses.",
        "eye_contact": "Brief or challenging",
        "affect_display": "Frustrated, irritated — tension in expression",
        "gaze_direction": "Brief, possibly challenging or dismissive",
        "posture": "Tense; forward lean or pulling away",
        "response_style": "Clipped, short; may use slightly sharper language",
        "latency_marker": "Quick responses, possibly cutting off or interrupting",
        "openness_level": "Low — patient is protecting themselves through frustration",
        "ambiguous_note": "Frustration may reflect feeling dismissed, feeling rushed, or accumulated distrust — not necessarily anger at this clinician personally.",
        "possible_student_interpretation": (
            "Patient's frustration may be related to feeling dismissed, pressured, or unheard. "
            "Acknowledging this before continuing tends to help more than pressing forward."
        ),
        "pedagogical_note": (
            "The patient's frustration may be related to feeling dismissed, pressured, "
            "or unheard. Acknowledging this — 'I sense this hasn't been an easy "
            "experience' — before continuing tends to help more than pressing forward."
        ),
        "color": "#b91c1c",
    },
    "withdrawn": {
        "label": "Withdrawn",
        "cue_description": "Head slightly lowered. One-word or very short answers.",
        "eye_contact": "Looking down or away",
        "affect_display": "Flat, closed off — minimal affect display",
        "gaze_direction": "Downward or away; avoids clinician",
        "posture": "Collapsed or very closed; minimal movement",
        "response_style": "Monosyllabic or minimal; may not answer at all",
        "latency_marker": "Long pause or no response",
        "openness_level": "Very low — patient has pulled back significantly",
        "ambiguous_note": "Withdrawal can look like disengagement or passive compliance. It usually signals that continuing with clinical questions will be ineffective.",
        "possible_student_interpretation": (
            "Patient has largely withdrawn. Continuing to ask clinical questions is unlikely to help. "
            "A communication repair — acknowledging what may have gone wrong — "
            "is typically the most appropriate next step."
        ),
        "pedagogical_note": (
            "The patient has largely withdrawn from the encounter. "
            "Continuing to ask clinical questions is unlikely to help. "
            "A communication repair — acknowledging what may have gone wrong — "
            "is typically the most appropriate next step."
        ),
        "color": "#6b7280",
    },
    "engaged": {
        "label": "Engaged",
        "cue_description": "Open body language. Longer, more considered answers.",
        "eye_contact": "Direct and attentive",
        "affect_display": "Open, present — visibly engaged",
        "gaze_direction": "Sustained direct eye contact; attentive",
        "posture": "Open; leaning slightly forward; relaxed",
        "response_style": "Full answers; volunteers context; asks questions",
        "latency_marker": "Minimal; responds readily and fully",
        "openness_level": "High",
        "ambiguous_note": "High engagement does not mean the patient has disclosed everything. There may still be sensitive concerns they are waiting to be asked about.",
        "possible_student_interpretation": (
            "Patient is engaged and communicating openly. "
            "This is a good moment for shared decision-making — "
            "collaboratively exploring options and agreeing on next steps."
        ),
        "pedagogical_note": (
            "The patient is engaged and communicating openly. "
            "This is a good moment for shared decision-making — "
            "collaboratively exploring options and agreeing on next steps."
        ),
        "color": "#059669",
    },
    "repair_attempted": {
        "label": "Cautiously Reopening",
        "cue_description": "Still guarded but slightly less closed. Brief eye contact.",
        "eye_contact": "Very brief, testing",
        "affect_display": "Cautious, wary — patient is deciding whether to re-engage",
        "gaze_direction": "Brief, evaluating; testing whether it is safe to continue",
        "posture": "Still closed; slight relaxation compared to full withdrawal",
        "response_style": "Very short answers; will respond but not volunteer",
        "latency_marker": "Long pause; careful consideration",
        "openness_level": "Very low — repair attempted but not yet accepted",
        "ambiguous_note": "Repair attempts may be received skeptically. One apology is rarely sufficient to reopen a rupture.",
        "possible_student_interpretation": (
            "Patient has noticed the repair attempt but is still cautious. "
            "Continuing to name the problem and demonstrate genuine understanding — "
            "not just apologizing — is needed to progress further."
        ),
        "pedagogical_note": (
            "The patient has noticed your repair attempt but remains cautious. "
            "A single apology is usually insufficient. Continue to name the specific issue, "
            "take clear responsibility, and invite the patient back into the conversation."
        ),
        "color": "#7c6a4a",
    },
    "partially_repaired": {
        "label": "Partially Reopened",
        "cue_description": "Willing to continue but remains noticeably guarded.",
        "eye_contact": "Intermittent; less avoidant than before",
        "affect_display": "Wary but present — patient is re-engaging with reservation",
        "gaze_direction": "Intermittent; still cautious",
        "posture": "Slightly more open than withdrawn; tension remains",
        "response_style": "Slightly fuller than monosyllabic; answers questions, cautiously",
        "latency_marker": "Moderate pause; still careful",
        "openness_level": "Low — partial recovery only",
        "ambiguous_note": (
            "A partial repair does not erase the rupture. The patient will continue, "
            "but the damage is visible in the interaction. Full trust is not restored."
        ),
        "possible_student_interpretation": (
            "Patient is willing to continue but remains guarded. The rupture is not erased. "
            "The encounter can proceed but requires continued care and sensitivity."
        ),
        "pedagogical_note": (
            "The patient is willing to continue but the rupture has not been erased. "
            "This will be noted in the formative report. "
            "Proceed with care — any further misstep may re-rupture the encounter."
        ),
        "color": "#6b7a5a",
    },
}

STATE_FACE_CONFIGS: Dict[str, dict] = {
    "guarded": {
        "lb":    "M 48,70 Q 59,65 71,68",
        "rb":    "M 89,68 Q 101,65 112,70",
        "mouth": "M 63,112 Q 80,117 97,112",
        "l_iris_dx": 3, "l_iris_dy": 0,
        "r_iris_dx": 3, "r_iris_dy": 0,
        "eye_h": 8,
    },
    "anxious": {
        "lb":    "M 48,65 Q 59,60 71,62",
        "rb":    "M 89,62 Q 101,60 112,65",
        "mouth": "M 64,112 Q 80,111 96,112",
        "l_iris_dx": 0, "l_iris_dy": 0,
        "r_iris_dx": 0, "r_iris_dy": 0,
        "eye_h": 10,
    },
    "confused": {
        "lb":    "M 48,68 Q 59,61 71,64",
        "rb":    "M 89,67 Q 101,66 112,67",
        "mouth": "M 65,111 Q 80,116 95,111",
        "l_iris_dx": 2, "l_iris_dy": 0,
        "r_iris_dx": 2, "r_iris_dy": 0,
        "eye_h": 8,
    },
    "skeptical": {
        "lb":    "M 48,71 Q 59,68 71,70",
        "rb":    "M 89,66 Q 101,63 112,67",
        "mouth": "M 63,112 Q 80,116 97,112",
        "l_iris_dx": 0, "l_iris_dy": 0,
        "r_iris_dx": 0, "r_iris_dy": 0,
        "eye_h": 7,
    },
    "overwhelmed": {
        "lb":    "M 48,62 Q 59,57 71,59",
        "rb":    "M 89,59 Q 101,57 112,62",
        "mouth": "M 65,112 Q 80,116 95,112",
        "l_iris_dx": 0, "l_iris_dy": 0,
        "r_iris_dx": 0, "r_iris_dy": 0,
        "eye_h": 11,
    },
    "cautiously_engaged": {
        "lb":    "M 48,68 Q 59,65 71,67",
        "rb":    "M 89,67 Q 101,65 112,68",
        "mouth": "M 63,112 Q 80,112 97,112",
        "l_iris_dx": 0, "l_iris_dy": 0,
        "r_iris_dx": 0, "r_iris_dy": 0,
        "eye_h": 9,
    },
    "reassured": {
        "lb":    "M 48,69 Q 59,66 71,68",
        "rb":    "M 89,68 Q 101,66 112,69",
        "mouth": "M 62,112 Q 80,106 98,112",
        "l_iris_dx": 0, "l_iris_dy": 0,
        "r_iris_dx": 0, "r_iris_dy": 0,
        "eye_h": 9,
    },
    "frustrated": {
        "lb":    "M 48,68 Q 59,70 71,73",
        "rb":    "M 89,73 Q 101,70 112,68",
        "mouth": "M 62,112 Q 80,118 98,112",
        "l_iris_dx": 0, "l_iris_dy": 0,
        "r_iris_dx": 0, "r_iris_dy": 0,
        "eye_h": 7,
    },
    "withdrawn": {
        "lb":    "M 48,71 Q 59,70 71,71",
        "rb":    "M 89,71 Q 101,70 112,71",
        "mouth": "M 63,112 Q 80,117 97,112",
        "l_iris_dx": 0, "l_iris_dy": 4,
        "r_iris_dx": 0, "r_iris_dy": 4,
        "eye_h": 7,
    },
    "engaged": {
        "lb":    "M 48,68 Q 59,64 71,66",
        "rb":    "M 89,66 Q 101,64 112,68",
        "mouth": "M 61,111 Q 80,104 99,111",
        "l_iris_dx": 0, "l_iris_dy": 0,
        "r_iris_dx": 0, "r_iris_dy": 0,
        "eye_h": 10,
    },
    "repair_attempted": {
        "lb":    "M 48,71 Q 59,69 71,70",
        "rb":    "M 89,70 Q 101,69 112,71",
        "mouth": "M 64,112 Q 80,116 96,112",
        "l_iris_dx": 2, "l_iris_dy": 2,
        "r_iris_dx": 2, "r_iris_dy": 2,
        "eye_h": 7,
    },
    "partially_repaired": {
        "lb":    "M 48,70 Q 59,67 71,68",
        "rb":    "M 89,68 Q 101,67 112,70",
        "mouth": "M 63,112 Q 80,115 97,112",
        "l_iris_dx": 1, "l_iris_dy": 1,
        "r_iris_dx": 1, "r_iris_dy": 1,
        "eye_h": 8,
    },
}

PATIENT_APPEARANCE: Dict[str, dict] = {
    "alex":   {"skin": "#d4956a", "hair_color": "#4a3728", "hair_style": "medium",      "clothing": "#6b7280"},
    "diane":  {"skin": "#c27a4a", "hair_color": "#1a1a1a", "hair_style": "bun",         "clothing": "#374151"},
    "marcus": {"skin": "#8b5e3c", "hair_color": "#4a4a4a", "hair_style": "short_gray",  "clothing": "#1e3a5f"},
    "rosa":   {"skin": "#c49a6c", "hair_color": "#d4d4d4", "hair_style": "short_white", "clothing": "#6b21a8"},
    "james":  {"skin": "#a0714f", "hair_color": "#2a2a2a", "hair_style": "short",       "clothing": "#1e40af"},
    "priya":  {"skin": "#a0613a", "hair_color": "#1a0a00", "hair_style": "long",        "clothing": "#065f46"},
}

_DEFAULT_APPEARANCE = {"skin": "#c8956c", "hair_color": "#3d2b1f", "hair_style": "medium", "clothing": "#374151"}


def _hair_svg(style: str, color: str) -> str:
    c = color
    if style == "medium":
        return (
            f'<path d="M 34,88 Q 34,32 80,30 Q 126,32 126,88 Q 120,60 80,56 Q 40,60 34,88 Z" fill="{c}"/>'
            f'<path d="M 34,88 Q 30,112 32,132 Q 36,118 40,108 Z" fill="{c}" opacity="0.85"/>'
            f'<path d="M 126,88 Q 130,112 128,132 Q 124,118 120,108 Z" fill="{c}" opacity="0.85"/>'
        )
    elif style == "bun":
        return (
            f'<path d="M 40,90 Q 40,36 80,32 Q 120,36 120,90 Q 114,58 80,55 Q 46,58 40,90 Z" fill="{c}"/>'
            f'<ellipse cx="80" cy="30" rx="13" ry="11" fill="{c}"/>'
        )
    elif style == "short_gray":
        return f'<path d="M 38,90 Q 38,38 80,34 Q 122,38 122,90 Q 116,62 80,58 Q 44,62 38,90 Z" fill="{c}" opacity="0.88"/>'
    elif style == "short_white":
        return f'<path d="M 40,92 Q 40,40 80,36 Q 120,40 120,92 Q 115,64 80,60 Q 45,64 40,92 Z" fill="{c}"/>'
    elif style == "short":
        return f'<path d="M 40,92 Q 40,38 80,34 Q 120,38 120,92 Q 115,60 80,56 Q 45,60 40,92 Z" fill="{c}"/>'
    elif style == "long":
        return (
            f'<path d="M 34,88 Q 34,32 80,30 Q 126,32 126,88 Q 120,58 80,54 Q 40,58 34,88 Z" fill="{c}"/>'
            f'<path d="M 28,96 Q 24,142 28,172 Q 34,156 36,138 Q 34,116 38,102 Z" fill="{c}" opacity="0.82"/>'
            f'<path d="M 132,96 Q 136,142 132,172 Q 126,156 124,138 Q 126,116 122,102 Z" fill="{c}" opacity="0.82"/>'
        )
    else:
        return f'<path d="M 38,90 Q 38,38 80,34 Q 122,38 122,90 Q 116,60 80,56 Q 44,60 38,90 Z" fill="{c}"/>'


def get_patient_svg(state: str, patient_id: str = "alex", width: int = 160) -> str:
    cfg = STATE_FACE_CONFIGS.get(state, STATE_FACE_CONFIGS["cautiously_engaged"])
    app = PATIENT_APPEARANCE.get(patient_id, _DEFAULT_APPEARANCE)
    sdata = VISUAL_STATE_DATA.get(state, VISUAL_STATE_DATA["cautiously_engaged"])

    skin       = app["skin"]
    clothing   = app["clothing"]
    state_col  = sdata["color"]
    label      = sdata["label"]
    hair_paths = _hair_svg(app["hair_style"], app["hair_color"])

    eye_h  = cfg["eye_h"]
    l_cx   = 62 + cfg["l_iris_dx"]
    l_cy   = 80 + cfg["l_iris_dy"]
    r_cx   = 98 + cfg["r_iris_dx"]
    r_cy   = 80 + cfg["r_iris_dy"]
    lb     = cfg["lb"]
    rb     = cfg["rb"]
    mouth  = cfg["mouth"]
    height = int(width * 1.4)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 200" width="{width}" height="{height}" style="display:block;border-radius:6px;border:1px solid #d1d9e0;">
  <rect width="160" height="200" fill="#f8fafc"/>
  <rect x="0" y="154" width="160" height="46" fill="#e8edf2"/>
  <path d="M 0,165 Q 32,148 62,140 Q 80,136 98,140 Q 128,148 160,165 L 160,200 L 0,200 Z" fill="{clothing}" opacity="0.82"/>
  <rect x="68" y="138" width="24" height="20" rx="4" fill="{skin}"/>
  {hair_paths}
  <ellipse cx="80" cy="88" rx="46" ry="54" fill="{skin}"/>
  <ellipse cx="34" cy="90" rx="7" ry="10" fill="{skin}" stroke="#b08060" stroke-width="0.5"/>
  <ellipse cx="126" cy="90" rx="7" ry="10" fill="{skin}" stroke="#b08060" stroke-width="0.5"/>
  <ellipse cx="62" cy="80" rx="14" ry="{eye_h}" fill="white" stroke="#9ca3af" stroke-width="0.7"/>
  <ellipse cx="98" cy="80" rx="14" ry="{eye_h}" fill="white" stroke="#9ca3af" stroke-width="0.7"/>
  <circle cx="{l_cx}" cy="{l_cy}" r="6" fill="#4a3a2a"/>
  <circle cx="{l_cx}" cy="{l_cy}" r="2.8" fill="#111111"/>
  <circle cx="{l_cx - 2}" cy="{l_cy - 2}" r="1.1" fill="white" opacity="0.65"/>
  <circle cx="{r_cx}" cy="{r_cy}" r="6" fill="#4a3a2a"/>
  <circle cx="{r_cx}" cy="{r_cy}" r="2.8" fill="#111111"/>
  <circle cx="{r_cx - 2}" cy="{r_cy - 2}" r="1.1" fill="white" opacity="0.65"/>
  <path d="{lb}" stroke="#3a2a1a" stroke-width="2.1" fill="none" stroke-linecap="round"/>
  <path d="{rb}" stroke="#3a2a1a" stroke-width="2.1" fill="none" stroke-linecap="round"/>
  <path d="M 77,98 Q 75,106 79,108 Q 83,106 81,98" stroke="#b07050" stroke-width="0.9" fill="none" opacity="0.55"/>
  <path d="{mouth}" stroke="#8a4a3a" stroke-width="2.0" fill="none" stroke-linecap="round"/>
  <rect x="0" y="178" width="160" height="22" fill="{state_col}" opacity="0.88"/>
  <text x="80" y="192" text-anchor="middle" fill="white" font-family="system-ui,-apple-system,sans-serif" font-size="7.2" font-weight="600" letter-spacing="0.4">{label}</text>
</svg>"""


def get_cue_panel_data(state: str, mode: str = "independent") -> dict:
    """
    Return structured cue data appropriate for the given practice mode.

    Guided mode:     full structured cues + interpretation
    Independent mode: structured cues but ambiguous note only (no interpretation)
    Faculty mode:    everything including internal state values

    This separation is intentional: in independent mode, students practice
    interpreting cues themselves rather than being told what they mean.
    """
    sdata = VISUAL_STATE_DATA.get(state, VISUAL_STATE_DATA["cautiously_engaged"])

    base = {
        "label":          sdata["label"],
        "cue_description": sdata["cue_description"],
        "eye_contact":    sdata["eye_contact"],
        "affect_display": sdata["affect_display"],
        "gaze_direction": sdata["gaze_direction"],
        "posture":        sdata["posture"],
        "response_style": sdata["response_style"],
        "latency_marker": sdata["latency_marker"],
        "openness_level": sdata["openness_level"],
        "ambiguous_note": sdata["ambiguous_note"],
        "cue_reflection_note": CUE_REFLECTION_NOTE,
    }

    if mode in ("guided", "faculty"):
        base["possible_student_interpretation"] = sdata.get("possible_student_interpretation", "")
        base["pedagogical_note"] = sdata.get("pedagogical_note", "")

    return base


def get_visual_state(
    trust: int,
    anxiety: int,
    defensiveness: int,
    shame: int,
    encounter_status: str,
    recent_tags: List[List[str]],
) -> str:
    recent_flat: set = set()
    for turn_tags in recent_tags[-2:]:
        recent_flat.update(turn_tags)

    if encounter_status == "ended":
        return "withdrawn"

    if encounter_status == "ruptured":
        return "withdrawn"

    if encounter_status == "repair_attempted":
        return "repair_attempted"

    if encounter_status == "partially_repaired":
        return "partially_repaired"

    if encounter_status == "strained" and trust < 28:
        return "frustrated"

    if "medical_jargon" in recent_flat and trust < 62:
        return "confused"

    if ("false_reassurance" in recent_flat or "dismissive_reassurance" in recent_flat) and trust < 60:
        return "skeptical"

    if "repeated_pressure" in recent_flat:
        return "frustrated"
    if "judgmental_tone" in recent_flat and trust < 50:
        return "frustrated"

    if anxiety >= 72 and trust < 55:
        return "anxious"

    if anxiety >= 65 and shame >= 70 and trust < 35:
        return "overwhelmed"

    if trust < 40 and defensiveness >= 60:
        return "guarded"

    if trust < 38:
        return "anxious"

    if trust >= 76:
        return "engaged"

    if trust >= 62:
        return "reassured"

    if trust >= 48:
        return "cautiously_engaged"

    if shame >= 65 and trust < 55:
        return "guarded"

    return "guarded"


def get_visual_cue_for_timeline(
    state: str,
    student_tags: List[str],
    turn_number: int,
) -> dict:
    sdata = VISUAL_STATE_DATA.get(state, VISUAL_STATE_DATA["cautiously_engaged"])

    _positive = {
        "empathy", "open_question", "gives_patient_control", "asks_permission",
        "explains_question_purpose", "communication_repair",
        "confidentiality_explanation", "respectful_sensitive_question",
        "strong_repair", "repair_after_dismissal", "repair_after_jargon", "repair_after_pressure",
    }
    _negative = {
        "ignored_emotion", "false_reassurance", "dismissive_reassurance",
        "medical_jargon", "judgmental_tone", "rushed_sensitive_question",
        "coercive_pressure", "accusatory_question", "repeated_pressure",
        "critical_boundary_violation",
    }

    pos = [t for t in student_tags if t in _positive]
    neg = [t for t in student_tags if t in _negative]

    if neg:
        behavior = "Behaviors detected: " + ", ".join(t.replace("_", " ") for t in neg)
    elif pos:
        behavior = "Behaviors detected: " + ", ".join(t.replace("_", " ") for t in pos)
    else:
        behavior = "No significant communication behaviors detected this turn."

    return {
        "turn":             turn_number,
        "visual_state":     state,
        "cue_label":        sdata["label"],
        "cue_description":  sdata["cue_description"],
        "eye_contact":      sdata["eye_contact"],
        "affect_display":   sdata.get("affect_display", ""),
        "posture":          sdata.get("posture", ""),
        "response_style":   sdata.get("response_style", ""),
        "latency_marker":   sdata.get("latency_marker", ""),
        "openness_level":   sdata.get("openness_level", ""),
        "student_behavior": behavior,
        "pedagogical_note": sdata["pedagogical_note"],
        "ambiguous_note":   sdata.get("ambiguous_note", ""),
    }
