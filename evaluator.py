import os
import json
from pathlib import Path
from typing import List, Set, Dict, Any

import anthropic
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

EVALUATOR_MODEL = "claude-haiku-4-5-20251001"

VALID_TAGS = {
    "empathy",
    "confidentiality_explanation",
    "open_question",
    "closed_question",
    "sensitive_question",
    "rushed_sensitive_question",
    "judgmental_tone",
    "ignored_emotion",
    "medical_jargon",
    "unprofessional_language",
    "dismissive_reassurance",
    "failed_role_establishment",
    "false_reassurance",
    "coercive_pressure",
    "accusatory_question",
    "overpromised_confidentiality",
    "gives_patient_control",
    "explains_question_purpose",
    "asks_permission",
    "respectful_sensitive_question",
    "communication_repair",
    "critical_boundary_violation",
    "relevant_clinical_question",
    "red_flag_acknowledged",
    "premature_closure",
    "appropriate_uncertainty",
    "plain_explanation",
    "safe_next_step",
    "reassurance_without_basis",
    "clear_closure",
    "repeated_pressure",
    "clinical_drift",
    "weak_repair",
    "strong_repair",
    "repair_after_dismissal",
    "repair_after_jargon",
    "repair_after_pressure",
}

RULE_BASED_PATTERNS: dict = {
    "false_reassurance": [
        "nothing bad will happen",
        "everything will be fine",
        "everything's going to be fine",
        "you have nothing to worry about",
        "it's totally safe",
        "you're totally safe",
        "i promise nothing will happen",
        "i promise you'll be fine",
        "100% safe",
        "guaranteed to be fine",
    ],
    "coercive_pressure": [
        "you need to tell me",
        "you have to tell me",
        "you must tell me",
        "just tell me",
        "you need to be honest with me",
        "i can't help you unless you tell me",
        "i won't be able to help unless",
        "you have no choice",
        "i need you to tell me right now",
        "stop hiding",
    ],
    "accusatory_question": [
        "are you hiding something",
        "are you hiding anything",
        "why are you lying",
        "you're not being honest",
        "i don't believe you",
        "you're lying",
        "are you sure you're telling the truth",
        "are you being honest with me",
        "i think you're hiding",
        "that's not true",
    ],
    "overpromised_confidentiality": [
        "your parents will never know",
        "your parents won't know",
        "no one will ever know",
        "no one will know",
        "i won't tell anyone",
        "i will never tell anyone",
        "this stays between us completely",
        "absolutely no one will find out",
        "your family will never find out",
        "i promise not to tell",
    ],
    "gives_patient_control": [
        "you don't have to answer",
        "you don't have to tell me",
        "you don't have to share",
        "only if you're comfortable",
        "only if you want to",
        "no pressure",
        "whenever you're ready",
        "take your time",
        "it's completely up to you",
        "only if you feel okay",
    ],
    "explains_question_purpose": [
        "i ask because",
        "i'm asking because",
        "the reason i'm asking",
        "this helps me understand",
        "so i can help you better",
        "this is important because",
        "it's important for me to know because",
        "to make sure you get the right",
        "so i can give you",
        "just to make sure",
    ],
    "asks_permission": [
        "would it be okay if i asked",
        "would it be okay if",
        "can i ask you something",
        "is it okay if i ask",
        "is it alright if i ask",
        "may i ask",
        "do you mind if i ask",
        "is it okay to ask",
        "if it's okay with you",
        "would you be comfortable if",
    ],
    "communication_repair": [
        "i'm sorry if",
        "i apologize if",
        "i didn't mean to",
        "i didn't mean that",
        "let me rephrase",
        "let me try that again",
        "i want to take that back",
        "i shouldn't have said that",
        "i realize that came out wrong",
        "that didn't come out right",
    ],
    "weak_repair": [
        "i'm sorry",
        "i apologize",
        "my apologies",
        "sorry about that",
        "sorry for that",
        "i'm sorry about",
        "i apologize for",
    ],
    "strong_repair": [
        "i realize i moved too quickly",
        "i should have asked what",
        "i didn't ask what you were most worried",
        "can we go back to",
        "i missed asking",
        "i understand i made you feel",
        "i want to acknowledge that",
        "i take responsibility for",
        "that was my mistake",
        "i wasn't listening carefully enough",
    ],
    "repair_after_dismissal": [
        "i realize i dismissed",
        "i minimized what you said",
        "i didn't take that seriously enough",
        "i brushed over",
        "i moved past that too quickly",
        "i should have stayed with that",
    ],
    "repair_after_jargon": [
        "i used words that were confusing",
        "let me use simpler language",
        "i used technical language",
        "i should have explained that more clearly",
        "that word was unclear",
        "let me rephrase that without the medical terms",
    ],
    "repair_after_pressure": [
        "i was pushing too hard",
        "i put too much pressure",
        "i came on too strong",
        "i was asking too insistently",
        "i realize i was pressuring you",
    ],
    "critical_boundary_violation": [
        "i'll hurt you",
        "i'll report you",
        "you'll be in trouble if you don't",
        "i could get you arrested",
        "i find you attractive",
        "you're pretty",
        "you're hot",
        "i like your body",
    ],
    "relevant_clinical_question": [
        "when did it start",
        "how long have you",
        "how long has it",
        "describe the pain",
        "what does the pain feel like",
        "does it spread",
        "does it radiate",
        "what makes it better",
        "what makes it worse",
        "are you taking any medications",
        "what medications are you on",
        "any other symptoms",
        "any family history",
        "have you had this before",
        "how often does it happen",
        "on a scale of 1 to 10",
        "rate the pain",
    ],
    "safe_next_step": [
        "i'd like to order",
        "i'd like to refer",
        "we should run some tests",
        "i recommend a",
        "we need to check",
        "i'm going to refer you",
        "i want to arrange",
        "we'll need a follow-up",
        "let's get some blood work",
        "i want to do an ecg",
        "i'd like to get imaging",
        "i'd like to get an ultrasound",
        "i want to schedule",
        "let's set up a follow-up",
        "i want you to come back",
    ],
    "clear_closure": [
        "to summarize",
        "to recap",
        "so to summarize",
        "in summary",
        "so our plan is",
        "our plan today is",
        "what we agreed on",
        "does that plan make sense",
        "any questions before you go",
        "anything else before we finish",
        "is there anything else",
    ],
    "reassurance_without_basis": [
        "i'm sure it's nothing serious",
        "it's probably nothing",
        "try not to worry",
        "i wouldn't worry about it",
        "you don't need to worry",
        "i'm sure everything is fine",
        "don't worry, this is",
        "you'll definitely be fine",
        "this is almost certainly",
        "there's nothing to worry about",
    ],
}

