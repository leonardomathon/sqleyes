"""Fear of the Unknown anti-pattern detector class"""
import re
from sqleyes.detector.antipatterns.abstract_base_class import AbstractDetector
from sqleyes.detector.definitions import DEFINITIONS
from sqleyes.detector.detector_output import DetectorOutput


class FearOfTheUnknownDetector(AbstractDetector):
    
    type = DEFINITIONS["anti_patterns"]["fear_of_the_unknown"]["type"]

    def __init__(self, query):
        super().__init__(query)

    def check(self):
        patterns = [re.compile(r'<>\s*NULL', re.IGNORECASE),
                    re.compile(r'!=\s*NULL', re.IGNORECASE),
                    re.compile(r'=\s*NULL', re.IGNORECASE)]
        for pattern in patterns:
            if pattern.search(self.query):
                return DetectorOutput(detector_type=self.detector_type,
                                      type=self.type)

        return None
