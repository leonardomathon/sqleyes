"""Implicit Columns anti-pattern detector class"""
import re

import sqlparse
from sqleyes.detector.antipatterns.abstract_base_class import AbstractDetector
from sqleyes.detector.definitions import DEFINITIONS
from sqleyes.detector.detector_output import DetectorOutput


class SpaghettiQueryDetector(AbstractDetector):

    type = DEFINITIONS["anti_patterns"]["spaghetti_query"]["type"]

    def __init__(self, query):
        super().__init__(query)

    def check(self):
        parsed_query = sqlparse.parse()
        
        return DetectorOutput(certainty="high",
                              detector_type=self.detector_type,
                              type=self.type)

        return None
