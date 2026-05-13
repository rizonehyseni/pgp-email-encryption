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