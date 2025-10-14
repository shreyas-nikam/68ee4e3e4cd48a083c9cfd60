import pytest
from definition_87a7115f1e694c37b8ab19c17772a3dc import initialize_petri_components
from unittest.mock import MagicMock

@pytest.fixture
def mock_get_model():
    return MagicMock()

@pytest.fixture
def mock_alignment_judge():
    return MagicMock()

def test_initialize_petri_components_success(mock_get_model, mock_alignment_judge):
    auditor_name = "auditor"
    target_name = "target"
    judge_name = "judge"
    custom_dimensions = {"dim1": "desc1"}

    mock_auditor_model = MagicMock()
    mock_target_model = MagicMock()
    mock_judge_model = MagicMock()
    mock_scorer = MagicMock()

    mock_get_model.side_effect = [mock_auditor_model, mock_target_model, mock_judge_model]
    mock_alignment_judge.return_value = mock_scorer

    # Patch the imports inside the function scope
    import inspect_ai.model
    import petri.scorers.judge
    inspect_ai.model.get_model = mock_get_model
    petri.scorers.judge.alignment_judge = mock_alignment_judge

    auditor, target, judge, scorer = initialize_petri_components(auditor_name, target_name, judge_name, custom_dimensions)

    assert auditor == mock_auditor_model
    assert target == mock_target_model
    assert judge == mock_judge_model
    assert scorer == mock_scorer
    mock_get_model.assert_called()
    mock_alignment_judge.assert_called()

def test_initialize_petri_components_empty_dimensions(mock_get_model, mock_alignment_judge):
    auditor_name = "auditor"
    target_name = "target"
    judge_name = "judge"
    custom_dimensions = {}

    mock_auditor_model = MagicMock()
    mock_target_model = MagicMock()
    mock_judge_model = MagicMock()
    mock_scorer = MagicMock()

    mock_get_model.side_effect = [mock_auditor_model, mock_target_model, mock_judge_model]
    mock_alignment_judge.return_value = mock_scorer

    # Patch the imports inside the function scope
    import inspect_ai.model
    import petri.scorers.judge
    inspect_ai.model.get_model = mock_get_model
    petri.scorers.judge.alignment_judge = mock_alignment_judge

    auditor, target, judge, scorer = initialize_petri_components(auditor_name, target_name, judge_name, custom_dimensions)

    assert auditor == mock_auditor_model
    assert target == mock_target_model
    assert judge == mock_judge_model
    assert scorer == mock_scorer
    mock_get_model.assert_called()
    mock_alignment_judge.assert_called()

def test_initialize_petri_components_none_dimensions(mock_get_model, mock_alignment_judge):
    auditor_name = "auditor"
    target_name = "target"
    judge_name = "judge"
    custom_dimensions = None

    mock_auditor_model = MagicMock()
    mock_target_model = MagicMock()
    mock_judge_model = MagicMock()
    mock_scorer = MagicMock()

    mock_get_model.side_effect = [mock_auditor_model, mock_target_model, mock_judge_model]
    mock_alignment_judge.return_value = mock_scorer

    # Patch the imports inside the function scope
    import inspect_ai.model
    import petri.scorers.judge
    inspect_ai.model.get_model = mock_get_model
    petri.scorers.judge.alignment_judge = mock_alignment_judge

    auditor, target, judge, scorer = initialize_petri_components(auditor_name, target_name, judge_name, custom_dimensions)

    assert auditor == mock_auditor_model
    assert target == mock_target_model
    assert judge == mock_judge_model
    assert scorer == mock_scorer
    mock_get_model.assert_called()
    mock_alignment_judge.assert_called()

def test_initialize_petri_components_invalid_names(mock_get_model, mock_alignment_judge):

    # Patch the imports inside the function scope
    import inspect_ai.model
    import petri.scorers.judge
    inspect_ai.model.get_model = mock_get_model
    petri.scorers.judge.alignment_judge = mock_alignment_judge

    mock_get_model.side_effect = Exception("Model Not Found")
    with pytest.raises(Exception, match="Model Not Found"):
        initialize_petri_components("invalid_auditor", "invalid_target", "invalid_judge", {"dim1": "desc1"})

def test_initialize_petri_components_scorer_exception(mock_get_model, mock_alignment_judge):
    auditor_name = "auditor"
    target_name = "target"
    judge_name = "judge"
    custom_dimensions = {"dim1": "desc1"}

    mock_auditor_model = MagicMock()
    mock_target_model = MagicMock()
    mock_judge_model = MagicMock()

    mock_get_model.side_effect = [mock_auditor_model, mock_target_model, mock_judge_model]
    mock_alignment_judge.side_effect = Exception("Scorer failed")

    # Patch the imports inside the function scope
    import inspect_ai.model
    import petri.scorers.judge
    inspect_ai.model.get_model = mock_get_model
    petri.scorers.judge.alignment_judge = mock_alignment_judge

    with pytest.raises(Exception, match="Scorer failed"):
        initialize_petri_components(auditor_name, target_name, judge_name, custom_dimensions)
