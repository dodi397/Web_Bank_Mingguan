from flask import Blueprint, flash, redirect, render_template, url_for

from ..utils.helpers import login_required
from ..services.contact_service import (
    delete_contact_message,
    get_contact_message,
    list_contact_messages,
    mark_contact_message_read,
)


pesan_kontak_bp = Blueprint("pesan_kontak", __name__, url_prefix="/dashboard/pesan-kontak")


@pesan_kontak_bp.route("/")
@login_required
def list_pesan_kontak():
    data = list_contact_messages()
    return render_template("dashboard/pesan_kontak.html", contact_messages=data)


@pesan_kontak_bp.route("/detail/<int:message_id>")
@login_required
def detail_pesan_kontak(message_id):
    message = get_contact_message(message_id)
    mark_contact_message_read(message)
    return render_template("dashboard/detail_pesan_kontak.html", message=message)


@pesan_kontak_bp.route("/mark-read/<int:message_id>", methods=["POST"])
@login_required
def mark_read_pesan_kontak(message_id):
    message = get_contact_message(message_id)
    mark_contact_message_read(message)
    flash("Pesan ditandai sudah dibaca.", "success")
    return redirect(url_for("pesan_kontak.list_pesan_kontak"))


@pesan_kontak_bp.route("/delete/<int:message_id>", methods=["POST"])
@login_required
def delete_pesan_kontak(message_id):
    message = get_contact_message(message_id)
    delete_contact_message(message)
    flash("Pesan kontak berhasil dihapus.", "success")
    return redirect(url_for("pesan_kontak.list_pesan_kontak"))
