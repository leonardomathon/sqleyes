"""Tests for sqleyes.main"""
import pytest
from sqleyes.definitions.definitions import DEFINITIONS
from sqleyes.detector.detector_output import DetectorOutput

from sqleyes.main import main
from sqleyes.utils.load_file import load_description


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
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "implicit_columns.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["implicit_columns"]["title"],
         DEFINITIONS["anti_patterns"]["implicit_columns"]["type"])]
    ),
    (
        "SELECT    *    FROM product",
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "implicit_columns.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["implicit_columns"]["title"],
         DEFINITIONS["anti_patterns"]["implicit_columns"]["type"])]
    ),
    (
        "select * FROM product",
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "implicit_columns.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["implicit_columns"]["title"],
         DEFINITIONS["anti_patterns"]["implicit_columns"]["type"])]
    ),
    (
        "SeLECt * FROM product",
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "implicit_columns.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["implicit_columns"]["title"],
         DEFINITIONS["anti_patterns"]["implicit_columns"]["type"])]
    ),
    (
        "SeLECt      *      FROM product",
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "implicit_columns.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["implicit_columns"]["title"],
         DEFINITIONS["anti_patterns"]["implicit_columns"]["type"])]
    ),
])
def test_main_implicit_columns(test_input, expected):
    assert main(test_input) == expected


@pytest.mark.parametrize("test_input, expected", [
    (
        "SELECT pId FROM product WHERE pCategory <> NULL",
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "fear_of_the_unknown.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["fear_of_the_unknown"]["title"],
         DEFINITIONS["anti_patterns"]["fear_of_the_unknown"]["type"])]
    ),
    (
        "SELECT pId FROM product WHERE pCategory != NULL",
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "fear_of_the_unknown.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["fear_of_the_unknown"]["title"],
         DEFINITIONS["anti_patterns"]["fear_of_the_unknown"]["type"])]
    ),
    (
        "SELECT pId FROM product WHERE pCategory = NULL",
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "fear_of_the_unknown.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["fear_of_the_unknown"]["title"],
         DEFINITIONS["anti_patterns"]["fear_of_the_unknown"]["type"])]
    ),
    (
        "SELECT pId FROM product WHERE pCategory = null",
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "fear_of_the_unknown.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["fear_of_the_unknown"]["title"],
         DEFINITIONS["anti_patterns"]["fear_of_the_unknown"]["type"])]
    ),
    (
        "SELECT pId FROM product WHERE pCategory =     null",
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "fear_of_the_unknown.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["fear_of_the_unknown"]["title"],
         DEFINITIONS["anti_patterns"]["fear_of_the_unknown"]["type"])]
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
    assert main(test_input) == expected


@pytest.mark.parametrize("test_input, expected", [
    (
        "SELECT pSupplier, price, count(pId) FROM product GROUP BY pSupplier",
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "ambiguous_groups.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["ambiguous_groups"]["title"],
         DEFINITIONS["anti_patterns"]["ambiguous_groups"]["type"])]
    ),
    (
        "SELECT pSupplier, price, count(pId) FROM product group by pSupplier",
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "ambiguous_groups.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["ambiguous_groups"]["title"],
         DEFINITIONS["anti_patterns"]["ambiguous_groups"]["type"])]
    ),
    (
        """SELECT pSupplier, price, count(pId)
           FROM product
           GROUP BY pSupplier
           HAVING price > 9.99""",
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "ambiguous_groups.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["ambiguous_groups"]["title"],
         DEFINITIONS["anti_patterns"]["ambiguous_groups"]["type"])]
    ),
    (
        """SELECT pSupplier, price, count(pId)
           FROM product
           WHERE price > 9.99
           GROUP BY pSupplier
           HAVING count(pId) > 10""",
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "ambiguous_groups.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["ambiguous_groups"]["title"],
         DEFINITIONS["anti_patterns"]["ambiguous_groups"]["type"])]
    ),
    (
        "SELECT pSupplier, count(pId) FROM product GROUP BY pSupplier",
        []
    ),
])
def test_main_ambiguous_groups(test_input, expected):
    assert main(test_input) == expected


