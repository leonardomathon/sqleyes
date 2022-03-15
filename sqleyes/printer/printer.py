import time
from abc import ABC, abstractmethod
from typing import List
import pkg_resources
import sqlparse
from rich.columns import Columns
from rich.console import Console
from rich.layout import Layout
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
        table = Table(title=f"[bold cyan]Summary of analysis[/bold cyan] \nFound {len(self.detector_output)} errors in the given query", title_justify="left")


        table.add_column("Error", justify="right", style="cyan", no_wrap=True)
        table.add_column("Type", style="red")
        table.add_column("Certainty", justify="right", style="green")

        for output in self.detector_output:
            table.add_row(output["detector_type"], output["type"], output["certainty"])
        
        self.console.print(table)

    def print_descriptions(self):
        self.console.print(f"[bold cyan]Detailed descriptions of found errors[/bold cyan]")

        for output in self.detector_output:
            type = output["type"]
            filename = output["type"].replace(" ", "_").replace("'", "").lower()

            self.console.print("-"*10, style="underline")

            with open(pkg_resources.resource_filename("sqleyes.definitions", f"antipatterns/{filename}.md"), "r+") as definition:
                self.console.print(f"[bold red]type[/bold red]: {type}")
                self.console.print(f"[bold red]Description[/bold red]:")
                self.console.print(Padding(Markdown(definition.read()), (1,2)))
                self.console.print("-"*10, style="underline")
                

    def print(self, descriptions=False):
        self.print_summary()
        if descriptions:
            self.console.print()
            self.print_descriptions()
        