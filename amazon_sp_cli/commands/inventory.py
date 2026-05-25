"""Inventory commands."""

import json

import click

from ..cli import handle_errors


def register_inventory_commands(cli_group, ensure_auth_client):
    """Register inventory CLI commands."""

    @cli_group.command("list-fba-inventory")
    @click.option("--sku", help="Filter by specific SKU (comma-separated for multiple)")
    @click.option("--next-token", help="Pagination token from a previous response")
    @click.pass_context
    @handle_errors
    def list_fba_inventory(ctx, sku, next_token):
        """List FBA inventory summaries."""
        _, client = ensure_auth_client(ctx)
        response = client.get_fba_inventory(seller_skus=sku, next_token=next_token)

        payload = response.get("payload", {})
        summaries = payload.get("inventorySummaries", [])
        result = {"inventory": summaries}

        pagination = payload.get("pagination", {})
        if pagination.get("nextToken"):
            result["nextToken"] = pagination["nextToken"]

        click.echo(json.dumps(result, indent=2))
