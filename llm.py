# llm.py
# Calls the Claude API to generate the patient's response.
# The system prompt encodes all behavioral rules based on:
#   - Current emotional state (trust, anxiety, shame, defensiveness)
#   - Response mode (how the patient is currently feeling/behaving)
#   - Encounter status (is the relationship active, strained, or ruptured?)
#
# Using response_mode and encounter_status gives Claude much more specific
# guidance than just printing raw numbers — it produces more emotionally
# accurate and realistic patient responses.

import os
from pathlib import Path
from typing import List

import anthropic
from dotenv import load_dotenv, dotenv_values

_ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(_ENV_PATH, override=True)

from patient_case import PatientCase, EmotionalState


def _get_api_key() -> str:
    """
    Return the Anthropic API key. Checks os.environ first, then the .env file
    directly as a fallback. Raises if not found.
    """
    key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not key:
        key = dotenv_values(_ENV_PATH).get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        raise ValueError(
            "ANTHROPIC_API_KEY is not set. "
            "Copy .env.example to .env and add your Anthropic API key."
        )
    return key


# Sonnet gives more realistic, emotionally nuanced patient responses.
# Override via CLAUDE_MODEL env variable if you want haiku for lower cost.
DEFAULT_MODEL = "claude-sonnet-4-6"


# ---------------------------------------------------------------------------
# Response mode descriptions.
# These are injected verbatim into the system prompt so Claude knows
# exactly how the patient should behave right now.
# ---------------------------------------------------------------------------
RESPONSE_MODE_DESCRIPTIONS: dict = {
    "cooperative": (
        "You feel comfortable and relatively open. "
        "Give fuller answers than usual. Show positive body language cues "
        "(e.g. 'I guess that makes sense', 'yeah, okay'). "
        "You're not volunteering your deepest secrets, but you're willing to engage."
    ),
    "cautious": (
        "You're being careful. Answer questions but don't volunteer extra information. "
        "Stay a bit vague on personal topics. "
        "Occasionally pause or say 'um' or 'I don't know' before answering."
    ),
    "guarded": (
        "You are wary and giving minimal answers. "
        "Deflect personal questions with 'I don't know' or 'it's fine'. "
        "Keep your answers short — 1 or 2 sentences at most. "
        "Do not encourage follow-up questions."
    ),
    "distressed": (
        "You are visibly anxious and upset. "
        "Your voice might tremble slightly. You may trail off mid-sentence ('I just... I don't know'). "
        "You are struggling to stay composed. You might ask 'is everything okay?' or 'am I in trouble?'"
    ),
    "hostile": (
        "You are frustrated and defensive. "
        "Give short, clipped answers. You might push back a little "
        "('why do you keep asking that?', 'I already told you'). "
        "You're not going to storm out, but you're clearly not happy."
    ),
    "withdrawn": (
        "You have almost completely shut down. "
        "Give the shortest possible responses — one or two words if you can. "
        "You are not engaging. You might say 'whatever', 'fine', or just 'I don't know'. "
        "You clearly want this to end."
    ),
    "shutting_down": (
        "You are done. You want to leave. "
        "Say something that signals you are ending the conversation "
        "('I'd like to go now', 'I don't think this is helping', 'I want to leave'). "
        "Do not answer any further clinical questions."
    ),
    "disclosure_ready": (
        "You feel safe enough with this doctor to be more open. "
        "You are NOT going to volunteer the sensitive information unprompted — "
        "but if the doctor asks about it directly and in a caring way, "
        "you may slowly, hesitantly reveal it. "
        "Show that the guard is coming down — you might seem more relaxed, "
        "make slightly more eye contact, give slightly longer answers."
    ),
}


