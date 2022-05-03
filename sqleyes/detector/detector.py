"""Detector class running various detectors"""
from typing import List
from sqleyes.detector.antipatterns.ambiguous_groups import AmbiguousGroupsDetector
from sqleyes.detector.antipatterns.fear_of_the_unknown import FearOfTheUnknownDetector
from sqleyes.detector.antipatterns.implicit_columns import ImplicitColumnsDetector
from sqleyes.detector.antipatterns.poor_mans_search_engine import PoorMansSearchEngineDetector
from sqleyes.detector.antipatterns.random_selection import RandomSelectionDetector
from sqleyes.detector.antipatterns.spaghetti_query import SpaghettiQueryDetector
from sqleyes.detector.detector_output import DetectorOutput
from sqleyes.utils.query_functions import parse_query


class Detector:
    """
    This is a Detector class that is responsible for detecting errors
    in a given query.

    Attributes:
        query (str): The query to be analyzed.
    """

    def __init__(self, query: str):
        self.query = query
        self.subqueries = parse_query(query)
        self.anti_pattern_list: List[DetectorOutput] = []

    def run(self) -> List[DetectorOutput]:
        """
        This function runs various detectors on a query.

        Returns:
            List[DetectorOutput]: A list of Detector outputs of various
            detectors.
        """
        if self.query == "":
            return []

        ap_ambiguous_groups = AmbiguousGroupsDetector(query=self.query,
                                                      subqueries=self.subqueries).check()
        self.anti_pattern_list.append(ap_ambiguous_groups)

        ap_fear_of_the_unknown = FearOfTheUnknownDetector(query=self.query) \
            .check()
        self.anti_pattern_list.append(ap_fear_of_the_unknown)

        ap_implicit_col = ImplicitColumnsDetector(query=self.query).check()
        self.anti_pattern_list.append(ap_implicit_col)

        ap_pm_search_engine = PoorMansSearchEngineDetector(query=self.query) \
            .check()
        self.anti_pattern_list.append(ap_pm_search_engine)

        ap_random_selection = RandomSelectionDetector(query=self.query).check()
        self.anti_pattern_list.append(ap_random_selection)

        ap_spaghetti_query = SpaghettiQueryDetector(query=self.query).check()
        self.anti_pattern_list.append(ap_spaghetti_query)

        return [ap for ap in self.anti_pattern_list if ap is not None]
