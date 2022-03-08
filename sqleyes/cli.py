# Setup argument parser
import argparse

from sqleyes.main import main


parser = argparse.ArgumentParser(
    description="Analyze raw SQL queries for anti-patterns")

parser.add_argument('-q', '--query', metavar="", type=str, required=True,
                    help="A raw SQL query to analyze")

args = parser.parse_args()


def cli():
    print(main(args.query))


if __name__ == '__main__':
    print(main(args.query))
