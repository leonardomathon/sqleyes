"""Ambiguous Groups anti-pattern detector class"""
import re

from sqleyes.detector.abstract_ap import APDetector
from sqleyes.detector.detector_output import DetectorOutput
from sqleyes.utils.query_functions import (check_single_value_rule,
    get_columns_from_group_by_statement,
    get_columns_from_select_statement)

class AmbiguousGroupsAPDetector(APDetector):
    type = "Ambiguous Groups"

    def __init__(self, query):
        super().__init__(query)

    def check(self):
        pattern = re.compile(r'GROUP\s*BY', re.IGNORECASE)

        if pattern.search(self.query):
            # GROUP BY pattern is found in the query

            # Get columns in SELECT & GROUP BY statement
            select_columns = get_columns_from_select_statement(self.query)
            group_columns =  get_columns_from_group_by_statement(self.query)

            # Get columns which are in select_columns but not in group_columns
            remaining_columns = list(set(select_columns) - set(group_columns))

            # Check if the remaining columns break single-value rule
            single_values = check_single_value_rule(remaining_columns)

            if not single_values:
                return DetectorOutput(detector_type=self.detector_type,
                    type=self.type)

            return None

        return None
