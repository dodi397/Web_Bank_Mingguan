import os
from flask import current_app
from ..utils.helpers import allowed_file, unique_filename


def save_transfer_proof(file_storage):
    if not file_storage or not file_storage.filename:
        raise ValueError("File bukti transfer belum dipilih.")
    if not allowed_file(file_storage.filename):
        raise ValueError("Format file harus PNG, JPG, JPEG, atau WEBP.")
    filename = unique_filename(file_storage.filename, prefix="bukti")
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)
    path = os.path.join(upload_folder, filename)
    file_storage.save(path)
    return filename
