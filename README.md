# PGP Email Encryption

Ky projekt eshte nje aplikacion qe simulon menyren si funksionon PGP
(Pretty Good Privacy) per komunikim te sigurt me email.
Aplikacioni demonstron
gjenerimin e celesave, enkriptimin, nenshkrimin digjital, dergimin permes nje
serveri te simuluar, dekriptimin dhe verifikimin e nenshkrimit.

Projekti mund te testohet ne dy menyra:

- permes web interface ne `localhost`
- permes console application

## Teknologjite e perdorura

- Python 3.10+
- Flask per web interface
- GnuPG / Gpg4win per operacionet PGP
- `python-gnupg` per lidhjen mes Python dhe GPG
- Rich dhe Questionary per console interface
- Loguru per log files
