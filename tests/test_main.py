"""Tests for sqleyes.main"""
import pytest
from sqleyes.definitions.definitions import DEFINITIONS

from sqleyes.main import main


@pytest.mark.parametrize("test_input, expected", [
    (
        "",
        []
    ),
])
def test_main_empty(test_input, expected):
    assert main(test_input) == expected


@pytest.mark.parametrize("test_input, expected", [
    (
        "SELECT pId, price FROM product",
        []
    ),
])
def test_main_valid_query(test_input, expected):
    assert main(test_input) == expected


@pytest.mark.parametrize("test_input, expected", [
    (
        "SELECT * FROM product",
        [[DEFINITIONS["anti_patterns"]["implicit_columns"]["title"],
         DEFINITIONS["anti_patterns"]["implicit_columns"]["type"]]]
    ),
    (
        "SELECT    *    FROM product",
        [[DEFINITIONS["anti_patterns"]["implicit_columns"]["title"],
         DEFINITIONS["anti_patterns"]["implicit_columns"]["type"]]]
    ),
    (
        "select * FROM product",
        [[DEFINITIONS["anti_patterns"]["implicit_columns"]["title"],
         DEFINITIONS["anti_patterns"]["implicit_columns"]["type"]]]
    ),
    (
        "SeLECt * FROM product",
        [[DEFINITIONS["anti_patterns"]["implicit_columns"]["title"],
         DEFINITIONS["anti_patterns"]["implicit_columns"]["type"]]]
    ),
    (
        "SeLECt      *      FROM product",
        [[DEFINITIONS["anti_patterns"]["implicit_columns"]["title"],
         DEFINITIONS["anti_patterns"]["implicit_columns"]["type"]]]
    ),
])
def test_main_implicit_columns(test_input, expected):
    outputs = main(test_input)

    if len(outputs) == 0:
        assert outputs == expected
    else:
        for index, output in enumerate(outputs):
            assert [output.title, output.type] == expected[index]


@pytest.mark.parametrize("test_input, expected", [
    (
        "SELECT pId FROM product WHERE pCategory <> NULL",
        [[DEFINITIONS["anti_patterns"]["fear_of_the_unknown"]["title"],
         DEFINITIONS["anti_patterns"]["fear_of_the_unknown"]["type"]]]
    ),
    (
        "SELECT pId FROM product WHERE pCategory != NULL",
        [[DEFINITIONS["anti_patterns"]["fear_of_the_unknown"]["title"],
         DEFINITIONS["anti_patterns"]["fear_of_the_unknown"]["type"]]]
    ),
    (
        "SELECT pId FROM product WHERE pCategory = NULL",
        [[DEFINITIONS["anti_patterns"]["fear_of_the_unknown"]["title"],
         DEFINITIONS["anti_patterns"]["fear_of_the_unknown"]["type"]]]
    ),
    (
        "SELECT pId FROM product WHERE pCategory = null",
        [[DEFINITIONS["anti_patterns"]["fear_of_the_unknown"]["title"],
         DEFINITIONS["anti_patterns"]["fear_of_the_unknown"]["type"]]]
    ),
    (
        "SELECT pId FROM product WHERE pCategory =     null",
        [[DEFINITIONS["anti_patterns"]["fear_of_the_unknown"]["title"],
         DEFINITIONS["anti_patterns"]["fear_of_the_unknown"]["type"]]]
    ),
    (
        "SELECT pId FROM product WHERE pCategory is NULL",
        []
    ),
    (
        "SELECT pId FROM product WHERE pCategory is not NULL",
        []
    ),
])
def test_main_fear_of_the_unknown(test_input, expected):
    outputs = main(test_input)

    if len(outputs) == 0:
        assert outputs == expected
    else:
        for index, output in enumerate(outputs):
            assert [output.title, output.type] == expected[index]


@pytest.mark.parametrize("test_input, expected", [
    (
        "SELECT pSupplier, price, count(pId) FROM product GROUP BY pSupplier",
        [[DEFINITIONS["anti_patterns"]["ambiguous_groups"]["title"],
         DEFINITIONS["anti_patterns"]["ambiguous_groups"]["type"]]]
    ),
    (
        "SELECT pSupplier, price, count(pId) FROM product group by pSupplier",
        [[DEFINITIONS["anti_patterns"]["ambiguous_groups"]["title"],
         DEFINITIONS["anti_patterns"]["ambiguous_groups"]["type"]]]
    ),
    (
        """SELECT pSupplier, price, count(pId)
           FROM product
           GROUP BY pSupplier
           HAVING price > 9.99""",
        [[DEFINITIONS["anti_patterns"]["ambiguous_groups"]["title"],
         DEFINITIONS["anti_patterns"]["ambiguous_groups"]["type"]]]
    ),
    (
        """SELECT pSupplier, price, count(pId)
           FROM product
           WHERE price > 9.99
           GROUP BY pSupplier
        """,
        [[DEFINITIONS["anti_patterns"]["ambiguous_groups"]["title"],
         DEFINITIONS["anti_patterns"]["ambiguous_groups"]["type"]]]
    ),
    (
        "SELECT pSupplier, count(pId) FROM product GROUP BY pSupplier",
        []
    ),
])
def test_main_ambiguous_groups(test_input, expected):
    outputs = main(test_input)

    if len(outputs) == 0:
        assert outputs == expected
    else:
        for index, output in enumerate(outputs):
            assert [output.title, output.type] == expected[index]


