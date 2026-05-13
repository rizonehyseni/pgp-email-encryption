from dataclasses import dataclass
from pathlib import Path
import shutil

import gnupg


@dataclass
class DecryptionResult:
    plaintext: str
    status: str
    username: str | None = None
    key_id: str | None = None
    fingerprint: str | None = None
    signature_id: str | None = None
    trust_text: str | None = None

    @property
    def verified(self) -> bool:
        return bool(self.username or self.key_id or self.fingerprint)


class PGPHandler:
    def __init__(self, keys_dir: str = "keys"):
        self.keys_dir = Path(keys_dir).resolve()
        self.keys_dir.mkdir(exist_ok=True)
        self.gpg = gnupg.GPG(
            gpgbinary=self._resolve_gpg_binary(),
            gnupghome=str(self.keys_dir),
            options=["--pinentry-mode", "loopback"],
        )

    def encrypt_and_sign(self, message, sender: str, receiver: str, passphrase: str = "") -> str:
        text = message.body if hasattr(message, "body") else str(message)
        sender_fingerprint = self.find_secret_key(sender)
        receiver_fingerprint = self.find_public_key(receiver)

        encrypted = self.gpg.encrypt(
            text,
            recipients=[receiver_fingerprint],
            sign=sender_fingerprint,
            passphrase=passphrase,
            always_trust=True,
        )

        if not encrypted.ok:
            raise ValueError(f"Encryption/signing failed: {encrypted.status}")

        return str(encrypted)

    def sign_and_encrypt(self, message, sender: str, receiver: str, passphrase: str = "") -> str:
        return self.encrypt_and_sign(message, sender, receiver, passphrase)

    def decrypt_and_verify(self, encrypted_text: str, passphrase: str = "") -> DecryptionResult:
        decrypted = self.gpg.decrypt(encrypted_text, passphrase=passphrase)

        if not decrypted.ok:
            raise ValueError(f"Decryption failed: {decrypted.status}")

        return DecryptionResult(
            plaintext=str(decrypted),
            status=decrypted.status,
            username=getattr(decrypted, "username", None),
            key_id=getattr(decrypted, "key_id", None),
            fingerprint=getattr(decrypted, "fingerprint", None),
            signature_id=getattr(decrypted, "signature_id", None),
            trust_text=getattr(decrypted, "trust_text", None),
        )

    def decrypt(self, encrypted_text: str, passphrase: str = "") -> str:
        return self.decrypt_and_verify(encrypted_text, passphrase).plaintext

    def find_public_key(self, email_or_fingerprint: str) -> str:
        return self._find_key(email_or_fingerprint, secret=False)

    def find_secret_key(self, email_or_fingerprint: str) -> str:
        return self._find_key(email_or_fingerprint, secret=True)

    def _find_key(self, email_or_fingerprint: str, secret: bool) -> str:
        query = email_or_fingerprint.strip().lower()
        keys = self.gpg.list_keys(secret=secret)

        for key in keys:
            fingerprint = key.get("fingerprint", "")
            uids = " ".join(key.get("uids", [])).lower()
            if query == fingerprint.lower() or query in uids:
                return fingerprint

        key_type = "private" if secret else "public"
        raise ValueError(f"No {key_type} PGP key found for {email_or_fingerprint}")

    @staticmethod
    def _resolve_gpg_binary() -> str:
        candidates = [
            r"C:\Program Files\GnuPG\bin\gpg.exe",
            r"C:\Program Files (x86)\GnuPG\bin\gpg.exe",
            r"C:\Program Files\Gpg4win\..\GnuPG\bin\gpg.exe",
            shutil.which("gpg"),
        ]

        for candidate in candidates:
            if candidate and Path(candidate).exists():
                return str(Path(candidate).resolve())

        return "gpg"