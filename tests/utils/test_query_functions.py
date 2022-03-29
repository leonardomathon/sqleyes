"""Tests for sqleyes.utils.query_functions"""
import pytest

from sqleyes.utils.query_functions import (check_single_value_rule, format_query, get_all_columns, get_columns_from_order_by_statement,
                                           get_columns_from_select_statement,
                                           get_columns_from_group_by_statement, has_subqueries, has_union)


@pytest.mark.parametrize("test_input, expected", [
    (
        "select a, b FROM c, d where a > e, GROUP BY f, g",
        "SELECT a, b FROM c, d WHERE a > e, GROUP BY f, g"
    ),
])
def test_format_query(test_input, expected):
    assert format_query(test_input) == expected

@pytest.mark.parametrize("test_input, expected", [
    (
        "SELECT a FROM b WHERE a = 1",
        False
    ),
    (
        "SELECT a FROM b WHERE a in (SELECT a FROM c WHERE a > 10)",
        True
    ),
    (
        "SELECT a FROM b WHERE a = 1 UNION SELECT c from b WHERE c = 2",
        False
    ),
    (
        """SELECT a
        FROM b
        WHERE
            a in (SELECT a FROM c WHERE a > 10) AND
            d in (SELECT d from k)
        """,
        True
    ),
    (
        """SELECT COUNT(1) FROM
(SELECT std.task_id FROM some_task_detail std WHERE std.STATUS = 1) a
JOIN (SELECT st.task_id FROM some_task st WHERE task_type_id = 80) b
ON a.task_id = b.task_id;
        """,
        True
    ),
])
def test_has_subqueries(test_input, expected):
    assert has_subqueries(test_input) == expected



@pytest.mark.parametrize("test_input, expected", [
    (
        "SELECT a FROM b WHERE a = 1",
        False
    ),
    (
        "SELECT a FROM b WHERE a in (SELECT a FROM c WHERE a > 10)",
        False
    ),
    (
        "SELECT a FROM b WHERE a = 1 UNION SELECT c from b WHERE c = 2",
        True
    ),
])
def test_has_union(test_input, expected):
    assert has_union(test_input) == expected


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


@pytest.mark.parametrize("test_input, expected", [
    (
        "SELECT * FROM product WHERE pId > 10",
        []
    ),
    (
        "SELECT * FROM product WHERE pId > 10 ORDER BY price",
        ["price"]
    ),
    (
        "SELECT * FROM product WHERE pId > 10 order by price",
        ["price"]
    ),
    (
        "SELECT * FROM product WHERE pId > 10 order BY price",
        ["price"]
    ),
    (
        "SELECT * FROM product WHERE pId > 10 ORDER BY    price  ,    state",
        ["price", "state"]
    ),
    (
        "SELECT * FROM product WHERE pId > 10 ORDER BY price ASC",
        ["price"]
    ),
    (
        "SELECT * FROM product WHERE pId > 10 ORDER BY price DESC",
        ["price"]
    ),
    (
        """SELECT *
        FROM product
        WHERE pId > 10
        ORDER BY price DESC
        UNION
        FROM product
        WHERE price > 9.99
        """,
        ["price"]
    ),
])
def test_get_columns_from_order_by_statement(test_input, expected):
    assert get_columns_from_order_by_statement(test_input) == expected


@pytest.mark.parametrize("test_input, expected", [
    (
        "SELECT pId FROM product WHERE pId > 10",
        ["pId"]
    ),
    (
        "SELECT pId FROM product WHERE pId > 10 GROUP BY pCat, supplier",
        ["pId", "pCat", "supplier"]
    ),
    (
        """SELECT pId, pCat
        FROM product
        WHERE pId > 10
        GROUP BY pCat, supplier
        ORDER BY pCat ASC""",
        ["pId", "pCat", "pCat", "supplier", "pCat"]
    ),
    (
        """SELECT pId, pCat
        FROM product
        WHERE pId > 10
        ORDER BY pCat ASC""",
        ["pId", "pCat", "pCat"]
    ),
])
def test_get_all_columns(test_input, expected):
    assert get_all_columns(test_input) == expected