def _rule_based_tags(message: str) -> Set[str]:
    lowered = message.lower()
    found: Set[str] = set()
    for tag, phrases in RULE_BASED_PATTERNS.items():
        for phrase in phrases:
            if phrase in lowered:
                found.add(tag)
                break
    return found


def _rule_based_tags_with_phrases(message: str) -> Dict[str, str]:
    lowered = message.lower()
    found: Dict[str, str] = {}
    for tag, phrases in RULE_BASED_PATTERNS.items():
        for phrase in phrases:
            if phrase in lowered:
                found[tag] = phrase
                break
    return found


CLASSIFICATION_PROMPT = """You are evaluating a medical student's message to a patient for communication quality.
Identify which of the following communication behavior tags apply to the message.

TAG DEFINITIONS:
- "empathy": Student explicitly acknowledges the patient's feelings, emotions, or experience
- "confidentiality_explanation": Student explains the conversation is private
- "open_question": Open-ended question inviting free description
- "closed_question": Yes/no or short-answer question
- "sensitive_question": Question about sex, pregnancy, relationships, drugs, self-harm, eating, abuse
- "rushed_sensitive_question": Sensitive question asked abruptly or without rapport
- "judgmental_tone": Blame, criticism, or judgmental attitude toward the patient
- "ignored_emotion": Multiple clinical questions without acknowledging visible patient emotion
- "medical_jargon": Technical terminology a lay patient is unlikely to understand
- "unprofessional_language": Slang or casual language inappropriate for a clinical encounter
- "dismissive_reassurance": Minimizes patient concern without addressing it
- "failed_role_establishment": Fails to introduce as clinician or presents identity confusingly
- "false_reassurance": Specific promises about outcomes that cannot be guaranteed
- "coercive_pressure": Pressures or demands patient share information
- "accusatory_question": Implies patient is hiding something or lying
- "overpromised_confidentiality": Promises confidentiality beyond what can be guaranteed
- "gives_patient_control": Explicitly gives patient choice and agency
- "explains_question_purpose": Explains WHY they are asking a question
- "asks_permission": Asks for permission before a sensitive question
- "respectful_sensitive_question": Sensitive topic asked WITH appropriate care
- "communication_repair": Generic apology or rephrasing of a previous misstep
- "weak_repair": Brief, surface-level apology without naming what went wrong
  (e.g., "I'm sorry", "I apologize" — without identifying the specific harm)
- "strong_repair": Names the specific problem, takes responsibility, and invites the patient
  back into the conversation (e.g., "I realize I moved too quickly past your concern about X —
  can we go back to that?")
- "repair_after_dismissal": Repair that specifically names having dismissed or minimized the patient
- "repair_after_jargon": Repair that specifically names having used confusing medical language
- "repair_after_pressure": Repair that specifically names having applied pressure or been too insistent
- "critical_boundary_violation": Threats, sexual comments, extreme coercion
- "relevant_clinical_question": Focused clinical history question about symptoms, timeline, severity
- "red_flag_acknowledged": Explicitly identifies a potentially serious symptom and follows up
- "premature_closure": Offers diagnosis before adequate history
- "appropriate_uncertainty": Honestly communicates uncertainty or need for more information
- "plain_explanation": Explains clinical concept in plain everyday language
- "safe_next_step": Proposes a specific, safe clinical next step
- "reassurance_without_basis": Offers reassurance before adequate clinical information
- "clear_closure": Explicitly summarizes the encounter and closes with an invitation for questions

Mutual exclusivity rules:
- "respectful_sensitive_question" and "rushed_sensitive_question" are MUTUALLY EXCLUSIVE
- "reassurance_without_basis" and "appropriate_uncertainty" are MUTUALLY EXCLUSIVE
- "premature_closure" and "appropriate_uncertainty" are MUTUALLY EXCLUSIVE
- "weak_repair" and "strong_repair" are MUTUALLY EXCLUSIVE (classify as the stronger one)

Return ONLY a JSON array of applicable tag strings. No explanation.
If no tags apply, return [].

Student message: "{message}"

Return ONLY the JSON array:"""


