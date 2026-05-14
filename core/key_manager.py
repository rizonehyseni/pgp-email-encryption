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
def find_secret_key(self, email_or_fingerprint: str):
        return self._find_key(email_or_fingerprint, secret=True)

    def _find_key(self, email_or_fingerprint: str, secret: bool):
        query = email_or_fingerprint.strip().lower()
        if not query:
            return None

        for key in self.gpg.list_keys(secret=secret):
            fingerprint = key.get("fingerprint", "")
            uids = " ".join(key.get("uids", [])).lower()
            if query == fingerprint.lower() or query in uids:
                return key

        return None
     def _generate_key_pair_with_gpg(self, email: str, name: str, passphrase: str) -> str:
        self._cleanup_stale_locks()
        user_id = f"{name.strip()} <{email.strip()}>"
        command = [
            self.gpg_binary,
            "--homedir",
            str(self.keys_dir),
            "--batch",
            "--pinentry-mode",
            "loopback",
            "--passphrase",
            passphrase,
            "--quick-generate-key",
            user_id,
            "rsa2048",
            "default",
            "0",
        ]
         result = subprocess.run(command, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            generated = self.find_public_key(email)
            if generated and "already exists" in (result.stderr or result.stdout):
                return generated["fingerprint"]
            details = (result.stderr or result.stdout or "").strip()
            raise ValueError(f"Key generation failed: {details or 'GnuPG returned an unknown error.'}")