"""Tests for inventory commands."""

import json
from unittest.mock import Mock, patch

import pytest
from click.testing import CliRunner

from amazon_sp_cli.main import cli


class TestListFbaInventory:
    """Test list-fba-inventory command."""

    @pytest.fixture
    def runner(self):
        """Create Click test runner."""
        return CliRunner()

    @pytest.fixture
    def mock_inventory_response(self):
        """Mock FBA inventory response."""
        return {
            "payload": {
                "inventorySummaries": [
                    {
                        "sellerSku": "SKU-123",
                        "asin": "B09BBL8T4Z",
                        "fnSku": "X123456789",
                        "productName": "Test Product",
                        "condition": "NewItem",
                        "inventoryDetails": {
                            "fulfillableQuantity": 10,
                            "inboundWorkingQuantity": 5,
                        },
                    }
                ],
                "pagination": {"nextToken": "token123"},
            }
        }

    @patch("amazon_sp_cli.cli.SPAPIAuth")
    @patch("amazon_sp_cli.cli.SPAPIClient")
    def test_list_fba_inventory(self, mock_client_class, mock_auth_class, runner, mock_inventory_response):
        """Test listing FBA inventory."""
        mock_client = Mock()
        mock_client.get_fba_inventory.return_value = mock_inventory_response
        mock_client_class.return_value = mock_client

        mock_auth = Mock()
        mock_auth_class.return_value = mock_auth

        result = runner.invoke(cli, ["list-fba-inventory"])

        assert result.exit_code == 0
        # Strip PATH warning if present
        output_text = result.output
        if "{" in output_text:
            brace_idx = output_text.index("{")
            output_text = output_text[brace_idx:]
        output = json.loads(output_text)
        assert len(output["inventory"]) == 1
        assert output["inventory"][0]["sellerSku"] == "SKU-123"
        assert output["nextToken"] == "token123"

    @patch("amazon_sp_cli.cli.SPAPIAuth")
    @patch("amazon_sp_cli.cli.SPAPIClient")
    def test_list_fba_inventory_with_sku_filter(
        self, mock_client_class, mock_auth_class, runner, mock_inventory_response
    ):
        """Test listing FBA inventory filtered by SKU."""
        mock_client = Mock()
        mock_client.get_fba_inventory.return_value = mock_inventory_response
        mock_client_class.return_value = mock_client

        mock_auth = Mock()
        mock_auth_class.return_value = mock_auth

        result = runner.invoke(cli, ["list-fba-inventory", "--sku", "SKU-123,SKU-456"])

        assert result.exit_code == 0
        mock_client.get_fba_inventory.assert_called_once_with(seller_skus="SKU-123,SKU-456", next_token=None)

    @patch("amazon_sp_cli.cli.SPAPIAuth")
    @patch("amazon_sp_cli.cli.SPAPIClient")
    def test_list_fba_inventory_with_next_token(
        self, mock_client_class, mock_auth_class, runner, mock_inventory_response
    ):
        """Test listing FBA inventory with pagination token."""
        mock_client = Mock()
        mock_client.get_fba_inventory.return_value = mock_inventory_response
        mock_client_class.return_value = mock_client

        mock_auth = Mock()
        mock_auth_class.return_value = mock_auth

        result = runner.invoke(cli, ["list-fba-inventory", "--next-token", "token456"])

        assert result.exit_code == 0
        mock_client.get_fba_inventory.assert_called_once_with(seller_skus=None, next_token="token456")

    @patch("amazon_sp_cli.cli.SPAPIAuth")
    @patch("amazon_sp_cli.cli.SPAPIClient")
    def test_list_fba_inventory_empty(self, mock_client_class, mock_auth_class, runner):
        """Test listing FBA inventory with no results."""
        mock_client = Mock()
        mock_client.get_fba_inventory.return_value = {"payload": {"inventorySummaries": []}}
        mock_client_class.return_value = mock_client

        mock_auth = Mock()
        mock_auth_class.return_value = mock_auth

        result = runner.invoke(cli, ["list-fba-inventory"])

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["inventory"] == []
        assert "nextToken" not in output
