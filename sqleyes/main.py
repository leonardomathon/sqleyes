import argparse
from sqleyes.detector.detector import Detector

def run(query: str):
    return Detector(query).run()

# Setup argument parser
parser = argparse.ArgumentParser(
    description="Analyze raw SQL queries for anti-patterns")

parser.add_argument('-q', '--query', metavar="", type=str, required=True, 
    help="A raw SQL query to analyze")

args = parser.parse_args()

if __name__ == '__main__':
    print(run(args.query))