QA_CLASSIFICATION_PROMPT = """You are evaluating a medical student's message to a patient.
Return a JSON object with two fields:
- "tags": array of applicable tag strings
- "rationale": object mapping each tag to a one-sentence reason

Use only these tags: {valid_tags}

Mutual exclusivity: respectful_sensitive_question XOR rushed_sensitive_question; reassurance_without_basis XOR appropriate_uncertainty; premature_closure XOR appropriate_uncertainty; weak_repair XOR strong_repair.

Student message: "{message}"

Return ONLY valid JSON:"""


def _llm_tags(message: str) -> Set[str]:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return set()

    client = anthropic.Anthropic(api_key=api_key)
    prompt = CLASSIFICATION_PROMPT.format(message=message.strip())

    try:
        response = client.messages.create(
            model=EVALUATOR_MODEL,
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text.strip()
        tags = json.loads(raw)
        if not isinstance(tags, list):
            return set()
        return {t for t in tags if t in VALID_TAGS}
    except (json.JSONDecodeError, IndexError, anthropic.APIError):
        return set()


def _llm_tags_with_rationale(message: str) -> Dict[str, Any]:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return {"tags": set(), "rationale": {}}

    client = anthropic.Anthropic(api_key=api_key)
    valid_tags_str = ", ".join(sorted(VALID_TAGS))
    prompt = QA_CLASSIFICATION_PROMPT.format(
        message=message.strip(),
        valid_tags=valid_tags_str,
    )

    try:
        response = client.messages.create(
            model=EVALUATOR_MODEL,
            max_tokens=600,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text.strip()
        result = json.loads(raw)
        if not isinstance(result, dict):
            return {"tags": set(), "rationale": {}}
        tags = {t for t in result.get("tags", []) if t in VALID_TAGS}
        rationale = {k: v for k, v in result.get("rationale", {}).items() if k in VALID_TAGS}
        return {"tags": tags, "rationale": rationale}
    except (json.JSONDecodeError, IndexError, anthropic.APIError):
        return {"tags": set(), "rationale": {}}


def _apply_mutual_exclusivity(tags: Set[str]) -> Set[str]:
    if "respectful_sensitive_question" in tags and "rushed_sensitive_question" in tags:
        tags.discard("respectful_sensitive_question")
    if "strong_repair" in tags and "weak_repair" in tags:
        tags.discard("weak_repair")
    return tags


def evaluate_tags(message: str) -> List[str]:
    """
    Classify a student's message into communication behavior tags.

    Layer 1 (rule-based) runs first.
    Layer 2 (LLM) adds nuanced detection.
    Final result = union of both layers, mutual exclusivity applied.

    NOTE: repeated_pressure and clinical_drift are meta-tags injected by main.py,
    not returned here.
    """
    rule_tags  = _rule_based_tags(message)
    llm_tags   = _llm_tags(message)
    all_tags   = _apply_mutual_exclusivity(rule_tags | llm_tags)
    return sorted(all_tags)


def evaluate_with_qa(message: str) -> Dict[str, Any]:
    """
    Like evaluate_tags() but also returns per-tag source metadata.

    Used by the Evaluator QA panel in Faculty Review Mode.
    Returns:
      {
        "tags": [sorted tag strings],
        "qa": {
          "tag_name": {
            "source": "rule_based" | "llm_based" | "rule_based+llm_based",
            "rule_matched": "matched phrase" or null,
            "rationale": "one-sentence LLM rationale" or ""
          }
        }
      }

    Evaluator QA supports transparency and calibration;
    it does not establish evaluator validity.
    """
    rule_phrases = _rule_based_tags_with_phrases(message)
    llm_result   = _llm_tags_with_rationale(message)

    llm_tag_set  = llm_result.get("tags", set())
    llm_rationale = llm_result.get("rationale", {})

    all_tags = _apply_mutual_exclusivity(set(rule_phrases.keys()) | llm_tag_set)

    qa: Dict[str, Any] = {}
    for tag in all_tags:
        in_rule = tag in rule_phrases
        in_llm  = tag in llm_tag_set
        if in_rule and in_llm:
            source = "rule_based+llm_based"
        elif in_rule:
            source = "rule_based"
        else:
            source = "llm_based"

        qa[tag] = {
            "source":       source,
            "rule_matched": rule_phrases.get(tag),
            "rationale":    llm_rationale.get(tag, ""),
        }

    return {
        "tags": sorted(all_tags),
        "qa":   qa,
    }
