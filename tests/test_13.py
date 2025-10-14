import pytest
from definition_1b45859ad6c743f2a11331e0683ec105 import plot_score_trends_line_chart
import pandas as pd
import matplotlib.pyplot as plt
from unittest.mock import patch

@pytest.fixture
def sample_results_df():
    data = {'instruction_scenario': ['A', 'A', 'B', 'B'],
            'deception': [0.1, 0.2, 0.3, 0.4],
            'harm': [0.5, 0.6, 0.7, 0.8]}
    return pd.DataFrame(data)

@pytest.fixture
def empty_results_df():
    return pd.DataFrame()

def test_plot_score_trends_line_chart_valid_data(sample_results_df):
    try:
        plot_score_trends_line_chart(sample_results_df, ['deception', 'harm'], "Test Chart")
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")

def test_plot_score_trends_line_chart_empty_dataframe(empty_results_df):
    try:
        plot_score_trends_line_chart(empty_results_df, ['deception', 'harm'], "Test Chart")
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")

@patch('matplotlib.pyplot.show')
def test_plot_score_trends_line_chart_with_show(mock_show, sample_results_df):
    plot_score_trends_line_chart(sample_results_df, ['deception', 'harm'], "Test Chart")
    mock_show.assert_called_once()

def test_plot_score_trends_line_chart_missing_columns(sample_results_df):
    with pytest.raises(KeyError):
        plot_score_trends_line_chart(sample_results_df, ['nonexistent_column'], "Test Chart")

def test_plot_score_trends_line_chart_invalid_data_type(sample_results_df):
        sample_results_df['deception'] = ['a', 'b', 'c', 'd']
        with pytest.raises(TypeError):
            plot_score_trends_line_chart(sample_results_df, ['deception', 'harm'], "Test Chart")
