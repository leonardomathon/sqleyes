"""Implicit Columns anti-pattern detector class"""
from sqleyes.definitions.definitions import DEFINITIONS
from sqleyes.detector.antipatterns.abstract_base_class import AbstractDetector
from sqleyes.detector.detector_output import DetectorOutput
from sqleyes.utils.query_functions import get_query_complexity


class SpaghettiQueryDetector(AbstractDetector):

    filename = DEFINITIONS["anti_patterns"]["spaghetti_query"]["filename"]
    type = DEFINITIONS["anti_patterns"]["spaghetti_query"]["type"]
    title = DEFINITIONS["anti_patterns"]["spaghetti_query"]["title"]

    def __init__(self, query):
        super().__init__(query)

    def check(self):
        LOW_THRESHOLD = 2.5
        MEDIUM_THRESHOLD = 4
        HIGH_THRESHOLD = 5.5

        query_complexity = get_query_complexity(self.query)

        if query_complexity < LOW_THRESHOLD:
            return None

        if LOW_THRESHOLD <= query_complexity < MEDIUM_THRESHOLD:
            certainty = "low"

        if MEDIUM_THRESHOLD <= query_complexity < HIGH_THRESHOLD:
            certainty = "medium"

        if HIGH_THRESHOLD <= query_complexity:
            certainty = "high"

        return DetectorOutput(query=self.query,
                              certainty=certainty,
                              description=super().get_description(),
                              detector_type=self.detector_type,
                              locations=[],
                              title=self.title,
                              type=self.type)
