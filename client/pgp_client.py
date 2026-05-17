import json
from datetime import datetime
from pathlib import Path

from loguru import logger

from core.email_message import EmailMessage
from core.key_manager import KeyManager
from core.pgp_handler import PGPHandler
from server.mail_server import MailServer


class PGPClient:
    def __init__(self, email: str | None = None):
        self.email = email
        self.pgp_handler = PGPHandler()
        self.key_manager = KeyManager()
        self.mail_server = MailServer()

        Path("logs").mkdir(exist_ok=True)

        logger.add("logs/client.log", rotation="10 MB")


def register_user(self, email: str, name: str, passphrase: str):
    self.email = email

    try:
        fingerprint = self.key_manager.generate_key_pair(
            email=email,
            name=name,
            passphrase=passphrase
        )

        logger.info(f"User registered: {email}")

        return fingerprint

    except Exception as exc:
        logger.error(f"Error registering user: {exc}")
        return None

def send_email(self, receiver: str, subject: str, body: str, passphrase: str):
    if not self.email:
        print("You must register or select a sender first.")
        return None

    email_msg = EmailMessage(
        sender=self.email,
        receiver=receiver,
        subject=subject,
        body=body
    )

    try:
        print("Encrypting and signing the email...")

        encrypted_body = self.pgp_handler.sign_and_encrypt(
            email_msg,
            self.email,
            receiver,
            passphrase
        )

        stored = self.mail_server.receive_email(
            {
                "sender": self.email,
                "receiver": receiver,
                "subject": subject,
                "encrypted_body": encrypted_body,
                "is_encrypted": True,
                "is_signed": True,
            }
        )

        self._save_sent_message(stored)

        print(f"Email successfully sent to {receiver}")

        return stored

    except Exception as exc:
        print(f"Encryption failed: {exc}")

        logger.error(f"Send email error: {exc}")

        return None

def receive_email(self, passphrase: str):
    if not self.email:
        print("You must register or select an email first.")
        return []

    decrypted_messages = []

    for message in self.mail_server.get_emails_for_user(self.email):
        try:
            result = self.pgp_handler.decrypt_and_verify(
                message["encrypted_body"],
                passphrase
            )

            decrypted_messages.append((message, result))

        except Exception as exc:
            logger.error(
                f"Receive email error for {message.get('id')}: {exc}"
            )

    return decrypted_messages

def _save_sent_message(self, message: dict):
    sent_dir = Path("data") / "sent"

    sent_dir.mkdir(parents=True, exist_ok=True)

    filename = (
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{message['id']}.json"
    )

    (sent_dir / filename).write_text(
        json.dumps(message, indent=2),
        encoding="utf-8"
    )