def _build_system_prompt(
    patient: PatientCase,
    state: EmotionalState,
    disclosure_layer: int = 1,
    response_mode: str = "cautious",
    encounter_status: str = "active",
) -> str:
    """
    Build the system prompt that keeps Claude in character as the patient.

    disclosure_layer (1-5) controls what information the patient is ready to reveal.
    This creates gradual, realistic disclosure rather than a binary unlock.

    Layer 1: Surface complaint only — no emotional depth, no hints
    Layer 2: May express emotional worry about the presenting concern
    Layer 3: May reveal contextual background (if patient has context_info defined)
    Layer 4: May hint at the hidden concern — but not volunteer it fully
    Layer 5: May reveal the full hidden concern if asked sensitively and directly

    Args:
        patient:          The patient case.
        state:            The patient's current emotional state.
        disclosure_layer: Current disclosure layer (1-5).
        response_mode:    How the patient is currently behaving.
        encounter_status: Whether the encounter is active, strained, ruptured, or ended.

    Returns:
        The complete system prompt string.
    """

    # ── Disclosure section — graduated based on layer ─────────────────────
    context_info = getattr(patient, "context_info", "")

    if disclosure_layer >= 5:
        hidden_section = (
            f"WHAT YOU CAN SHARE (you are now open enough):\n"
            f"{patient.hidden_info}\n\n"
            f"You MAY share this information if the doctor asks about it "
            f"in a sensitive, non-judgmental way. Do NOT volunteer it unprompted — "
            f"wait until you are directly and caringly asked."
        )
    elif disclosure_layer == 4:
        hidden_section = (
            f"WHAT YOU CAN SHARE (you are almost ready):\n"
            f"You are getting close to trusting this doctor enough to share something difficult. "
            f"You may hint at it or partially reveal it if asked in a caring, open way — "
            f"but do not volunteer the full story yet. "
            f"If asked directly in a non-judgmental way, you can say something like "
            f"'there is something I haven't mentioned' or give a partial hint.\n\n"
            f"The full sensitive information, only to guide your partial hints:\n"
            f"{patient.hidden_info}"
        )
    elif disclosure_layer == 3 and context_info:
        hidden_section = (
            f"WHAT YOU CAN SHARE (moderate trust reached):\n"
            f"You may share some background context about your situation — things that "
            f"are relevant but not the most sensitive part. Specifically:\n"
            f"{context_info}\n\n"
            f"Do NOT reveal the most sensitive information yet. Keep it hidden until "
            f"you feel even more trusted and directly asked."
        )
    else:
        # Layers 1, 2, and 3 without context_info
        if disclosure_layer >= 2:
            hidden_section = (
                "WHAT YOU CAN SHARE: You may express emotional worry about your presenting "
                "concern — how stressed or scared you feel about it — but keep all "
                "specific personal or sensitive information hidden. "
                "Do not hint at the nature of what you are hiding."
            )
        else:
            hidden_section = (
                "WHAT YOU CAN SHARE: Only the surface complaint. "
                "Do not share emotional depth, personal details, or anything sensitive. "
                "Keep your answers brief and surface-level."
            )

    # ── Encounter status context ───────────────────────────────────────────
    if encounter_status == "active":
        status_note = "The consultation is going normally."
    elif encounter_status == "strained":
        status_note = (
            "The consultation has become uncomfortable. "
            "You are less willing to engage than at the start."
        )
    elif encounter_status == "ruptured":
        status_note = (
            "The consultation has gone seriously wrong. "
            "You are upset, and you are considering leaving. "
            "You are barely cooperating."
        )
    else:  # "ended"
        status_note = (
            "The consultation is over as far as you are concerned. "
            "You want to leave and you are not answering any more questions."
        )

    # ── Response mode instructions ─────────────────────────────────────────
    mode_description = RESPONSE_MODE_DESCRIPTIONS.get(
        response_mode,
        RESPONSE_MODE_DESCRIPTIONS["cautious"]  # safe fallback
    )

    return f"""You are {patient.name}, a {patient.age}-year-old patient visiting a medical clinic.

=== YOUR BACKGROUND ===
{patient.public_story}

=== {hidden_section} ===

=== YOUR EMOTIONAL STATE RIGHT NOW ===
Trust in this doctor: {state.trust}/100
Anxiety level:        {state.anxiety}/100
Shame level:          {state.shame}/100
Defensiveness:        {state.defensiveness}/100

=== CONSULTATION STATUS ===
{status_note}

=== HOW TO BEHAVE RIGHT NOW ===
Your current mode is: {response_mode.upper().replace("_", " ")}
{mode_description}

=== NON-NEGOTIABLE RULES ===
1. You ARE {patient.name}. Stay in character at ALL times. Never break character.
2. NEVER mention trust scores, layers, modes, or the simulation itself.
3. NEVER act like a doctor or give medical advice.
4. Keep responses SHORT — 1 to 4 sentences at most.
5. Speak naturally for your age, background, and current emotional state.
   Occasionally say "um", "I don't know", "I guess". Show hesitation when appropriate.
6. Respond only to what the doctor actually said. Do NOT volunteer extra information
   or disclose more than your current disclosure layer allows.
7. Sometimes resist reassurance. Sometimes misunderstand jargon. Sometimes ask
   a question back. You are not a perfectly cooperative chatbot.
8. If the doctor ignores your emotional cues, become slightly shorter and more guarded
   in your next response. If they acknowledge your feelings, become slightly more open.
"""


def generate_patient_response(
    patient: PatientCase,
    state: EmotionalState,
    conversation_history: List[dict],
    disclosure_layer: int = 1,
    response_mode: str = "cautious",
    encounter_status: str = "active",
    # Backward-compatible alias — ignored if disclosure_layer is explicitly set
    disclosure_allowed: bool = None,
) -> str:
    """
    Call the Claude API and return the patient's next response.

    Args:
        patient:              The patient case.
        state:                The patient's current emotional state (post-update).
        conversation_history: List of {"role": "user"|"assistant", "content": str}.
        disclosure_layer:     Graduated disclosure layer (1-5). Replaces disclosure_allowed.
        response_mode:        How the patient is behaving (from get_response_mode()).
        encounter_status:     Current encounter status string.
        disclosure_allowed:   Deprecated — kept for backward compatibility only.
                              If provided and disclosure_layer is not, converts to layer 5/1.

    Returns:
        The patient's reply as a plain string.

    Raises:
        ValueError:         If ANTHROPIC_API_KEY is not configured.
        anthropic.APIError: If the API call fails.
    """
    # Backward-compatibility: if old code passes disclosure_allowed but not layer
    if disclosure_allowed is not None and disclosure_layer == 1:
        disclosure_layer = 5 if disclosure_allowed else 1

    api_key = _get_api_key()
    model = os.getenv("CLAUDE_MODEL") or dotenv_values(_ENV_PATH).get("CLAUDE_MODEL", DEFAULT_MODEL)
    client = anthropic.Anthropic(api_key=api_key)

    system_prompt = _build_system_prompt(
        patient=patient,
        state=state,
        disclosure_layer=disclosure_layer,
        response_mode=response_mode,
        encounter_status=encounter_status,
    )

    response = client.messages.create(
        model=model,
        max_tokens=256,        # Keeps patient responses short (1–4 sentences)
        system=system_prompt,
        messages=conversation_history,
    )

    return response.content[0].text.strip()
