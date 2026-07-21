from datetime import datetime

from ..extensions import db
from ..models import ContactMessage


def create_contact_message(form):
    message = ContactMessage(
        nama=(form.get("nama") or "").strip(),
        email=(form.get("email") or "").strip() or None,
        no_hp=(form.get("no_hp") or "").strip() or None,
        pesan=(form.get("pesan") or "").strip(),
        status="Baru",
    )
    db.session.add(message)
    db.session.commit()
    return message


def list_contact_messages():
    return ContactMessage.query.order_by(ContactMessage.id.desc()).all()


def get_contact_message(message_id: int):
    return ContactMessage.query.get_or_404(message_id)


def mark_contact_message_read(message: ContactMessage):
    if message.status != "Dibaca":
        message.status = "Dibaca"
        message.dibaca_at = datetime.utcnow()
        db.session.commit()
    return message


def delete_contact_message(message: ContactMessage):
    db.session.delete(message)
    db.session.commit()
