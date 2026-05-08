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

## Struktura e projektit

```text
client/              Klienti ne console
core/                Logjika kryesore per PGP dhe modele te mesazhit
data/                Mesazhet e ruajtura nga serveri i simuluar
keys/                Celesat PGP te ruajtur lokalisht
logs/                Log files
server/              Serveri i simuluar i email-eve
web/                 Flask app, templates dhe CSS/JS
run_web.py           File per startimin e web app
requirements.txt     Dependencies
```
