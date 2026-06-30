
import json
from typing import Optional

from sqlalchemy import create_engine, Column, String, Text, text
from sqlalchemy.orm import declarative_base, sessionmaker

from patient_case import PATIENTS, EmotionalState

DATABASE_URL = "sqlite:///./trustsim.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class SessionRecord(Base):
    """One row per simulation session."""
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, nullable=False)
    created_at = Column(String, nullable=False)

    state_json = Column(Text, nullable=False)
    timeline_json = Column(Text, nullable=False)
    conversation_history_json = Column(Text, nullable=False)

    metadata_json = Column(Text, nullable=False, server_default="{}")

def init_db() -> None:
    """
    Create database tables if they don't exist. Call once at startup.

    Also runs a non-destructive migration: if the 'sessions' table exists
    but doesn't have the 'metadata_json' column yet (from v0.2.0), it adds it.
    Existing rows are not affected — they just get an empty metadata object.
    """
    Base.metadata.create_all(bind=engine)

    try:
        with engine.connect() as conn:
            conn.execute(
                text("ALTER TABLE sessions ADD COLUMN metadata_json TEXT DEFAULT '{}'")
            )
            conn.commit()
    except Exception:
        pass

def save_session(session_id: str, session_data: dict) -> None:
    """
    Insert or update a session record in the database.

    Args:
        session_id:   The UUID string for the session.
        session_data: The in-memory session dict (as managed by main.py).
    """
    db = SessionLocal()
    try:
        record = db.query(SessionRecord).filter(SessionRecord.id == session_id).first()

        state_json = json.dumps(session_data["state"].to_dict())
        timeline_json = json.dumps(session_data["timeline"])
        history_json = json.dumps(session_data["conversation_history"])

        metadata = {
            "tag_counts":           session_data.get("tag_counts", {}),
            "recent_tags":          session_data.get("recent_tags", []),
            "encounter_status":     session_data.get("encounter_status", "active"),
            "nonverbal_timeline":   session_data.get("nonverbal_timeline", []),
            "participant_id":       session_data.get("participant_id", ""),
            "attempt_number":       session_data.get("attempt_number", 1),
            "learning_mode":        session_data.get("learning_mode", "independent"),
            "disclosure_layer":     session_data.get("disclosure_layer", 1),
        }
        metadata_json = json.dumps(metadata)

        if record:
            record.state_json = state_json
            record.timeline_json = timeline_json
            record.conversation_history_json = history_json
            record.metadata_json = metadata_json
        else:
            record = SessionRecord(
                id=session_id,
                patient_id=session_data["patient_id"],
                created_at=session_data["created_at"],
                state_json=state_json,
                timeline_json=timeline_json,
                conversation_history_json=history_json,
                metadata_json=metadata_json,
            )
            db.add(record)

        db.commit()
    finally:
        db.close()

def load_session(session_id: str) -> Optional[dict]:
    """
    Load a session from the database and reconstruct Python objects.

    Returns None if the session does not exist.

    Args:
        session_id: The UUID string for the session.

    Returns:
        A session dict with the same structure used in main.py, or None.
    """
    db = SessionLocal()
    try:
        record = db.query(SessionRecord).filter(SessionRecord.id == session_id).first()
        if record is None:
            return None

        patient = PATIENTS.get(record.patient_id)
        if patient is None:
            return None

        state_dict = json.loads(record.state_json)
        state = EmotionalState(**state_dict)

        try:
            metadata = json.loads(record.metadata_json or "{}")
        except (json.JSONDecodeError, TypeError):
            metadata = {}

        return {
            "session_id":           record.id,
            "patient_id":           record.patient_id,
            "patient":              patient,
            "state":                state,
            "timeline":             json.loads(record.timeline_json),
            "conversation_history": json.loads(record.conversation_history_json),
            "created_at":           record.created_at,
            "tag_counts":           metadata.get("tag_counts", {}),
            "recent_tags":          metadata.get("recent_tags", []),
            "encounter_status":     metadata.get("encounter_status", "active"),
            "nonverbal_timeline":   metadata.get("nonverbal_timeline", []),
            "participant_id":       metadata.get("participant_id", ""),
            "attempt_number":       metadata.get("attempt_number", 1),
            "learning_mode":        metadata.get("learning_mode", "independent"),
            "disclosure_layer":     metadata.get("disclosure_layer", 1),
        }
    finally:
        db.close()
