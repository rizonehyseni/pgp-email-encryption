from pathlib import Path

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

from core.email_message import EmailMessage
from core.key_manager import KeyManager
from core.pgp_handler import PGPHandler
from server.mail_server import MailServer

app = Flask(__name__)
app.secret_key = "pgp-email-simulation-dev-key"

BASE_DIR = Path(__file__).resolve().parent.parent
keys_path = BASE_DIR / "keys"
keys_path.mkdir(exist_ok=True)

key_manager = KeyManager(str(keys_path))
pgp_handler = PGPHandler(str(keys_path))
mail_server = MailServer(str(BASE_DIR / "data"))


@app.context_processor
def inject_user():
    return {"user": {"email": session.get("email")} if session.get("email") else None}


@app.route("/", methods=["GET"])
def index():
    public_keys = key_manager.list_public_keys()
    secret_keys = key_manager.list_secret_keys()
    recent_messages = mail_server.get_all_emails()[:6]
    return render_template(
        "index.html",
        public_keys=public_keys,
        secret_keys=secret_keys,
        recent_messages=recent_messages,
    )


@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "GET":
        return render_template("register.html")

    email = _field("email")
    name = _field("name")
    passphrase = _field("passphrase")

    if not email or not name or not passphrase:
        flash("Please enter name, email, and a private-key passphrase.", "error")
        return redirect(url_for("register_page"))

    try:
        fingerprint = key_manager.generate_key_pair(email=email, name=name, passphrase=passphrase)
        session["email"] = email
        flash(f"PGP key ready for {email}. Fingerprint: {fingerprint}", "success")
        return redirect(url_for("index"))
    except Exception as exc:
        flash(str(exc), "error")
        return redirect(url_for("register_page"))


@app.route("/send", methods=["GET", "POST"])
def send_page():
    if request.method == "GET":
        return render_template("send.html")

    sender = session.get("email") or _field("sender")
    receiver = _field("receiver")
    subject = _field("subject") or "No subject"
    body = _field("body")
    passphrase = _field("passphrase")

    if not sender:
        flash("Register or enter a sender email before sending.", "error")
        return redirect(url_for("register_page"))

    try:
        message = EmailMessage(sender=sender, receiver=receiver, subject=subject, body=body)
        encrypted_body = pgp_handler.encrypt_and_sign(message, sender, receiver, passphrase)
        stored = mail_server.receive_email(
            {
                "sender": sender,
                "receiver": receiver,
                "subject": subject,
                "encrypted_body": encrypted_body,
                "is_encrypted": True,
                "is_signed": True,
            }
        )
        flash(f"Encrypted email sent to {receiver}. Message id: {stored['id']}", "success")
        return render_template("send.html", encrypted_message=encrypted_body, sent_message=stored)
    except Exception as exc:
        flash(str(exc), "error")
        return redirect(url_for("send_page"))


@app.route("/receive", methods=["GET", "POST"])
def receive_page():
    email = _field("email") or session.get("email") or request.args.get("email", "")
    selected_message = None
    decrypted_result = None

    if request.method == "POST":
        message_id = _field("message_id")
        passphrase = _field("passphrase")
        selected_message = mail_server.get_email(message_id)

        if not selected_message:
            flash("Message not found.", "error")
        else:
            try:
                decrypted_result = pgp_handler.decrypt_and_verify(
                    selected_message["encrypted_body"],
                    passphrase=passphrase,
                )
                flash("Message decrypted successfully.", "success")
            except Exception as exc:
                flash(str(exc), "error")

    messages = mail_server.get_emails_for_user(email) if email else []
    return render_template(
        "receive.html",
        email=email,
        messages=messages,
        selected_message=selected_message,
        decrypted_result=decrypted_result,
    )


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Signed out of this browser session.", "success")
    return redirect(url_for("index"))


@app.route("/api/register", methods=["POST"])
def register_api():
    data = request.get_json(silent=True) or {}

    try:
        fingerprint = key_manager.generate_key_pair(
            email=data["email"],
            name=data["name"],
        passphrase=data.get("passphrase", ""),
        )
        return jsonify(
            {
                "success": True,
                "public_key": key_manager.export_public_key(fingerprint),
                "fingerprint": fingerprint,
            }
        )
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 400


@app.route("/api/send", methods=["POST"])
def send_api():
    data = request.get_json(silent=True) or {}

    try:
        sender = data["sender"]
        receiver = data["receiver"]
        message = EmailMessage(
            sender=sender,
            receiver=receiver,
            subject=data.get("subject", "API message"),
            body=data["message"],
        )
        encrypted_body = pgp_handler.encrypt_and_sign(
            message,
            sender,
            receiver,
            data.get("passphrase", ""),
        )
        stored = mail_server.receive_email(
            {
                "sender": sender,
                "receiver": receiver,
                "subject": message.subject,
                "encrypted_body": encrypted_body,
                "is_encrypted": True,
                "is_signed": True,
            }
        )
        return jsonify({"success": True, "encrypted_message": encrypted_body, "message_id": stored["id"]})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 400


def _field(name: str) -> str:
    if request.form:
        return request.form.get(name, "").strip()
    data = request.get_json(silent=True) or {}
    return str(data.get(name, "")).strip()


if __name__ == "__main__":
    app.run(debug=True, port=5000)