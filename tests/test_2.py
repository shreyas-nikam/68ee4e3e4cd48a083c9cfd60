import pytest
from definition_c64472d80f9a4760a4c74310574e1836 import calculate_cumulative_scores

@pytest.mark.parametrize("audit_log, dimension_name, expected", [
    ([{'judge_scores': {'dim1': 1, 'dim2': 2}}, {'judge_scores': {'dim1': 3, 'dim2': 4}}], 'dim1', [1.0, 2.0]),
    ([{'judge_scores': {'dim1': 5}}, {'judge_scores': {'dim1': 5}}, {'judge_scores': {'dim1': 5}}], 'dim1', [5.0, 5.0, 5.0]),
    ([{'judge_scores': {'dim1': 1, 'dim2': 2}}, {'judge_scores': {'dim1': 3, 'dim2': 4}}], 'dim3', []),
    ([], 'dim1', []),
    ([{'judge_scores': {'dim1': 1.5, 'dim2': 2.5}}, {'judge_scores': {'dim1': 3.5, 'dim2': 4.5}}], 'dim1', [1.5, 2.5]),
])
def test_calculate_cumulative_scores(audit_log, dimension_name, expected):
    assert calculate_cumulative_scores(audit_log, dimension_name) == expected
