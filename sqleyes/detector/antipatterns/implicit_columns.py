"""Implicit Columns anti-pattern detector class"""
import re
from sqleyes.detector.antipatterns.abstract_base_class import AbstractDetector
from sqleyes.definitions.definitions import DEFINITIONS
from sqleyes.detector.detector_output import DetectorOutput


class ImplicitColumnsDetector(AbstractDetector):

    type = DEFINITIONS["anti_patterns"]["implicit_columns"]["type"]
    title = DEFINITIONS["anti_patterns"]["implicit_columns"]["title"]

    def __init__(self, query):
        super().__init__(query)

    def check(self):
        pattern = re.compile("(SELECT\\s+\\*)", re.IGNORECASE)

        if pattern.search(self.query):
            return DetectorOutput(certainty="high",
                                  detector_type=self.detector_type,
                                  title=self.title,
                                  type=self.type)

        return None
