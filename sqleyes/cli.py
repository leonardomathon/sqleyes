# Setup argument parser
import argparse

from sqleyes.main import main
from sqleyes.printer.printer import IntroPrinter, OutputPrinter


parser = argparse.ArgumentParser(
    description="Analyze raw SQL queries for anti-patterns")

parser.add_argument('-q', '--query', metavar="", type=str, required=True,
                    help="A raw SQL query to analyze")

args = parser.parse_args()


def cli():
    IntroPrinter(args.query).print()
    output = main(args.query)
    OutputPrinter(output).print()


if __name__ == '__main__':
    IntroPrinter(args.query).print()
    output = main(args.query)
    OutputPrinter(output).print()
