"""A Python CLI tool for detecting anti-patterns in raw SQL queries"""

from sqleyes.detector.detector import Detector

def main(query: str):
    """
    This function bootstraps the detector and runs it

    Parameters:
        query (str): A raw SQL query.

    Returns:
        dict: A dictionary of detected anti-patterns.
    """
    return Detector(query).run()
