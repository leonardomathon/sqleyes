"""Random Selection anti-pattern detector class"""
import re
from sqleyes.detector.antipatterns.abstract_base_class import AbstractDetector
from sqleyes.definitions.definitions import DEFINITIONS
from sqleyes.detector.detector_output import DetectorOutput


class RandomSelectionDetector(AbstractDetector):

    filename = DEFINITIONS["anti_patterns"]["random_selection"]["filename"]
    type = DEFINITIONS["anti_patterns"]["random_selection"]["type"]
    title = DEFINITIONS["anti_patterns"]["random_selection"]["title"]

    def __init__(self, query):
        super().__init__(query)

    def check(self):
        patterns = [re.compile("(ORDER\\s+BY\\s+RAND\\s*())", re.IGNORECASE),
                    re.compile("(ORDER\\s+BY\\s+RANDOM\\s*())", re.IGNORECASE)]

        for pattern in patterns:
            if pattern.search(self.query):
                return DetectorOutput(certainty="high",
                                      description=super().get_description(),
                                      detector_type=self.detector_type,
                                      title=self.title,
                                      type=self.type)
        return None
