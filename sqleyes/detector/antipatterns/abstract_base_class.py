"""Abstract anti-pattern detector class"""
from abc import ABC, abstractmethod

from sqleyes.utils.load_file import load_description


class AbstractDetector(ABC):
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
    filename: str = NotImplemented
    type: str = NotImplemented
    title: str = NotImplemented

    @abstractmethod
    def __init__(self, query):
        self.detector_type = "anti-pattern"
        self.query = query

    @abstractmethod
    def check(self):
        pass

    def get_description(self):
        return load_description("sqleyes.definitions", "antipatterns/", 
                                self.filename)
        