import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from subverted.subversion import SubversionConnector
import subprocess


@pytest.fixture
def mock_repo_path(tmp_path):
    """Fixture to create a mock SVN repository."""
    repo_path = tmp_path / "mock_repo"
    repo_path.mkdir()
    svn_dir = repo_path / ".svn"
    svn_dir.mkdir()
    return repo_path


@pytest.fixture
def svn_connector(mock_repo_path):
    """Fixture to create a SubversionConnector instance."""
    return SubversionConnector(repo_path=mock_repo_path)


@patch("subverted.subversion.subprocess.run")
def test_run_command_success(mock_subprocess, svn_connector):
    """Test the _run_command method for successful execution."""
    mock_result = MagicMock()
    mock_result.stdout = "Command executed successfully"
    mock_result.returncode = 0
    mock_subprocess.return_value = mock_result

    result = svn_connector._run_command(["status"])
    assert result == "Command executed successfully"
    mock_subprocess.assert_called_once_with(
        ["svn", "status"],
        cwd=svn_connector.repo_path,
        capture_output=True,
        text=True,
        check=True,
    )


@patch("subverted.subversion.subprocess.run")
def test_run_command_failure(mock_subprocess, svn_connector):
    """Test the _run_command method for command failure."""
    mock_subprocess.side_effect = subprocess.CalledProcessError(
        returncode=1, cmd="svn status", stderr="Error message"
    )

    with pytest.raises(RuntimeError, match="Subversion command failed: Error message"):
        svn_connector._run_command(["status"])
