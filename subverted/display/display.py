from rich.table import Table
from pyfiglet import Figlet
from .console import console
from ..subversion import SubversionConnector

LOGO = "Subverted"


def display_header(connector: SubversionConnector) -> None:
    # Header
    fig = Figlet(font="slant", justify="center", width=console.width)
    print(fig.renderText(LOGO))
    console.rule(f"[italic bold yellow]Subversion Repository: {connector.repo_path}")


def display_info(connector: SubversionConnector) -> None:
    console.print("[bold yellow]Info[/]")
    info = connector.info()
    table = Table()
    table.add_column("Property", style="gold1", no_wrap=True)
    table.add_column("Value", no_wrap=True)
    for line in info.splitlines():
        if ":" in line:
            loc = line.find(":")
            table.add_row(line[:loc].strip(), line[loc + 1 :].strip())

    console.print(table)


def display_logs(connector: SubversionConnector) -> None:
    from rich.status import Status

    console.print("\n[bold yellow]Recent Log entries[/]")
    console.print(connector.log())
    stat = Status("Status here")
    console.print(stat)
