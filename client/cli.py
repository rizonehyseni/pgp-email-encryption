from rich.console import Console
from rich.prompt import Prompt

from client.pgp_client import PGPClient

console = Console()


class PGPClientCLI:
    def __init__(self):
        self.client = None

    def start(self):
        while True:
            console.print("\n[bold]Client Menu[/bold]")
            console.print("1. Register and generate PGP keys")
            console.print("2. Send encrypted email")
            console.print("3. Receive and decrypt email")
            console.print("4. Exit")

            choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4"])

            if choice == "1":
                self.register_user()
            elif choice == "2":
                self.send_email()
            elif choice == "3":
                self.receive_email()
            elif choice == "4":
                console.print("[green]Goodbye. Stay secure.[/green]")
                break
    def register_user(self):
        email = Prompt.ask("Email")
        name = Prompt.ask("Full name")
        passphrase = Prompt.ask("Passphrase", password=True)

        self.client = PGPClient()
        fingerprint = self.client.register_user(email, name, passphrase)

        if fingerprint:
            console.print(f"[bold green]Registered {email}[/bold green]")
            console.print(f"[dim]Fingerprint: {fingerprint}[/dim]")
        else:
            console.print("[red]Registration failed. Check logs/client.log for details.[/red]")
    def send_email(self):
        if not self.client or not self.client.email:
            console.print("[red]Register first so the client has a private key for signing.[/red]")
            return

        receiver = Prompt.ask("Recipient email")
        subject = Prompt.ask("Subject")

        console.print("Write the message. Submit an empty line to finish.")

        lines = []

        while True:
            line = console.input("> ")

            if line == "":
                break

            lines.append(line)

        body = "\n".join(lines)

        passphrase = Prompt.ask("Sender passphrase", password=True)

        self.client.send_email(receiver, subject, body, passphrase)
