import json
import os
import sys

from rich.console import Console
from rich.panel import Panel

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.mail_server import MailServer

console = Console()


class ServerCLI:
    def __init__(self):
        self.server = MailServer()

    def start(self):
        console.print(Panel.fit("[bold green]PGP Email Simulation Server[/bold green]", subtitle="Mail Transfer Agent"))
        console.print("[cyan]Email server started, waiting for messages.[/cyan]\n")

        while True:
            console.print("\n[bold]Server Menu[/bold]")
            console.print("1. View all received emails")
            console.print("2. View emails for a user")
            console.print("3. Clear all messages")
            console.print("4. Exit")

            choice = input("\nChoose an option (1-4): ").strip()

            if choice == "1":
                self.view_all_emails()
            elif choice == "2":
                self.view_user_emails()
            elif choice == "3":
                self.clear_messages()
            elif choice == "4":
                console.print("[green]Server closed.[/green]")
                break
            else:
                console.print("[red]Invalid choice. Try again.[/red]")

    def view_all_emails(self):
        messages = self.server.get_all_emails()
        if not messages:
            console.print("[yellow]No received messages yet.[/yellow]")
            return

        console.print(f"\n[bold]Received messages: {len(messages)}[/bold]\n")
        for data in messages[:15]:
            console.print(f"{data['timestamp']} | {data['sender']} -> {data['receiver']} | {data['subject']}")

    def view_user_emails(self):
        email = input("User email: ").strip()
        emails = self.server.get_emails_for_user(email)

        if not emails:
            console.print(f"[yellow]No messages found for {email}[/yellow]")
            return

        console.print(f"\n[bold]Messages for {email}[/bold]")
        for data in emails[:10]:
            console.print(f"{data['timestamp']} | From: {data['sender']} | {data.get('subject', 'No subject')}")

    def clear_messages(self):
        confirm = input("Delete all stored received messages? (yes/no): ").strip().lower()
        if confirm in ["yes", "y"]:
            for file in self.server.received_dir.glob("*.json"):
                file.unlink()
            console.print("[green]All messages were deleted.[/green]")
        else:
            console.print("Operation cancelled.")


if __name__ == "__main__":
    app = ServerCLI()
    app.start()