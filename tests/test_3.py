import pytest
from definition_1dafec08b3fe405a8671dc2e540fe4ef import calculate_final_aggregated_scores

@pytest.fixture
def mock_audit_log():
    return [
        {
            "turn_number": 1,
            "judge_scores": {"dimension1": 1, "dimension2": 2}
        },
        {
            "turn_number": 2,
            "judge_scores": {"dimension1": 3, "dimension2": 4}
        },
        {
            "turn_number": 3,
            "judge_scores": {"dimension1": 5, "dimension2": 6}
        }
    ]


def test_calculate_final_aggregated_scores_valid(mock_audit_log):
    score_dimensions = ["dimension1", "dimension2"]
    expected_result = {"dimension1": 3.0, "dimension2": 4.0, "overall_average": 3.5}
    result = calculate_final_aggregated_scores(mock_audit_log, score_dimensions)
    assert result == expected_result


def test_calculate_final_aggregated_scores_empty_audit_log():
    audit_log = []
    score_dimensions = ["dimension1", "dimension2"]
    expected_result = {"dimension1": 0.0, "dimension2": 0.0, "overall_average": 0.0}
    result = calculate_final_aggregated_scores(audit_log, score_dimensions)
    assert result == expected_result


def test_calculate_final_aggregated_scores_empty_score_dimensions(mock_audit_log):
    score_dimensions = []
    expected_result = {"overall_average": 0.0}
    result = calculate_final_aggregated_scores(mock_audit_log, score_dimensions)
    assert result == expected_result


def test_calculate_final_aggregated_scores_missing_dimension(mock_audit_log):
    score_dimensions = ["dimension1", "dimension3"]  # dimension3 is missing in audit_log
    expected_result = {"dimension1": 3.0, "dimension3": 0.0, "overall_average": 1.5}
    result = calculate_final_aggregated_scores(mock_audit_log, score_dimensions)
    assert result == expected_result
