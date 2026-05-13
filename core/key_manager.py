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
         key_options["passphrase"] = passphrase

        input_data = self.gpg.gen_key_input(**key_options)

        key = self.gpg.gen_key(input_data)

        if not key or not key.fingerprint:
            generated = self.find_public_key(email)
            if generated:
                return generated["fingerprint"]
            return self._generate_key_pair_with_gpg(email=email, name=name, passphrase=passphrase)

        return key.fingerprint
    def export_public_key(self, email_or_fingerprint: str) -> str:
        key = self.find_public_key(email_or_fingerprint)
        if not key:
            raise ValueError(f"No public key found for {email_or_fingerprint}")
        return self.gpg.export_keys(key["fingerprint"])
 def import_public_key(self, armored_key: str):
        result = self.gpg.import_keys(armored_key)
        if not result.count:
            raise ValueError("No valid public key was imported.")
        return result.fingerprints
def list_public_keys(self):
        return self.gpg.list_keys()

    def list_secret_keys(self):
        return self.gpg.list_keys(secret=True)

    def find_public_key(self, email_or_fingerprint: str):
        return self._find_key(email_or_fingerprint, secret=False)
