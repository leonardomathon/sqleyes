"""Poor Man's Search Engine anti-pattern detector class"""
import re
from sqleyes.detector.antipatterns.abstract_base_class import AbstractDetector
from sqleyes.definitions.definitions import DEFINITIONS
from sqleyes.detector.detector_output import DetectorOutput


class PoorMansSearchEngineDetector(AbstractDetector):

    filename = DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["filename"]
    type = DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["type"]
    title = DEFINITIONS["anti_patterns"]["poor_mans_search_engine"]["title"]

    def __init__(self, query):
        super().__init__(query)

    def check(self):
        patterns = [re.compile("(LIKE)", re.IGNORECASE),
                    re.compile("(REGEXP)", re.IGNORECASE)]

        locations = []

        for pattern in patterns:
            for match in pattern.finditer(self.query):
                locations.append(match.span())

        if len(locations) > 0:
            return DetectorOutput(query=self.query,
                                  certainty="medium",
                                  description=super().get_description(),
                                  detector_type=self.detector_type,
                                  locations=locations,
                                  title=self.title,
                                  type=self.type)
        return None
