"""Abstract anti-pattern detector class"""
from abc import ABC, abstractmethod


class APDetector(ABC):
    """
    This is a class for detecting anti-patterns.

    Parameters:
        query : str
            The query to be searched for.

    Attributes:
        detector_type : str
            The type of detector.
        query : str
            The query to be searched for.
    """

    type: str = NotImplemented

    @abstractmethod
    def __init__(self, query):
        self.detector_type = "anti-pattern"
        self.query = query

    @abstractmethod
    def check(self):
        pass
