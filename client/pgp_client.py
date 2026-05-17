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
