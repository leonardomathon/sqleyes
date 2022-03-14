"""Detector Ouput class specifying general output format"""
import json


class DetectorOutput:
    """
    This class represents the output of a detector.

    Attributes:
        certainty (str): The certainty of the detector detecting the AP.
        detector_type (str): The type of detector that produced this output.
        type (str): The type of output.
    """
    def __init__(self, certainty: str, detector_type: str, type: str):
        if certainty not in ["low", "medium", "high"]:
            raise Exception("Certainty must be specified as either 'low', \
                             'medium' or 'high' ")
        self.certainty = certainty
        self.detector_type = detector_type
        self.type = type

    def __create_dictionary(self):
        return {
            "certainty": self.certainty,
            "detector_type": self.detector_type,
            "type": self.type
        }

    def __repr__(self):
        return json.dumps(self.__create_dictionary())

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (self.type == other.type
                    and self.detector_type == other.detector_type)
