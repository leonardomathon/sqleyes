"""Implicit Columns anti-pattern detector class"""
import re
from sqleyes.detector.antipatterns.abstract_base_class import AbstractDetector
from sqleyes.detector.detector_output import DetectorOutput


class ImplicitColumnsDetector(AbstractDetector):

    type = "Implict Columns"

    def __init__(self, query):
        super().__init__(query)

    def check(self):
        pattern = re.compile("(SELECT\\s+\\*)", re.IGNORECASE)

        if pattern.search(self.query):
            return DetectorOutput(detector_type=self.detector_type,
                                  type=self.type)

        return None
