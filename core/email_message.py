from dataclasses import dataclass
from datetime import datetime

@dataclass
class EmailMessage:
    sender: str
    receiver: str
    subject: str
    body: str
    timestamp: datetime = None

def __post_init__(self):
    if self.timestamp is None:
        self.timestamp = datetime.now()