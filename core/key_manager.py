from pathlib import Path
import shutil
import subprocess
import gnupg
class KeyManager:
    def __init__(self, keys_dir: str = "keys"):
        self.keys_dir = Path(keys_dir).resolve()
        self.keys_dir.mkdir(exist_ok=True)
        self.gpg_binary = self._resolve_gpg_binary()
        self.gpg = gnupg.GPG(
            gpgbinary=self.gpg_binary,
            gnupghome=str(self.keys_dir),
            options=["--pinentry-mode", "loopback"],
        )
        def generate_key_pair(self, email: str, name: str, passphrase: str = "") -> str:
        if not passphrase:
            raise ValueError("A passphrase is required to protect the private key.")

        self._cleanup_stale_locks()

        existing = self.find_public_key(email)
        if existing:
            return existing["fingerprint"]
        key_options = {
            "name_real": name.strip(),
            "name_email": email.strip(),
            "key_type": "RSA",
            "key_length": 2048,
        }