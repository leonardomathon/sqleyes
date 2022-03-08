"""Tests for sqleyes.utils.query_functions"""
import pytest

from sqleyes.utils.query_functions import (check_single_value_rule,
                                           get_columns_from_select_statement,
                                           get_columns_from_group_by_statement)


@pytest.mark.parametrize("test_input, expected", [
    (
        "SELECT FROM product",
        []
    ),
    (
        "SELECT * FROM product",
        ["*"]
    ),
    (
        "SELECT pId FROM product",
        ["pId"]
    ),
    (
        "select pId from product",
        ["pId"]
    ),
    (
        "SELECT pId, pName FROM product",
        ["pId", "pName"]
    ),
    (
        "select pId, pName from product",
        ["pId", "pName"]
    ),
    (
        "SELECT pCat, AVG(price) FROM product GROUP BY pCat",
        ["pCat", "AVG(price)"]
    ),
    (
        "select pCat, AVG(price) from product GROUP BY pCat",
        ["pCat", "AVG(price)"]
    ),
])
def test_get_columns_from_select_statement(test_input, expected):
    assert get_columns_from_select_statement(test_input) == expected


@pytest.mark.parametrize("test_input, expected", [
    (
        "SELECT * FROM product WHERE pId > 10",
        []
    ),
    (
        "SELECT * FROM product WHERE pId > 10 GROUP BY pCat",
        ["pCat"]
    ),
    (
        "select * from product where pId > 10 group by pCat",
        ["pCat"]
    ),
    (
        "select * from product where pId > 10 group by pCat, supplier",
        ["pCat", "supplier"]
    ),
    (
        "select * from product where pId > 10 group by pSup having pSup > 5",
        ["pSup"]
    ),

])
def test_get_columns_from_group_by_statement(test_input, expected):
    assert get_columns_from_group_by_statement(test_input) == expected


@pytest.mark.parametrize("test_input, expected", [
        ([], True),
        (["pId"], False),
        (["AVG(price)"], True),
        (["avg(price)"], True),
        (["*"], True),
        (["pId", "AVG(price)"], False),
        (["AVG(price)", "pId"], False),
])
def test_check_single_value_rule(test_input, expected):
    assert check_single_value_rule(test_input) == expected
