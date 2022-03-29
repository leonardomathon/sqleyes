"""Utility functions w.r.t queries"""
import re
from typing import List

import sqlparse

from sqleyes.utils.code_complexity_metrics import halstead_metrics
from sqleyes.utils.query_keywords import SQL_FUNCTIONS


def format_query(query: str) -> str:
    """
    This function takes a query string as input and returns a formatted query.

    Parameters:
        query (str): The query string.

    Returns:
        str: A query that is properly formatted.
    """
    return sqlparse.format(query, keyword_case='upper')

def has_subqueries(query: str) -> bool:
    """
    This function takes a query string as input and returns True if that query
    contains subqueries.

    Parameters:
        query (str): The query string.

    Returns:
        bool: True if query contains subqueries, False otherwise
    """
    query = format_query(query)

    select_count = re.findall(r'\(\s*SELECT', query, flags=re.DOTALL |
                              re.IGNORECASE)

    return len(select_count) > 0

def has_union(query: str) -> bool:
    """
    This function takes a query string as input and returns True if that query
    contains a UNION.

    Parameters:
        query (str): The query string.

    Returns:
        bool: True if query contains a UNION, False otherwise
    """
    query = format_query(query)

    union_count = re.findall(r'UNION', query, flags=re.DOTALL |
                             re.IGNORECASE)

    return len(union_count) > 0

def get_columns_from_select_statement(query: str) -> List[str]:
    """
    This function takes a query string as input and returns a list of columns
    in the SELECT statement.

    Parameters:
        query (str): The query string.

    Returns:
        List[str]: A list of columns selected in the SELECT statement.
    """
    query = format_query(query)

    tokens = sqlparse.parse(query)[0].tokens

    columns = re.findall(r'SELECT (.*?) FROM', query,
                         flags=re.DOTALL | re.IGNORECASE)

    if len(columns) == 0:
        return []

    columns = columns[0].split(',')
    columns = [column.strip() for column in columns]
    return columns


def get_columns_from_group_by_statement(query: str) -> List[str]:
    """
    This function takes a query string as input and returns a list of columns
    in the GROUP BY statement.

    Parameters:
        query (str): A SQL query string.

    Returns:
        List[str]: A list of column names in the GROUP BY statement.
    """
    query = format_query(query)

    tokens = sqlparse.parse(query)[0].tokens

    # Find index of group by keyword in tokens
    for i in range(0, len(tokens)):
        if tokens[i].value.upper() == "GROUP BY":
            break

    # Query has no GROUP BY statement
    if i == len(tokens) - 1:
        return []

    # Find possible index of next keyword
    for j in range(i + 1, len(tokens)):
        if tokens[j].ttype is sqlparse.tokens.Keyword:
            break

    # Get column names
    group_columns = []
    for item in tokens[i:j + 1]:
        if isinstance(item, sqlparse.sql.IdentifierList):
            for identifier in item.get_identifiers():
                group_columns.append(identifier.get_name())
        elif isinstance(item, sqlparse.sql.Identifier):
            group_columns.append(item.get_name())

    return group_columns


def get_columns_from_order_by_statement(query: str) -> List[str]:
    """
    This function takes a query string as input and returns a list of columns
    in the ORDER BY statement.

    Parameters:
        query (str): The query string.

    Returns:
        List[str]: A list of columns selected in the SELECT statement.
    """
    query = format_query(query)

    tokens = sqlparse.parse(query)[0].tokens

    # Find index of group by keyword in tokens
    for i in range(0, len(tokens)):
        if tokens[i].value.upper() == "ORDER BY":
            break

    # Query has no GROUP BY statement
    if i == len(tokens) - 1:
        return []

    # Find possible index of next keyword
    for j in range(i + 1, len(tokens)):
        if tokens[j].ttype is sqlparse.tokens.Keyword:
            break

    # Get column names
    order_columns = []
    for item in tokens[i:j + 1]:
        if isinstance(item, sqlparse.sql.IdentifierList):
            for identifier in item.get_identifiers():
                order_columns.append(identifier.get_name())
        elif isinstance(item, sqlparse.sql.Identifier):
            order_columns.append(item.get_name())

    return order_columns


def get_all_columns(query: str) -> List[str]:
    select_columns = get_columns_from_select_statement(query)
    group_by_columns = get_columns_from_group_by_statement(query)
    order_by_columns = get_columns_from_order_by_statement(query)

    return select_columns + group_by_columns + order_by_columns


def get_query_complexity(query: str) -> int:
    """
    Calculates the complexity of a query based on the Halstead Metric + LoC

    Parameters:
        query (str): A SQL query string.

    Returns:
        int: The complexity of the query
    """

    # TODO
    # From paper 'Measuring Query Complexity in SQLShare Workload'
    # Number of operators and expressions as Halstead operators
    operators = []

    # Number of columns referenced in query as Halstead operants
    operands = get_all_columns(query)

    N1, N2 = len(operators), len(operands)
    n1, n2 = len(set(operators)), len(set(operands))

    return halstead_metrics(n1, n2, N1, N2)[4]


def check_single_value_rule(columns: List[str]) -> bool:
    """
    This function checks if the columns in the list break the single-value
    rule in SQL.

    Parameters:
        columns (List[str]): A list of columns.

    Returns:
        bool: True if all columns conform to the single value rule,
        False otherwise.
    """
    for column in columns:
        single_value = False

        if column == "*":
            single_value = True

        for function in SQL_FUNCTIONS:
            if re.search(function, column, re.IGNORECASE):
                single_value = True

        if not single_value:
            return False

    return True
