import pytest
from definition_a727b7123b8f4413868ff99e1daa611d import plot_aggregated_scores_bar_chart
import pandas as pd
import matplotlib.pyplot as plt
import io
from unittest.mock import patch

@pytest.fixture
def sample_dataframe():
    data = {'deception': [0.8, 0.6, 0.7],
            'harm': [0.2, 0.4, 0.3],
            'instruction_scenario': ['A', 'B', 'C']}
    return pd.DataFrame(data)

def test_plot_aggregated_scores_bar_chart_valid_data(sample_dataframe):
    try:
        plot_aggregated_scores_bar_chart(sample_dataframe.drop('instruction_scenario', axis=1), "Test Chart")
        plt.close()
    except Exception as e:
        pytest.fail(f"Plotting failed with exception: {e}")

def test_plot_aggregated_scores_bar_chart_empty_dataframe():
    empty_df = pd.DataFrame()
    with pytest.raises(Exception):
        plot_aggregated_scores_bar_chart(empty_df, "Test Chart")

def test_plot_aggregated_scores_bar_chart_non_numeric_data():
     data = {'deception': ['a', 'b', 'c'], 'harm': ['d', 'e', 'f']}
     non_numeric_df = pd.DataFrame(data)
     with pytest.raises(TypeError):
          plot_aggregated_scores_bar_chart(non_numeric_df, "Test Chart")

@patch('matplotlib.pyplot.savefig')
def test_plot_aggregated_scores_bar_chart_saves_figure(mock_savefig, sample_dataframe):
    plot_aggregated_scores_bar_chart(sample_dataframe.drop('instruction_scenario', axis=1), "Test Chart")
    mock_savefig.assert_called_once()

def test_plot_aggregated_scores_bar_chart_handles_single_dimension(sample_dataframe):
    single_dim_df = sample_dataframe[['deception']]
    try:
        plot_aggregated_scores_bar_chart(single_dim_df, "Test Chart")
        plt.close()
    except Exception as e:
        pytest.fail(f"Plotting failed with exception: {e}")
