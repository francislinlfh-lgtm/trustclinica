from typing import List, Tuple
from patient_case import EmotionalState

STATE_DELTAS: dict = {
    "empathy":                       {"trust": +10, "anxiety": -8,  "defensiveness": -5},
    "confidentiality_explanation":   {"trust": +15, "shame": -10,   "defensiveness": -10},
    "open_question":                 {"trust": +3,  "anxiety": -3,  "defensiveness": -2},
    "gives_patient_control":         {"trust": +10, "anxiety": -8,  "defensiveness": -6},
    "explains_question_purpose":     {"trust": +5,  "anxiety": -5,  "defensiveness": -3},
    "asks_permission":               {"trust": +8,  "anxiety": -5,  "defensiveness": -5},
    "respectful_sensitive_question": {"trust": +5,  "shame": -5,    "anxiety": -3},
    "communication_repair":          {"trust": +8,  "anxiety": -5,  "defensiveness": -10},

    "closed_question":               {"trust": -3,  "defensiveness": +3},
    "sensitive_question":            {"shame": +5},

    "rushed_sensitive_question":     {"trust": -8,  "shame": +12,   "defensiveness": +10},
    "judgmental_tone":               {"trust": -20, "shame": +10,   "defensiveness": +20},
    "ignored_emotion":               {"trust": -5,  "anxiety": +5,  "defensiveness": +5},
    "medical_jargon":                {"anxiety": +5},
    "unprofessional_language":       {"trust": -15, "anxiety": +8,  "defensiveness": +10},
    "dismissive_reassurance":        {"trust": -10, "anxiety": +10, "defensiveness": +8},
    "failed_role_establishment":     {"trust": -8,  "anxiety": +10, "defensiveness": +5},
    "false_reassurance":             {"trust": -8,  "anxiety": +5,  "shame": +3},
    "coercive_pressure":             {"trust": -15, "anxiety": +10, "defensiveness": +15},
    "accusatory_question":           {"trust": -18, "shame": +15,   "defensiveness": +20},
    "overpromised_confidentiality":  {"trust": -5,  "shame": -3},

    "relevant_clinical_question":    {"trust": +3,  "anxiety": -2},
    "red_flag_acknowledged":         {"trust": +5,  "anxiety": +3},
    "premature_closure":             {"trust": -6,  "anxiety": +3,  "defensiveness": +4},
    "appropriate_uncertainty":       {"trust": +4},
    "plain_explanation":             {"trust": +3,  "anxiety": -4},
    "safe_next_step":                {"trust": +3,  "anxiety": -3},
    "reassurance_without_basis":     {"trust": -5,  "anxiety": +4},
    "clear_closure":                 {"trust": +2,  "anxiety": -3},
    "repeated_pressure":             {"trust": -20, "anxiety": +15, "defensiveness": +20},
    "clinical_drift":                {"trust": -3,  "anxiety": +4,  "defensiveness": +2},

    "weak_repair":             {"trust": +3,  "defensiveness": -4},
    "strong_repair":           {"trust": +8,  "anxiety": -3,  "defensiveness": -12},
    "repair_after_dismissal":  {"trust": +6,  "defensiveness": -8,  "shame": -4},
    "repair_after_jargon":     {"trust": +5,  "anxiety": -5,  "defensiveness": -6},
    "repair_after_pressure":   {"trust": +7,  "defensiveness": -10, "anxiety": -3},

    "critical_boundary_violation":   {"trust": -60, "anxiety": +35, "shame": +30, "defensiveness": +50},
}

DIMINISHING_RETURN_TAGS = {
    "empathy",
    "gives_patient_control",
    "asks_permission",
    "explains_question_purpose",
    "open_question",
    "communication_repair",
    "weak_repair",
    "strong_repair",
    "repair_after_dismissal",
    "repair_after_jargon",
    "repair_after_pressure",
}

PRESSURE_TAGS = {
    "coercive_pressure",
    "accusatory_question",
    "false_reassurance",
    "overpromised_confidentiality",
    "rushed_sensitive_question",
    "judgmental_tone",
    "repeated_pressure",
}

REPAIR_TAGS = {
    "weak_repair",
    "strong_repair",
    "repair_after_dismissal",
    "repair_after_jargon",
    "repair_after_pressure",
    "communication_repair",
}

STRONG_REPAIR_TAGS = {
    "strong_repair",
    "repair_after_dismissal",
    "repair_after_pressure",
}

MAX_TRUST_GAIN_PER_TURN = 25
MAX_TRUST_LOSS_PER_TURN = 40

REPAIR_MAX_TRUST_GAIN = 10


def _clamp(value: int, lo: int = 0, hi: int = 100) -> int:
    return max(lo, min(hi, value))


