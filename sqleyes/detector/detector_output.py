"""Detector Ouput class specifying general output format"""
import json
from typing import List, Tuple


class DetectorOutput(object):
    """
    This class represents the output of a detector.

    Attributes:
        query (str): The query that generated the detector.
        certainty (str): The certainty of the detector detecting the AP.
        description (str): The detector description for the detection.
        detector_type (str): The type of detector that produced this output.
        locations (Tuple): Start and end location where something is detected
        title (str): The title of output.
        type (str): The type of output.
    """
    def __init__(self, query: str, certainty: str, description: str,
                 detector_type: str, locations: List[Tuple[int, int]],
                 title: str, type: str):
        if certainty not in ["low", "medium", "high"]:
            raise Exception("Certainty must be specified as either 'low', \
                             'medium' or 'high' ")
        self.query = query
        self.certainty = certainty
        self.description = description
        self.detector_type = detector_type
        self.locations = locations
        self.title = title
        self.type = type
        self.location_snippets = self.__create_location_snippets()
        self.dict = self.__create_dictionary()

    def __create_location_snippets(self):
        # Convert possible multiline query back to single line
        query = "".join(self.query.splitlines())

        snippets = []

        for location in self.locations:
            snippet = []

            length = location[1] - location[0]

            snippet.append("Query contains an ")
            snippet.append(self.detector_type.title())
            snippet.append(":\n\n")

            # Create query snippet
            if location[0] < length:
                snippet.append(query[location[0]:location[1]+length])
                snippet.append("\n")
            else:
                snippet.append("...")
                snippet.append(query[location[0]-length:location[1]+length])
                snippet.append("...\n")

            # Create error highlight
            if location[0] < length:
                snippet.append("^")
                snippet.append("-" * (length - 1))
            else:
                snippet.append(" " * (length + 3))
                snippet.append("^")
                snippet.append("-" * (length - 1))

            snippets.append("""{}""".format("".join(snippet)))

        return snippets

    def __create_dictionary(self):
        return {
            "certainty": self.certainty,
            "description": self.description,
            "detector_type": self.detector_type,
            "locations": self.locations,
            "location_snippets": json.dumps(self.location_snippets),
            "title": self.title,
            "type": self.type
        }

    def __getitem__(self, item):
        return self.dict[item]

    def __repr__(self):
        return json.dumps(self.__create_dictionary())

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (self.type == other.type
                    and self.detector_type == other.detector_type)