@pytest.mark.parametrize("test_input, expected", [
    (
        "SELECT pId FROM product ORDER BY price",
        []
    ),
    (
        "SELECT pId FROM product ORDER BY RAND()",
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "random_selection.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["random_selection"]["title"],
         DEFINITIONS["anti_patterns"]["random_selection"]["type"])]
    ),
    (
        "SELECT pId FROM product ORDER BY RANDOM()",
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "random_selection.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["random_selection"]["title"],
         DEFINITIONS["anti_patterns"]["random_selection"]["type"])]
    ),
    (
        "SELECT pId FROM product ORDER BY rand()",
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "random_selection.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["random_selection"]["title"],
         DEFINITIONS["anti_patterns"]["random_selection"]["type"])]
    ),
    (
        "SELECT pId FROM product ORDER BY random()",
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "random_selection.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["random_selection"]["title"],
         DEFINITIONS["anti_patterns"]["random_selection"]["type"])]
    ),
    (
        "SELECT pId FROM product order by rand()",
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "random_selection.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["random_selection"]["title"],
         DEFINITIONS["anti_patterns"]["random_selection"]["type"])]
    ),
    (
        "SELECT pId FROM product ORDER BY RAND() LIMIT 1",
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "random_selection.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["random_selection"]["title"],
         DEFINITIONS["anti_patterns"]["random_selection"]["type"])]
    ),
    (
        "SELECT pId FROM product WHERE price > 9.99 ORDER BY RAND() LIMIT 1",
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "random_selection.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["random_selection"]["title"],
         DEFINITIONS["anti_patterns"]["random_selection"]["type"])]
    ),
    (
        "SELECT pId FROM product WHERE price > 9.99 ORDER BY  RAND()  LIMIT 1",
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "random_selection.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["random_selection"]["title"],
         DEFINITIONS["anti_patterns"]["random_selection"]["type"])]
    ),
    (
        "SELECT pId FROM product ORDER BY RAND(6) LIMIT 1",
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "random_selection.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["random_selection"]["title"],
         DEFINITIONS["anti_patterns"]["random_selection"]["type"])]
    ),
    (
        "SELECT pId FROM product ORDER BY RAND(6) LIMIT 1",
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "random_selection.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["random_selection"]["title"],
         DEFINITIONS["anti_patterns"]["random_selection"]["type"])]
    ),
    (
        "SELECT pId FROM product ORDER BY RAND(6)*(10-5+1)+5 LIMIT 1",
        [DetectorOutput("high",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "random_selection.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["random_selection"]["title"],
         DEFINITIONS["anti_patterns"]["random_selection"]["type"])]
    ),
])
def test_main_random_selection(test_input, expected):
    assert main(test_input) == expected


@pytest.mark.parametrize("test_input, expected", [
    (
        "SELECT pId FROM product ORDER BY price",
        []
    ),
    (
        "SELECT pId FROM product WHERE description LIKE '%ice%';",
        [DetectorOutput("medium",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "poor_mans_search_engine.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["title"],
         DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["type"])]
    ),
    (
        "SELECT pId FROM product WHERE description like '%ice%';",
        [DetectorOutput("medium",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "poor_mans_search_engine.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["title"],
         DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["type"])]
    ),
    (
        "SELECT pId FROM product WHERE description like    '%ice%';",
        [DetectorOutput("medium",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "poor_mans_search_engine.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["title"],
         DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["type"])]
    ),
    (
        "SELECT pId FROM product WHERE description REGEXP 'ice';",
        [DetectorOutput("medium",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "poor_mans_search_engine.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["title"],
         DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["type"])]
    ),
    (
        "SELECT pId FROM product WHERE description LIKE '%ice%';",
        [DetectorOutput("medium",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "poor_mans_search_engine.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["title"],
         DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["type"])]
    ),
    (
        """SELECT pId
           FROM product
           WHERE description REGEXP '[[:<:]]ice[[:>:]]';""",
        [DetectorOutput("medium",
         load_description("sqleyes.definitions", "antipatterns/", 
                          "poor_mans_search_engine.md"),
         "anti-pattern",
         DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["title"],
         DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["type"])]
    ),
])
def test_main_poor_mans_search_engine(test_input, expected):
    assert main(test_input) == expected
