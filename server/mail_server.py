import json
import re
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from loguru import logger

from core.email_message import EmailMessage


class MailServer:
    def __init__(self, storage_dir: str = "data"):
        self.storage_dir = Path(storage_dir).resolve()
        self.received_dir = self.storage_dir / "received"
        self.sent_dir = self.storage_dir / "sent"

        self.received_dir.mkdir(parents=True, exist_ok=True)
        self.sent_dir.mkdir(parents=True, exist_ok=True)
        log_dir = self.storage_dir.parent / "logs"
        log_dir.mkdir(exist_ok=True)

        logger.add(log_dir / "server.log", rotation="10 MB")
        logger.info("PGP Mail Server started")

    def receive_email(self, encrypted_message: EmailMessage | dict):
        try:
            if isinstance(encrypted_message, dict):
                data = encrypted_message
            else:
                data = {
                    "sender": encrypted_message.sender,
                    "receiver": encrypted_message.receiver,
                    "subject": encrypted_message.subject,
                    "encrypted_body": encrypted_message.encrypted_body,
                    "timestamp": encrypted_message.timestamp.isoformat(),
                    "is_encrypted": encrypted_message.is_encrypted,
                    "is_signed": encrypted_message.is_signed,
                }

            data.setdefault("id", uuid4().hex)
            data.setdefault("timestamp", datetime.now().isoformat(timespec="seconds"))
            data.setdefault("is_encrypted", True)
            data.setdefault("is_signed", True)

            filename = self._message_filename(data)
            file_path = self.received_dir / filename
            file_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

            logger.info(f"Email received from {data['sender']} to {data['receiver']}")
            print(f"New encrypted email received from {data['sender']}")
            print(f"Email forwarded to {data['receiver']}")
            return data
        except Exception as exc:
            logger.error(f"Error receiving email: {exc}")
            raise

    def get_emails_for_user(self, email: str):
        target = email.strip().lower()
        return [message for message in self.get_all_emails() if message["receiver"].lower() == target]

    def get_all_emails(self):
        emails = []
        for file in self.received_dir.glob("*.json"):
            try:
                data = json.loads(file.read_text(encoding="utf-8"))
                data["_file"] = str(file)
                emails.append(data)
            except (OSError, json.JSONDecodeError) as exc:
                logger.warning(f"Skipping unreadable message {file}: {exc}")
        return sorted(emails, key=lambda item: item.get("timestamp", ""), reverse=True)

    def get_email(self, message_id: str):
        for message in self.get_all_emails():
            if message.get("id") == message_id:
                return message
        return None

    def forward_email(self, message: EmailMessage):
        print(f"Email forwarded to {message.receiver}")

    def _message_filename(self, data: dict) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sender = self._safe_slug(data.get("sender", "unknown"))
        receiver = self._safe_slug(data.get("receiver", "unknown"))
        return f"{timestamp}_{sender}_to_{receiver}_{data['id']}.json"

    @staticmethod
    def _safe_slug(value: str) -> str:
        return re.sub(r"[^a-zA-Z0-9_.-]+", "_", value)[:80]