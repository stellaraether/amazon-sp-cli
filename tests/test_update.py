"""Tests for update and version commands."""

from unittest.mock import patch

import pytest
from click.testing import CliRunner

from amazon_sp_cli import __version__
from amazon_sp_cli.main import cli


class TestUpdate:
    """Test self-update command."""

    @pytest.fixture
    def runner(self):
        """Create Click test runner."""
        return CliRunner()

    @patch("amazon_sp_cli.commands.update.subprocess.run")
    def test_update(self, mock_run, runner):
        """Test update command succeeds."""
        mock_run.return_value.returncode = 0

        result = runner.invoke(cli, ["update"])

        assert result.exit_code == 0
        assert "Updating amazon-sp-cli" in result.output
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args[-1] == "amazon-sp-cli"

    @patch("amazon_sp_cli.commands.update.subprocess.run")
    def test_update_failure(self, mock_run, runner):
        """Test update command aborts on failure."""
        mock_run.return_value.returncode = 1

        result = runner.invoke(cli, ["update"])

        assert result.exit_code != 0

    def test_update_dry_run(self, runner):
        """Test update --dry-run prints command without running."""
        result = runner.invoke(cli, ["update", "--dry-run"])

        assert result.exit_code == 0
        assert "Would run:" in result.output
        assert "amazon-sp-cli" in result.output

    def test_version_flag(self, runner):
        """Test --version outputs version."""
        result = runner.invoke(cli, ["--version"])

        assert result.exit_code == 0
        assert f"amz-sp, version {__version__}" in result.output
