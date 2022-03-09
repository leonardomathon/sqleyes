"""Detector class running various detectors"""
from typing import List
from sqleyes.detector.antipatterns.ambiguous_groups import AmbiguousGroupsDetector
from sqleyes.detector.antipatterns.fear_of_the_unknown import FearOfTheUnknownDetector
from sqleyes.detector.antipatterns.implicit_columns import ImplicitColumnsDetector
from sqleyes.detector.antipatterns.random_selection import RandomSelectionDetector
from sqleyes.detector.detector_output import DetectorOutput


class Detector:
    """
    This is a Detector class that is responsible for detecting errors
    in a given query.

    Attributes:
        query (str): The query to be analyzed.
    """

    def __init__(self, query: str):
        self.query = query
        self.anti_pattern_list: List[DetectorOutput] = []

    def run(self) -> List[DetectorOutput]:
        """
        This function runs various detectors on a query.

        Returns:
            List[DetectorOutput]: A list of Detector outputs of various
            detectors.
        """
        ap_ambiguous_groups = AmbiguousGroupsDetector(query=self.query) \
            .check()
        self.anti_pattern_list.append(ap_ambiguous_groups)

        ap_fear_of_the_unknown = FearOfTheUnknownDetector(query=self.query) \
            .check()
        self.anti_pattern_list.append(ap_fear_of_the_unknown)

        ap_implicit_col = ImplicitColumnsDetector(query=self.query).check()
        self.anti_pattern_list.append(ap_implicit_col)

        ap_random_selection = RandomSelectionDetector(query=self.query).check()
        self.anti_pattern_list.append(ap_random_selection)

        return [ap for ap in self.anti_pattern_list if ap is not None]
