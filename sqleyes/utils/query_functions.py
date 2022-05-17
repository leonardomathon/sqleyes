"""Utility functions w.r.t queries"""
import re
from typing import List, Tuple

import sqlparse

from sqleyes.utils.code_complexity_metrics import halstead_metrics
from sqleyes.utils.query_keywords import SQL_FUNCTIONS


OPERATORS = ["+", "-", "*", "**", "/", "%", "&", "|", "||", "^", "=", "!=",
             ">", "<", ">=", "<=", "!<", "!>", "<>", "+=", "-=", "/=", "/=",
             "%=", "&=", "^-=", "|*=", "ALL", "AND", "&&", "ANY", "BETWEEN",
             "EXISTS", "IN", "LIKE", "NOT", "OR", "SOME", "IS NULL",
             "IS NOT NULL", "UNIQUE"]

EXPRESSIONS = ["CASE", "DECODE", "IF", "NULLIF", "COALESCE", "GREATEST",
               "GREATER", "LEAST", "LESSER", "CAST", "JOIN", "GROUP BY",
               "WHERE", "HAVING", "ORDER BY", "UNION", "EXCEPT"]


def get_subqueries(parsed_query: sqlparse.sql.Statement) -> Tuple[str, List[str]]:
    """
    This function takes parsed query Statement object as input and returns a
    list of the main query and all the subqueries.

    Parameters:
        query (sqlparse.sql.Statement): A statement object defined by sqlparse

    Returns:
        List[str]: A list of queries contained in the query.
    """
    if type(parsed_query) != sqlparse.sql.Token:
        paren = isinstance(parsed_query, sqlparse.sql.Parenthesis)
        v = [get_subqueries(i) for i in (parsed_query if not paren else parsed_query[1:-1])]
        subseq, qrs = ''.join(str(i[0]) for i in v), [x for _, y in v for x in y]
        if [*parsed_query][paren].value == 'SELECT':
            return '<subquery>', [subseq]+qrs
        return subseq, qrs
    return parsed_query, []


def parse_query(query: str) -> List[str]:
    """
    This function takes a query string as input and returns a list of the main
    query and all the subqueries.

    Parameters:
        query (str): The query string.

    Returns:
        List[str]: A list of queries contained in the query.
    """
    if query == "":
        return []

    parsed_query = sqlparse.parse(query)[0]
    _, subqueries = get_subqueries(parsed_query)

    return subqueries


def format_query(query: str) -> str:
    """
    This function takes a query string as input and returns a formatted query.

    Parameters:
        query (str): The query string.

    Returns:
        str: A query that is properly formatted.
    """
    return str(sqlparse.format(query, keyword_case='upper'))


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


def get_unions(query: str) -> List[str]:
    """
    This function takes a query string as input and returns a list of query
    unions

    Parameters:
        query (str): The query string.

    Returns:
        List[str]: A list of query unions
    """
    if not has_union(query):
        return [query]

    return re.split("\\s*UNION\\s*", query, flags=re.DOTALL | re.IGNORECASE)


def has_except(query: str) -> bool:
    """
    This function takes a query string as input and returns True if that query
    contains a EXCEPT.

    Parameters:
        query (str): The query string.

    Returns:
        bool: True if query contains a EXCEPT, False otherwise
    """
    query = format_query(query)

    except_count = re.findall(r'EXCEPT', query, flags=re.DOTALL |
                              re.IGNORECASE)

    return len(except_count) > 0


def get_excepts(query: str) -> List[str]:
    """
    This function takes a query string as input and returns a list of query
    excepts

    Parameters:
        query (str): The query string.

    Returns:
        List[str]: A list of query excepts
    """
    if not has_except(query):
        return [query]

    return re.split("\\s*EXCEPT\\s*", query, flags=re.DOTALL | re.IGNORECASE)


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


def get_query_ops_and_expr(query: str) -> List[str]:
    """
    Finds all the operators and expressions used inside a query. Returns a list
    of all operators and expressions

    Parameters:
        query (str): A SQL query string.

    Returns:
        List[str]: A list a all operators and expressions from the input query
    """
    result = []

    # Format the query
    query = sqlparse.format(query, keyword_case="upper")

    # Split the query
    query_tokens = query.split()

    # Fix split
    # Merges ["SELECT", "*"] into ["SELECT *"]
    # Merges ["IS", "NULL"] into ["IS NULL"]
    # Merges ["ORDER", "BY"] into ["ORDER BY"]
    # Merges ["GROUP", "BY"] into ["GROUP BY"]
    i, query_len = 0, len(query_tokens)
    while i < query_len - 1:
        merge_current_cel = False
        if "SELECT" in query_tokens[i] and query_tokens[i + 1] == "*":
            merge_current_cel = True
        elif query_tokens[i] == "IS" and query_tokens[i + 1] == "NULL":
            merge_current_cel = True
        elif query_tokens[i] == "ORDER" and query_tokens[i + 1] == "BY":
            merge_current_cel = True
        elif query_tokens[i] == "GROUP" and query_tokens[i + 1] == "BY":
            merge_current_cel = True

        # Merge two cells into one
        # Adjust overall query length since we have one less cell
        if merge_current_cel:
            query_tokens[i:i + 2] = [' '.join(query_tokens[i:i + 2])]
            query_len -= 1

        i += 1

    # Fix split
    # Merges ["IS", "NOT", "NULL"] into ["IS NOT NULL"]
    i, query_len = 0, len(query_tokens)
    while i < query_len - 1:
        if (query_tokens[i] == "IS" and query_tokens[i + 1] == "NOT" and
                query_tokens[i + 2] == "NULL"):
            query_tokens[i:i + 3] = [' '.join(query_tokens[i: i + 3])]
            query_len -= 2
        i += 1

    # Check every element if its an operator or expression
    for elem in query:
        for operator in OPERATORS:
            if elem == operator:
                result.append(operator)

        for expression in EXPRESSIONS:
            if elem == expression:
                result.append(expression)

    return result


def get_query_complexity(query: str) -> float:
    """
    Calculates the complexity of a query based on the Halstead Metric + LoC

    Parameters:
        query (str): A SQL query string.

    Returns:
        int: The complexity of the query
    """
    query = format_query(query)

    # From paper 'Measuring Query Complexity in SQLShare Workload'
    # Number of operators and expressions as Halstead operators
    operators = get_query_ops_and_expr(query)

    # Number of columns referenced in query as Halstead operants
    # If query has a UNION, get all columns for each query in the union
    operands = []
    if (has_union(query)):
        for q in get_unions(query):
            operands.extend(get_all_columns(q))
    else:
        operands.extend(get_all_columns(query))

    N1, N2 = len(operators), len(operands)
    n1, n2 = len(set(operators)), len(set(operands))

    complexity = float(halstead_metrics(n1, n2, N1, N2)[3])

    return complexity


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
