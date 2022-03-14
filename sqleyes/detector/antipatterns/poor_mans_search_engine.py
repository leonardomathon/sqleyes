"""Poor Man's Search Engine anti-pattern detector class"""
import re
from sqleyes.detector.antipatterns.abstract_base_class import AbstractDetector
from sqleyes.detector.definitions import DEFINITIONS
from sqleyes.detector.detector_output import DetectorOutput


class PoorMansSearchEngineDetector(AbstractDetector):

    type = DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["type"]

    def __init__(self, query):
        super().__init__(query)

    def check(self):
        patterns = [re.compile("(LIKE)", re.IGNORECASE),
                    re.compile("(REGEXP)", re.IGNORECASE)]

        for pattern in patterns:
            if pattern.search(self.query):
                return DetectorOutput(certainty="medium",
                                      detector_type=self.detector_type,
                                      type=self.type)

        return None