@pytest.mark.parametrize("test_input, expected", [
    (
        "SELECT pId FROM product ORDER BY price",
        []
    ),
    (
        "SELECT pId FROM product ORDER BY RAND()",
        [[DEFINITIONS["anti_patterns"]["random_selection"]["title"],
         DEFINITIONS["anti_patterns"]["random_selection"]["type"]]]
    ),
    (
        "SELECT pId FROM product ORDER BY RANDOM()",
        [[DEFINITIONS["anti_patterns"]["random_selection"]["title"],
         DEFINITIONS["anti_patterns"]["random_selection"]["type"]]]
    ),
    (
        "SELECT pId FROM product ORDER BY rand()",
        [[DEFINITIONS["anti_patterns"]["random_selection"]["title"],
         DEFINITIONS["anti_patterns"]["random_selection"]["type"]]]
    ),
    (
        "SELECT pId FROM product ORDER BY random()",
        [[DEFINITIONS["anti_patterns"]["random_selection"]["title"],
         DEFINITIONS["anti_patterns"]["random_selection"]["type"]]]
    ),
    (
        "SELECT pId FROM product order by rand()",
        [[DEFINITIONS["anti_patterns"]["random_selection"]["title"],
         DEFINITIONS["anti_patterns"]["random_selection"]["type"]]]
    ),
    (
        "SELECT pId FROM product ORDER BY RAND() LIMIT 1",
        [[DEFINITIONS["anti_patterns"]["random_selection"]["title"],
         DEFINITIONS["anti_patterns"]["random_selection"]["type"]]]
    ),
    (
        "SELECT pId FROM product WHERE price > 9.99 ORDER BY RAND() LIMIT 1",
        [[DEFINITIONS["anti_patterns"]["random_selection"]["title"],
         DEFINITIONS["anti_patterns"]["random_selection"]["type"]]]
    ),
    (
        "SELECT pId FROM product WHERE price > 9.99 ORDER BY  RAND()  LIMIT 1",
        [[DEFINITIONS["anti_patterns"]["random_selection"]["title"],
         DEFINITIONS["anti_patterns"]["random_selection"]["type"]]]
    ),
    (
        "SELECT pId FROM product ORDER BY RAND(6) LIMIT 1",
        [[DEFINITIONS["anti_patterns"]["random_selection"]["title"],
         DEFINITIONS["anti_patterns"]["random_selection"]["type"]]]
    ),
    (
        "SELECT pId FROM product ORDER BY RAND(6) LIMIT 1",
        [[DEFINITIONS["anti_patterns"]["random_selection"]["title"],
         DEFINITIONS["anti_patterns"]["random_selection"]["type"]]]
    ),
    (
        "SELECT pId FROM product ORDER BY RAND(6)*5 LIMIT 1",
        [[DEFINITIONS["anti_patterns"]["random_selection"]["title"],
         DEFINITIONS["anti_patterns"]["random_selection"]["type"]]]
    ),
])
def test_main_random_selection(test_input, expected):
    outputs = main(test_input)

    if len(outputs) == 0:
        assert outputs == expected
    else:
        for index, output in enumerate(outputs):
            assert [output.title, output.type] == expected[index]


@pytest.mark.parametrize("test_input, expected", [
    (
        "SELECT pId FROM product ORDER BY price",
        []
    ),
    (
        "SELECT pId FROM product WHERE description LIKE '%ice%';",
        [[DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["title"],
         DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["type"]]]
    ),
    (
        "SELECT pId FROM product WHERE description like '%ice%';",
        [[DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["title"],
         DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["type"]]]
    ),
    (
        "SELECT pId FROM product WHERE description like    '%ice%';",
        [[DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["title"],
         DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["type"]]]
    ),
    (
        "SELECT pId FROM product WHERE description REGEXP 'ice';",
        [[DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["title"],
         DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["type"]]]
    ),
    (
        "SELECT pId FROM product WHERE description LIKE '%ice%';",
        [[DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["title"],
         DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["type"]]]
    ),
    (
        """SELECT pId
           FROM product
           WHERE description REGEXP '[[:<:]]ice[[:>:]]';""",
        [[DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["title"],
         DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["type"]]]
    ),
])
def test_main_poor_mans_search_engine(test_input, expected):
    outputs = main(test_input)

    if len(outputs) == 0:
        assert outputs == expected
    else:
        for index, output in enumerate(outputs):
            assert [output.title, output.type] == expected[index]


@pytest.mark.parametrize("test_input, expected", [
    (
        "SELECT pId FROM product ORDER BY price",
        []
    ),
    (
        """SELECT COUNT(bp.product_id) AS how_many_products,
COUNT(dev.account_id) AS how_many_developers,
COUNT(b.bug_id)/COUNT(dev.account_id) AS avg_bugs_per_developer,
COUNT(cust.account_id) AS how_many_customers
FROM Bugs b JOIN BugsProducts bp ON (b.bug_id = bp.bug_id)
JOIN Accounts dev ON (b.assigned_to = dev.account_id)
JOIN Accounts cust ON (b.reported_by = cust.account_id)
WHERE cust.email IS NOT NULL
GROUP BY bp.product_id""",
        [[DEFINITIONS["anti_patterns"]["spaghetti_query"]["title"],
         DEFINITIONS["anti_patterns"]["spaghetti_query"]["type"],
         "low"]],
    ),
])
def test_main_spaghetti_query(test_input, expected):
    outputs = main(test_input)

    if len(outputs) == 0:
        assert outputs == expected
    else:
        for index, output in enumerate(outputs):
            assert [output.title, output.type, output.certainty] == expected[index]
