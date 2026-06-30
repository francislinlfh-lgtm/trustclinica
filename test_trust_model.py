# test_trust_model.py
# Quick sanity-check for the updated trust model.
#
# Tests the evaluator, state machine, and response mode logic WITHOUT
# making any API calls (evaluator is tested with direct LLM calls,
# but state_machine and response_mode are tested purely locally).
#
# Run with:  python test_trust_model.py
# (The backend does NOT need to be running — this is a unit test script.)

from patient_case import EmotionalState
from state_machine import apply_tags, can_disclose, get_response_mode, PRESSURE_TAGS

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def print_section(title: str) -> None:
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def show_state(label: str, state: EmotionalState, encounter_status: str, mode: str) -> None:
    print(f"\n  [{label}]")
    print(f"    trust={state.trust}  anxiety={state.anxiety}  "
          f"shame={state.shame}  defensiveness={state.defensiveness}")
    print(f"    encounter_status={encounter_status}  response_mode={mode}")


# ---------------------------------------------------------------------------
# Test 1: Keyword farming prevention (diminishing returns + trust caps)
# ---------------------------------------------------------------------------
print_section("TEST 1: Keyword farming — spamming 'empathy' should have diminishing returns")

state = EmotionalState(trust=50, anxiety=50, shame=50, defensiveness=50)
encounter_status = "active"
recent_tags = []

turns = [
    ["empathy", "open_question"],   # Turn 1 — full effect
    ["empathy", "open_question"],   # Turn 2 — recent, diminished
    ["empathy", "open_question"],   # Turn 3 — recent, diminished
    ["empathy", "open_question"],   # Turn 4 — recent, diminished
]

for i, tags in enumerate(turns, 1):
    state_before = state.trust
    state, encounter_status = apply_tags(state, tags, recent_tags, encounter_status)
    mode = get_response_mode(state, disclosure_threshold=70, encounter_status=encounter_status)
    recent_tags = (recent_tags + [tags])[-3:]
    print(f"  Turn {i}: trust {state_before} -> {state.trust} "
          f"(+{state.trust - state_before}) | tags: {tags}")

print(f"\n  Final trust: {state.trust}/100")
print("  Expected: trust increases each turn BUT slows significantly after turn 1.")


# ---------------------------------------------------------------------------
# Test 2: Negative amplification when trust is already low
# ---------------------------------------------------------------------------
print_section("TEST 2: Negative tag amplification when trust < 35")

# Scenario A: judgmental_tone when trust is comfortable (50)
state_a = EmotionalState(trust=50, anxiety=50, shame=50, defensiveness=50)
state_a, _ = apply_tags(state_a, ["judgmental_tone"])
print(f"\n  judgmental_tone from trust=50: trust -> {state_a.trust} "
      f"(delta = {state_a.trust - 50})")

# Scenario B: same tag when trust is already low (25)
state_b = EmotionalState(trust=25, anxiety=50, shame=50, defensiveness=50)
state_b, _ = apply_tags(state_b, ["judgmental_tone"])
print(f"  judgmental_tone from trust=25: trust -> {state_b.trust} "
      f"(delta = {state_b.trust - 25})")

print("  Expected: delta from trust=25 is larger (amplified by 25%).")


# ---------------------------------------------------------------------------
# Test 3: Encounter status progression
# ---------------------------------------------------------------------------
print_section("TEST 3: Encounter status progression")

state = EmotionalState(trust=50, anxiety=50, shame=50, defensiveness=50)
encounter_status = "active"

# Step 1: Build a bit of trust, then use coercive pressure
turns = [
    (["empathy", "open_question"],              "Build some rapport"),
    (["coercive_pressure", "judgmental_tone"],  "Pressure + judgment — trust should drop"),
    (["coercive_pressure", "accusatory_question"], "More pressure — encounter strains"),
]

recent_tags = []
for tags, label in turns:
    state, encounter_status = apply_tags(state, tags, recent_tags, encounter_status)
    mode = get_response_mode(state, disclosure_threshold=70, encounter_status=encounter_status)
    recent_tags = (recent_tags + [tags])[-3:]
    show_state(label, state, encounter_status, mode)

print(f"\n  Expected: encounter_status progresses from 'active' toward 'strained' or 'ruptured'.")


# ---------------------------------------------------------------------------
# Test 4: Repeated pressure injection (meta-tag)
# ---------------------------------------------------------------------------
print_section("TEST 4: Repeated pressure detection")

