"""Detector class running various detectors"""
from typing import List
from sqleyes.detector.ambiguous_groups_ap import AmbiguousGroupsAPDetector
from sqleyes.detector.detector_output import DetectorOutput
from sqleyes.detector.fear_of_the_unknown_ap import FearOfTheUnknownApDetector
from sqleyes.detector.implicit_columns_ap import ImplicitColumnsAPDetector

class Detector:
    """
    This is a Detector class that is responsible for detecting errors
    in a given query.

    Attributes:
        query (str): The query to be analyzed.
    """

    def __init__(self, query: str):
        self.query = query
        self.anti_pattern_list = []

    def run(self) -> List[DetectorOutput]:
        """
        This function runs various detectors on a query.

        Returns:
            List[DetectorOutput]: A list of Detector outputs of various
            detectors.
        """
        ap_implicit_col = ImplicitColumnsAPDetector(query=self.query).check()
        self.anti_pattern_list.append(ap_implicit_col)

        ap_fear_of_the_unknown = FearOfTheUnknownApDetector(query=self.query) \
        .check()
        self.anti_pattern_list.append(ap_fear_of_the_unknown)

        ap_ambiguous_groups = AmbiguousGroupsAPDetector(query=self.query).check()
        self.anti_pattern_list.append(ap_ambiguous_groups)

        return [ap for ap in self.anti_pattern_list if ap is not None]
