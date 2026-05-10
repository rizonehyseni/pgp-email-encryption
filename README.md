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

## Instalimi

Hape terminalin ne folderin e projektit:

```powershell
cd C:\Users\Lenovo\Desktop\pgp-email-encryption
```

Instalo dependencies:

```powershell
pip install -r requirements.txt
```

Nese `pip` ose `python` nuk njihen, provo:

```powershell
py -m pip install -r requirements.txt
```

Duhet gjithashtu te jete i instaluar GnuPG/Gpg4win. Mund ta kontrollosh me:

```powershell
gpg --version
```

## Startimi i web app

Mos e hap projektin me **Go Live** ose portin `5500`, sepse ky projekt ka backend
Python. Duhet te startohet me Flask:

```powershell
python run_web.py
```

ose:

```powershell
py run_web.py
```

Pastaj hap:

```text
http://127.0.0.1:5000
```

## Si funksionon web app

### Dashboard

Faqja kryesore tregon gjendjen e aplikacionit:

- sa public keys jane ruajtur
- sa private keys jane ruajtur
- sa mesazhe jane ruajtur ne server
- aktivitetet e fundit te serverit

Nga kjo faqe mund te shkosh te gjenerimi i celesave, dergimi ose pranimi i
email-eve.

### Generate keys

Kjo faqe krijon nje PGP key pair per nje perdorues.

Fushat qe plotesohen jane:

- `Name`: emri i perdoruesit, p.sh. `Arbena`
- `Email`: email unik, p.sh. `arbena@example.com`
- `Passphrase`: fjalekalim per mbrojtjen e private key

Programi krijon:

- public key, qe perdoret nga te tjeret per te enkriptuar mesazhe per kete user
- private key, qe perdoret nga user-i per dekriptim dhe nenshkrim

Nese email-i ekziston tashme, programi nuk krijon key te ri, por perdor key-in
ekzistues.

### Send

Kjo faqe perdoret per te derguar email te enkriptuar.

Procesi eshte:

1. Merret mesazhi i shkruar nga user-i.
2. Mesazhi nenshkruhet me private key te derguesit.
3. Mesazhi enkriptohet me public key te marresit.
4. Serveri i simuluar e ruan mesazhin te `data/received`.

Shembull:

```text
Sender: alice@example.com
Recipient: bob@example.com
Subject: Test PGP
Message: Pershendetje Bob
Sender passphrase: alice123
```

Pas dergimit shfaqet nje tekst qe fillon me:

```text
-----BEGIN PGP MESSAGE-----
```

Ky eshte mesazhi i enkriptuar.

### Receive

Kjo faqe perdoret per te lexuar email-et e enkriptuara.

Procesi eshte:

1. Shkruhet email-i i marresit.
2. Klikohet `Load inbox`.
3. Zgjidhet mesazhi.
4. Shkruhet passphrase e marresit.
5. Klikohet butoni unlock per dekriptim.

Nese gjithcka eshte ne rregull, aplikacioni shfaq:

```text
Message decrypted successfully.
Verified
```

`Verified` tregon qe nenshkrimi digjital i derguesit u verifikua me sukses.

## Shembull testimi ne web

Krijo dy user-a:

```text
Name: Alice
Email: alice@example.com
Passphrase: alice123
```

```text
Name: Bob
Email: bob@example.com
Passphrase: bob123
```

Pastaj dergo email nga Alice te Bob:

```text
Recipient: bob@example.com
Subject: Test PGP
Message: Pershendetje Bob, ky eshte email i enkriptuar.
Sender passphrase: alice123
```

Per ta lexuar:

```text
Recipient inbox: bob@example.com
Passphrase: bob123
```

Rezultati duhet te jete mesazhi origjinal dhe statusi `Verified`.

## Si te shohesh user-at e ruajtur

User-at ruhen si PGP keys ne folderin `keys/`.

Per public keys:

```powershell
gpg --homedir keys --list-keys
```

Per private keys:

```powershell
gpg --homedir keys --list-secret-keys
```

Ne output do te shfaqen rreshta te tille:

```text
uid [ultimate] Alice <alice@example.com>
uid [ultimate] Bob <bob@example.com>
```

Keta jane user-at qe mund te perdoren ne aplikacion.

## Perdorimi ne console

Projekti ka edhe version console per klientin dhe serverin.

### Console client

Starto klientin:

```powershell
python client/main.py
```

ose:

```powershell
py client/main.py
```

Menuja e klientit lejon:

- regjistrimin e user-it dhe gjenerimin e PGP keys
- dergimin e email-it te enkriptuar
- pranimin dhe dekriptimin e email-eve
- daljen nga aplikacioni

### Console server

Starto server monitor:

```powershell
python server/main.py
```

ose:

```powershell
py server/main.py
```

Server console lejon:

- shikimin e te gjitha mesazheve te ruajtura
- shikimin e mesazheve per nje user specifik
- pastrimin e mesazheve te ruajtura

Console app dhe web app perdorin te njejtet foldera:

- `keys/` per celesat
- `data/received` per mesazhet e pranuara
- `data/sent` per mesazhet e derguara

Kjo do te thote qe nje mesazh i derguar nga web mund te shihet edhe nga console,
dhe anasjelltas.

## Si funksionon PGP ne kete projekt

PGP perdor kombinim te kriptografise asimetrike dhe simetrike.

Ne kete simulim:

1. Cdo user ka nje public key dhe nje private key.
2. Public key mund te ndahet me te tjeret.
3. Private key ruhet lokalisht dhe mbrohet me passphrase.
4. Kur dergohet email:
   - mesazhi nenshkruhet me private key te derguesit
   - mesazhi enkriptohet me public key te marresit
5. Kur pranohet email:
   - mesazhi dekriptohet me private key te marresit
   - nenshkrimi verifikohet me public key te derguesit

Kjo siguron:

- konfidencialitet, sepse vetem marresi mund ta dekriptoje
- autenticitet, sepse verifikohet derguesi
- integritet, sepse ndryshimet ne mesazh do ta prishnin verifikimin

## Gabime te zakonshme

### Po hapet porti 5500

Kjo ndodh kur perdoret VS Code Live Server. Mos e perdor `Go Live`.

Perdor:

```text
http://127.0.0.1:5000
```

### Key generation failed

Kontrollo qe:

- Gpg4win/GnuPG eshte i instaluar
- serveri eshte restartuar pas ndryshimeve
- po perdor email unik per user te ri
- passphrase nuk eshte bosh

### Decryption failed

Zakonisht ndodh kur:

- po perdoret passphrase e gabuar
- po tenton ta dekriptosh me user te gabuar
- mesazhi eshte derguar per email tjeter

## Shenim sigurie

Ky projekt eshte per qellime edukative. Nuk eshte sistem real per email ne
production. Te gjithe user-at dhe celesat ruhen lokalisht ne nje GnuPG home
directory per ta bere demonstrimin me te thjeshte.