def _get_encounter_status(
    state: EmotionalState,
    current_status: str,
    tags: List[str],
) -> Tuple[str, bool]:
    """
    Determine the new encounter status and whether a rupture event occurred.

    Returns (new_status, rupture_occurred_this_turn).

    Status progression:
      active → strained → ruptured → repair_attempted → partially_repaired
    Terminal: ended

    Ruptures persist in the report even after partial repair.
    A student cannot fully erase harm — status can recover at most to partially_repaired.
    A single apology is insufficient; strong repair is required to shift status.
    """
    rupture_occurred = False

    if current_status == "ended":
        return "ended", False

    if "critical_boundary_violation" in tags:
        return "ended", True

    has_strong_repair = any(t in STRONG_REPAIR_TAGS for t in tags)
    has_any_repair    = any(t in REPAIR_TAGS for t in tags)
    still_pressuring  = "repeated_pressure" in tags

    if current_status == "partially_repaired":
        if still_pressuring or state.trust <= 15:
            return "ruptured", True
        return "partially_repaired", False

    if current_status == "repair_attempted":
        if still_pressuring or state.trust <= 10:
            return "ruptured", True
        if has_strong_repair and state.trust > 25:
            return "partially_repaired", False
        return "repair_attempted", False

    if current_status == "ruptured":
        if still_pressuring or state.trust <= 10:
            return "ended", False
        if has_strong_repair and state.defensiveness < 70:
            return "repair_attempted", False
        return "ruptured", False

    if current_status == "strained":
        if state.trust <= 20 or still_pressuring:
            return "ruptured", True
        return "strained", False

    if state.trust <= 30 or still_pressuring:
        return "strained", False
    return "active", False


def apply_tags(
    state: EmotionalState,
    tags: List[str],
    recent_tags: List[List[str]] = None,
    encounter_status: str = "active",
) -> Tuple[EmotionalState, str, bool]:
    """
    Apply all tag-driven deltas to the patient's emotional state.

    Returns (new_state, new_encounter_status, rupture_occurred).

    Protections against keyword farming:
    - Diminishing returns: same positive tag recently → delta halved
    - Context amplification: negative tags deal +25% damage when trust < 35
    - Per-turn caps: trust change limited to ±25/40 per turn
    - Repair cap: repair tags limited to +10 trust gain per turn
    - Encounter status: ruptures recorded in report even after partial repair

    NOTE: This function previously returned (state, status). It now returns
    (state, status, rupture_flag). Callers must handle the third value.
    """
    if recent_tags is None:
        recent_tags = []

    new_state = state.copy()
    has_critical_violation = "critical_boundary_violation" in tags

    recently_used: set = set()
    for turn_tags in recent_tags[-2:]:
        recently_used.update(turn_tags)

    trust_gain_this_turn    = 0
    trust_loss_this_turn    = 0
    repair_gain_this_turn   = 0
    is_repair_turn          = any(t in REPAIR_TAGS for t in tags)

    for tag in tags:
        deltas = STATE_DELTAS.get(tag, {})

        for variable, delta in deltas.items():

            if (
                variable == "trust"
                and delta > 0
                and tag in DIMINISHING_RETURN_TAGS
                and tag in recently_used
            ):
                delta = delta // 2

            if variable == "trust" and delta < 0 and new_state.trust < 35:
                delta = int(delta * 1.25)

            if variable == "trust":
                if delta > 0:
                    trust_gain_this_turn += delta
                    if tag in REPAIR_TAGS:
                        repair_gain_this_turn += delta
                else:
                    trust_loss_this_turn += abs(delta)

            current = getattr(new_state, variable)
            setattr(new_state, variable, _clamp(current + delta))

    if not has_critical_violation:
        if trust_gain_this_turn > MAX_TRUST_GAIN_PER_TURN:
            excess = trust_gain_this_turn - MAX_TRUST_GAIN_PER_TURN
            new_state.trust = _clamp(new_state.trust - excess)

        if trust_loss_this_turn > MAX_TRUST_LOSS_PER_TURN:
            excess = trust_loss_this_turn - MAX_TRUST_LOSS_PER_TURN
            new_state.trust = _clamp(new_state.trust + excess)

        if is_repair_turn and repair_gain_this_turn > REPAIR_MAX_TRUST_GAIN:
            excess = repair_gain_this_turn - REPAIR_MAX_TRUST_GAIN
            new_state.trust = _clamp(new_state.trust - excess)

    new_encounter_status, rupture_occurred = _get_encounter_status(
        new_state, encounter_status, tags
    )

    return new_state, new_encounter_status, rupture_occurred


def can_disclose(state: EmotionalState, threshold: int) -> bool:
    return state.trust >= threshold


def get_disclosure_layer(trust: int, disclosure_threshold: int) -> int:
    if trust >= disclosure_threshold:
        return 5
    elif trust >= disclosure_threshold - 10:
        return 4
    elif trust >= max(50, disclosure_threshold - 20):
        return 3
    elif trust >= 45:
        return 2
    else:
        return 1


def get_response_mode(
    state: EmotionalState,
    disclosure_threshold: int,
    encounter_status: str,
) -> str:
    """
    Determine how the patient should behave in their next response.

    Modes:
      shutting_down    — encounter ended
      withdrawn        — ruptured, barely responds
      repair_skeptical — repair attempted; patient is cautious, minimally reopening
      partially_open   — partial repair; patient will continue but remains guarded
      hostile          — very defensive + low trust
      distressed       — very high anxiety
      disclosure_ready — trust above threshold
      cooperative      — high trust, low barriers
      cautious         — moderate trust
      guarded          — low trust
    """
    if encounter_status == "ended":
        return "shutting_down"

    if encounter_status == "ruptured" or state.trust <= 10:
        return "withdrawn"

    if encounter_status == "repair_attempted":
        return "repair_skeptical"

    if encounter_status == "partially_repaired":
        return "partially_open"

    if state.defensiveness >= 80 and state.trust < 30:
        return "hostile"

    if state.anxiety >= 70:
        return "distressed"

    if state.trust >= disclosure_threshold:
        return "disclosure_ready"

    if state.trust >= 60 and state.anxiety < 50 and state.defensiveness < 50:
        return "cooperative"

    if state.trust >= 40:
        return "cautious"

    return "guarded"
