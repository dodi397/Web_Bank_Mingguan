import os
from pathlib import Path

from flask import current_app

from ..extensions import db
from ..models import PaymentSetting
from ..utils.helpers import allowed_file, unique_filename


def get_payment_setting():
    setting = PaymentSetting.query.first()
    if setting:
        return setting

    setting = PaymentSetting(
        bank_name=current_app.config.get("BANK_NAME", "BCA"),
        account_name=current_app.config.get("ACCOUNT_NAME", "A/N BANK MINGGUAN"),
        account_number=current_app.config.get("ACCOUNT_NUMBER", "1234567890"),
        qris_label=current_app.config.get("QRIS_TEXT", "BANK MINGGUAN QRIS"),
    )
    db.session.add(setting)
    db.session.commit()
    return setting


def save_qris_image(file_storage):
    if not file_storage or not file_storage.filename:
        return None
    if not allowed_file(file_storage.filename):
        raise ValueError("Format gambar QRIS harus PNG, JPG, JPEG, atau WEBP.")

    folder = current_app.config["QRIS_UPLOAD_FOLDER"]
    Path(folder).mkdir(parents=True, exist_ok=True)
    filename = unique_filename(file_storage.filename, prefix="qris")
    path = os.path.join(folder, filename)
    file_storage.save(path)
    return filename


def update_payment_setting(setting, form, file_storage=None):
    bank_name = (form.get("bank_name") or "").strip()
    account_name = (form.get("account_name") or "").strip()
    account_number = (form.get("account_number") or "").strip()
    qris_label = (form.get("qris_label") or "").strip()

    if not bank_name:
        raise ValueError("Nama bank wajib diisi.")
    if not account_name:
        raise ValueError("Nama rekening wajib diisi.")
    if not account_number:
        raise ValueError("Nomor rekening wajib diisi.")
    if not qris_label:
        raise ValueError("Label QRIS wajib diisi.")

    setting.bank_name = bank_name
    setting.account_name = account_name
    setting.account_number = account_number
    setting.qris_label = qris_label

    if file_storage and file_storage.filename:
        new_filename = save_qris_image(file_storage)
        if setting.qris_image and setting.qris_image != new_filename:
            old_path = os.path.join(current_app.config["QRIS_UPLOAD_FOLDER"], setting.qris_image)
            if os.path.isfile(old_path):
                try:
                    os.remove(old_path)
                except OSError:
                    pass
        setting.qris_image = new_filename

    db.session.commit()
    return setting
