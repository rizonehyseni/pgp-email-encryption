from dataclasses import dataclass

@dataclass
class EmailMessage:
    sender: str
    receiver: str
    subject: str
    body: str