"""Implicit Columns anti-pattern detector class"""
import re
from sqleyes.detector.antipatterns.abstract_base_class import AbstractDetector
from sqleyes.definitions.definitions import DEFINITIONS
from sqleyes.detector.detector_output import DetectorOutput


class ImplicitColumnsDetector(AbstractDetector):

    filename = DEFINITIONS["anti_patterns"]["implicit_columns"]["filename"]
    type = DEFINITIONS["anti_patterns"]["implicit_columns"]["type"]
    title = DEFINITIONS["anti_patterns"]["implicit_columns"]["title"]

    def __init__(self, query):
        super().__init__(query)

    def check(self):
        pattern = re.compile("(SELECT\\s+\\*)", re.IGNORECASE)

        locations = []

        for match in pattern.finditer(self.query):
            locations.append(match.span())  

        
        if len(locations) > 0:
            return DetectorOutput(certainty="high",
                                  description=super().get_description(),
                                  detector_type=self.detector_type,
                                  location=locations,
                                  title=self.title,
                                  type=self.type)

        return None
