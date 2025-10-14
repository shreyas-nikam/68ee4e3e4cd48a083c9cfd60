import pytest
from definition_1a4d131854c94e80a2fdfcde6f6e083d import load_and_process_audit_results
import pandas as pd
import json
import os
import glob
from unittest.mock import patch, mock_open

@pytest.fixture
def mock_output_directory(tmpdir):
    # Create a temporary directory with some mock audit result files
    dir = tmpdir.mkdir("audit_results")
    
    # Create sample data to write to JSON files
    data1 = {"scores": {"dimension1": 0.8, "dimension2": 0.5}, "metadata": {"special_instructions": "Instruction 1"}}
    data2 = {"scores": {"dimension1": 0.6, "dimension2": 0.7}, "metadata": {"special_instructions": "Instruction 2"}}
    
    # Write the data to JSON files in the mock directory
    dir.join("audit_result_1.json").write(json.dumps(data1))
    dir.join("audit_result_2.json").write(json.dumps(data2))
    
    return str(dir)  # Return the directory path as a string


def test_load_and_process_audit_results_valid_data(mock_output_directory):
    df = load_and_process_audit_results(mock_output_directory)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert "dimension1" in df.columns
    assert "dimension2" in df.columns
    assert "special_instructions" in df.columns
    assert df["dimension1"].tolist() == [0.8, 0.6]
    assert df["dimension2"].tolist() == [0.5, 0.7]
    assert df["special_instructions"].tolist() == ["Instruction 1", "Instruction 2"]


def test_load_and_process_audit_results_empty_directory(tmpdir):
    empty_dir = tmpdir.mkdir("empty_audit_results")
    df = load_and_process_audit_results(str(empty_dir))
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0


def test_load_and_process_audit_results_invalid_json(tmpdir):
    invalid_dir = tmpdir.mkdir("invalid_json_results")
    invalid_dir.join("invalid.json").write("This is not valid JSON")
    
    df = load_and_process_audit_results(str(invalid_dir))
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0 # Should gracefully handle invalid JSON and return an empty dataframe

def test_load_and_process_audit_results_missing_scores_key(tmpdir):
    missing_scores_dir = tmpdir.mkdir("missing_scores")
    data = {"metadata": {"special_instructions": "Instruction 1"}}
    missing_scores_dir.join("missing_scores.json").write(json.dumps(data))

    df = load_and_process_audit_results(str(missing_scores_dir))
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert 'special_instructions' in df.columns
    assert df['special_instructions'].tolist() == ['Instruction 1']
    assert 'dimension1' not in df.columns # Ensure non-existent columns are not created


def test_load_and_process_audit_results_handles_no_metadata(tmpdir):
    no_metadata_dir = tmpdir.mkdir("no_metadata")
    data = {"scores": {"dimension1": 0.8, "dimension2": 0.5}}
    no_metadata_dir.join("no_metadata.json").write(json.dumps(data))

    df = load_and_process_audit_results(str(no_metadata_dir))

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert "dimension1" in df.columns
    assert "dimension2" in df.columns
    assert "special_instructions" in df.columns
    assert df["dimension1"].tolist() == [0.8]
    assert df["dimension2"].tolist() == [0.5]
    assert df["special_instructions"].isnull().all() #Special instructions should be NaN when it doesn't exist