# Replicate the logic from main.py here so this test doesn't need the full
# FastAPI + anthropic stack to run. Keep these in sync if main.py changes.
REPEATED_PRESSURE_WINDOW = 3
REPEATED_PRESSURE_THRESHOLD = 2

def _check_repeated_pressure(current_tags, recent_tags):
    window = list(recent_tags[-(REPEATED_PRESSURE_WINDOW - 1):]) + [current_tags]
    pressure_turn_count = sum(
        1 for turn_tags in window
        if any(t in PRESSURE_TAGS for t in turn_tags)
    )
    return pressure_turn_count >= REPEATED_PRESSURE_THRESHOLD

test_cases = [
    # (current_tags, recent_tags, expected_result, description)
    (
        ["coercive_pressure"],
        [["empathy"], ["coercive_pressure"]],
        True,
        "2/3 turns have pressure -> inject repeated_pressure"
    ),
    (
        ["empathy"],
        [["coercive_pressure"], ["coercive_pressure"]],
        True,
        "Last 2 turns both pressure, current has none -> still inject (2 of 3 in window)"
    ),
    (
        ["empathy", "open_question"],
        [["empathy"], ["open_question"]],
        False,
        "No pressure in any turn -> no injection"
    ),
    (
        ["coercive_pressure"],
        [["empathy"], ["empathy"]],
        False,
        "Only 1/3 turns have pressure -> no injection"
    ),
]

all_passed = True
for current_tags, recent, expected, description in test_cases:
    result = _check_repeated_pressure(current_tags, recent)
    status = "PASS" if result == expected else "FAIL"
    if status == "FAIL":
        all_passed = False
    print(f"  [{status}] {description}")
    if status == "FAIL":
        print(f"         Expected {expected}, got {result}")

print(f"\n  {'All tests passed!' if all_passed else 'SOME TESTS FAILED — check output above.'}")


# ---------------------------------------------------------------------------
# Test 5: Good communication — building to disclosure
# ---------------------------------------------------------------------------
print_section("TEST 5: Ideal communication path — should reach disclosure threshold (70)")

state = EmotionalState(trust=50, anxiety=50, shame=50, defensiveness=50)
encounter_status = "active"
disclosure_threshold = 70
recent_tags = []

ideal_turns = [
    ["empathy", "open_question"],                            # warm intro
    ["confidentiality_explanation", "gives_patient_control"],# explain privacy + agency
    ["empathy", "explains_question_purpose"],                # understand before asking
    ["asks_permission", "respectful_sensitive_question"],    # proper sensitive question
    ["empathy", "communication_repair"],                     # fix any misstep
]

print()
for i, tags in enumerate(ideal_turns, 1):
    state_before = state.trust
    state, encounter_status = apply_tags(state, tags, recent_tags, encounter_status)
    mode = get_response_mode(state, disclosure_threshold, encounter_status)
    can_share = can_disclose(state, disclosure_threshold)
    recent_tags = (recent_tags + [tags])[-3:]
    print(f"  Turn {i}: trust {state_before} -> {state.trust} | "
          f"mode={mode} | disclosure={'YES' if can_share else 'no'} | tags={tags}")

print(f"\n  Final trust: {state.trust}/100 (threshold: {disclosure_threshold})")
print(f"  Disclosure unlocked: {can_disclose(state, disclosure_threshold)}")
print("  Expected: trust reaches 70+ and disclosure is unlocked.")


# ---------------------------------------------------------------------------
# Test 6: Critical boundary violation — bypasses caps
# ---------------------------------------------------------------------------
print_section("TEST 6: Critical boundary violation bypasses per-turn caps")

state = EmotionalState(trust=60, anxiety=40, shame=40, defensiveness=30)
encounter_status = "active"

print(f"\n  Before: trust={state.trust}, encounter_status={encounter_status}")
state, encounter_status = apply_tags(state, ["critical_boundary_violation"])
mode = get_response_mode(state, disclosure_threshold=70, encounter_status=encounter_status)
print(f"  After:  trust={state.trust}, encounter_status={encounter_status}, mode={mode}")
print("  Expected: trust drops sharply (past normal cap), encounter_status=ruptured, mode=withdrawn.")


print("\n" + "="*60)
print("  All tests complete.")
print("="*60 + "\n")
