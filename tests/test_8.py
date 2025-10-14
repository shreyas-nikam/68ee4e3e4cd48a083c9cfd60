import pytest
from definition_ecfda0711f9d49f2876a34307ea9e66a import view_transcripts
import subprocess
import os

def test_view_transcripts_command_generation(tmpdir):
    output_directory = tmpdir.mkdir("test_output")
    
    # Capture printed output (if your function prints)
    import io
    import sys
    captured_output = io.StringIO()
    sys.stdout = captured_output

    view_transcripts(str(output_directory))
    sys.stdout = sys.__stdout__
    printed_output = captured_output.getvalue().strip()
    
    expected_command_part = f"npx @kaifronsdal/transcript-viewer@latest --dir {str(output_directory)}"

    assert expected_command_part in printed_output, "Command generation failed. Expected to find directory."

@pytest.mark.skip(reason="Requires npx and a browser environment, better tested manually")
def test_view_transcripts_execution(tmpdir):
    output_directory = tmpdir.mkdir("test_output")
    # Create a dummy json file to avoid errors when viewer opens
    dummy_file = output_directory.join("dummy.json")
    dummy_file.write('{"test": "data"}')

    try:
        view_transcripts(str(output_directory))
        # If the command executes without error, consider it a pass for this test
    except FileNotFoundError:
        pytest.fail("npx command not found. Ensure Node.js and npm are installed and npx is in your PATH.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Transcript viewer execution failed: {e}")

def test_view_transcripts_default_directory():
    # Test with the default directory
    import io
    import sys
    captured_output = io.StringIO()
    sys.stdout = captured_output

    view_transcripts()
    sys.stdout = sys.__stdout__
    printed_output = captured_output.getvalue().strip()

    assert "npx @kaifronsdal/transcript-viewer@latest --dir ./outputs/single_audit" in printed_output, "Default directory not used correctly."

def test_view_transcripts_empty_directory(tmpdir):
    output_directory = tmpdir.mkdir("empty_output")
    import io
    import sys
    captured_output = io.StringIO()
    sys.stdout = captured_output

    view_transcripts(str(output_directory))
    sys.stdout = sys.__stdout__
    printed_output = captured_output.getvalue().strip()
    
    expected_command_part = f"npx @kaifronsdal/transcript-viewer@latest --dir {str(output_directory)}"

    assert expected_command_part in printed_output, "Directory not passed correctly."
