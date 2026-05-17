import os
import sys

from rich.console import Console
from rich.panel import Panel

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.cli import PGPClientCLI

console = Console()

if __name__ == "__main__":
    console.print(Panel.fit("[bold cyan]PGP Email Simulation Client[/bold cyan]", subtitle="Pretty Good Privacy"))
    app = PGPClientCLI()
    app.start()
