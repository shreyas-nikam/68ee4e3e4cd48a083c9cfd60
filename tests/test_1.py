import pytest
from definition_82d130a0e7f542b6b6fec59ee0e5205a import configure_api_keys
import os
from unittest.mock import patch

@patch('getpass.getpass', side_effect=['test_anthropic_key', 'test_openai_key'])
@patch.dict(os.environ, {}, clear=True)
def test_configure_api_keys_sets_env_vars(mock_getpass, monkeypatch):
    configure_api_keys()
    assert os.environ["ANTHROPIC_API_KEY"] == "test_anthropic_key"
    assert os.environ["OPENAI_API_KEY"] == "test_openai_key"

@patch('getpass.getpass', side_effect=[EOFError, EOFError])
@patch.dict(os.environ, {}, clear=True)
def test_configure_api_keys_handles_eof_error(mock_getpass, monkeypatch):
    configure_api_keys()
    assert "ANTHROPIC_API_KEY" not in os.environ
    assert "OPENAI_API_KEY" not in os.environ

@patch('getpass.getpass', side_effect=['   test_anthropic_key   ', '   test_openai_key   '])
@patch.dict(os.environ, {}, clear=True)
def test_configure_api_keys_handles_whitespace(mock_getpass, monkeypatch):
    configure_api_keys()
    assert os.environ["ANTHROPIC_API_KEY"] == '   test_anthropic_key   '
    assert os.environ["OPENAI_API_KEY"] == '   test_openai_key   '

@patch('getpass.getpass', side_effect=['', ''])
@patch.dict(os.environ, {}, clear=True)
def test_configure_api_keys_empty_input(mock_getpass, monkeypatch):
    configure_api_keys()
    assert "ANTHROPIC_API_KEY" not in os.environ
    assert "OPENAI_API_KEY" not in os.environ

