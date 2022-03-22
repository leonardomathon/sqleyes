from abc import ABC, abstractmethod
from typing import List
import pkg_resources
import sqlparse
from rich.console import Console
from rich.markdown import Markdown
from rich.padding import Padding
from rich.table import Table
from sqleyes.detector.detector_output import DetectorOutput


class AbstractPrinter(ABC):
    """
    This is a class for printing to console.

    Parameters:
        none

    Attributes:
        console : object
            The rich console object
    """

    @abstractmethod
    def __init__(self):
        self.console = Console()

    @abstractmethod
    def print(self):
        pass


class IntroPrinter(AbstractPrinter):
    def __init__(self, input_query):
        super().__init__()
        self.input_query = sqlparse.format(input_query, reindent=True,
                                           keyword_case='upper')

    def print(self):
        self.console.print(f"[bold cyan]SQLEyes v{pkg_resources.require('sqleyes')[0].version}[/bold cyan]")
        self.console.print()


class OutputPrinter(AbstractPrinter):
    def __init__(self, detector_output: List[DetectorOutput]):
        super().__init__()
        self.detector_output = detector_output

    def print_summary(self):
        table = Table(
            title=f"""[bold cyan]Summary of analysis[/bold cyan] \nFound {len(self.detector_output)} errors in the given query""",
            title_justify="left")

        table.add_column("Error", justify="right", style="cyan", no_wrap=True)
        table.add_column("Title", style="red")
        table.add_column("Type", style="red")
        table.add_column("Certainty", justify="right", style="green")
        table.add_column("Location", justify="right")
        for output in self.detector_output:
            table.add_row(output["detector_type"],
                          output["title"],
                          output["type"],
                          output["certainty"],
                          str(output["location"]).replace("[", "").replace("]", ""))

        self.console.print(table)

    def print_line(self):
        self.console.print("-" * 10)

    def print_descriptions(self):
        self.console.print("[bold cyan]Detailed descriptions of found errors[/bold cyan]")

        self.print_line()

        for output in self.detector_output:
            type = output["type"]
            title = output["title"]
            filename = output["type"].replace(" ", "_").replace("'", "").lower()

            

            with open(pkg_resources.resource_filename("sqleyes.definitions", f"antipatterns/{filename}.md"), "r+") as definition:
                self.console.print()
                self.console.print(f"[bold red]type[/bold red]: {type}")
                self.console.print(f"[bold red]title[/bold red]: {title}")
                self.console.print("[bold red]Description[/bold red]:")
                self.console.print(Padding(Markdown(definition.read()), (1, 2)))
                self.print_line()

    def print(self, descriptions=False):
        self.print_summary()
        if descriptions:
            self.console.print()
            self.print_descriptions()
