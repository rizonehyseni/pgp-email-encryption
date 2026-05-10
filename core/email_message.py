from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class EmailMessage:
    sender: str
    receiver: str
    subject: str
    body: str
    timestamp: datetime = None
    encrypted_body: Optional[bytes] = None
    signature: Optional[bytes] = None
    is_encrypted: bool = False
    is_signed: bool = False

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()