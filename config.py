import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "bank-mingguan-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'instance' / 'bank_mingguan.db'}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = str(BASE_DIR / "bank_app" / "static" / "uploads" / "bukti_transfer")
    QRIS_UPLOAD_FOLDER = str(BASE_DIR / "bank_app" / "static" / "uploads" / "qris")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")
    ADMIN_NAMA = os.environ.get("ADMIN_NAMA", "Administrator")
    BANK_NAME = "Bank Mingguan"
    ACCOUNT_NAME = "A/N BANK MINGGUAN"
    ACCOUNT_NUMBER = "1234567890"
    QRIS_TEXT = "BANK MINGGUAN QRIS"
    CONTACT_EMAIL = "info@bankmingguan.id"
    CONTACT_PHONE = "0812-3456-7890"
    ADDRESS = "Jl. Buah batu No. 123, Bandung"
