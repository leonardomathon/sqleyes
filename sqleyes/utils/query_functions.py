"""Utility functions w.r.t queries"""
import re
from typing import List

import sqlparse

from sqleyes.utils.query_keywords import SQL_FUNCTIONS


def get_columns_from_select_statement(query: str) -> List[str]:
    """
    This function takes a query string as input and returns a list of columns
    in the SELECT statement.

    Parameters:
        query (str): The query string.

    Returns:
        columns (list): A list of columns selected in the SELECT statement.
    """
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
