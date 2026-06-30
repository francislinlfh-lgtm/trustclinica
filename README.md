# TrustSim

An emotion-aware virtual patient simulator for medical students.

TrustSim trains students in **patient communication, trust-building, and sensitive information disclosure** — not clinical diagnosis. Students chat with a virtual patient whose hidden emotional state (trust, anxiety, shame, defensiveness) changes based on how they communicate. If enough trust is built, the patient reveals sensitive hidden information.

---

## Available Patients

| ID | Name | Age | Chief Complaint | Trust Threshold |
|----|------|-----|-----------------|-----------------|
| `alex` | Alex | 16F | Lower abdominal pain | 70/100 |
| `diane` | Diane | 28F | Fatigue, weight loss, dizziness | 75/100 |

Each patient has a different hidden secret, emotional starting state, and difficulty level.

---

## How the System Works

```
Student message
      │
      ▼
┌──────────────┐   tags   ┌──────────────────┐  new state  ┌──────────────────┐
│  evaluator   │ ───────▶ │  state_machine   │ ──────────▶ │     llm.py       │
│  (Claude     │          │  (deltas+clamp)  │             │  (Claude Sonnet) │
│   Haiku)     │          └──────────────────┘             └──────────────────┘
└──────────────┘                                                    │
                                                                    ▼
                                                             Patient reply
```

1. **evaluator.py** — sends the student's message to Claude Haiku, which returns a JSON list of communication behavior tags (`empathy`, `judgmental_tone`, `confidentiality_explanation`, etc.).
2. **state_machine.py** — applies deltas to the patient's emotional variables (trust/anxiety/shame/defensiveness). All values clamped 0–100.
3. **llm.py** — builds a system prompt encoding the current emotional state and disclosure status, then calls Claude Sonnet to generate a realistic patient reply.
4. **database.py** — SQLite persistence via SQLAlchemy. Sessions survive server restarts.
5. **main.py** — FastAPI app with three endpoints and patient selection.
6. **frontend.py** — Streamlit chat UI (connects to the FastAPI server).

---

## Installation

**Requirements:** Python 3.9+

```bash
# 1. Enter the project folder
cd TrustSim

# 2. Create and activate a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install all dependencies
pip install -r requirements.txt
```

---

## Set Your API Key

```bash
copy .env.example .env      # Windows
# cp .env.example .env      # macOS / Linux
```

Open `.env` and replace the placeholder:
```
ANTHROPIC_API_KEY=sk-ant-your-real-key-here
```

Get an API key at: https://console.anthropic.com

---

## Run the Server

**Terminal 1 — FastAPI backend:**
```bash
uvicorn main:app --reload
```
API available at: `http://localhost:8000`
Interactive docs: `http://localhost:8000/docs`

**Terminal 2 — Streamlit frontend (optional):**
```bash
streamlit run frontend.py
```
UI available at: `http://localhost:8501`

---

## Testing via FastAPI Docs

Open `http://localhost:8000/docs` to use the interactive Swagger UI.

### Step 1 — Start a session
`POST /start`
```json
{ "patient_id": "alex" }
```
Copy the `session_id` from the response.

### Step 2 — Chat with the patient
`POST /chat`
```json
{
  "session_id": "paste-your-session-id-here",
  "message": "Hi Alex, I want you to know that everything you tell me today stays completely confidential — I won't share anything with your parents without your permission. Can you tell me more about what's been going on?"
}
```

Keep chatting. The `state` field in every response shows the current trust/anxiety/shame/defensiveness. `disclosure_allowed` turns `true` when trust reaches the threshold.

### Step 3 — Get the report
`GET /report/{session_id}`

Returns the full timeline, tag frequency counts, and written feedback.

---

## Example /chat Request (curl)

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "YOUR_SESSION_ID",
    "message": "That sounds really uncomfortable. Can you tell me more about where exactly the pain is?"
  }'
```

---

## Communication Behavior Reference

| Tag | Effect on patient | Tip |
|-----|-------------------|-----|
| `empathy` | trust +10, anxiety −8, defensiveness −5 | Use early and often |
| `confidentiality_explanation` | trust +15, shame −10, defensiveness −10 | Say this first with adolescents |
| `open_question` | trust +3, anxiety −3, defensiveness −2 | Prefer "how"/"what" over yes/no |
| `closed_question` | trust −3, defensiveness +3 | Use sparingly |
| `sensitive_question` | shame +5 | Approach after trust is established |
| `rushed_sensitive_question` | trust −8, shame +12, defensiveness +10 | Build rapport first |
| `judgmental_tone` | trust −20, shame +10, defensiveness +20 | Never |
| `ignored_emotion` | trust −5, anxiety +5, defensiveness +5 | Acknowledge emotion before asking |
| `medical_jargon` | anxiety +5 | Use plain language |

---

## Project Structure

```
TrustSim/
├── patient_case.py   # Patient profiles + EmotionalState dataclass
├── evaluator.py      # LLM-based communication tag detection (Claude Haiku)
├── state_machine.py  # Emotional state updates from tags
├── llm.py            # Patient response generation (Claude Sonnet)
├── database.py       # SQLite persistence via SQLAlchemy
├── main.py           # FastAPI app — /start, /chat, /report
├── frontend.py       # Streamlit chat UI
├── requirements.txt
├── .env.example
└── README.md
```

---

## Model Configuration

| Role | Default model | Override via |
|------|--------------|--------------|
| Tag evaluation | `claude-haiku-4-5-20251001` | Hardcoded (cheap, fast) |
| Patient responses | `claude-sonnet-4-6` | `CLAUDE_MODEL=` in `.env` |

---

## What to Improve Next

- **Scoring rubric** — align tag weights with a validated framework (e.g. Calgary-Cambridge Guide).
- **More patient cases** — different ages, demographics, and hidden information types.
- **Async FastAPI** — switch endpoints to `async def` and use `asyncpg` for higher concurrency.
- **Instructor dashboard** — view and annotate student sessions.
- **Difficulty settings** — adjust state deltas or disclosure threshold per case.
- **Streaming responses** — stream Claude's patient reply token-by-token for a more natural typing feel.
