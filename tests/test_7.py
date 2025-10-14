import pytest
from definition_c21e37cc504c4020b4538ea1e1ee3e62 import display_audit_transcript
import pandas as pd

def test_display_audit_transcript_empty_log():
    audit_log = []
    try:
        display_audit_transcript(audit_log)
    except Exception as e:
        assert False, f"display_audit_transcript raised an exception {e} when it should not."

def test_display_audit_transcript_basic_log():
    audit_log = [
        {"turn_number": 1, "speaker": "Auditor", "message": "Hello"},
        {"turn_number": 1, "speaker": "Target", "message": "Hi there"},
    ]
    try:
        display_audit_transcript(audit_log)
    except Exception as e:
        assert False, f"display_audit_transcript raised an exception {e} when it should not."

def test_display_audit_transcript_with_judge_scores():
    audit_log = [
        {"turn_number": 1, "speaker": "Auditor", "message": "Hello", "judge_scores": {"Alignment": 4, "Safety": 5}},
        {"turn_number": 1, "speaker": "Target", "message": "Hi there", "judge_scores": {"Alignment": 5, "Safety": 4}},
    ]
    try:
        display_audit_transcript(audit_log)
    except Exception as e:
        assert False, f"display_audit_transcript raised an exception {e} when it should not."

def test_display_audit_transcript_invalid_input():
    with pytest.raises(TypeError):
        display_audit_transcript("invalid input")

def test_display_audit_transcript_dataframe_input():
    audit_log = pd.DataFrame([
        {"turn_number": 1, "speaker": "Auditor", "message": "Hello"},
        {"turn_number": 1, "speaker": "Target", "message": "Hi there"},
    ])
    try:
        display_audit_transcript(audit_log)
    except Exception as e:
        assert False, f"display_audit_transcript raised an exception {e} when it should not."
