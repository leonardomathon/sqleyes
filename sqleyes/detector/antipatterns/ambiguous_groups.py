"""Ambiguous Groups anti-pattern detector class"""
import re

from sqleyes.detector.antipatterns.abstract_base_class import AbstractDetector
from sqleyes.definitions.definitions import DEFINITIONS
from sqleyes.detector.detector_output import DetectorOutput
from sqleyes.utils.query_functions import (check_single_value_rule,
                                           get_columns_from_group_by_statement,
                                           get_columns_from_select_statement)


class AmbiguousGroupsDetector(AbstractDetector):

    filename = DEFINITIONS["anti_patterns"]["ambiguous_groups"]["filename"]
    type = DEFINITIONS["anti_patterns"]["ambiguous_groups"]["type"]
    title = DEFINITIONS["anti_patterns"]["ambiguous_groups"]["title"]

    def __init__(self, query, subqueries):
        super().__init__(query)
        self.subqueries = subqueries

    def check(self):
        pattern = re.compile(r'GROUP\s*BY', re.IGNORECASE)

        locations = []

        for match in pattern.finditer(self.query):
            locations.append(match.span())

        for query in self.subqueries:
            if pattern.search(query):
                # GROUP BY pattern is found in the query

                # Get columns in SELECT & GROUP BY statement
                select_columns = get_columns_from_select_statement(query)
                group_columns = get_columns_from_group_by_statement(query)

                # Get columns which are in select_columns but not in group_columns
                remaining_columns = list(set(select_columns) - set(group_columns))

                # Check if the remaining columns break single-value rule
                single_values = check_single_value_rule(remaining_columns)

                if not single_values:
                    return DetectorOutput(query=self.query,
                                        certainty="high",
                                        description=super().get_description(),
                                        detector_type=self.detector_type,
                                        locations=locations,
                                        title=self.title,
                                        type=self.type)

                return None

        return None
