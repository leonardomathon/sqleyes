"""Random Selection anti-pattern detector class"""
import re
from sqleyes.detector.antipatterns.abstract_base_class import AbstractDetector
from sqleyes.detector.definitions import DEFINITIONS
from sqleyes.detector.detector_output import DetectorOutput


class RandomSelectionDetector(AbstractDetector):

    type = DEFINITIONS["anti_patterns"]["random_selection"]["type"]

    def __init__(self, query):
        super().__init__(query)

    def check(self):
        patterns = [re.compile("(ORDER\\s+BY\\s+RAND\\s*())", re.IGNORECASE),
                    re.compile("(ORDER\\s+BY\\s+RANDOM\\s*())", re.IGNORECASE)]

        for pattern in patterns:
            if pattern.search(self.query):
                return DetectorOutput(detector_type=self.detector_type,
                                      type=self.type)

        return None
