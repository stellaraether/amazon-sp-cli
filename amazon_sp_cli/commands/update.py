"""Self-update command."""

import subprocess
import sys

import click

from ..cli import handle_errors

PACKAGE_NAME = "amazon-sp-cli"


def register_update_commands(cli_group):
    """Register update CLI commands."""

    @cli_group.command()
    @click.option("--dry-run", is_flag=True, help="Show the command without running it")
    @handle_errors
    def update(dry_run):
        """Update to the latest version from PyPI."""
        cmd = [sys.executable, "-m", "pip", "install", "--upgrade", PACKAGE_NAME]

        if dry_run:
            click.echo("Would run: " + " ".join(cmd))
            return

        click.echo("Updating amazon-sp-cli...")
        result = subprocess.run(cmd, capture_output=False)

        if result.returncode != 0:
            click.echo("Update failed.", err=True)
            raise click.Abort()

        click.echo("Update complete. Run 'amz-sp --version' to verify.")
