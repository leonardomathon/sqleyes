"""Tests for sqleyes.main"""
import pytest

from sqleyes.main import main


@pytest.mark.parametrize("test_input, expected", [
    (
        "SELECT * FROM product",
        []
    ),
])
def test_get_columns_from_select_statement(test_input, expected):
    assert main(test_input) == expected