"""Implicit Columns anti-pattern detector class"""
from sqleyes.definitions.definitions import DEFINITIONS
from sqleyes.detector.antipatterns.abstract_base_class import AbstractDetector
from sqleyes.detector.detector_output import DetectorOutput


class SpaghettiQueryDetector(AbstractDetector):

    filename = DEFINITIONS["anti_patterns"]["spaghetti_query"]["filename"]
    type = DEFINITIONS["anti_patterns"]["spaghetti_query"]["type"]
    title = DEFINITIONS["anti_patterns"]["spaghetti_query"]["title"]

    def __init__(self, query):
        super().__init__(query)

    def check(self):
        return
